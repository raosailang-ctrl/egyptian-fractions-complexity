from __future__ import annotations

import json
import re
import shutil
import subprocess
import tarfile
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 compatibility.
    import tomli as tomllib


class SyncError(RuntimeError):
    """Raised when a synchronization operation cannot be completed safely."""


class VerificationError(SyncError):
    """Raised when a configured verifier returns a non-zero exit code."""


class BrowserError(SyncError):
    """Raised when the browser cannot provide a usable ChatGPT page."""


@dataclass(frozen=True)
class CommandResult:
    command: str
    returncode: int
    stdout: str = ""
    stderr: str = ""


@dataclass(frozen=True)
class RoundResult:
    changed_paths: tuple[Path, ...] = ()
    verifier_results: tuple[CommandResult, ...] = ()
    commit_sha: str | None = None
    context_handoff: bool = False
    state_updated: bool = False
    response_text: str = ""


STATE_BEGIN = "<!-- RESEARCH_STATE_BEGIN -->"
STATE_END = "<!-- RESEARCH_STATE_END -->"
DEFAULT_ALLOWED_SUFFIXES = (
    ".md",
    ".py",
    ".txt",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".zip",
    ".tar",
    ".gz",
)
CONTEXT_LIMIT_PHRASES = (
    "conversation is too long",
    "maximum context",
    "context length",
    "context window",
    "too many tokens",
)
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
IGNORED_NAMES = {".ds_store", "thumbs.db"}


@dataclass(frozen=True)
class Config:
    repo_path: Path
    chat_url: str
    remote: str = "origin"
    branch: str = "main"
    chrome_path: Path | None = None
    cdp_port: int = 9222
    profile_dir: Path = Path("chatgpt-automation-profile")
    download_dir: Path = Path("chatgpt-automation-downloads")
    staging_dir: Path = Path("chatgpt-automation-staging")
    logs_dir: Path = Path("chatgpt-automation-logs")
    allowed_suffixes: tuple[str, ...] = DEFAULT_ALLOWED_SUFFIXES
    verify_commands: tuple[str, ...] = ()
    continue_prompt: str = ""
    handoff_prompt: str = ""
    response_timeout_seconds: int = 300
    stable_poll_seconds: float = 2.0


def _path_value(value: Any, base: Path) -> Path:
    path = Path(str(value)).expanduser()
    return path if path.is_absolute() else (base / path).resolve()


def load_config(path: Path) -> Config:
    """Load the local TOML configuration without creating any directories."""
    with path.open("rb") as handle:
        raw = tomllib.load(handle)
    base = path.parent.resolve()
    repo_path = _path_value(raw["repo_path"], base)
    browser = raw.get("browser", {})
    paths = raw.get("paths", {})
    git = raw.get("git", {})
    prompts = raw.get("prompts", {})
    runtime = raw.get("runtime", {})
    suffixes = tuple(
        suffix if str(suffix).startswith(".") else f".{suffix}"
        for suffix in raw.get("allowed_suffixes", DEFAULT_ALLOWED_SUFFIXES)
    )
    chrome_value = browser.get("chrome_path")
    return Config(
        repo_path=repo_path,
        chat_url=str(raw["chat_url"]),
        remote=str(git.get("remote", "origin")),
        branch=str(git.get("branch", "main")),
        chrome_path=_path_value(chrome_value, base) if chrome_value else None,
        cdp_port=int(browser.get("cdp_port", 9222)),
        profile_dir=_path_value(paths.get("profile_dir", "chatgpt-automation-profile"), base),
        download_dir=_path_value(paths.get("download_dir", "chatgpt-automation-downloads"), base),
        staging_dir=_path_value(paths.get("staging_dir", "chatgpt-automation-staging"), base),
        logs_dir=_path_value(paths.get("logs_dir", "chatgpt-automation-logs"), base),
        allowed_suffixes=suffixes,
        verify_commands=tuple(str(command) for command in raw.get("verify_commands", [])),
        continue_prompt=str(prompts.get("continue", "")),
        handoff_prompt=str(prompts.get("handoff", "")),
        response_timeout_seconds=int(runtime.get("response_timeout_seconds", 300)),
        stable_poll_seconds=float(runtime.get("stable_poll_seconds", 2.0)),
    )


def extract_state_block(text: str) -> str | None:
    """Extract visible text markers or legacy HTML-comment markers.

    Browser inner_text() omits HTML comments, so new prompts use visible lines.
    """
    begin = r"(?:<!--\s*RESEARCH_STATE_BEGIN\s*-->|(?m:^\s*RESEARCH_STATE_BEGIN\s*$))"
    end = r"(?:<!--\s*RESEARCH_STATE_END\s*-->|(?m:^\s*RESEARCH_STATE_END\s*$))"
    match = re.search(begin + r"\s*(.*?)\s*" + end, text, flags=re.DOTALL)
    return match.group(1).strip() if match else None


