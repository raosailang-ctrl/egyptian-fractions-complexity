Current question:
Complete the first dedicated Chrome dry-run after updating the stale local synchronizer; inspect the generated diagnostic to identify whether the wrong conversation/message was captured or the attachment selector failed.

Completed:
- Read the repository research_state.md and recent commits.
- User reran git pull --ff-only origin main; it failed with "Recv failure: Connection was reset".
- User then reran the launcher, but the traceback still showed the old SyncError branch. This confirms the local working copy had not received the diagnostic fix; the second dry-run did not test the new code.
- Verified the current GitHub source contains write_dry_run_diagnostic(), writes dry-run-diagnostic.md with real line breaks, and warns rather than raising when no state block and no attachments are found.
- Added a recovery note with two safe update routes: retry Git over HTTP/1.1, or download the one source file from raw.githubusercontent.com and verify its exact Git blob SHA before replacing the local file.
- No attachment selector changes were made because the captured response is still unknown.

Evidence:
- User screenshot: git pull failed with "fatal: unable to access ... Recv failure: Connection was reset".
- Same screenshot: following dry-run still raised the old SyncError: The response contained no downloadable artifacts or research state. This is the stale local code path.
- Current GitHub source blob SHA: 4a70ee401ebebfb0961b4467e3faf693517c7a85.
- Diagnostic fix commits: b7b89d67f95f82823e9989c0d724b1ea24b46089; newline correction 2cd4ee26be0a717e1328ccc72acbc125b17eeafd.
- Regression test commit: 2c6cd498711f383d3e24f039c6128cd0dad253ec.
- Recovery documentation commit: 7b494545e9d9b296834b5c12190f50b29ff769ef.
- Diagnostic source change and test have been committed on GitHub; no real browser dry-run with the updated file has yet occurred.

Open problems:
- Local synchronizer is still stale until updated from GitHub.
- Git HTTPS connection reset prevents normal pull at present.
- The actual page URL, captured assistant response, state-marker status, and attachment list remain unknown.
- The raw GitHub fallback download has not yet been attempted.
- Do not run a real sync or remove DryRun.

Next step:
1. Try git -c http.version=HTTP/1.1 pull --ff-only origin main.
2. If it still fails, download only research-automation/chatgpt_research_sync.py from https://raw.githubusercontent.com/raosailang-ctrl/egyptian-fractions-complexity/main/research-automation/chatgpt_research_sync.py, then verify git hash-object equals 4a70ee401ebebfb0961b4467e3faf693517c7a85 before replacing the local file.
3. Confirm Select-String finds write_dry_run_diagnostic and Dry-run diagnostic saved.
4. Rerun the launcher with -Once -DryRun.
5. Send the console output and newest dry-run-diagnostic.md for review.

Artifacts:
- research-automation/WINDOWS_DRY_RUN_GIT_RESET_RECOVERY_2026-11-07.md
- research-automation/DRY_RUN_PREFLIGHT_AUDIT_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/tests/test_sync.py
- research_state.md
