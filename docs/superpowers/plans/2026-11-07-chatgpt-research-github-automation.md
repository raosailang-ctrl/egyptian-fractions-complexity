# ChatGPT Research GitHub Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Windows helper that uses a dedicated Chrome profile to collect ChatGPT research artifacts, update `research_state.md`, verify them, and push each completed round to GitHub.

**Architecture:** A Python Playwright synchronizer connects to a Chrome instance over CDP. Pure file, archive, state, and Git operations stay in small functions that can be tested without a browser; the browser adapter handles selectors, downloads, continuation prompts, and context handoff. A PowerShell launcher owns the dedicated Chrome profile and starts the synchronizer.

**Tech Stack:** Python 3.10+, standard library (`tomllib`, `zipfile`, `tarfile`, `subprocess`, `unittest`), Playwright Python, PowerShell, Git.

**Spec:** `docs/superpowers/specs/2026-11-07-chatgpt-research-github-automation-design.md`

## Global Constraints

- Windows is the primary runtime.
- The dedicated Chrome profile, downloads, logs, and local config remain outside Git.
- The repository is `raosailang-ctrl/egyptian-fractions-complexity`, target branch `main`.
- Synchronization is limited to downloaded artifacts and `research_state.md`; full chat transcripts are not stored.
- Existing unrelated working-tree changes cause the synchronizer to stop before mutation.
- `.git`, `__pycache__`, temporary files, and archive path traversal entries are never copied into the repository.
- Failed verification, failed push, authentication prompts, CAPTCHA, or merge conflicts stop the loop and do not send the next research prompt.

---

### Task 1: Add configuration, state, and safe file primitives

**Files:**
- Create: `research-automation/chatgpt_research_sync.py`
- Create: `research-automation/config.example.toml`
- Create: `research-automation/requirements.txt`
- Create: `research-automation/tests/test_sync.py`
- Modify: `.gitignore`

**Interfaces:**
- `load_config(path: Path) -> Config`
- `extract_state_block(text: str) -> str | None`
- `safe_extract_archive(archive: Path, repo_root: Path, allowed_suffixes: set[str]) -> list[Path]`
- `copy_artifact(src: Path, repo_root: Path, allowed_suffixes: set[str]) -> list[Path]`
- `working_tree_is_clean(repo_root: Path) -> bool`

- [ ] **Step 1: Write failing unit tests**

Add tests for:

```python
class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_extract_state_block_returns_only_marked_content(self):
        text = "before\n<!-- RESEARCH_STATE_BEGIN -->\nNext step: prove lemma\n<!-- RESEARCH_STATE_END -->\nafter"
        self.assertEqual(extract_state_block(text), "Next step: prove lemma")

    def test_safe_extract_archive_flattens_one_outer_directory(self):
        archive = self.root / "package.zip"
        repo = self.root / "repo"
        make_zip(archive, {"package/result.md": "ok", "package/__pycache__/x.pyc": "bad"})
        copied = safe_extract_archive(archive, repo, {".md"})
        self.assertEqual([p.name for p in copied], ["result.md"])

    def test_safe_extract_archive_rejects_path_traversal(self):
        archive = self.root / "package.zip"
        make_zip(archive, {"../escape.md": "bad"})
        with self.assertRaises(SyncError):
            safe_extract_archive(archive, self.root / "repo", {".md"})

    def test_dirty_repository_is_detected(self):
        init_git_repo_with_file(self.root)
        (self.root / "changed.md").write_text("changed", encoding="utf-8")
        self.assertFalse(working_tree_is_clean(self.root))
```

Use `unittest` helpers instead of adding pytest as a runtime dependency. The test module must define `make_zip`, `init_git_repo_with_file`, and a temporary-directory setup using `tempfile.TemporaryDirectory` or `unittest`'s `TemporaryDirectory` helper.

- [ ] **Step 2: Run the focused tests and confirm they fail**

Run:

```powershell
python -m unittest research-automation.tests.test_sync -v
```

Expected: import or missing-function failures because the primitives are not implemented yet.

- [ ] **Step 3: Implement the primitives**

Create a `Config` dataclass with repository, browser, directory, Git, and prompt fields. Parse TOML with `tomllib`. Implement archive handling with `zipfile` and `tarfile`; normalize each member, reject absolute paths and paths that resolve outside `repo_root`, flatten a single common directory, and skip `.git`, `__pycache__`, hidden temporary names, and suffixes outside the configured allowlist. Implement Git status through `subprocess.run(["git", "status", "--porcelain"], check=True, ...)`.