def write_dry_run_diagnostic(
    round_dir: Path,
    browser: Any,
    response: str,
    downloaded: Iterable[Path],
    state_text: str | None,
) -> Path:
    """Write a local-only report so a failed dry-run can be diagnosed safely."""
    round_dir.mkdir(parents=True, exist_ok=True)
    page = getattr(browser, "page", None)
    page_url = getattr(page, "url", "(page URL unavailable)")
    files = list(downloaded)
    scan = getattr(browser, "_attachment_scan", None)
    lines = [
        "# ChatGPT research dry-run diagnostic",
        "",
        f"- Page URL: {page_url}",
        f"- Assistant response characters: {len(response)}",
        f"- State block found: {'yes' if state_text is not None else 'no'}",
        f"- Downloaded attachments: {len(files)}",
        "",
        "## Downloaded files",
        "",
    ]
    if files:
        for path in files:
            try:
                size = path.stat().st_size
            except OSError:
                size = "unavailable"
            lines.append(f"- {path.name} ({size} bytes)")
    else:
        lines.append("- None")
    lines.extend(["", "## Attachment DOM scan", ""])
    if scan:
        lines.append(f"- Latest assistant locator found: {scan.get('message_found', 'unknown')}")
        lines.append(f"- Scoped candidate count: {scan.get('scoped_candidate_count', 'unknown')}")
        lines.append(f"- Page-wide candidate count: {scan.get('page_candidate_count', 'unknown')}")
        lines.append("")
        lines.append("### Scoped candidate metadata")
        lines.extend(f"- {item}" for item in scan.get("scoped_candidates", []))
        lines.append("")
        lines.append("### Page-wide candidate metadata")
        lines.extend(f"- {item}" for item in scan.get("page_candidates", []))
        lines.append("")
        lines.append("### Download attempts")
        for attempt in scan.get("download_attempts", []):
            lines.append(f"- Candidate: {attempt.get('metadata', '')}")
            lines.append(f"  - Method: {attempt.get('method')}")
            lines.append(f"  - Visible: {attempt.get('visible')}; enabled: {attempt.get('enabled')}")
            lines.append(f"  - Bounding box: {attempt.get('bounding_box')}")
            lines.append(f"  - Error: {attempt.get('error') or '(none)'}")
            lines.append(f"  - Result file: {attempt.get('fallback_file') or '(none)'}")
            if attempt.get("control_html"):
                lines.extend(["  - Control HTML:", "    ```html", "    " + attempt["control_html"].replace("\\n", " "), "    ```"])
        if scan.get("message_html"):
            lines.extend(["", "### Latest assistant container HTML (truncated)", "", "```html", scan["message_html"], "```"])
    else:
        lines.append("- No DOM scan data available.")
    lines.extend([
        "",
        "## Latest assistant response captured by the synchronizer",
        "",
        response,
        "",
    ])
    target = round_dir / "dry-run-diagnostic.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    return target


def context_limit_detected(text: str) -> bool:
    normalized = re.sub(r"\s+", " ", text.lower())
    return any(phrase in normalized for phrase in CONTEXT_LIMIT_PHRASES)


def _is_ignored(path: PurePosixPath) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts) or any(
        part.lower() in IGNORED_NAMES or part.startswith("~") for part in path.parts
    )


def _suffix_allowed(name: str, allowed_suffixes: set[str]) -> bool:
    lowered = name.lower()
    return any(lowered.endswith(suffix.lower()) for suffix in allowed_suffixes)


def _normalize_member_name(name: str) -> PurePosixPath:
    normalized = name.replace("\\", "/")
    candidate = PurePosixPath(normalized)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise SyncError(f"Archive member escapes the repository: {name}")
    return candidate


def _flatten_prefix(names: Iterable[PurePosixPath]) -> str | None:
    parts = [name.parts for name in names if name.parts]
    if not parts:
        return None
    first = parts[0][0]
    return first if all(items[0] == first for items in parts) else None


def _target_path(repo_root: Path, relative: PurePosixPath) -> Path:
    repo_root = repo_root.resolve()
    target = (repo_root / Path(*relative.parts)).resolve()
    if target != repo_root and repo_root not in target.parents:
        raise SyncError(f"Target escapes repository: {relative}")
    return target


