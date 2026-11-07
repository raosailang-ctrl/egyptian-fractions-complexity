Current question:
Diagnose the first dedicated Chrome dry-run that connected successfully but captured zero attachments and no research-state marker; rerun once and inspect the saved diagnostic before enabling real sync.

Completed:
- Read research_state.md and latest commit history. Baseline before this round was ca5ffdad7b1ad149cde06de77c2c963b563bdd7a; the repository state also contained the dry-run preflight audit.
- Reviewed the latest Chrome tab-selection/composer fix and the synchronizer's response capture, attachment collection, and dry-run branches.
- User executed: powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun.
- Live result: Chrome connected and waited; attachment collection returned 0; run stopped with SyncError: "The response contained no downloadable artifacts or research state."
- Identified that the old dry-run branch discarded the captured assistant response when both the state marker and attachments were missing, preventing diagnosis.
- Updated research-automation/chatgpt_research_sync.py so every dry-run writes staging/<round>/dry-run-diagnostic.md with page URL, response character count, state-marker detection, attachment names/sizes, and captured latest assistant response. A zero-artifact response now emits a warning and exits without changing repository files or sending a continuation prompt.
- Added a regression test covering the zero-state/zero-attachment case.

Evidence:
- User-provided live screenshot shows successful CDP/ChatGPT connection, 0 attachments, then SyncError at run_round line 833.
- Code commit: b7b89d67f95f82823e9989c0d724b1ea24b46089.
- Test commit: 2c6cd498711f383d3e24f039c6128cd0dad253ec.
- Updated source blob SHA: 8a5791c773d65df705f63ff7e0a01cc5a7292989.
- Updated test blob SHA: 2c67adb8486554c640ba0574fc7163dcca8595cb.
- Previous preflight audit: research-automation/DRY_RUN_PREFLIGHT_AUDIT_2026-11-07.md.
- No real sync, commit or push was performed by the local dry-run; the above GitHub commits are this assistant's repository edits.

Open problems:
- The actual captured page URL and latest assistant response have not yet been inspected; zero attachments alone does not prove wrong conversation or broken selectors.
- The user's local config.toml and authenticated Chrome profile are not accessible through GitHub.
- The new diagnostic code has not yet been executed on the user's Windows machine.
- Once the diagnostic is reviewed, attachment-card selectors or chat_url may need adjustment.

Next step:
On Windows, pull the latest main branch, then rerun:
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun
Open the newest dry-run-diagnostic.md under the configured staging directory. Check Page URL, State block found, Downloaded attachments, and the captured latest assistant response. Send the diagnostic text (redacting private content if desired) and the PowerShell output for the next targeted fix. Do not run without -DryRun yet.

Artifacts:
- research-automation/DRY_RUN_PREFLIGHT_AUDIT_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/tests/test_sync.py
- research_state.md
