Current question:
Use the new attachment DOM scan diagnostics to identify why the assistant file card is visible in the captured response but the collector downloads zero files.

Completed:
- Reviewed the user's UTF-8 diagnostic from round 20261107-211358.
- Confirmed the correct research conversation URL and that the captured 884-character assistant response is the preceding attachment smoke-test instruction.
- Confirmed the captured response ends with the attachment filename and document label, so the intended file card is represented in rendered text.
- Concluded that zero downloads most likely comes from the collector's candidate selector or its message-scoped search, not from chat_url or latest-message selection.
- Explained state_block=no: that captured assistant answer used legacy HTML-comment delimiters, which inner_text() omits. Visible standalone markers are required.
- Added DOM instrumentation to record latest-message locator status, scoped/page-wide candidate counts, candidate metadata, and a truncated latest-message HTML snapshot. It does not click broader page candidates.
- Added a regression test for diagnostic metadata and documented the workflow in README.

Evidence:
- User diagnostic URL: https://chatgpt.com/c/6aeddb48-9710-83ea-98b5-3458eb53642a.
- Captured response length: 884 characters.
- Captured text ends with attachment-smoke-test-2026-11-07.md and the document label.
- User diagnostic: state_block=no, attachments=0.
- DOM scan instrumentation commit: 114d20225a0d5ff33542ac446f1b5c4ea687a063.
- Whitespace fix: 53546ad62f00426b62f83d8486cc6d89000f39f6.
- Regression test: 55099cf474cb0d74d253b075116dba01683a17a0.
- README: c81f37a4c207d6fb62fa8c612d4307d307d104e6.
- Diagnosis note: research-automation/ATTACHMENT_DOM_SCAN_DIAGNOSIS_2026-11-07.md (commit 1333d00c9393565a582d9b2e2d12cd799b967d1f).

Open problems:
- New DOM scan instrumentation has not yet been pulled or executed on Windows.
- Need inspect whether the attachment card is inside the latest assistant container and which elements/attributes expose it.
- Need determine why the download event or fallback is not triggered.
- State marker is absent in the previous captured response because HTML comments are invisible; the next assistant response must use visible standalone markers.
- Do not run without -DryRun.

Next step:
1. Pull origin/main using git -c http.version=HTTP/1.1 pull --ff-only origin main.
2. Rerun the launcher with -Once -DryRun while the assistant response includes attachment-smoke-test-2026-11-07.md and visible RESEARCH_STATE_BEGIN/END lines.
3. Open the newest dry-run-diagnostic.md with Get-Content -Encoding UTF8.
4. Send the Attachment DOM scan section and captured response. Use its scoped/page-wide candidate counts and HTML snapshot to make the next targeted change.

Artifacts:
- research-automation/ATTACHMENT_DOM_SCAN_DIAGNOSIS_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/tests/test_sync.py
- research-automation/README.md
- research_state.md
