# Attachment DOM scan result: candidate is found; download action is the failing stage

**Date:** 2026-11-07

## 1. New evidence from the user's diagnostic

The uploaded diagnostic for round `20261107-212436` shows:

- Page URL: `https://chatgpt.com/c/6aeddb48-9710-83ea-98b5-3458eb53642a`
- Assistant response length: 2,782 characters.
- State block found: yes.
- Downloaded attachments: 0.
- Latest assistant locator found: True.
- Scoped candidate count: 18.
- Page-wide candidate count: 171.

Most importantly, inside the latest assistant message the collector already sees:

- `button | aria-label=打开 attachment-smoke-test-2026-11-07.md 的预览`
- `button | aria-label=下载文件`

Therefore:
- The correct conversation is selected.
- The latest assistant message container is found.
- The attachment card's preview and download buttons are inside that container.
- The current CSS candidate selector already matches the download button.
- The failure is not caused by the attachment being outside the message or by a missing CSS selector.

The collector classifies the Chinese label `下载文件` as a direct-download control and attempts to click it. However, the old diagnostic did not record whether the button was visible/enabled, its bounding box/HTML, whether Playwright fired a download event, or why the fallback scan found no file.

## 2. Targeted instrumentation added

The collector now records each actual download attempt:
- Candidate metadata and HTML.
- Visibility and enabled state.
- Bounding box.
- Whether the Playwright download event succeeded.
- Exception class/message if the event did not fire.
- Whether the filesystem fallback found a file.
- Final download method and saved path.

The diagnostic report now includes a `### Download attempts` section. The change does not broaden selectors, click page-wide candidates, or download unrelated controls.

The test suite now checks that these attempt details appear in the diagnostic. README describes the diagnostic section.

## 3. Next test artifact

A new harmless attachment is included in the next assistant response:

`attachment-smoke-test-2026-11-08.md`

It contains visible state markers and is 768 bytes. The next Windows dry-run should produce `state_block=yes` and a `Download attempts` section. Whether a file downloads remains to be measured.

## 4. Next action

On Windows:

```powershell
git -c http.version=HTTP/1.1 pull --ff-only origin main
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun
```

Then inspect the newest diagnostic with:

```powershell
Get-Content -Encoding UTF8 -LiteralPath $diag -Raw
```

Send the `### Download attempts` section, especially:
- visible/enabled;
- bounding box;
- control HTML;
- method;
- error;
- fallback file.

## 5. Safety

Keep `-DryRun`. The collector remains scoped to the latest assistant message. The instrumentation only observes and logs candidate details. No real synchronization, repository overlay, automated commit/push, or continuation prompt has occurred.
