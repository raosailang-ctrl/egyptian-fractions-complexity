Current question:
Verify that the synchronizer can extract research state from the rendered ChatGPT assistant response after replacing invisible HTML-comment delimiters with visible text markers.

Completed:
- Read the generated dry-run diagnostic supplied by the user.
- Confirmed the captured page URL is https://chatgpt.com/c/6aeddb48-9710-83ea-98b5-3458eb53642a and the captured 765-character response is the immediately preceding assistant reply in this same conversation, about the successful GitHub HTTP/1.1 fast-forward.
- Concluded the evidence does not indicate wrong conversation/tab selection. Zero attachments are expected because the captured reply was explanatory text, not an artifact-producing response.
- Identified the actual state-extraction defect: Playwright inner_text() returns rendered text and omits HTML comments, so the prior <!-- RESEARCH_STATE_BEGIN/END --> delimiters are invisible to the synchronizer.
- Updated extract_state_block() to accept visible standalone RESEARCH_STATE_BEGIN/END lines while retaining legacy HTML-comment parsing.
- Updated build_continue_prompt() and build_handoff_prompt() to convert legacy comment delimiters in existing local config.toml templates into visible markers at send time.
- Updated config.example.toml and README to use visible marker lines; updated handoff instructions.
- Added regression tests for visible-marker extraction and legacy-template conversion.
- Added a diagnostic interpretation note and PowerShell UTF-8 reading instructions.

Evidence:
- User diagnostic: page URL above; response length 765; state_block=no; attachments=0.
- Captured response text is the preceding assistant reply in this conversation; no downloadable attachment was expected.
- Parser commit: 15a7b48c4e21842b40543ac7ccc06b5cd328e340.
- Test commit: 76bf68fd532d010ff3dfcf127589d97ae3f1bb7f; corrected newline fixtures: 45901e50d734f753b3fdb91ceeb9c976374577f5.
- Example config commit: 931c59f3190fe2d7c2239b6ee399f7cc973f6115; visible handoff markers: 5f4066d587b2d28c36f5d43c80d5fb0fe2a4d8ac.
- README protocol commit: b5f711e150b432aa857b48077a12ade7228290d9.
- Diagnostic interpretation note: research-automation/DRY_RUN_DIAGNOSTIC_AND_VISIBLE_MARKER_FIX_2026-11-07.md (commit 2b17fd622f36228c650763c3cfd75eb69cf54d85).
- PowerShell mojibake is a text-decoding/display issue; diagnostic is written as UTF-8. Use Get-Content -Encoding UTF8.

Open problems:
- Latest parser/test changes have not yet been pulled to the user's Windows checkout or executed there.
- Need verify the next dry-run reports state_block=yes. attachments=0 is acceptable for a text-only response.
- Need separately test attachment downloading with a response that actually includes an artifact.
- The full unit test suite has not been run in the user's Windows environment; no claim of test-suite success is made.
- Do not run without -DryRun until state extraction is verified.

Next step:
1. Run git -c http.version=HTTP/1.1 pull --ff-only origin main.
2. Run the launcher with -Once -DryRun.
3. Check for "state_block=yes" and inspect the new diagnostic using Get-Content -Encoding UTF8 -LiteralPath $diag -Raw.
4. If state extraction succeeds, perform a separate attachment test only when a response genuinely contains an attached file. Keep -DryRun enabled.

Artifacts:
- research-automation/DRY_RUN_DIAGNOSTIC_AND_VISIBLE_MARKER_FIX_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/tests/test_sync.py
- research-automation/config.example.toml
- research-automation/README.md
- research_state.md
