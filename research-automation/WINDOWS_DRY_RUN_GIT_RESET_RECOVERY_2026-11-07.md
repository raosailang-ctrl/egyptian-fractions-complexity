# Windows dry-run follow-up: Git pull reset and stale local synchronizer

**Date:** 2026-11-07  
**Observed by user:** `git pull --ff-only origin main` failed with `Recv failure: Connection was reset`; the following dry-run still raised the old `SyncError` after collecting zero attachments.

## Diagnosis

The second screenshot is consistent with the local checkout not receiving the latest synchronizer changes. The Git pull failed before updating the working tree. The user then ran the launcher anyway, so Python executed the old local `research-automation/chatgpt_research_sync.py`.

This is confirmed by the old traceback ending at:

```python
raise SyncError("The response contained no downloadable artifacts or research state.")
```

The current GitHub version does not raise at that point. It calls `write_dry_run_diagnostic()`, saves `dry-run-diagnostic.md`, and prints a warning if both attachments and the state block are absent.

Current source blob SHA on GitHub:
`4a70ee401ebebfb0961b4467e3faf693517c7a85`

## Recovery route A: retry Git using HTTP/1.1

From the repository root:

```powershell
git -c http.version=HTTP/1.1 pull --ff-only origin main
```

If this succeeds, verify that the source contains the diagnostic writer:

```powershell
Select-String -Path .\research-automation\chatgpt_research_sync.py -Pattern "write_dry_run_diagnostic|Dry-run diagnostic saved"
```

Expected: both patterns are found.

## Recovery route B: update only the synchronizer from the public raw file

Use this if Git pull continues to reset. It avoids transferring the whole Git history and verifies the exact Git blob before replacing the local file.

```powershell
$target = ".\research-automation\chatgpt_research_sync.py"
$temp = "$target.download"
$url = "https://raw.githubusercontent.com/raosailang-ctrl/egyptian-fractions-complexity/main/research-automation/chatgpt_research_sync.py"
$expected = "4a70ee401ebebfb0961b4467e3faf693517c7a85"

curl.exe -fL --retry 3 --retry-delay 2 --connect-timeout 20 -o $temp $url
if ($LASTEXITCODE -ne 0) {
    Remove-Item -LiteralPath $temp -ErrorAction SilentlyContinue
    throw "Download failed. Do not run the dry-run again yet."
}

$actual = (git hash-object $temp).Trim()
if ($actual -ne $expected) {
    Remove-Item -LiteralPath $temp -ErrorAction SilentlyContinue
    throw "Downloaded file SHA mismatch. Expected $expected but got $actual"
}

Copy-Item -LiteralPath $target -Destination "$target.before-diagnostic-fix.bak" -Force
Move-Item -LiteralPath $temp -Destination $target -Force
Write-Host "Synchronizer updated and Git blob SHA verified: $actual"
```

If `curl.exe` also fails, open the raw URL in a browser and save the response as `research-automation/chatgpt_research_sync.py`; then run `git hash-object .\research-automation\chatgpt_research_sync.py` and compare with the expected SHA above before continuing.

## Verify and rerun

```powershell
Select-String -Path .\research-automation\chatgpt_research_sync.py -Pattern "write_dry_run_diagnostic|Dry-run diagnostic saved"
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun
```

Expected new output includes a line similar to:

```text
Dry-run diagnostic saved: C:\egypt fractions\chatgpt-automation-staging\<round>\dry-run-diagnostic.md (state_block=no, attachments=0)
WARNING: the captured latest assistant message contained neither a research-state block nor downloadable attachments.
```

The exact values depend on the captured page. The diagnostic is the next evidence needed: inspect its Page URL, state-marker flag, attachment list, and captured response. Do not run without `-DryRun` until that evidence has been reviewed.

## Safety and scope

- The screenshot does not prove the current attachment selector is wrong; it proves the local code was stale because the update failed.
- Do not change selectors until the captured response is available.
- The raw-file fallback changes only the local synchronizer file. It does not update the local Git branch metadata; later, after network connectivity returns, use `git pull --ff-only origin main` to reconcile the repository.
- No real synchronization, repository overlay, automated commit/push, or continuation prompt has been run.
