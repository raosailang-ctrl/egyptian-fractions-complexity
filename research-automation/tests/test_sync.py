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


if __name__ == "__main__":
    unittest.main()