- [ ] **Step 4: Run the focused tests and confirm they pass**

Run:

```powershell
python -m unittest research-automation.tests.test_sync -v
```

Expected: all archive, state, and clean-tree tests pass.

- [ ] **Step 5: Commit the primitive layer**

```powershell
git add .gitignore research-automation/chatgpt_research_sync.py research-automation/config.example.toml research-automation/requirements.txt research-automation/tests/test_sync.py
git commit -m "Add research sync configuration and safe file primitives"
```

### Task 2: Add Git staging, verification, and state persistence

**Files:**
- Modify: `research-automation/chatgpt_research_sync.py`
- Modify: `research-automation/tests/test_sync.py`
- Create: `research_state.md`

**Interfaces:**
- `write_research_state(repo_root: Path, state_text: str) -> Path`
- `run_verifiers(repo_root: Path, changed_paths: list[Path], commands: list[str], dry_run: bool) -> list[CommandResult]`
- `commit_and_push(repo_root: Path, remote: str, branch: str, paths: list[Path], message: str, dry_run: bool) -> str | None`

- [ ] **Step 1: Write failing tests**

Cover state replacement, command failure, selected-path staging, and commit message generation. A verification failure must raise `VerificationError` and leave Git untouched.

- [ ] **Step 2: Run the focused tests and confirm they fail**

```powershell
python -m unittest research-automation.tests.test_sync -v
```

- [ ] **Step 3: Implement state and Git operations**

Write only the extracted state block to `research_state.md`. Run only commands explicitly listed in TOML, with the repository root as the working directory. Stage exact changed paths plus `research_state.md`; never call `git add .`. Before committing, run `git pull --ff-only origin main`; after committing, run `git push origin main`. Return the new SHA from `git rev-parse HEAD`.

- [ ] **Step 4: Add the initial state template**

Create `research_state.md` with the six required headings: `Current question`, `Completed`, `Evidence`, `Open problems`, `Next step`, and `Artifacts`.

- [ ] **Step 5: Run tests and commit**

```powershell
python -m unittest research-automation.tests.test_sync -v
git add research-automation/chatgpt_research_sync.py research-automation/tests/test_sync.py research_state.md
git commit -m "Add research state and verified Git publishing"
```

### Task 3: Add the Playwright browser adapter

**Files:**
- Modify: `research-automation/chatgpt_research_sync.py`
- Modify: `research-automation/tests/test_sync.py`

**Interfaces:**
- `class ChatGPTBrowser:`
- `connect() -> None`
- `wait_for_login() -> None`
- `latest_assistant_text() -> str`
- `send_prompt(prompt: str) -> None`
- `collect_downloads(destination: Path) -> list[Path]`
- `open_new_conversation() -> None`
- `close() -> None`

- [ ] **Step 1: Add adapter tests using a fake page**

Test that the adapter recognizes a completed response, extracts assistant text from the preferred role selector, and marks context-limit phrases such as `conversation is too long`, `maximum context`, and `context length`.

- [ ] **Step 2: Run adapter tests and confirm they fail**

```powershell
python -m unittest research-automation.tests.test_sync -v
```

- [ ] **Step 3: Implement CDP connection**

Use `playwright.sync_api.sync_playwright()` and `chromium.connect_over_cdp(f"http://127.0.0.1:{port}")`. Prefer selectors in this order: `[data-message-author-role='assistant']`, `main article`, then a bounded `main` fallback. Locate the composer through `textarea` and contenteditable fallbacks. Wait for the stop button to disappear and for assistant text to remain unchanged across two polling intervals.

- [ ] **Step 4: Implement downloads and context detection**

For each link whose href begins with `sandbox:` or whose text contains `download`, click inside `page.expect_download`, save to the external staging directory, and ignore duplicate filenames. Expose `context_limit_detected(text: str) -> bool` as a pure helper so it can be tested without a browser.

- [ ] **Step 5: Run tests and commit**

```powershell
python -m unittest research-automation.tests.test_sync -v
git add research-automation/chatgpt_research_sync.py research-automation/tests/test_sync.py
git commit -m "Add Playwright ChatGPT browser adapter"
```

### Task 4: Add the round loop and context handoff

**Files:**
- Modify: `research-automation/chatgpt_research_sync.py`
- Modify: `research-automation/tests/test_sync.py`
- Modify: `research-automation/config.example.toml`

