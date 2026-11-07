# Attachment-bearing message selection: diagnostic finding and targeted fix

**Date:** 2026-11-07  
**Conversation:** `https://chatgpt.com/c/6aeddb48-9710-83ea-98b5-3458eb53642a`

## 1. Diagnostic finding

The user's uploaded diagnostic for run `20261107-214412` proves that the synchronizer was selecting the latest assistant message, but the attachment was attached to the preceding assistant message.

The diagnostic shows four rendered message containers:

| DOM index | Message ID | Relevant content |
|---:|---|---|
| 0 | `afc04b5c-1c80-4461-82c6-f9202e406455` | Older 2026-11-07 smoke-test card |
| 1 | `7d65d6a9-6169-42e3-b208-220099ba0c28` | Text-only reply |
| 2 | `d701ac03-ee7a-4ba4-bd19-1c7443484947` | Contains preview button for `attachment-smoke-test-2026-11-08.md` |
| 3 | `4f2aff91-1198-49c2-a285-92b9f5f85150` | Latest text-only explanation; no attachment card |

The old collector always scoped attachment detection to DOM index 3. It therefore saw 11 ordinary controls but no attachment candidate, and `Download attempts` remained empty. It never attempted to download the file in index 2.

This resolves the apparent contradiction: latest-response extraction was correct, but latest-response attachment selection was too narrow.

## 2. Targeted code change

The synchronizer now separates two concepts:

- **Latest assistant response:** still used by `wait_for_response()` and `extract_state_block()`.
- **Latest attachment-bearing assistant message:** found by scanning backward through the last eight `data-chatgpt-selection-message-id` containers for a preview/download/file control.

The collector selects the most recent message containing a file card and scopes attachment controls to that message. The diagnostic records both the latest message ID and the selected attachment message ID/index.

This preserves the current research-state protocol while allowing a file attached to the immediately preceding assistant response to be collected.

## 3. Preview hover and download control

The 2026-11-08 message's button list shows a preview button but no visible download button before hover. The collector therefore no longer treats clicking the preview button as a download.

For preview-only cards, the new sequence is:
1. Hover the preview control.
2. Wait briefly for the card toolbar.
3. Search within the same attachment-bearing message for a visible, enabled `下载文件` / `Download` control.
4. If found, click that control under `expect_download`.
5. If not found, record `preview-hover-no-download-control` and do not click the preview.

This avoids opening a preview and incorrectly treating it as a successful download.

## 4. Tests and documentation

Added a regression test where the last assistant message is text-only but the immediately preceding message contains an attachment card. The test verifies that the collector's selection helper chooses the preceding attachment-bearing message.

Added a negative test for messages without attachment controls. README now explains the distinction between latest response and latest attachment-bearing message.

## 5. Current status and limitations

**Code changes are committed, but have not yet been executed on the user's Windows Chrome session.** No claim of a successful download is made.

The last-eight-message search can encounter an already processed older attachment if a later response has no new file. A persistent processed-message/file-ID deduplication mechanism should be added before enabling continuous real synchronization.

## 6. Next verification

On Windows:
1. Pull `origin/main` with HTTP/1.1.
2. Rerun `start_chatgpt_research.ps1 -Once -DryRun`.
3. Inspect the diagnostic:
   - latest message ID should be `4f2aff91-1198-49c2-a285-92b9f5f85150` or a newer ID;
   - selected attachment message ID should be `d701ac03-ee7a-4ba4-bd19-1c7443484947` if the same DOM is still loaded;
   - attachment message DOM index should be 2;
   - Download attempts should report whether hovering revealed the download control;
   - success requires a non-empty downloaded file with non-zero size.

Keep `-DryRun` enabled. Do not run a real sync until the attachment download and duplicate protection are both verified.
