Current question:
Verify actual attachment-card detection and download in the dedicated Chrome synchronizer after the visible research-state marker fix passed.

Completed:
- User successfully pulled origin/main over HTTP/1.1 from 1cc9657 to b7ec246.
- User reran the dedicated Chrome launcher with -Once -DryRun.
- Live output confirms ChatGPT connected, diagnostic saved, and state_block=yes.
- This verifies that visible RESEARCH_STATE_BEGIN/END markers are now extracted correctly from browser inner_text().
- Attachment count was zero, which is expected for the captured text-only assistant response; attachment detection remains untested.
- Created a harmless Markdown attachment smoke-test artifact for the next dry-run.
- Recorded the successful live state-marker test in the repository.

Evidence:
- User console: diagnostic path C:\egypt fractions\chatgpt-automation-staging\20261107-210954\dry-run-diagnostic.md.
- User console: state_block=yes, attachments=0.
- User console: round completed with unchanged HEAD b7ec24607e50e4de0a7047138a297f33f3eeff25.
- Live result note: research-automation/VISIBLE_STATE_MARKER_DRY_RUN_PASSED_2026-11-07.md.
- No real synchronization or synchronizer-driven commit/push occurred.

Open problems:
- Attachment-card detection/download has not yet been tested with a real attachment.
- The actual downloaded attachment name and size are not yet known.
- Real sync remains disabled.

Next step:
Run the launcher again with -Once -DryRun while this assistant response containing attachment-smoke-test-2026-11-07.md is the latest response. Confirm the diagnostic says state_block=yes and attachments=1, and verify the staged file has non-zero size. Keep -DryRun enabled.

Artifacts:
- research-automation/VISIBLE_STATE_MARKER_DRY_RUN_PASSED_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/tests/test_sync.py
- research_state.md
- attachment-smoke-test-2026-11-07.md
