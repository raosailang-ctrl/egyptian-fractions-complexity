from __future__ import annotations

import json
import re
import shutil
import subprocess
import tarfile
import tomllib
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


class SyncError(RuntimeError):
    """Raised when a synchronization operation cannot be completed safely."""


class VerificationError(SyncError):
    """Raised when a configured verifier returns a non-zero exit code."""


class BrowserError(SyncError):
    """Raised when the browser cannot provide a usable ChatGPT page."""


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
    """Return the marked state payload, or None when the response omitted it."""
    pattern = re.escape(STATE_BEGIN) + r"\s*(.*?)\s*" + re.escape(STATE_END)
    match = re.search(pattern, text, flags=re.DOTALL)
    return match.group(1).strip() if match else None


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


def _json_log(path: Path, event: str, **fields: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"event": event, **fields}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> int:
    raise SystemExit("Browser orchestration is added in the next implementation task.")


if __name__ == "__main__":
    main()
