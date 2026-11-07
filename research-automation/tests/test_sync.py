import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "chatgpt_research_sync.py"
SPEC = importlib.util.spec_from_file_location("chatgpt_research_sync", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load synchronizer module from {MODULE_PATH}")
sync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync
SPEC.loader.exec_module(sync)


def make_zip(path: Path, files: dict[str, str]) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)


def init_git_repo_with_file(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "tracked.md").write_text("tracked", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Test User"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "tracked.md"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "initial"], check=True)
    subprocess.run(["git", "-C", str(root), "branch", "-M", "main"], check=True)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_extract_state_block_returns_only_marked_content(self):
        text = (
            "before\n"
            "<!-- RESEARCH_STATE_BEGIN -->\n"
            "Next step: prove lemma\n"
            "<!-- RESEARCH_STATE_END -->\n"
            "after"
        )
        self.assertEqual(sync.extract_state_block(text), "Next step: prove lemma")

    def test_extract_state_block_accepts_visible_markers(self):
        text = (
            "before\n"
            "RESEARCH_STATE_BEGIN\n"
            "Next step: prove lemma\n"
            "Artifacts: report.md\n"
            "RESEARCH_STATE_END\n"
            "after"
        )
        self.assertEqual(
            sync.extract_state_block(text),
            "Next step: prove lemma\nArtifacts: report.md",
        )

    def test_prompt_builders_convert_legacy_html_markers_to_visible_text(self):
        template = "Return state: <!-- RESEARCH_STATE_BEGIN --> ... <!-- RESEARCH_STATE_END -->"
        self.assertEqual(
            sync.build_continue_prompt("state", "abc", template),
            "Return state: RESEARCH_STATE_BEGIN ... RESEARCH_STATE_END",
        )
        self.assertEqual(
            sync.build_handoff_prompt("state", "abc", template),
            "Return state: RESEARCH_STATE_BEGIN ... RESEARCH_STATE_END",
        )

    def test_safe_extract_archive_flattens_one_outer_directory(self):
        archive = self.root / "package.zip"
        repo = self.root / "repo"
        make_zip(
            archive,
            {
                "package/result.md": "ok",
                "package/__pycache__/x.pyc": "bad",
            },
        )
        copied = sync.safe_extract_archive(archive, repo, {".md"})
        self.assertEqual([path.name for path in copied], ["result.md"])
        self.assertEqual((repo / "result.md").read_text(encoding="utf-8"), "ok")

    def test_safe_extract_archive_rejects_path_traversal(self):
        archive = self.root / "package.zip"
        make_zip(archive, {"../escape.md": "bad"})
        with self.assertRaises(sync.SyncError):
            sync.safe_extract_archive(archive, self.root / "repo", {".md"})

    def test_dirty_repository_is_detected(self):
        init_git_repo_with_file(self.root)
        (self.root / "changed.md").write_text("changed", encoding="utf-8")
        self.assertFalse(sync.working_tree_is_clean(self.root))

    def test_write_research_state_replaces_file(self):
        state_path = sync.write_research_state(self.root, "Next step: prove lemma")
        self.assertEqual(state_path, self.root / "research_state.md")
        self.assertEqual(state_path.read_text(encoding="utf-8"), "Next step: prove lemma\n")

    def test_run_verifiers_raises_when_command_fails(self):
        init_git_repo_with_file(self.root)
        command = f'"{sys.executable}" -c "raise SystemExit(2)"'
        with self.assertRaises(sync.VerificationError):
            sync.run_verifiers(self.root, [], [command], dry_run=False)

    def test_commit_and_push_updates_bare_remote(self):
        init_git_repo_with_file(self.root)
        remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        subprocess.run(["git", "-C", str(self.root), "remote", "add", "origin", str(remote)], check=True)
        subprocess.run(["git", "-C", str(self.root), "push", "-qu", "origin", "main"], check=True)
        artifact = self.root / "result.md"
        artifact.write_text("result", encoding="utf-8")
        sha = sync.commit_and_push(
            self.root,
            "origin",
            "main",
            [artifact],
            "Update research result",
            dry_run=False,
        )
        remote_sha = subprocess.run(
            ["git", "--git-dir", str(remote), "rev-parse", "refs/heads/main"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        self.assertEqual(sha, remote_sha)

    def test_context_limit_detection_matches_common_messages(self):
        self.assertTrue(sync.context_limit_detected("This conversation is too long to continue."))
        self.assertTrue(sync.context_limit_detected("maximum context length reached"))
        self.assertFalse(sync.context_limit_detected("The proof is complete; continue with the next lemma."))

    def test_latest_assistant_text_uses_author_role_locator(self):
        class Locator:
            def count(self):
                return 2

            def nth(self, index):
                return self

            def inner_text(self):
                return "latest assistant result"

        class Page:
            def locator(self, selector):
                self.selector = selector
                return Locator()

        browser = sync.ChatGPTBrowser.__new__(sync.ChatGPTBrowser)
        self.assertEqual(browser.latest_assistant_text(Page()), "latest assistant result")

    def test_run_round_publishes_state_before_continuation(self):
        init_git_repo_with_file(self.root)
        remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        subprocess.run(["git", "-C", str(self.root), "remote", "add", "origin", str(remote)], check=True)
        subprocess.run(["git", "-C", str(self.root), "push", "-qu", "origin", "main"], check=True)
        events = []

        class FakeBrowser:
            def wait_for_response(self, previous_text=None):
                return (
                    "artifact result\n"
                    "<!-- RESEARCH_STATE_BEGIN -->\n"
                    "Next step: check lemma\n"
                    "<!-- RESEARCH_STATE_END -->"
                )

            def collect_downloads(self, destination):
                return []

            def send_prompt(self, prompt):
                pass

            def open_new_conversation(self):
                pass

        config = sync.Config(
            repo_path=self.root,
            chat_url="https://chatgpt.com/",
            continue_prompt="continue",
            handoff_prompt="handoff {commit_sha} {state_text}",
        )
        result = sync.run_round(FakeBrowser(), config, dry_run=False, events=events)
        self.assertFalse(result.context_handoff)
        self.assertEqual(events, ["response", "collect", "continue"])
        self.assertIn("Next step: check lemma", (self.root / "research_state.md").read_text(encoding="utf-8"))

    def test_dry_run_does_not_modify_repository_files(self):
        init_git_repo_with_file(self.root)
        events = []

        class FakeBrowser:
            def wait_for_response(self, previous_text=None):
                return (
                    "artifact result\n"
                    "<!-- RESEARCH_STATE_BEGIN -->\n"
                    "Next step: check lemma\n"
                    "<!-- RESEARCH_STATE_END -->"
                )

            def collect_downloads(self, destination):
                destination.mkdir(parents=True, exist_ok=True)
                artifact = destination / "result.md"
                artifact.write_text("result", encoding="utf-8")
                return [artifact]

            def send_prompt(self, prompt):
                raise AssertionError("dry-run must not send a continuation prompt")

            def open_new_conversation(self):
                raise AssertionError("dry-run must not open a new conversation")

        config = sync.Config(repo_path=self.root, chat_url="https://chatgpt.com/")
        sync.run_round(FakeBrowser(), config, dry_run=True, events=events)
        self.assertEqual(events, ["response", "collect", "dry_run_skip_continue"])
        self.assertFalse((self.root / "research_state.md").exists())
        self.assertFalse((self.root / "result.md").exists())

    def test_dry_run_writes_diagnostic_when_state_and_attachments_are_missing(self):
        init_git_repo_with_file(self.root)

        class FakeBrowser:
            page = type("Page", (), {"url": "https://chatgpt.com/c/example"})()
            _attachment_scan = {
                "message_found": True,
                "scoped_candidate_count": 0,
                "page_candidate_count": 1,
                "scoped_candidates": [],
                "page_candidates": ["tag=button | text=attachment.md"],
                "message_html": "<div>attachment</div>",
            }

            def wait_for_response(self, previous_text=None):
                return "Captured response without state marker."

            def collect_downloads(self, destination):
                destination.mkdir(parents=True, exist_ok=True)
                return []

            def send_prompt(self, prompt):
                raise AssertionError("dry-run must not send a continuation prompt")

        config = sync.Config(
            repo_path=self.root,
            chat_url="https://chatgpt.com/c/example",
            staging_dir=self.root / "outside-staging",
        )
        result = sync.run_round(FakeBrowser(), config, dry_run=True)
        self.assertEqual(result.changed_paths, ())
        diagnostic = self.root / "outside-staging"
        reports = list(diagnostic.glob("*/dry-run-diagnostic.md"))
        self.assertEqual(len(reports), 1)
        report = reports[0].read_text(encoding="utf-8")
        self.assertIn("State block found: no", report)
        self.assertIn("Captured response without state marker.", report)
        self.assertIn("Page-wide candidate count: 1", report)
        self.assertIn("tag=button | text=attachment.md", report)
        self.assertFalse((self.root / "research_state.md").exists())

    def test_run_round_hands_off_when_context_is_exhausted(self):
        init_git_repo_with_file(self.root)
        events = []

        class FakeBrowser:
            def wait_for_response(self, previous_text=None):
                return "The conversation is too long to continue."

            def collect_downloads(self, destination):
                return []

            def open_new_conversation(self):
                pass

            def send_prompt(self, prompt):
                pass

        config = sync.Config(
            repo_path=self.root,
            chat_url="https://chatgpt.com/",
            continue_prompt="continue",
            handoff_prompt="handoff {commit_sha} {state_text}",
        )
        result = sync.run_round(FakeBrowser(), config, dry_run=False, events=events)
        self.assertTrue(result.context_handoff)
        self.assertEqual(events[0:2], ["response", "new"])
        self.assertEqual(events[2][0], "handoff")

    def test_prompt_builders_insert_state_and_commit(self):
        self.assertEqual(
            sync.build_continue_prompt("state", "abc123", "continue {commit_sha} {state_text}"),
            "continue abc123 state",
        )
        self.assertEqual(
            sync.build_handoff_prompt("state", "abc123", "handoff {commit_sha} {state_text}"),
            "handoff abc123 state",
        )

    def test_wait_for_response_ignores_previous_assistant_message(self):
        class Page:
            def wait_for_timeout(self, milliseconds):
                pass

        browser = sync.ChatGPTBrowser.__new__(sync.ChatGPTBrowser)
        browser.page = Page()
        browser.response_timeout_seconds = 1
        browser.stable_poll_seconds = 0
        values = iter(["old answer", "old answer", "new answer", "new answer", "new answer"])
        browser.latest_assistant_text = lambda: next(values)
        browser._stop_button_visible = lambda: False
        self.assertEqual(browser.wait_for_response("old answer"), "new answer")

    def test_collect_downloads_reads_links_from_latest_assistant_message(self):
        class Download:
            suggested_filename = "result.md"

            def save_as(self, target):
                Path(target).write_text("result", encoding="utf-8")

        class DownloadContext:
            def __init__(self):
                self.value = Download()

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                return False

        class Link:
            def get_attribute(self, name):
                return "sandbox:/mnt/data/result.md" if name == "href" else None

            def inner_text(self):
                return "Download result"

            def click(self):
                pass

        class Links:
            def count(self):
                return 1

            def nth(self, index):
                return Link()

        class Message:
            def count(self):
                return 1

            def nth(self, index):
                return self

            def locator(self, selector):
                return Links()

        class Page:
            def locator(self, selector):
                return Message()

            def expect_download(self, timeout):
                return DownloadContext()

        browser = sync.ChatGPTBrowser.__new__(sync.ChatGPTBrowser)
        browser.page = Page()
        destination = self.root / "downloads"
        files = browser.collect_downloads(destination)
        self.assertEqual([path.name for path in files], ["result.md"])
        self.assertEqual(files[0].read_text(encoding="utf-8"), "result")

    def test_collect_downloads_reads_filename_from_attachment_button(self):
        class Download:
            suggested_filename = "verify_explicit_modular_sieve.py"

            def save_as(self, target):
                Path(target).write_text("result", encoding="utf-8")

        class DownloadContext:
            def __init__(self):
                self.value = Download()

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                return False

        class AttachmentButton:
            def get_attribute(self, name):
                return None

            def inner_text(self):
                return "verify_explicit_modular_sieve.py\n代码"

            def click(self):
                pass

        class Candidates:
            def count(self):
                return 1

            def nth(self, index):
                return AttachmentButton()

        class Message:
            def count(self):
                return 1

            def nth(self, index):
                return self

            def locator(self, selector):
                self.selector = selector
                return Candidates()

        class Page:
            def locator(self, selector):
                return Message()

            def expect_download(self, timeout):
                return DownloadContext()

        browser = sync.ChatGPTBrowser.__new__(sync.ChatGPTBrowser)
        browser.page = Page()
        destination = self.root / "downloads"
        files = browser.collect_downloads(destination)
        self.assertEqual([path.name for path in files], ["verify_explicit_modular_sieve.py"])
        self.assertEqual(files[0].read_text(encoding="utf-8"), "result")

    def test_collect_downloads_falls_back_to_browser_download_directory(self):
        fallback_dir = self.root / "browser-downloads"
        fallback_dir.mkdir()

        class DownloadContext:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                return False

        class AttachmentButton:
            def get_attribute(self, name):
                return None

            def inner_text(self):
                return "result.md"

            def click(self):
                (fallback_dir / "result.md").write_text("result", encoding="utf-8")
                raise TimeoutError("CDP download event unavailable")

        class Candidates:
            def count(self):
                return 1

            def nth(self, index):
                return AttachmentButton()

        class Message:
            def count(self):
                return 1

            def nth(self, index):
                return self

            def locator(self, selector):
                return Candidates()

        class Page:
            def locator(self, selector):
                return Message()

            def expect_download(self, timeout):
                return DownloadContext()

        browser = sync.ChatGPTBrowser.__new__(sync.ChatGPTBrowser)
        browser.page = Page()
        browser.download_dir = fallback_dir
        destination = self.root / "downloads"
        files = browser.collect_downloads(destination)
        self.assertEqual([path.name for path in files], ["result.md"])
        self.assertEqual(files[0].read_text(encoding="utf-8"), "result")


if __name__ == "__main__":
    unittest.main()