**Interfaces:**
- `run_round(browser: ChatGPTBrowser, config: Config) -> RoundResult`
- `build_continue_prompt(state_text: str, commit_sha: str | None) -> str`
- `build_handoff_prompt(state_text: str, commit_sha: str | None) -> str`
- `run_loop(config_path: Path, once: bool, dry_run: bool) -> None`

- [ ] **Step 1: Write failing orchestration tests**

Test that a successful round follows the order `collect -> overlay -> state -> verify -> commit -> continue`, that a verification failure does not send the continuation prompt, and that a context-limit response calls `open_new_conversation` before sending the handoff prompt.

- [ ] **Step 2: Run orchestration tests and confirm they fail**

```powershell
python -m unittest research-automation.tests.test_sync -v
```

- [ ] **Step 3: Implement one-round orchestration**

Create a staging directory outside the repository. Pull fast-forward before starting. Require a clean tree. Collect downloads, overlay them, extract the state marker from the final assistant response, write `research_state.md`, run configured verifiers, commit selected paths, push, then send the continuation prompt. Return a structured `RoundResult` containing changed paths, verifier results, and commit SHA.

- [ ] **Step 4: Implement context handoff and loop controls**

When context-limit detection returns true, open `https://chatgpt.com/?new=true`, wait for the composer, and send a prompt containing the repository URL, latest commit SHA, and the complete `research_state.md` contents. Support `--once`, `--rounds N`, `--dry-run`, and Ctrl+C. Log each round as JSON lines outside the repository.

- [ ] **Step 5: Run tests and commit**

```powershell
python -m unittest research-automation.tests.test_sync -v
git add research-automation/chatgpt_research_sync.py research-automation/tests/test_sync.py research-automation/config.example.toml
git commit -m "Add research rounds and context handoff"
```

### Task 5: Add launcher, documentation, and runtime setup

**Files:**
- Create: `research-automation/start_chatgpt_research.ps1`
- Create: `research-automation/README.md`
- Modify: `research-automation/config.example.toml`
- Modify: `.gitignore`

- [ ] **Step 1: Write the launcher**

The PowerShell script must create external paths, find Chrome in the two standard Windows installation locations, start it with `--user-data-dir`, `--remote-debugging-port`, `--download-default-directory`, and the configured chat URL, then invoke the Python synchronizer. It must not put the profile or downloads under the repository.

- [ ] **Step 2: Add configuration and ignore rules**

Document `config.toml`, `chat_url`, `repo_path`, `verify_commands`, and the external paths. Add these patterns to `.gitignore`: `research-automation/config.toml`, local profile directories, external staging, and logs.

- [ ] **Step 3: Document first-run and recovery**

Explain `pip install -r research-automation/requirements.txt`, first login in the separate Chrome window, `--once`, `--dry-run`, continuous mode, CAPTCHA handling, and push conflict recovery. State that the profile directory contains login cookies and must not be copied or committed.

- [ ] **Step 4: Run offline tests and commit**

```powershell
python -m unittest research-automation.tests.test_sync -v
git diff --check
git add research-automation/start_chatgpt_research.ps1 research-automation/README.md research-automation/config.example.toml .gitignore
git commit -m "Add Windows launcher and research automation instructions"
```

### Task 6: Run first live dry run and verify the complete workflow

**Files:**
- Modify: `research-automation/config.toml` locally only; do not commit it.
- Modify: `research_state.md` only if the user chooses a real one-round run.

- [ ] **Step 1: Create local config from the example**

Set the absolute repository path, the current ChatGPT research conversation URL, the target branch `main`, and one explicitly allowed verifier command.

- [ ] **Step 2: Start the dedicated browser and log in**

Run the PowerShell launcher. If ChatGPT requests login, complete it manually in the dedicated window and return to the terminal.

- [ ] **Step 3: Run one dry round**

```powershell
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun
```

Expected: the script connects to the conversation, identifies the composer and latest response, reports candidate downloads, and performs no Git commit or push.

- [ ] **Step 4: Run offline verification after the dry run**

```powershell
python -m unittest research-automation.tests.test_sync -v
git diff --check
```

- [ ] **Step 5: Run one real round only after the dry run is reviewed**

```powershell
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once
```

Expected: new artifacts and `research_state.md` are staged selectively, the configured verifier passes, a commit is pushed, and only then is the continuation prompt sent.

- [ ] **Step 6: Final verification**

```powershell
git status --short --branch
git log -1 --oneline --decorate
git ls-remote origin refs/heads/main
```

Expected: the worktree is clean and the remote branch points to the new commit.
