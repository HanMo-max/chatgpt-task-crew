# ChatGPT Task Crew

让 ChatGPT / Codex 按任务分工：**Astra 负责判断、拆解和验收，Luna 负责明确、有边界的执行。**

这是一套从本机项目实践整理出的 Codex 配置与 Skill 模板。它利用 Codex 已有的子 Agent 能力，不需要另建调度服务。

默认模型为 `gpt-6-astra` + `gpt-6-luna`；用户选择 Sol 主控时也可沿用相同分工。仓库名包含 ChatGPT，是因为这些模型可通过相关产品使用；这里的 `.codex/` 文件面向支持本地配置的 Codex 客户端，不能直接安装到普通 ChatGPT 网页聊天中。本项目由个人维护，与 OpenAI 无官方隶属关系。

## 怎么分工

| 任务 | 建议处理方式 | 责任 |
|---|---|---|
| 独立的简单问答、格式整理、小范围修改 | 新会话直接选择 Luna | Luna 完成并给出必要验证 |
| Astra 会话中的琐碎一步操作 | 当前主 Agent 直接完成 | 避免交接成本超过执行成本 |
| 明确方案后的实现、文件定位、常规验证 | 有交接收益时派一个 Luna | 主 Agent 给清楚边界并验收 |
| 存在独立工作流的复杂任务 | Astra 拆解，Luna 分别执行 | Astra 负责依赖、冲突与集成 |
| 架构取舍、需求歧义、跨模块决策 | Astra 主控 | 先做决定，再派执行任务 |
| 有实际收益的独立审查 | Astra reviewer | 只读检查真实改动与证据 |

**任务涉及多个文件，并不自动意味着必须开多个 Agent。** 并行要有独立的输入、输出和文件所有权。测试跟在对应实现之后，不把所有角色机械地走一遍。

```mermaid
flowchart TD
    U[用户任务] --> T{任务判断}
    T -->|独立简单任务| L[Luna 直接执行]
    T -->|需要统筹| A[Astra 主控]
    A -->|需要定位或核对| E[Luna explorer / researcher]
    A --> D[Astra 确定方案和边界]
    E --> D
    D --> W[Luna worker]
    W --> V[按需要验证 / 独立审查]
    V --> F[Astra 集成与验收]
    W -->|范围不清或推理受阻| D
```

## 仓库内容

```text
templates/project/
  AGENTS.md                              合并到项目入口的简短规则
  .codex/config.toml                     Astra 主控与 Luna 默认子代理
  .codex/agents/{explorer,worker,tester,researcher,reviewer}.toml
  .agents/skills/astra-orchestrator/SKILL.md
docs/
  installation.md                        安装、已有配置合并与回滚
  usage-review.md                        本机实践、证据边界和整理改动
  runtime-verification.md                实际模型和委派的验收方法
examples/delegation.md                   可以直接改写使用的任务契约
scripts/check_bundle.py                  无第三方依赖的静态检查
```

文件放在 `templates/project/` 下，所以打开本仓库不会自动改动当前会话模型。安装时把模板合并进目标项目，完整步骤见 [installation.md](docs/installation.md)。

## 开始使用

1. 确认客户端提供子 Agent 工具、项目级配置和需要的模型；本地配置不能给账户增加模型权限。
2. 备份目标项目已有的 `AGENTS.md`、`.codex/` 和同名 Skill；合并模板，而不是覆盖整个项目规则。
3. 在 Codex 中打开目标项目，新建会话，在模型选择器确认主控模型。
4. 对复杂任务使用下面的提示，并按 [runtime-verification.md](docs/runtime-verification.md) 检查实际调用。

```text
使用 astra-orchestrator。
先判断是否有值得委派的独立工作流。主 Agent 保留方案、集成和最终验收，
常规执行交给 GPT-6 Luna medium；需要独立审查时使用 Astra reviewer。
每个委派说明范围、文件所有权、输出和验收标准，并简要标明实际模型。
不要为琐碎操作开子 Agent；遇到共享文件或依赖关系时按顺序处理。
```

独立的简单任务直接在新会话选择 Luna。模板不会自动把正在运行的 Astra 会话切换成 Luna。

## 已验证到哪一步

截至 **2026-10-08**，本机存在项目级正式部署，并有 Luna 执行和 Astra 审查的真实记录。早期计算器验证里，主 Agent 实际是 Sol，两个子 Agent 实际是旧版本 Luna；不能把它写成完整 Astra 拓扑测试。

本仓库是对现行部署的可移植整理，收紧了过度委派条件，移除了特定业务项目的职责和专用升级流程。**源项目运行证据不等于新版模板已经在目标客户端完成端到端安装验证。** 静态检查与规则审查的范围见 [usage-review.md](docs/usage-review.md)。没有经过配对实验的成本或耗时下降比例。

运行静态检查需要 Python 3.11 或更新版本：

```bash
python3 scripts/check_bundle.py
```

## 官方资料

- [子 Agent、模型选择与项目级角色文件](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [OpenAI 模型目录](https://developers.openai.com/api/docs/models)

模型名、配置字段和客户端支持可能变化；记录中的日期和版本属于当时的实际情况。模型可用性和权限以当前账户、客户端及会话运行结果为准。