def _write_members(
    members: list[tuple[PurePosixPath, bytes]],
    repo_root: Path,
    allowed_suffixes: set[str],
) -> list[Path]:
    repo_root.mkdir(parents=True, exist_ok=True)
    prefix = _flatten_prefix(name for name, _ in members)
    copied: list[Path] = []
    for name, content in members:
        if prefix and name.parts and name.parts[0] == prefix:
            name = PurePosixPath(*name.parts[1:])
        if not name.parts or _is_ignored(name) or not _suffix_allowed(str(name), allowed_suffixes):
            continue
        target = _target_path(repo_root, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        copied.append(target)
    return sorted(set(copied))


def _zip_members(archive: Path) -> list[tuple[PurePosixPath, bytes]]:
    with zipfile.ZipFile(archive) as handle:
        members: list[tuple[PurePosixPath, bytes]] = []
        for info in handle.infolist():
            if info.is_dir():
                continue
            name = _normalize_member_name(info.filename)
            members.append((name, handle.read(info)))
        return members


def _tar_members(archive: Path) -> list[tuple[PurePosixPath, bytes]]:
    with tarfile.open(archive, "r:*") as handle:
        members: list[tuple[PurePosixPath, bytes]] = []
        for info in handle.getmembers():
            if not info.isfile():
                if info.issym() or info.islnk():
                    raise SyncError(f"Archive links are not allowed: {info.name}")
                continue
            name = _normalize_member_name(info.name)
            stream = handle.extractfile(info)
            if stream is None:
                raise SyncError(f"Cannot read archive member: {info.name}")
            members.append((name, stream.read()))
        return members


def safe_extract_archive(
    archive: Path,
    repo_root: Path,
    allowed_suffixes: set[str],
) -> list[Path]:
    """Overlay safe archive members into the repository and return changed paths."""
    suffix = archive.name.lower()
    if suffix.endswith((".tar", ".tar.gz", ".tgz")):
        members = _tar_members(archive)
    elif suffix.endswith(".zip"):
        members = _zip_members(archive)
    else:
        raise SyncError(f"Unsupported archive type: {archive.name}")
    return _write_members(members, repo_root, allowed_suffixes)


def copy_artifact(src: Path, repo_root: Path, allowed_suffixes: set[str]) -> list[Path]:
    """Copy a downloaded file or unpack an archive using the same safety rules."""
    lowered = src.name.lower()
    if lowered.endswith((".zip", ".tar", ".tar.gz", ".tgz")):
        return safe_extract_archive(src, repo_root, allowed_suffixes)
    if not _suffix_allowed(src.name, allowed_suffixes) or _is_ignored(PurePosixPath(src.name)):
        return []
    target = _target_path(repo_root, PurePosixPath(src.name))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, target)
    return [target]


def working_tree_is_clean(repo_root: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
    )
    return not result.stdout.strip()


def write_research_state(repo_root: Path, state_text: str) -> Path:
    """Persist the compact state protocol at the repository root."""
    target = repo_root / "research_state.md"
    target.write_text(state_text.rstrip() + "\n", encoding="utf-8")
    return target


def run_verifiers(
    repo_root: Path,
    changed_paths: list[Path],
    commands: list[str] | tuple[str, ...],
    dry_run: bool = False,
) -> list[CommandResult]:
    """Run only explicitly configured verifier commands."""
    del changed_paths  # The allowlist is configured by the user, not inferred from filenames.
    results: list[CommandResult] = []
    for command in commands:
        if dry_run:
            results.append(CommandResult(command, 0, "DRY_RUN", ""))
            continue
        completed = subprocess.run(
            command,
            cwd=repo_root,
            shell=True,
            capture_output=True,
            text=True,
        )
        result = CommandResult(command, completed.returncode, completed.stdout, completed.stderr)
        results.append(result)
        if completed.returncode != 0:
            details = (completed.stderr or completed.stdout).strip()
            raise VerificationError(f"Verifier failed ({completed.returncode}): {command}\n{details}")
    return results


def _git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=check,
        capture_output=True,
        text=True,
    )


def _relative_git_paths(repo_root: Path, paths: Iterable[Path]) -> list[str]:
    root = repo_root.resolve()
    relative: list[str] = []
    for path in paths:
        resolved = path.resolve()
        if resolved != root and root not in resolved.parents:
            raise SyncError(f"Cannot stage a path outside the repository: {path}")
        relative.append(resolved.relative_to(root).as_posix())
    return sorted(set(relative))


def commit_and_push(
    repo_root: Path,
    remote: str,
    branch: str,
    paths: list[Path],
    message: str,
    dry_run: bool = False,
) -> str | None:
    """Stage exact paths, create one commit, push it, and return its SHA."""
    relative = _relative_git_paths(repo_root, paths)
    if not relative:
        return _git(repo_root, "rev-parse", "HEAD").stdout.strip()
    if dry_run:
        return _git(repo_root, "rev-parse", "HEAD").stdout.strip()

    _git(repo_root, "pull", "--ff-only", remote, branch)
    _git(repo_root, "add", "--", *relative)
    staged = _git(repo_root, "diff", "--cached", "--quiet", check=False)
    if staged.returncode == 0:
        return _git(repo_root, "rev-parse", "HEAD").stdout.strip()
    _git(repo_root, "commit", "-m", message)
    _git(repo_root, "push", remote, branch)
    return _git(repo_root, "rev-parse", "HEAD").stdout.strip()


