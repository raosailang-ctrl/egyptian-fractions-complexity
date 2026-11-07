Current question:
Diagnose the first dedicated Chrome dry-run that connected successfully but captured zero attachments and no research-state marker; rerun once and inspect the saved diagnostic before enabling real sync.

Completed:
- Read research_state.md and recent GitHub commits; inspected the latest tab-selection/composer fix and the current dry-run implementation.
- User executed the dedicated Chrome launcher with -Once -DryRun. The screenshot confirms Chrome/ChatGPT connected, but the synchronizer reported 0 attachments and raised SyncError because no state block was extracted.
- Audited the relevant code path. The old dry-run branch raised immediately and discarded the captured assistant response, so the failure could not be diagnosed.
- Added write_dry_run_diagnostic() to save the captured page URL, response character count, state-marker detection, attachment names/sizes, and full captured assistant response under the staging round directory.
- Changed zero-artifact dry-runs to emit a warning and return safely instead of throwing; they still do not modify repository files or send a continuation prompt.
- Added a regression test for the zero-state/zero-attachment path.
- Reviewed the new diagnostic writer and corrected its line joining to use real newline characters.
- Updated the repository state after the changes.

Evidence:
- User screenshot: successful connection; "附件收集完成：0 个"; previous SyncError at run_round.
- Code commits:
  - b7b89d67f95f82823e9989c0d724b1ea24b46089 (diagnostic report)
  - 2c6cd498711f383d3e24f039c6128cd0dad253ec (regression test)
  - 2cd4ee26be0a717e1328ccc72acbc125b17eeafd (fix diagnostic line breaks)
  - 8da17339b0d82e2993a5ea35196e568d9c794758 (state record before this update)
- The screenshot does not establish whether the configured chat_url points to the intended conversation or whether the latest-message selector captured the intended message.
- Code review confirms the diagnostic is written only to staging during dry-run; no actual repository overlay, state replacement, verifier execution, Git commit/push, or continuation prompt occurs.

Open problems:
- The updated code and regression test have not yet been executed on the user's Windows machine.
- The captured page URL and assistant response are unknown until the new diagnostic file is inspected.
- The local config.toml and authenticated Chrome profile are not accessible through GitHub.
- Attachment selector changes should not be made until the diagnostic shows whether the wrong message was captured or the correct message genuinely has no attachments/state marker.
- Do not run a real sync yet.

Next step:
1. On Windows, pull the latest main branch.
2. Rerun: powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun
3. Open the newest dry-run-diagnostic.md under the configured staging directory.
4. Inspect Page URL, State block found, Downloaded attachments, and the captured response. Send the diagnostic and console output, redacting private text if needed.
5. Only after confirming the correct conversation/message and complete downloads should the first real sync be considered.

Artifacts:
- research-automation/DRY_RUN_PREFLIGHT_AUDIT_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/tests/test_sync.py
- research_state.md
