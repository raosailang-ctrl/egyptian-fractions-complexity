Current question:
Inspect the latest attachment smoke-test diagnostic and determine why the run captured zero attachments and no state marker.

Completed:
- User ran the updated launcher with -Once -DryRun.
- The run connected to ChatGPT and generated a new diagnostic without throwing.
- The console reported attachments=0 and state_block=no.
- Recorded the result and the required diagnostic review steps in the repository.
- No attachment selector changes were made because the captured assistant response has not yet been inspected.

Evidence:
- User console diagnostic path: C:\egypt fractions\chatgpt-automation-staging\20261107-211358\dry-run-diagnostic.md.
- Console summary: state_block=no, attachments=0.
- Unchanged HEAD: b7ec24607e50e4de0a7047138a297f33f3eeff25.
- Note: research-automation/ATTACHMENT_SMOKE_TEST_INCONCLUSIVE_2026-11-07.md.
- Note commit: a4beb6932ee39299369e8e40862c3bbd7634a864.
- Previous run successfully verified state_block=yes, so this regression needs diagnosis rather than assumption.

Open problems:
- The actual captured response in the new diagnostic has not been reviewed.
- It is unknown whether the wrong assistant message was selected or whether the attachment card/link was not detected.
- Attachment download remains unverified.
- Do not run without -DryRun.

Next step:
Run:
$diag = "C:\egypt fractions\chatgpt-automation-staging\20261107-211358\dry-run-diagnostic.md"
Get-Content -Encoding UTF8 -LiteralPath $diag -Raw
Send the output for review, especially Page URL and the full captured assistant response. Only then adjust selectors or conversation targeting.

Artifacts:
- research-automation/ATTACHMENT_SMOKE_TEST_INCONCLUSIVE_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/tests/test_sync.py
- research_state.md