class ChatGPTBrowser:
    """Small Playwright adapter for a dedicated Chrome CDP session."""

    def __init__(
        self,
        chat_url: str,
        cdp_port: int = 9222,
        response_timeout_seconds: int = 300,
        stable_poll_seconds: float = 2.0,
        download_dir: Path | None = None,
    ) -> None:
        self.chat_url = chat_url
        self.cdp_port = cdp_port
        self.response_timeout_seconds = response_timeout_seconds
        self.stable_poll_seconds = stable_poll_seconds
        self.download_dir = download_dir.resolve() if download_dir else None
        self._playwright = None
        self._browser = None
        self._context = None
        self.page = None

    def connect(self) -> None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise BrowserError(
                "Playwright is not installed. Run: python -m pip install -r research-automation/requirements.txt"
            ) from exc
        self._playwright = sync_playwright().start()
        try:
            self._browser = self._playwright.chromium.connect_over_cdp(
                f"http://127.0.0.1:{self.cdp_port}"
            )
        except Exception as exc:  # Playwright exposes several transport exception types.
            self.close()
            raise BrowserError(
                f"Cannot connect to Chrome CDP port {self.cdp_port}. Start the dedicated Chrome launcher first."
            ) from exc
        contexts = self._browser.contexts
        if not contexts:
            self.close()
            raise BrowserError("Chrome CDP is connected but has no browser context.")
        self._context = contexts[0]
        pages = self._context.pages
        chat_pages = [page for page in pages if (page.url or "").startswith("https://chatgpt.com")]
        self.page = (chat_pages[-1] if chat_pages else pages[0]) if pages else self._context.new_page()
        # A ChatGPT profile can contain both the normal conversation tab and a
        # floating-chat tab.  The floating tab has a tall narrow composer and
        # can block fill/Enter operations, so prefer a normal wide composer.
        for page in pages:
            try:
                composer = page.locator(
                    ("textarea, [contenteditable='true'], div[role='textbox']")
                ).last
                box = composer.bounding_box()
            except Exception:
                box = None
            if box and box["width"] >= 300 and box["height"] <= 120:
                self.page = page
                break
        try:
            self.page.bring_to_front()
        except Exception:
            pass
        if not self.page.url or self.page.url == "about:blank":
            self.page.goto(self.chat_url, wait_until="domcontentloaded")

    def wait_for_login(self) -> None:
        if self.page is None:
            raise BrowserError("Browser is not connected.")
        deadline = time.monotonic() + self.response_timeout_seconds
        while time.monotonic() < deadline:
            url = (self.page.url or "").lower()
            try:
                body = self.page.locator("body").inner_text(timeout=1000).lower()
            except Exception:
                body = ""
            if "/auth/" not in url and "log in" not in body and "sign up" not in body:
                return
            self.page.wait_for_timeout(1000)
        raise BrowserError("ChatGPT login is still required in the dedicated Chrome window.")

    def _last_locator(self, selectors: tuple[str, ...], page=None):
        page = page or getattr(self, "page", None)
        if page is None:
            raise BrowserError("Browser is not connected.")
        for selector in selectors:
            locator = page.locator(selector)
            try:
                count = locator.count()
            except Exception:
                count = 0
            if count:
                return locator.nth(count - 1)
        return None

    def _latest_assistant_locator(self, page=None):
        page = page or self.page
        if page is None:
            raise BrowserError("Browser is not connected.")
        # ChatGPT's current DOM uses data-chatgpt-selection-message-id for
        # rendered assistant messages.  Keep the older selectors as fallbacks
        # for accounts that still receive the previous message markup.
        return self._last_locator(
            (
                "[data-chatgpt-selection-message-id]",
                "[data-message-author-role='assistant']",
                "main article",
                "[data-turn-key]",
            ),
            page=page,
        )

    def latest_assistant_text(self, page=None) -> str:
        page = page or self.page
        if page is None:
            raise BrowserError("Browser is not connected.")
        locator = self._latest_assistant_locator(page)
        if locator is None:
            locator = page.locator("main")
        return locator.inner_text().strip()

    def _composer(self):
        return self._last_locator(("textarea", "[contenteditable='true']", "div[role='textbox']"))

    def send_prompt(self, prompt: str) -> None:
        composer = self._composer()
        if composer is None:
            raise BrowserError("Cannot find the ChatGPT message composer.")
        try:
            composer.fill(prompt, timeout=5000)
        except Exception:
            try:
                composer.click(force=True, timeout=5000)
                composer.press_sequentially(prompt, timeout=15000)
            except Exception as exc:
                raise BrowserError("Cannot edit the ChatGPT message composer.") from exc
        composer.press("Enter")

    def _stop_button_visible(self) -> bool:
        if self.page is None:
            return False
        for selector in (
            "button[aria-label*='Stop']",
            "button:has-text('Stop')",
            "[data-testid*='stop']",
        ):
            try:
                if self.page.locator(selector).count():
                    return True
            except Exception:
                continue
        return False

    def wait_for_response(self, previous_text: str | None = None) -> str:
        deadline = time.monotonic() + self.response_timeout_seconds
        previous = previous_text
        saw_new_text = previous_text is None
        stable = 0
        while time.monotonic() < deadline:
            current = self.latest_assistant_text()
            if self._stop_button_visible():
                stable = 0
            elif previous_text is not None and not saw_new_text and current == previous_text:
                stable = 0
            elif current and current == previous:
                saw_new_text = True
                stable += 1
                if stable >= 2:
                    return current
            else:
                saw_new_text = saw_new_text or bool(current)
                stable = 0
            previous = current
            self.page.wait_for_timeout(int(self.stable_poll_seconds * 1000))
        raise BrowserError("Timed out waiting for the ChatGPT response to finish.")

    def _download_directories(self, destination: Path) -> tuple[Path, ...]:
        directories = [destination]
        configured_download_dir = getattr(self, "download_dir", None)
        if configured_download_dir is not None:
            directories.append(configured_download_dir)
        # Chrome launched with --remote-debugging-port can ignore the command
        # line download directory on some builds.  Its normal Windows fallback
        # is the user's Downloads folder, so include it as a safe fallback.
        directories.append(Path.home() / "Downloads")
        unique: list[Path] = []
        seen: set[Path] = set()
        for directory in directories:
            resolved = directory.resolve()
            if resolved not in seen:
                seen.add(resolved)
                unique.append(resolved)
        return tuple(unique)

    @staticmethod
    def _file_snapshot(directories: tuple[Path, ...]) -> dict[Path, tuple[int, int]]:
        snapshot: dict[Path, tuple[int, int]] = {}
        for directory in directories:
            if not directory.is_dir():
                continue
            try:
                entries = directory.iterdir()
            except OSError:
                continue
            for path in entries:
                if not path.is_file() or path.name.lower().endswith((".crdownload", ".part", ".tmp")):
                    continue
                try:
                    stat = path.stat()
                except OSError:
                    continue
                snapshot[path] = (stat.st_size, stat.st_mtime_ns)
        return snapshot

    def _wait_for_fallback_download(
        self,
        directories: tuple[Path, ...],
        before: dict[Path, tuple[int, int]],
        timeout_seconds: float = 3.0,
    ) -> Path | None:
        deadline = time.monotonic() + timeout_seconds
        stable_candidate: Path | None = None
        stable_size: int | None = None
        stable_count = 0
        while time.monotonic() < deadline:
            after = self._file_snapshot(directories)
            candidates = [
                (path, values)
                for path, values in after.items()
                if path not in before or before[path] != values
            ]
            if candidates:
                path, (size, _) = max(candidates, key=lambda item: item[1][1])
                if path == stable_candidate and size == stable_size:
                    stable_count += 1
                else:
                    stable_candidate = path
                    stable_size = size
                    stable_count = 1
                if stable_count >= 2 and size > 0:
                    return path
            time.sleep(0.25)
        return None

    @staticmethod
    def _unique_target(destination: Path, name: str) -> Path:
        target = destination / Path(name).name
        counter = 2
        while target.exists():
            target = destination / f"{target.stem}-{counter}{target.suffix}"
            counter += 1
        return target

    def _click_candidate(self, candidate) -> None:
        """Click a file control after activating its hover-only toolbar."""
        try:
            candidate.hover(timeout=3000)
        except Exception:
            pass
        mouse = getattr(self.page, "mouse", None)
        if mouse is not None:
            try:
                box = candidate.bounding_box()
                if box:
                    x = box["x"] + box["width"] / 2
                    y = box["y"] + box["height"] / 2
                    mouse.move(x, y)
                    mouse.click(x, y)
                    return
            except Exception:
                pass
        candidate.click()

    def collect_downloads(self, destination: Path) -> list[Path]:
        if self.page is None:
            raise BrowserError("Browser is not connected.")
        destination.mkdir(parents=True, exist_ok=True)
        message = self._latest_assistant_locator()
        # Generated files are currently rendered as file cards.  Depending on
        # the ChatGPT build, the card itself may be an anchor, a button, or a
        # role=button element, and the visible filename may be the only useful
        # metadata.  Keep the search scoped to the latest assistant message so
        # old rounds are not downloaded again.
        selector = (
            "a, button, [role='button'], "
            "[data-testid*='file'], [data-testid*='attachment'], "
            "[data-testid*='download']"
        )
        candidates = message.locator(selector) if message is not None else self.page.locator(selector)
        page_candidates = self.page.locator(selector)
        scan: dict[str, Any] = {
            "message_found": message is not None,
            "scoped_candidate_count": candidates.count(),
            "page_candidate_count": page_candidates.count(),
            "scoped_candidates": [],
            "page_candidates": [],
            "message_html": "",
            "download_attempts": [],
        }

        def candidate_metadata(locator: Any, limit: int = 30) -> list[str]:
            result: list[str] = []
            for candidate_index in range(min(locator.count(), limit)):
                candidate = locator.nth(candidate_index)
                values: list[str] = []
                for attribute in ("href", "download", "aria-label", "title", "data-testid", "data-file-name", "data-filename", "data-name"):
                    try:
                        value = candidate.get_attribute(attribute) or ""
                    except Exception:
                        value = ""
                    if value:
                        values.append(f"{attribute}={value}")
                try:
                    label = re.sub(r"\s+", " ", candidate.inner_text().strip())
                except Exception:
                    label = ""
                if label:
                    values.append(f"text={label[:160]}")
                try:
                    tag = candidate.evaluate("(el) => el.tagName.toLowerCase()")
                    values.insert(0, f"tag={tag}")
                except Exception:
                    pass
                result.append(" | ".join(values)[:500] or "(no readable metadata)")
            return result

        scan["scoped_candidates"] = candidate_metadata(candidates)
        scan["page_candidates"] = candidate_metadata(page_candidates)
        if message is not None:
            try:
                scan["message_html"] = message.evaluate("(el) => el.outerHTML.slice(0, 6000)")
            except Exception:
                pass
        self._attachment_scan = scan
        allowed_suffixes = DEFAULT_ALLOWED_SUFFIXES
        filename_pattern = re.compile(
            r"(?:^|[\s/\\])([^\s/\\]+(?:" + "|".join(re.escape(suffix) for suffix in allowed_suffixes) + r"))(?:$|[\s])",
            flags=re.IGNORECASE,
        )
        downloaded: list[Path] = []
        download_directories = self._download_directories(destination)
        seen_candidates: set[tuple[str, str]] = set()
        direct: list[tuple[Any, str, str, str]] = []
        deferred: list[tuple[Any, str, str, str]] = []
        for index in range(candidates.count()):
            candidate = candidates.nth(index)
            attributes: list[str] = []
            for name in (
                "href",
                "download",
                "aria-label",
                "title",
                "data-testid",
                "data-file-name",
                "data-filename",
                "data-name",
            ):
                try:
                    value = candidate.get_attribute(name) or ""
                except Exception:
                    value = ""
                if value:
                    attributes.append(value)
            try:
                label = candidate.inner_text().strip()
            except Exception:
                label = ""
            metadata = " ".join(attributes + [label])
            href = next((value for value in attributes if value.startswith("sandbox:")), "")
            normalized = metadata.lower()
            if not href and "download" not in normalized and "下载" not in normalized:
                if not filename_pattern.search(metadata):
                    continue
            # A download control has no filename in its own DOM node and is
            # paired with a separate preview button.  Try these controls first;
            # file-name-only cards are a fallback for older ChatGPT layouts.
            is_preview = any(token in normalized for token in ("preview", "预览"))
            is_direct = bool(href) or "download" in normalized or "下载" in normalized
            record = (candidate, href, label, metadata)
            (deferred if is_preview and not href else direct if is_direct else deferred).append(record)

        # Modern cards expose a dedicated download button.  If those controls
        # exist, do not also click the full-card preview buttons: a preview can
        # open a viewer instead of producing a download and would make a round
        # unnecessarily slow.  Older layouts without download controls use the
        # deferred filename cards as their fallback.
        records = direct or deferred
        for candidate, href, label, metadata in records:
            # Do not click a filename card after its dedicated download control
            # has already succeeded.  Generic controls such as "下载文件" have
            # no stable filename, so they are intentionally not deduplicated.
            filename_match = filename_pattern.search(metadata)
            identity = (
                href.lower(),
                filename_match.group(1).lower() if filename_match else re.sub(r"\s+", " ", label.lower()),
            )
            if (href or filename_match) and identity in seen_candidates:
                continue
            if href or filename_match:
                seen_candidates.add(identity)
            attempt: dict[str, Any] = {
                "label": label,
                "metadata": metadata[:500],
                "href": href,
                "method": "not-started",
                "visible": None,
                "enabled": None,
                "bounding_box": None,
                "control_html": "",
                "error": "",
                "fallback_file": "",
            }
            try:
                attempt["visible"] = candidate.is_visible()
            except Exception as exc:
                attempt["visible"] = f"error: {type(exc).__name__}: {exc}"
            try:
                attempt["enabled"] = candidate.is_enabled()
            except Exception as exc:
                attempt["enabled"] = f"error: {type(exc).__name__}: {exc}"
            try:
                attempt["bounding_box"] = candidate.bounding_box()
            except Exception as exc:
                attempt["bounding_box"] = f"error: {type(exc).__name__}: {exc}"
            try:
                attempt["control_html"] = candidate.evaluate("(el) => el.outerHTML.slice(0, 3000)")
            except Exception as exc:
                attempt["control_html"] = f"unavailable: {type(exc).__name__}: {exc}"
            before = self._file_snapshot(download_directories)
            try:
                with self.page.expect_download(timeout=5000) as download_info:
                    self._click_candidate(candidate)
                download = download_info.value
                target = self._unique_target(destination, download.suggested_filename)
                download.save_as(str(target))
                downloaded.append(target)
                attempt["method"] = "playwright-download"
                attempt["fallback_file"] = str(target)
            except Exception as exc:
                attempt["error"] = f"{type(exc).__name__}: {exc}"
                fallback = self._wait_for_fallback_download(download_directories, before, timeout_seconds=5.0)
                if fallback is None:
                    attempt["method"] = "no-download-observed"
                    scan["download_attempts"].append(attempt)
                    continue
                target = self._unique_target(destination, fallback.name)
                try:
                    shutil.copy2(fallback, target)
                except OSError as copy_exc:
                    attempt["method"] = "fallback-copy-failed"
                    attempt["error"] += f"; copy {type(copy_exc).__name__}: {copy_exc}"
                    scan["download_attempts"].append(attempt)
                    continue
                downloaded.append(target)
                attempt["method"] = "fallback-copy"
                attempt["fallback_file"] = str(fallback)
            scan["download_attempts"].append(attempt)
        return downloaded

    def open_new_conversation(self) -> None:
        if self.page is None:
            raise BrowserError("Browser is not connected.")
        self.page.goto("https://chatgpt.com/?new=true", wait_until="domcontentloaded")

    def close(self) -> None:
        if self._browser is not None:
            try:
                self._browser.close()
            except Exception:
                pass
        if self._playwright is not None:
            try:
                self._playwright.stop()
            except Exception:
                pass
        self._browser = None
        self._playwright = None
        self._context = None
        self.page = None


