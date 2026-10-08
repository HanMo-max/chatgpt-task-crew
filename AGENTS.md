# Repository instructions

本仓库维护可移植的 Codex 模型分工模板。

- 维护内容以 `templates/project/` 为准；这些模板不应自动安装到维护者的全局环境。
- 默认 Astra 统筹，Luna 执行常规任务；保留用户实际选择的主模型。
- 委派需要实际收益、明确输入输出与文件边界；不要为修改文案机械派发所有角色。
- 配置与 Skill 改动后运行 `python3 scripts/check_bundle.py`。
- 静态检查、历史源项目运行和新版模板端到端运行应分别报告。
- 不提交原始聊天日志、个人绝对路径、全局账户配置、凭据或业务素材。
