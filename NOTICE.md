# Notice / 版权与分发边界

`mcm-harness` 是面向中文数学建模 C 题的多 Agent 协作框架。项目原创代码、工作流、提示词、模板及文档采用 [MIT License](LICENSE)，版权人为 gdl1605，年份为 2026。复制或分发时保留相应版权声明和许可文本。

## 发布内容

本项目发布可复用的调度规则、上下文隔离协议、建模与论文工作流、机械辅助脚本、测试及内置 mcm Skill。它不是官方竞赛工具，不代表竞赛组织方意见，也不保证模型正确、论文合规或获奖。

公开包不应包含赛题原件、官方附件、真实竞赛数据、完整参考论文、答卷、个人运行记录或私有资料。内置 Skill 中的小型示例和表结构用于说明接口；诸如 `2021-C066` 的标记用于引用蒸馏经验，不表示分发对应论文，也不能作为实际建模结果。新增示例须明确来源和再分发权限。

MIT 授权不替代第三方数据、论文、字体、软件、模型服务或生成产物所适用的权利与使用条款。使用者仍需核对当届竞赛规则、AI 使用要求、学术诚信和数据授权，并人工核验模型、图表、引用与结论。

## 内置与外部组件

| 组件 | 来源和许可依据 | 本仓库处理方式 |
| --- | --- | --- |
| 内置 mcm Skill | [gdl1605/MCM.skill](https://github.com/gdl1605/MCM.skill)，MIT | 位于 `.agents/skills/mcm/`，保留其 [LICENSE](.agents/skills/mcm/LICENSE) 和 [NOTICE.md](.agents/skills/mcm/NOTICE.md)。含本项目集成调整，不宣称与上游某个版本完全一致。 |
| ssci-plots | [O0000-code/SSCI-Plots](https://github.com/O0000-code/SSCI-Plots)；[锁文件](Workflow/ssci-plots-skill.lock.json) 记录 MIT、来源 commit 和哈希 | 本仓库不分发技能目录，仅保留引用和锁定元数据。自行获取时核对所用版本并保留上游许可。 |
| nature-figure | [lth0/codexSkill](https://github.com/lth0/codexSkill)；[锁文件](Workflow/nature-figure-skill.lock.json) 记录当时未发现许可证、再分发前需核验 | 本仓库不分发技能目录。该记录不是当前上游许可状态的保证；未经核验与必要授权，不将其打包或纳入本项目 MIT。 |
| visualize-data、模型服务及其他运行工具 | 由用户的 Agent 平台或环境提供 | 不随本仓库分发，也不由本项目 MIT 重新授权。按各自条款使用。 |

外部绘图技能目录已列入 [.gitignore](.gitignore)。忽略规则不会移除已跟踪文件，也不会影响手工压缩整个目录；发布前必须核对实际文件清单，见 [发布清单](docs/releasing.md)。

运行期间由 `init_run.py` 记录的 mcm 文件哈希用于复现与漂移检查，不代表对内容正确性或版权状态的认证。
