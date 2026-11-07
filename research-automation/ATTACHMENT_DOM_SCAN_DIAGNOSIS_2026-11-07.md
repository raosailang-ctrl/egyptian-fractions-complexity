# Attachment smoke-test diagnosis and DOM instrumentation

**Date:** 2026-11-07

## 1. What the user's diagnostic proves

The diagnostic for round `20261107-211358` reports:
- Correct research conversation URL: `https://chatgpt.com/c/6aeddb48-9710-83ea-98b5-3458eb53642a`.
- Captured response length: 884 characters.
- The captured response is the preceding assistant answer that explicitly mentions the attachment smoke-test file.
- Its final visible text includes the attachment name `attachment-smoke-test-2026-11-07.md` followed by the document label.
- Downloaded attachments: 0.

This is evidence that the correct conversation and intended assistant response were captured. The attachment card appears in the rendered response text, but the collector did not identify a clickable candidate. Therefore the likely fault is in the attachment DOM candidate selector or its scope, not in chat_url or latest-message selection.

## 2. Why state_block=no is expected for this particular reply

The captured assistant answer used the legacy HTML-comment form of the state block. Browser `inner_text()` omits HTML comments, so the parser cannot see them. This is not a regression in the new visible-marker parser: this particular reply did not contain visible standalone `RESEARCH_STATE_BEGIN/END` lines.

Future research responses and smoke-test prompts must use visible standalone marker lines, not HTML comments.

## 3. New diagnostic instrumentation

The synchronizer now records, without clicking additional controls:
- whether a latest-assistant locator was found;
- number of candidate controls scoped to that message;
- number of candidate controls across the page;
- up to 30 candidate tags, labels and relevant attributes in each scope;
- a truncated 6,000-character HTML snapshot of the latest assistant container.

The report keeps the full captured response as before. This will distinguish:
- card outside the latest-message container (page-wide count > scoped count);
- card inside the message but not matching the candidate selector (visible in HTML snapshot, absent from candidates);
- candidate detected but not downloaded (metadata shows a candidate, download event/fallback failed).

The scan is diagnostic only. It does not click page-wide candidates or widen download scope, avoiding accidental downloads of unrelated page controls.

## 4. Regression test and README

Added a regression test ensuring the dry-run report includes page-wide candidate counts and candidate metadata. README documents the new diagnostics. Whitespace normalization in candidate labels was corrected.

## 5. Next run

Pull the latest `main` and rerun with `-Once -DryRun` while the assistant response contains the attached file `attachment-smoke-test-2026-11-07.md`.

Expected diagnostic sections:
- `## Attachment DOM scan`
- `Latest assistant locator found`
- `Scoped candidate count`
- `Page-wide candidate count`
- candidate metadata and HTML snapshot

Do not change the selector until this report shows where the card lives. Do not run a real sync yet.

## 6. Execution boundary

The latest user diagnostic was reviewed. The new DOM instrumentation and tests are committed, but have not yet been executed on the user's Windows machine. No real synchronization, repository overlay, automatic commit/push, or continuation prompt was performed.
