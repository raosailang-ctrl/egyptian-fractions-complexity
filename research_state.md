Current question:
Complete the first real dry-run of the dedicated Chrome research synchronizer, then review the latest assistant response and downloaded artifacts before enabling any real sync.

Completed:
- Read the repository research_state.md and recent commits.
- Reviewed commit e95cfcc9db216890b1b3b7703fdf65d76594e4a5: the synchronizer now prefers a normal wide ChatGPT tab over a floating-chat tab and has a composer-entry fallback.
- Reviewed commit ca5ffdad7b1ad149cde06de77c2c963b563bdd7a: added the 20-prime finite-field sieve.
- Audited start_chatgpt_research.ps1, chatgpt_research_sync.py, config.example.toml, requirements.txt, README, and tests/test_sync.py.
- Confirmed from code that dry-run stages downloads but does not overlay files into the repository, update research_state.md, run actual verifiers, commit/push, or send a continuation prompt.
- Added research-automation/DRY_RUN_PREFLIGHT_AUDIT_2026-11-07.md with the execution checklist, safety boundaries, and blockers.

Evidence:
- Latest inspected user commit: e95cfcc9db216890b1b3b7703fdf65d76594e4a5 (normal ChatGPT tab/composer fix).
- Latest audit commit: 244289ca7101a38729371758bd4f7cbf7b728fc9.
- Audit file: research-automation/DRY_RUN_PREFLIGHT_AUDIT_2026-11-07.md.
- Dry-run isolation branch in run_round() returns before copy_artifact(), write_research_state(), real verifier execution, commit_and_push(), and send_prompt().
- config.toml is gitignored and cannot be read from GitHub; it must be configured locally with the actual research conversation URL and repository path.

Open problems:
- A real Windows Chrome/CDP dry-run has NOT been executed from this environment; the user's local config.toml, authenticated Chrome profile, and local CDP session are not accessible here.
- The launcher reuses an already-listening CDP port without validating that the process belongs to the configured dedicated Chrome profile.
- Dry-run console output reports attachment count but does not provide a full response preview and per-file size/hash manifest; the staging directory and JSONL log need manual review.
- Need verify the actual response is the intended research conversation and that all attachment files are complete and correct.
- Do not claim dry-run success based on static review or mocked tests.

Next step:
On the user's Windows machine, from the repository root:
1. Ensure research-automation/config.toml exists; if not, copy config.example.toml and edit it locally.
2. Set chat_url to the exact current research conversation URL, repo_path to the local repository root, and keep profile/download/staging/log directories outside the repository.
3. Confirm port 9222 is not owned by an unrelated Chrome/CDP process.
4. Run: powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun
5. Review the latest assistant response in the dedicated Chrome window, list staged filenames and sizes, and inspect the final research-sync.jsonl event.
6. Return the console output and staging manifest for review. Only after that should a real sync be considered.

Artifacts:
- research-automation/DRY_RUN_PREFLIGHT_AUDIT_2026-11-07.md
- research-automation/chatgpt_research_sync.py
- research-automation/start_chatgpt_research.ps1
- research-automation/config.example.toml
- research-automation/tests/test_sync.py
