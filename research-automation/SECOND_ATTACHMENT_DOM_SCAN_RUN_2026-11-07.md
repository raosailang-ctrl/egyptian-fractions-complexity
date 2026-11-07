# Second attachment DOM diagnostic run: instrumentation active, download still zero

**Date:** 2026-11-07

## Live result supplied by user

The user successfully pulled origin/main from `b7ec246` to `59f1fc0` using HTTP/1.1. Seven files were updated, including the attachment DOM scan instrumentation.

The user then ran:
`powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun`

Observed:
- ChatGPT connected.
- Attachment collection: 0.
- Diagnostic saved to `C:\\egypt fractions\\chatgpt-automation-staging\\20261107-212436\\dry-run-diagnostic.md`.
- `state_block=yes, attachments=0`.
- Round completed with unchanged HEAD `59f1fc0612a3569ad164ab91077dcdaf17f1f7a1`.

## Interpretation

The visible state-marker parser is working again. The new DOM instrumentation is now in the local run, but the console summary alone cannot reveal why the attachment was not downloaded. The DOM scan section in the diagnostic is the required evidence.

Do not change selectors based only on the zero-download count. Inspect:
- latest assistant locator found;
- scoped candidate count;
- page-wide candidate count;
- scoped/page-wide candidate metadata;
- latest assistant container HTML;
- captured response.

Possible outcomes:
- page-wide candidates > scoped candidates: attachment is outside the selected message container;
- candidate count > 0 but no download: inspect candidate metadata and Playwright download/fallback handling;
- no candidate but filename/card visible in HTML: selector needs to match the actual card element;
- no card in HTML: attachment may not be rendered in the selected response/DOM.

## Next action

Read the diagnostic using UTF-8:

```powershell
$diag = "C:\\egypt fractions\\chatgpt-automation-staging\\20261107-212436\\dry-run-diagnostic.md"
Get-Content -Encoding UTF8 -LiteralPath $diag -Raw
```

Send the complete `## Attachment DOM scan` section and, if practical, the truncated HTML snapshot. Keep `-DryRun` enabled.

## Safety

No real synchronization, repository overlay, synchronizer-driven commit/push, or continuation prompt was executed.
