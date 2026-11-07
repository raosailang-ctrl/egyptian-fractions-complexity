# Dry-run diagnostic interpretation and visible state-marker fix

**Date:** 2026-11-07  
**Conversation:** `https://chatgpt.com/c/6aeddb48-9710-83ea-98b5-3458eb53642a`

## 1. Interpretation of the user's diagnostic

The user ran:

```powershell
Get-Content -LiteralPath $diag -Raw
```

The diagnostic reports:

- Page URL: the conversation URL above.
- Assistant response characters: 765.
- State block found: no.
- Downloaded attachments: 0.

The captured assistant text is visibly the immediately preceding assistant answer in this same conversation, beginning with the Chinese equivalent of "GitHub update succeeded" and describing the successful HTTP/1.1 fast-forward. Therefore, the browser is reading a real assistant response from the expected conversation; the evidence does not point to a wrong tab or a broken latest-message selector.

No attachments are expected for that previous answer: it was an ordinary explanatory reply, not an artifact-producing response. Thus zero attachments is not evidence of an attachment selector defect.

## 2. Root cause of missing state block

The synchronizer obtains assistant text with Playwright `inner_text()`. HTML comments are not rendered text and are omitted by `inner_text()`. The previous protocol used:

```text
<!-- RESEARCH_STATE_BEGIN -->
...
<!-- RESEARCH_STATE_END -->
```

Those delimiters are present in the authored Markdown source but are invisible in the browser's rendered text extraction. Therefore `extract_state_block()` cannot find them, even when the assistant message visually/structurally contains them in its source.

This is a protocol mismatch, not a conversation-selector failure.

## 3. Fix committed

The synchronizer now accepts both:
- visible standalone lines `RESEARCH_STATE_BEGIN` and `RESEARCH_STATE_END`;
- legacy HTML-comment delimiters, for compatibility with non-browser text sources.

Both continuation and handoff prompt builders convert legacy HTML-comment markers in an existing local `config.toml` template into visible text markers before sending the prompt. This avoids requiring the user to recreate their local ignored configuration file.

The example TOML and README now use visible markers. The regression suite adds:
- extraction from visible marker lines;
- preservation of legacy comment-marker extraction;
- conversion of legacy markers in continuation and handoff prompts.

## 4. PowerShell encoding note

The Chinese text in the diagnostic appears as mojibake because Windows PowerShell's default text decoding/output code page is not matching the UTF-8 diagnostic file. This is a display/encoding issue, not evidence that the browser captured corrupted text.

Use:

```powershell
Get-Content -Encoding UTF8 -LiteralPath $diag -Raw
```

The diagnostic writer saves UTF-8 explicitly.

## 5. Next verification

After pulling the latest `main`, run:

```powershell
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun
```

The current assistant response should now contain visible state delimiters, so the expected diagnostic should show `state_block=yes`. It may still show `attachments=0`, which is acceptable because this response does not contain a downloadable artifact.

The dry-run must remain enabled. A successful state-block extraction is the next acceptance criterion; actual artifact downloading should be tested separately with an assistant response that really includes an attachment.

## 6. Execution boundary

The user-provided diagnostic was reviewed. The code changes were committed to GitHub, but the new parser and tests have not yet been executed on the user's Windows machine in this round. No real synchronization or automatic Git commit/push was run by the local dry-run.
