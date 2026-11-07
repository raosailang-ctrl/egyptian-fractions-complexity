# 首次 Chrome dry-run 前置审计与执行记录

**日期：** 2026-11-07  
**仓库：** `raosailang-ctrl/egyptian-fractions-complexity`  
**审计基线：** `ca5ffdad7b1ad149cde06de77c2c963b563bdd7a`（`Sync ChatGPT research round 2026-11-07 19:45:54`）  
**状态：** 已完成仓库静态审计；尚未执行用户 Windows 桌面上的真实 Chrome dry-run。原因是本次执行环境无法读取被 .gitignore 排除的本机 `research-automation/config.toml`、Windows Chrome 登录配置文件和用户桌面 CDP 会话。

## 1. 已读取的状态

仓库根目录 `research_state.md` 当前内容：

- Current question: 在第一次自动化轮次前，完成 ChatGPT 研究同步器的浏览器 dry-run。
- Completed: 同步器已配置为增量接收研究成果。
- Evidence: 已有测试覆盖 state 提取、安全 ZIP 覆盖、verifier 失败和选择性 Git 发布。
- Open problems: 第一次真实浏览器轮次仍需 dry-run 和用户审核。
- Next step: 使用专用 Chrome 启动器运行 `--once --dry-run`，检查识别到的回复和下载附件。

最近一次提交 `ca5ffdad7b1ad149cde06de77c2c963b563bdd7a` 新增了20素数有限域筛选程序 `verify_20_prime_sieve.py`。该提交是数学研究产物同步，不是一次真实浏览器 dry-run 的执行记录。

## 2. 已审计文件与行为

### 2.1 启动器

文件：`research-automation/start_chatgpt_research.ps1`

执行流程：

1. 若 `research-automation/config.toml` 不存在，复制示例配置并停止；第一次运行不会自动继续。
2. 创建专用 Chrome profile 和下载目录。
3. 检查本机 Chrome 标准安装路径。
4. 若 CDP 端口未监听，则启动独立 Chrome 并开放调试端口。
5. 调用 Python 同步器，并传入 `--once`、`--dry-run`。

### 2.2 同步器 dry-run

文件：`research-automation/chatgpt_research_sync.py`

当前 dry-run 分支的行为：

- 连接 CDP 并等待页面登录状态；
- 读取最新 assistant message；
- 仅在最新回复内寻找附件控件；
- 将附件下载到 staging 目录；
- 提取回复中的 `RESEARCH_STATE_BEGIN/END` 标记；
- 不将附件覆盖到仓库文件；
- 不写入 `research_state.md`；
- 不执行实际 verifier 命令（只返回 dry-run 占位结果）；
- 不创建 Git commit，不 push；
- 不发送 continuation prompt。

因此 dry-run 的设计方向正确：它应只读取和暂存，不应改变仓库内容或向 ChatGPT 发送下一轮提示。

### 2.3 已有测试

文件：`research-automation/tests/test_sync.py`

已存在的测试覆盖：

- 状态标记提取；
- ZIP 安全解包和路径穿越拒绝；
- dirty worktree 检查；
- verifier 失败处理；
- Git commit/push；
- context-limit 检测；
- 最新 assistant message 选择；
- dry-run 不修改仓库文件；
- 附件卡片下载；
- CDP 下载事件不可用时的下载目录 fallback。

本次完成了测试源码审阅，但没有在用户 Windows 环境执行完整测试套件，也没有把模拟浏览器测试冒充成真实 ChatGPT 浏览器验收。

## 3. 风险与执行前检查

### 风险 A：本机配置必须存在且指向当前研究对话

`research-automation/config.toml` 是本地配置，不会提交到 GitHub。请确认：

- `repo_path` 指向实际克隆仓库的根目录；
- `chat_url` 是当前研究对话的完整 URL，而不是示例中的 `https://chatgpt.com/` 首页；
- `chrome_path`、CDP 端口和各目录路径符合本机实际情况。

### 风险 B：CDP 端口可能被其他 Chrome 占用

当前启动器发现端口已监听时，会复用端口，但不会验证监听进程是否使用指定 profile。执行前应确认9222端口没有被其他 Chrome/调试进程占用；若已占用，先确认进程命令行及 `--user-data-dir`，不要直接复用不明会话。

### 风险 C：dry-run 的 staging/log 路径

示例配置把 profile、download、staging 和 logs 放在仓库之外。请保留这一做法。若把相对路径解析到仓库内部，dry-run 可能产生未跟踪的暂存文件或日志，虽然不会 commit/push，但会污染工作区。

### 风险 D：当前控制台摘要不够充分

当前实现主要打印附件数量，并不会把完整 assistant 回复和每个附件的文件名、大小、哈希完整展示在终端。审核时应同时检查：

- ChatGPT 浏览器中当前研究对话的最新回复；
- 配置中的 staging 目录；
- 配置中的 logs 目录下的 `research-sync.jsonl`。

不要只凭“下载 N 个附件”就认定文件内容正确。

## 4. 用户 Windows 机器上的执行步骤

在 PowerShell 中，从实际仓库根目录执行：

```powershell
python -m pip install -r research-automation/requirements.txt

if (-not (Test-Path research-automation/config.toml)) {
    Copy-Item research-automation/config.example.toml research-automation/config.toml
    Write-Host "请先编辑 research-automation/config.toml，再运行 dry-run。"
    return
}

notepad research-automation/config.toml
```

确认 `chat_url` 是当前研究对话完整 URL、`repo_path` 正确、所有临时目录位于仓库之外后，运行：

```powershell
powershell -ExecutionPolicy Bypass -File research-automation/start_chatgpt_research.ps1 -Once -DryRun
```

预期控制台关键输出：

- `已连接 ChatGPT，等待最新回复…`
- `正在收集最新回复的附件…`
- `附件收集完成：N 个`
- `第 1 轮完成…`

完成后检查 staging 目录内的文件，并在浏览器中确认最新回复。dry-run 不应产生 Git commit/push，也不应在 ChatGPT 中发送 continuation prompt。

## 5. 本轮执行结论

**已完成：** 读取仓库状态和最近提交；审阅启动器、同步器、配置示例、README 和测试；确认 dry-run 的代码级安全边界；识别首次运行的配置、CDP 和审核可见性风险。

**未完成：** 真实 Windows 专用 Chrome dry-run。当前执行环境没有用户的本机 `config.toml`、登录 profile 或本地 CDP 会话；不能伪称已完成真实浏览器验收。

**下一步：** 用户在 Windows 上运行上述命令，并提供控制台输出、staging 文件名列表及 `research-sync.jsonl` 最后一条记录。收到这些证据后，再判断最新回复识别、附件下载和 dry-run 隔离是否通过；通过后才允许执行一次非 dry-run 同步。

## 6. 安全边界

- 不读取、不上传、不提交 `research-automation/config.toml`。
- 不复制或提交 Chrome profile、cookie、登录态或 CDP 凭据。
- 不在真实 dry-run 审核前执行非 dry-run 同步。
- 不将 dry-run 的模拟测试、静态代码审阅或有限域数学验证称为真实浏览器执行成功。