def _json_log(path: Path, event: str, **fields: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"event": event, **fields}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _head_sha(repo_root: Path) -> str | None:
    result = _git(repo_root, "rev-parse", "HEAD", check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def build_continue_prompt(
    state_text: str,
    commit_sha: str | None,
    template: str | None = None,
) -> str:
    base = template or (
        "继续研究。先读取仓库中的 research_state.md 和最近一次提交，"
        "结合现有文件推进 Next step。完成后输出新的成果文件，并在回答末尾包含状态标记。"
    )
    base = base.replace(STATE_BEGIN, "RESEARCH_STATE_BEGIN").replace(STATE_END, "RESEARCH_STATE_END")
    return base.replace("{commit_sha}", commit_sha or "unknown").replace("{state_text}", state_text)


def build_handoff_prompt(
    state_text: str,
    commit_sha: str | None,
    template: str | None = None,
) -> str:
    base = template or (
        "上下文已接近上限。请从仓库中的 research_state.md 继续研究，"
        "不要重复已经完成的内容。最近提交：{commit_sha}\n\n当前状态：\n{state_text}"
    )
    base = base.replace(STATE_BEGIN, "RESEARCH_STATE_BEGIN").replace(STATE_END, "RESEARCH_STATE_END")
    return base.replace("{commit_sha}", commit_sha or "unknown").replace("{state_text}", state_text)


def run_round(
    browser: ChatGPTBrowser,
    config: Config,
    dry_run: bool = False,
    events: list[Any] | None = None,
    previous_response_text: str | None = None,
) -> RoundResult:
    """Process one completed response and send exactly one follow-up prompt."""
    def mark(event: Any) -> None:
        if events is not None:
            events.append(event)

    response = browser.wait_for_response(previous_response_text)
    mark("response")
    if context_limit_detected(response):
        state_path = config.repo_path / "research_state.md"
        state_text = state_path.read_text(encoding="utf-8") if state_path.exists() else ""
        if dry_run:
            mark("dry_run_skip_handoff")
        else:
            browser.open_new_conversation()
            mark("new")
            prompt = build_handoff_prompt(state_text, _head_sha(config.repo_path), config.handoff_prompt)
            browser.send_prompt(prompt)
            mark(("handoff", prompt))
        return RoundResult(
            commit_sha=_head_sha(config.repo_path),
            context_handoff=True,
            response_text=response,
        )

    staging_root = config.staging_dir
    if not staging_root.is_absolute():
        staging_root = config.repo_path / staging_root
    staging_root.mkdir(parents=True, exist_ok=True)
    round_dir = staging_root / time.strftime("%Y%m%d-%H%M%S")
    print("正在收集最新回复的附件…", flush=True)
    downloaded = browser.collect_downloads(round_dir)
    print(f"附件收集完成：{len(downloaded)} 个", flush=True)
    mark("collect")
    state_text = extract_state_block(response)
    if dry_run:
        diagnostic_path = write_dry_run_diagnostic(
            round_dir, browser, response, downloaded, state_text
        )
        print(
            f"Dry-run diagnostic saved: {diagnostic_path} "
            f"(state_block={'yes' if state_text is not None else 'no'}, attachments={len(downloaded)})",
            flush=True,
        )
        if not downloaded and not state_text:
            print(
                "WARNING: the captured latest assistant message contained neither "
                "a research-state block nor downloadable attachments. "
                "Review dry-run-diagnostic.md and confirm chat_url/tab selection.",
                flush=True,
            )
        verifier_results = run_verifiers(config.repo_path, [], config.verify_commands, dry_run=True)
        mark("dry_run_skip_continue")
        return RoundResult(
            changed_paths=tuple(downloaded),
            verifier_results=tuple(verifier_results),
            commit_sha=_head_sha(config.repo_path),
            response_text=response,
        )

    changed: list[Path] = []
    allowed = set(config.allowed_suffixes)
    for artifact in downloaded:
        changed.extend(copy_artifact(artifact, config.repo_path, allowed))

    state_updated = False
    if state_text:
        changed.append(write_research_state(config.repo_path, state_text))
        state_updated = True
    if not changed:
        raise SyncError("The response contained no downloadable artifacts or research state.")

    verifier_results = run_verifiers(config.repo_path, changed, config.verify_commands, dry_run=dry_run)
    commit_message = f"Sync ChatGPT research round {time.strftime('%Y-%m-%d %H:%M:%S')}"
    commit_sha = commit_and_push(
        config.repo_path,
        config.remote,
        config.branch,
        changed,
        commit_message,
        dry_run=dry_run,
    )
    state_for_prompt = state_text or (config.repo_path / "research_state.md").read_text(encoding="utf-8")
    if dry_run:
        mark("dry_run_skip_continue")
    else:
        browser.send_prompt(build_continue_prompt(state_for_prompt, commit_sha, config.continue_prompt))
        mark("continue")
    return RoundResult(
        changed_paths=tuple(sorted(set(changed))),
        verifier_results=tuple(verifier_results),
        commit_sha=commit_sha,
        state_updated=state_updated,
        response_text=response,
    )


def run_loop(config_path: Path, once: bool = False, rounds: int = 0, dry_run: bool = False) -> None:
    config = load_config(config_path)
    if not config.repo_path.is_dir():
        raise SyncError(f"Repository path does not exist: {config.repo_path}")
    if not dry_run and not working_tree_is_clean(config.repo_path):
        raise SyncError("Repository has uncommitted changes; clean the worktree before automation.")
    if not dry_run:
        _git(config.repo_path, "pull", "--ff-only", config.remote, config.branch)

    config.logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = config.logs_dir / "research-sync.jsonl"
    browser = ChatGPTBrowser(
        config.chat_url,
        cdp_port=config.cdp_port,
        response_timeout_seconds=config.response_timeout_seconds,
        stable_poll_seconds=config.stable_poll_seconds,
        download_dir=config.download_dir,
    )
    browser.connect()
    try:
        print("已连接 ChatGPT，等待最新回复…", flush=True)
        browser.wait_for_login()
        if browser.page is not None and config.chat_url.rstrip("/") not in browser.page.url:
            browser.page.goto(config.chat_url, wait_until="domcontentloaded")
        completed = 0
        previous_response_text = None
        while True:
            if once and completed >= 1:
                break
            if not once and rounds > 0 and completed >= rounds:
                break
            result = run_round(
                browser,
                config,
                dry_run=dry_run,
                previous_response_text=previous_response_text,
            )
            completed += 1
            previous_response_text = result.response_text
            print(
                f"第 {completed} 轮完成：下载 {len(result.changed_paths)} 个变更，"
                f"提交 {result.commit_sha or '无'}",
                flush=True,
            )
            _json_log(
                log_path,
                "round_complete",
                commit_sha=result.commit_sha,
                changed_paths=[str(path) for path in result.changed_paths],
                context_handoff=result.context_handoff,
                dry_run=dry_run,
            )
    finally:
        browser.close()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Sync ChatGPT research artifacts to GitHub.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--once", action="store_true", help="Process one response and stop.")
    parser.add_argument("--rounds", type=int, default=0, help="Process N rounds; zero means continuous.")
    parser.add_argument("--dry-run", action="store_true", help="Skip Git mutation and follow-up prompts.")
    args = parser.parse_args()
    run_loop(args.config, once=args.once, rounds=args.rounds, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    main()
