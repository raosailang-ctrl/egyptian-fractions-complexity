Current question:
Set this in the ChatGPT research conversation before the first automated round.

Completed:
The automation repository is configured to receive research artifacts incrementally.

Evidence:
The synchronizer has unit tests for state extraction, safe archive overlay, verifier failure, and selective Git publishing.

Open problems:
The first live browser round still needs a dry run and user review.

Next step:
Run the dedicated Chrome launcher with --once --dry-run, then review the detected response and downloads.

Artifacts:
- research-automation/chatgpt_research_sync.py
- research-automation/config.example.toml
