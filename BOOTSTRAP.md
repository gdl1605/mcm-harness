# Bootstrap：默认初始化入口

用户 clone 仓库，在 Agent 中打开仓库后说“初始化”“执行初始化”“进行 init”或“bootstrap”，Agent 默认执行本流程。无需让用户先选目录、拼命令或阅读全部阶段文档。

## Agent 执行顺序

1. 确认用户是在要求初始化当前 Harness。开发/修改初始化代码、解释 init、明确禁止执行、`git init` 等请求不触发 Bootstrap。仅 clone 或打开仓库也不自动执行命令。
2. 在仓库根目录使用 Python 3.10+ 运行：

   ```bash
   python3 scripts/bootstrap.py --json
   ```

   平台只有 `python` 或 `py -3` 时，可先核对版本后使用等价命令。Python 未安装时说明阻塞，不自动改系统环境。
3. 用户已经明确提供附件路径、标题或运行目录时，转换为重复的 `--source`、`--title`、`--run-dir` 参数；带空格的路径必须正确引用。不要改成默认目录，不扫描仓库外寻找材料。
4. 按返回状态处理，不把退出码 0 等同于“全流程环境已就绪”：

   | 状态 | Agent 下一步 |
   | --- | --- |
   | `AWAITING_SOURCES` | `raw-sources/` 已准备，但不创建空来源 run。简短提示用户放入赛题和附件或提供文件路径；收到后重新 Bootstrap。 |
   | `INITIALIZED` | `run/` 已建立、来源与内置 Skill 哈希已记录、init 自检通过。汇报目录、材料数量和依赖缺项；仅初始化请求到此停止。 |
   | `EXISTING_RUN` | 已核对现有来源、快照和基础结构，没有改写任何运行记录。说明当前阶段，不重置、不重新启动 W1。 |
   | `BLOCKED` / 非零退出码 | 报告具体缺项或冲突；保留文件。来源变更、旧快照漂移、非空无效目录均不得用删除、覆盖或修改哈希“修复”。 |

5. 有 `skipped_source_entries` 时明确报告，不把未登记材料当作已可用。默认只登记 `raw-sources/` 顶层支持的文件，忽略隐藏文件和 Office 锁文件；不递归搜索、不跟随自动发现的符号链接、不解压压缩包。登记不等于已读懂附件，W0 仍须确认来源完整性和可读性。
6. 根据工具实际可用情况核对 subagent、文件/命令权限、文件读取与检索能力。后续绘图的两个本地 Skill 检查只验证入口文件哈希，不证明完整安装；`visualize-data` 和 `gpt-5.6-sol + high` 仍须由平台核实。不得自动下载技能、安装所有建模库、修改全局配置或声称完整环境已就绪。
7. 用户明确要求“初始化并开始解题/全流程”时，初始化成功、材料确认与所需能力可用后，才按 `AGENTS.md` 第 2 节进入对应阶段。已有 run 应续接当前阶段而不是重跑。仅初始化不创建 worker，不做文献检索或模型计算；H1 与最终人工接管始终保留。

## 默认路径与重复执行

- 原始材料：仓库内 `raw-sources/`，不复制、不修改原件。
- 新 run：仓库内 `run/`。这两个目录已被 `.gitignore` 排除。
- 多题或需要重新冻结材料：显式指定新的目录，例如 `--run-dir runs/case-02`；不覆盖旧 run。
- 既有 run 已登记外部来源、且默认材料目录为空时，重复 init 会核对原登记来源，无需再输入参数。
- `init_run.py` 保留为低层工具；普通用户从 Bootstrap 进入，不直接手工编辑 manifest 或状态文件。

这是 Agent 指令路由，不是 shell hook 或平台的 `/init` 命令。Agent 必须加载本仓库 `AGENTS.md`；不自动加载的客户端，明确让它先读该文件。Codex 的发现机制见 [官方 AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。
