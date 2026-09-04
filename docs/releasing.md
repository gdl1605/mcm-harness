# 发布前检查

本清单用于发布 `mcm-harness` 框架，不用于上传某次比赛的整套工作目录。建议从经过审查的 Git 提交生成源码包，避免直接压缩本地工程目录。

## 1. 文件与许可

- [ ] 根目录包含 `README.md`、`LICENSE`、`NOTICE.md`、`CONTRIBUTING.md`、`SECURITY.md` 和 `CHANGELOG.md`。
- [ ] 内置 `.agents/skills/mcm/` 完整，且保留其 `LICENSE`、`NOTICE.md`。
- [ ] 已核对 [NOTICE.md](../NOTICE.md) 中的来源和许可边界；新增第三方内容保留了必要声明。
- [ ] `.agents/skills/nature-figure/` 与 `.agents/skills/ssci-plots/` 不进入公开包；仅发布对应锁文件。nature-figure 的再分发许可未核验前，不因框架采用 MIT 就将它一并授权。
- [ ] 赛题、附件、真实数据、完整论文、运行记录、缓存、凭据和私人配置不进入公开包。
- [ ] 新示例注明来源、授权或合成性质，未混入实际比赛数据。

在仓库根目录检查候选文件与已跟踪文件：

```bash
git status --short --untracked-files=all
git ls-files
git ls-files --others --exclude-standard
git ls-files -ci --exclude-standard
git diff --check
```

最后一个 `git ls-files` 命令列出“已跟踪但命中忽略规则”的文件，预期为空。`.gitignore` 不会让已跟踪文件自动退出版本控制。发现问题后逐项确认处理范围，不对已有开发改动做批量清理。

## 2. 功能与文档

```bash
python3 -m unittest discover -s tests -v
python3 scripts/bootstrap.py --help
python3 scripts/init_run.py --help
python3 scripts/build_prompt.py --help
python3 scripts/check_workspace.py --help
```

- [ ] 在干净检出或发布包解压目录中复跑上述检查，而非仅在开发目录运行。
- [ ] 按 README 的步骤在临时目录验证初始化和 `--stage init` 检查。
- [ ] README 相对链接有效，示例命令与真实脚本参数一致。
- [ ] 如改动工作流，完成受影响阶段的人工语义检查，并记录没有验证的部分。
- [ ] 如宣称正式绘图可运行，已确认目标环境的模型、三个绘图技能及锁文件要求均可满足；缺失依赖应明确列为限制。
- [ ] `CHANGELOG.md` 只记录真实完成的内容，不把单元测试当成全流程回归或质量认证。

## 3. 敏感信息与历史

- [ ] 检查待发布文本、数据、文件名和 Git 历史中的秘密、个人路径及私人资料。常见字符串搜索只能辅助，不能证明绝无泄露。
- [ ] 若仓库将从私有改为公开，核对所有将公开的分支、标签和历史对象；仅检查当前工作树不够。
- [ ] 确认安全反馈邮箱仍可用。发现泄露时先按 [SECURITY.md](../SECURITY.md) 处理，不直接在公开 Issue 粘贴原文。

## 4. 生成发布包

先由维护者审查、选择并提交实际发布文件，确认目标提交、版本名和未解决限制。本项目不会自动提交、打标签、推送或修改仓库可见性。

以下示例仅在 `HEAD` 已是批准发布的提交时使用；它不包含尚未提交的新增文档或工作区改动：

```bash
git show --stat --oneline HEAD
git archive --format=zip --prefix=mcm-harness/ --output=../mcm-harness-source.zip HEAD
unzip -l ../mcm-harness-source.zip
```

若输出 ZIP 已存在，先另选文件名，避免覆盖旧包。源码 ZIP 不包含 Git 历史，但仍必须核对文件清单、许可和依赖说明；将仓库本身公开则还需完成上述历史审查。
