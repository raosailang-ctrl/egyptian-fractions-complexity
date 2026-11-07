# ChatGPT 网页研究自动同步 GitHub 设计

日期：2026-11-07

## 目标

为 Windows 上的 ChatGPT 网页研究流程提供一个本地自动化工具：

1. 使用独立 Chrome 配置文件保存 ChatGPT 登录状态；
2. 等待每轮研究回答完成；
3. 下载回答中的研究文件或 ZIP，并以增量方式覆盖到 Git 仓库；
4. 保存一份机器可读的研究状态摘要 `research_state.md`；
5. 运行本轮文件中的验证脚本；
6. 提交并推送到 `main`；
7. 推送成功后发送“继续研究”提示；
8. 检测上下文长度错误后，创建新对话并带入研究状态继续。

本版本同步文件和研究状态摘要，不保存完整聊天记录。

## 使用范围

目标仓库：`raosailang-ctrl/egyptian-fractions-complexity`

本地自动化目录：`research-automation/`

浏览器配置目录、下载临时目录和日志目录均放在仓库之外，避免登录 Cookie、临时附件或运行日志进入 Git。

## 组件

### 启动脚本

`research-automation/start_chatgpt_research.ps1`

- 创建独立 Chrome 配置目录和下载目录；
- 启动 Chrome，并设置 `--user-data-dir`、`--remote-debugging-port` 和下载目录；
- 打开配置中的研究对话 URL；
- 启动 Python 同步器；
- 第一次运行时让用户在独立窗口中完成登录，后续复用该会话。

### 同步器

`research-automation/chatgpt_research_sync.py`

- 通过 Playwright CDP 连接独立 Chrome；
- 定位 ChatGPT 编写框并发送提示；
- 等待回答稳定并检测生成完成；
- 查找回答中的下载链接，保存新附件；
- 解压 ZIP/TAR 文件时跳过 `.git`、`__pycache__`、临时文件和路径越界条目；
- 将包内相对路径映射到仓库根目录；
- 从回答末尾提取状态标记，写入 `research_state.md`；
- 运行配置中允许的验证命令；
- 检查仓库是否存在用户未处理的既有改动；
- 提交、推送并记录 commit SHA；
- 推送失败、验证失败、登录失效、验证码或合并冲突时停止循环。

### 配置

`research-automation/config.example.toml`

配置包括：

- 仓库路径、远程名和目标分支；
- ChatGPT 对话 URL；
- Chrome 可执行文件路径和 CDP 端口；
- 外部配置目录、下载目录和日志目录；
- 允许同步的扩展名；
- 验证命令白名单；
- 单轮或连续运行模式；
- 继续研究提示和新对话继承提示。

实际配置使用 `config.toml`，并加入 `.gitignore`。

## 研究状态协议

每轮回答末尾要求模型输出以下标记。同步器只保存标记中的内容，不保存完整回答：

```text
<!-- RESEARCH_STATE_BEGIN -->
Current question:
Completed:
Evidence:
Open problems:
Next step:
Artifacts:
<!-- RESEARCH_STATE_END -->
```

如果回答没有标记，同步器保留上一份状态，记录警告，并仍可保存检测到的附件。

## 单轮数据流

```text
ChatGPT response
    -> wait until complete
    -> collect download links
    -> download to external staging directory
    -> safe overlay into repository
    -> extract RESEARCH_STATE block
    -> run configured verifiers
    -> git pull --ff-only
    -> git add selected files
    -> git commit
    -> git push origin main
    -> send continuation prompt
```

同步器只会暂存本轮下载的文件和 `research_state.md`，不会使用 `git add .` 接管用户在脚本启动前留下的其他改动。

## 上下文耗尽处理

同步器检查页面中的错误提示和停止状态，识别以下语义：上下文过长、达到最大上下文、对话过长、无法继续生成。

检测到后：

1. 停止向旧对话发送消息；
2. 打开新的 ChatGPT 对话；
3. 发送仓库地址、最近 commit SHA 和 `research_state.md` 内容；
4. 要求新对话从 `Next step` 继续，不重复已完成工作；
5. 将新对话 URL 写入日志，继续正常轮次。

新对话继承研究状态文件，不依赖旧对话的完整聊天记录。

## 错误处理

- **Chrome 未安装或 CDP 端口不可用**：退出并给出启动命令；
- **登录过期/验证码**：暂停，等待用户处理，不自动绕过；
- **未找到下载附件**：记录警告，保留状态摘要并停止推送；
- **ZIP 路径越界或包含 `.git`**：拒绝该条目并记录；
- **验证命令失败**：不提交、不发送继续提示；
- **仓库启动前已有未提交改动**：拒绝自动化，避免覆盖用户工作；
- **远程有新提交导致推送失败**：停止并要求用户先处理分支同步；
- **页面选择器变化**：保存截图和日志，退出并提示更新选择器。

## 安全边界

- 独立 Chrome 配置目录可能包含登录 Cookie，只保存在本机；
- 配置文件、Cookie、下载暂存和日志不进入 Git；
- 只允许向配置的仓库和分支推送；
- 初次运行提供 `--once` 和 `--dry-run`；
- 默认不自动绕过 CAPTCHA、MFA 或任何登录验证；
- 默认拒绝已有工作区改动，避免覆盖用户手动编辑。

## 验证策略

1. 离线测试路径安全、ZIP 展开、状态标记解析和 Git 文件筛选；
2. 使用 `--dry-run` 验证浏览器连接和附件识别；
3. 使用 `--once` 完成一次真实下载、验证、提交流程；
4. 用户确认日志和提交结果后，再启用连续轮次；
5. 模拟上下文耗尽提示，确认新对话能收到状态文件并继续。

## 明确限制

该工具依赖 ChatGPT 网页 DOM、下载链接形式和页面提示文本。网页改版可能需要调整选择器或错误提示匹配。它同步的是最终文件和状态摘要，不会保存完整对话，也不能替代 ChatGPT 或 Codex 的官方 API。
