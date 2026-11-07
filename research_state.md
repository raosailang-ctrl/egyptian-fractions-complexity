Current question:
Diagnose why the detected ChatGPT attachment download button does not produce a saved file.

Completed:
- Reviewed the user's latest diagnostic from round 20261107-212436.
- Confirmed correct conversation URL and latest assistant message locator.
- Confirmed the latest assistant container includes both a preview button for attachment-smoke-test-2026-11-07.md and a button with aria-label "下载文件".
- Scoped selector already finds both buttons: 18 scoped candidates, 171 page-wide candidates.
- Concluded the CSS selector and message scope are not the cause; the failure is later in the click/download-event/filesystem-fallback path.
- Added per-attempt instrumentation: visibility, enabled state, bounding box, button HTML, Playwright download exception, fallback result and final method.
- Added regression coverage and a README note.
- Created a new 768-byte attachment smoke-test file with visible state markers for the next run.
- Added a research report documenting the DOM evidence and next test.

Evidence:
- User diagnostic: C:\egypt fractions\chatgpt-automation-staging\20261107-212436\dry-run-diagnostic.md.
- Correct conversation URL: https://chatgpt.com/c/6aeddb48-9710-83ea-98b5-3458eb53642a.
- Scoped candidates: 18; page-wide candidates: 171.
- Candidate metadata explicitly shows preview button and aria-label=下载文件.
- Instrumentation source commit: f4713c0657e372c7b8d61bb5b31c4bf72c2bd141.
- Regression test commit: 3ce7b5d07306a1b35cafcd8d01d03df418d80c4b.
- README commit: c81f37a4c207d6fb62fa8c612d4307d307d104e6.
- Research note: research-automation/ATTACHMENT_DOWNLOAD_ACTION_DIAGNOSTICS_2026-11-07.md (commit 6c50b9c5499f7b205c2543024bfb3a40246303dd).
- New test artifact: attachment-smoke-test-2026-11-08.md (768 bytes).

Open problems:
- New download-attempt diagnostics have not yet run on Windows.
- Need know whether the download button is visible/enabled and whether Playwright's download event fires.
- Need inspect button outerHTML and fallback result.
- Actual attachment download remains unverified.
- Real synchronization has not been performed.

Next step:
1. Pull origin/main with git -c http.version=HTTP/1.1 pull --ff-only origin main.
2. Rerun the launcher with -Once -DryRun while attachment-smoke-test-2026-11-08.md is attached to the latest assistant response.
3. Read the newest diagnostic as UTF-8.
4. Send the Download attempts section. Keep -DryRun enabled.

Artifacts:
- research-automation/ATTACHMENT_DOWNLOAD_ACTION_DIAGNOSTICS_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/tests/test_sync.py
- research-automation/README.md
- attachment-smoke-test-2026-11-08.md
- research_state.md
