Current question:
Verify the new backward search for the latest attachment-bearing assistant message and the hover-revealed download action.

Completed:
- Reviewed the user's uploaded diagnostic for run 20261107-214412.
- Confirmed four message containers in DOM order.
- Identified the actual attachment-bearing message at DOM index 2 (ID d701ac03-ee7a-4ba4-bd19-1c7443484947), containing the preview button for attachment-smoke-test-2026-11-08.md.
- Confirmed the synchronizer had selected DOM index 3 (ID 4f2aff91-1198-49c2-a285-92b9f5f85150), a newer text-only assistant reply. Its scoped candidate count was 11 and Download attempts was empty.
- Concluded the failure was not the click event yet: the attachment card was in the preceding assistant message and was never attempted.
- Added _message_has_attachment_control() and _latest_attachment_locator() to search backward through the last eight message containers.
- Separated latest response/state extraction from attachment-bearing message selection.
- Added diagnostic fields for latest message ID and attachment message DOM index.
- Changed preview-only handling to hover the card, locate a visible enabled download control inside the selected message, and click that control; it does not click the preview as a substitute for downloading.
- Added positive and negative selection regression tests.
- Updated README and documented the finding.

Evidence:
- User diagnostic: C:\egypt fractions\chatgpt-automation-staging\20261107-214412\dry-run-diagnostic.md.
- Message index 2: d701ac03-ee7a-4ba4-bd19-1c7443484947; preview button for attachment-smoke-test-2026-11-08.md.
- Message index 3: 4f2aff91-1198-49c2-a285-92b9f5f85150; text-only latest assistant reply.
- Previous selected message ID: 4f2aff91-1198-49c2-a285-92b9f5f85150.
- Source selection commit: 823508ac4e713ac8024a3944ac76bd459a014a79.
- Hover-download commit: 0cfc11f57cb21f63af950111a585bef76127b42e.
- Regression test commit: 5eff2d81dfda5319fd042da533958d47dafa77cc.
- README commit: 24c708e539e4aa2690dd50c25ac3d44f766ae1a3.
- Comment correction: 0eb30cf0faba0baf03b14aee8b61e921e0e93860.
- Research note: research-automation/ATTACHMENT_BEARING_MESSAGE_SELECTION_FIX_2026-11-07.md (commit 522e29159f3d21f0bc73b4167bddfbe13cec9b24).

Open problems:
- The new selection and hover-download logic have not yet been run on Windows.
- Need confirm the attachment message is selected (index 2 / ID d701...) and the latest response remains the state source.
- Need see whether hover reveals the download button and whether Playwright receives a download event.
- Persistent deduplication of already processed attachment message IDs/files is not implemented; required before continuous real sync.
- No successful attachment download or real synchronization has occurred.

Next step:
1. Pull origin/main with git -c http.version=HTTP/1.1 pull --ff-only origin main.
2. Rerun the launcher with -Once -DryRun.
3. Inspect latest message ID, selected attachment message ID/index, and Download attempts.
4. Verify a non-zero file appears in staging. Keep DryRun enabled.

Artifacts:
- research-automation/ATTACHMENT_BEARING_MESSAGE_SELECTION_FIX_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/tests/test_sync.py
- research-automation/README.md
- research_state.md
