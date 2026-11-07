# ChatGPT research synchronizer

This helper controls a dedicated Chrome profile, collects research artifacts from a ChatGPT conversation, updates `research_state.md`, runs configured verifiers, and publishes selected files to GitHub.

## First setup

From the repository root in PowerShell:

```powershell
python -m pip install -r research-automation/requirements.txt
Copy-Item research-automation/config.example.toml research-automation/config.toml
notepad research-automation/config.toml
```

Set `chat_url` to the full URL of the ChatGPT research conversation. Confirm `repo_path` points to this repository. Keep `config.toml` local; it is ignored by Git.

## First browser login

Run a single dry round:

```powershell
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun
```

The launcher creates `C:\egypt fractions\chatgpt-automation-profile` and opens a separate Chrome window. Complete ChatGPT login in that window. The profile stores the session locally and is reused on later runs. Do not copy this directory or commit it.

The dry run identifies the latest response and candidate downloads but does not push Git changes or send a follow-up prompt.

## One real round

After reviewing the dry-run output:

```powershell
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once
```

On success the helper downloads allowed files, safely overlays them into the repository, writes `research_state.md`, runs `verify_commands`, creates one commit, pushes `main`, and sends the continuation prompt.

## Continuous mode

Run a bounded number of rounds while testing:

```powershell
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Rounds 3
```

Omit `-Rounds` and `-Once` for continuous mode. Stop with `Ctrl+C`.

The assistant should end each response with:

```text
RESEARCH_STATE_BEGIN
Current question:
Completed:
Evidence:
Open problems:
Next step:
Artifacts:
RESEARCH_STATE_END
```

The helper stores this block only. It does not archive the full transcript.

## Recovery

- Login, CAPTCHA, selector, verification, or Git errors stop the loop.
- Clean the repository and resolve Git conflicts before restarting.
- If ChatGPT reaches its context limit, the helper opens a new conversation and sends the repository URL, last commit SHA, and `research_state.md`.
- Browser data, staging files, logs, and local configuration remain outside Git.


### Attachment diagnostics

When an attachment is not downloaded, the dry-run report includes scoped and page-wide DOM candidate counts, candidate labels/attributes, and a truncated HTML snapshot of the latest assistant message. Review this local diagnostic before changing selectors. The scan is diagnostic only; it does not click page-wide candidates or download unrelated controls.
