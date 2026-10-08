# 安装与回滚

推荐先在一个隔离项目安装，再合并到实际工作项目。模板只修改项目级规则，不需要复制全局账户配置。

## 安装前

确认 Codex 客户端支持 `.codex/config.toml`、`.codex/agents/*.toml`、项目级 Skill 和子 Agent 工具。
确认模型选择器提供需要的模型。官方文档支持这些配置形式，但账户权限与不同客户端版本仍需实测。

新建本地备份目录，把目标项目已有的以下内容复制进去：

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/` 中将合并的同名角色
- `.agents/skills/astra-orchestrator/`

备份保留在目标项目的本地备份目录，不提交 Git。

## 合并文件

可以在 Finder 或编辑器中操作：

1. 把 `templates/project/.codex/agents/` 中的五个角色文件合并到目标项目。已存在同名角色时先比较，保留项目专用约束。
2. 把 `templates/project/.agents/skills/astra-orchestrator/` 合并到目标项目同一路径。
3. 将模板 `AGENTS.md` 的规则段合并到项目已有的 `AGENTS.md`。
4. 将模板 `config.toml` 的主控默认值和 `[agents]` 字段合并到目标项目配置；已有 `[agents]` 表时修改其中的字段，不再追加第二个表。

Finder 默认隐藏以点开头的目录，使用 `Command + Shift + .` 显示 `.codex` 和 `.agents`。

主控默认 `gpt-6-astra` / `high`，也支持 `gpt-6.1-sol` / `high`；普通子 Agent 默认 `gpt-6-luna` / `medium`；reviewer 为 Astra / `low`。
如果需要 GPT-6.1 Sol 主控，在模型选择器选择它，或将项目配置顶层的 `model` 改为 `"gpt-6.1-sol"`，保持 `model_reasoning_effort = "high"`。独立简单任务直接选择 `gpt-6-luna`，常规子代理继续使用 Luna medium。

模板保留现行源项目的 6 个子线程上限，未做性能最优性测试。
运行时可能提供更少名额；实际并发以当前会话为准。

`approval_policy` 和 `sandbox_mode` 也要与原项目配置合并；角色文件不是绕过父会话权限的入口。
父会话的实时权限覆盖可能优先于角色默认值。尤其 tester 虽允许测试产物写入，默认不允许修改源码。

发布 Skill 保留现行委派门槛，并将 Astra/Sol 双支路中的旧 Sol 更新为 GPT-6.1 Sol。主控是 Astra 时，Luna → GPT-6.1 Sol high 的新增升级遵守现有用户授权要求；主控是 GPT-6.1 Sol 时由主控接管受阻部分，不重复派发同模型子代理。该更新属于规则修改，不能替代安装后的运行验证。
不同客户端的子 Agent 工具 schema 可能有上下文继承限制；显式覆盖模型时，先检查是否需要使用 `fork_turns="none"` 或有限历史，不能用旧示例越过当前工具约束。

## 生效验证

重新打开项目或新建会话，确认 Skill 可发现、角色可用、主模型正确。
在启动日志、派发请求和子会话元数据中核对实际模型。不要只检查 TOML。
现有会话不一定重新加载配置，模型选择器或实时覆盖也可能改变主模型。

按 [runtime-verification.md](runtime-verification.md) 完成一轮隔离验证。
在本项目所在的仓库中运行 `python3 scripts/check_bundle.py` 只能检查模板本身，不能证明目标项目已安装成功。

## 回滚

关闭相关运行中的 Agent，恢复本次备份的文件。对于安装时新增而原先不存在的角色或 Skill，只移除本次新增项。
重新打开项目并核对实际配置。不要用全局 `~/.codex/config.toml` 覆盖项目配置，也不要将项目模板覆盖整个全局配置。

## 适用产品

本仓库可作为 ChatGPT 中讨论任务分工的参考；实际安装目标是支持上述本地格式的 Codex 客户端。
普通 ChatGPT 网页不会读取本机 `.codex/` 目录。托管环境或其他客户端使用它们自己的配置接口。

参考：[官方子 Agent 配置说明](https://learn.chatgpt.com/docs/agent-configuration/subagents)。
