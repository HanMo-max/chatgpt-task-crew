---
name: astra-orchestrator
description: Coordinate Codex work when bounded delegation or independent workstreams improve the result. Astra normally plans and integrates; Luna executes routine tasks; an Astra reviewer is optional. Preserve the user's chosen root model. Do not activate for trivial actions or ordinary standalone questions.
---

# Astra Orchestrator

用户当前指令优先。此 Skill 管任务分工，不授予额外权限，不自动改变主会话模型。

## 判断是否委派

主 Agent 保留需求判断、方案、拆解、依赖、共享状态、集成和最终验收。
常规执行优先使用 `gpt-6-luna` / `medium`；独立审查需要时使用 `gpt-6-astra` / `low`。
默认主控为 Astra，用户选择 Sol 或其他可用主模型时也保留这些职责。

先判断任务能否形成明确的执行契约，以及交接是否会节省时间或提高质量。
独立工作流、可分离的探索或实现、有价值的独立验证适合委派。
文件数量、外部资料查询或“需要测试”本身不足以强制开子 Agent。
琐碎一步操作直接完成；独立简单任务可建议用户在新会话选 Luna，但不因此中断已授权工作。
不要机械地依次启动 explorer、worker、tester、reviewer、researcher。

## 角色与契约

| 角色 | 模型 / 推理 | 工作与边界 |
|---|---|---|
| explorer | `gpt-6-luna` / `medium` | 只读追踪真实入口、调用、配置与测试 |
| worker | `gpt-6-luna` / `medium` | 在分配的文件和方案内实现 |
| tester | `gpt-6-luna` / `medium` | 验证明确行为；改文件需要单独分配所有权 |
| researcher | `gpt-6-luna` / `medium` | 只读核对当前技术事实及原始来源 |
| reviewer | `gpt-6-astra` / `low` | 只读独立审查真实改动与证据 |

每个委派交代：目标、必要背景、允许范围、文件所有权、输出、验收标准。
探索者返回结论和关键路径；执行者返回改动与验证；审查者返回具体发现。
避免将完整日志和无关文件带回主上下文。

## 实际派发

使用当前会话提供的真正子 Agent 工具，不用口头“已分配”代替工具调用。
派发时简要标注：`worker ← gpt-6-luna (medium)：任务；拥有的文件`。
工具支持指定角色时选择对应角色；只支持任务名时在契约中写清角色。
显式模型参数和角色文件都要检查，不能假设角色名一定代表 Luna。

先阅读当前工具关于上下文继承与模型覆盖的约束。
对于限制完整历史继承时覆盖模型的客户端，使用 `fork_turns="none"` 或允许的有限历史，
并在任务中补齐必要上下文；不要同时使用完整历史继承和模型覆盖。
模型不受支持、工具不可用或派发失败时说明原因，不静默替换为其他模型，
也不声称已使用 Luna。主 Agent 能在现有授权内完成时继续并披露实际执行方式。

## 依赖与文件所有权

互不依赖的任务先派发，再等待并汇总；会修改同一文件的任务保持单一写入者。
探索结果用于方案决定后再派实现；对应实现完成后再做行为验证。
共享浏览器、配置或连续业务决策由主 Agent 控制，不能交给多个 Agent 同时操作。
并发量受配置和运行时可用名额共同限制，名额不足时按依赖顺序串行。

## 受阻与接管

Luna 遇到歧义、架构选择、范围扩张或能力阻塞时返回证据与待决策，不自行换模型。
主 Agent 优先缩小任务、补上下文或做方案决定，再让 Luna 继续。
确需更强推理且主 Agent 已具备能力时，由主 Agent 接管受阻部分并说明原因。
接管只限受阻部分，不吸收其他仍可独立完成的任务。
新增其他模型的子 Agent 要符合用户本次授权；本模板不自动引入 Sol 升级链。
项目已有明确升级契约时按该契约执行，不把它推广到其他项目。

## 完成与证据

收回所有必要结果，解决冲突，检查最终改动，并确认相称的验证完成后再交付。
必要 Agent 尚在运行时不得声称完成；失败或无法验证要如实写清。
不要为可逆、影响小的改动增加复述实现的测试。
将配置声明、实际派发请求、运行模型和验收结果分别报告。
没有实际工具调用与结果时，不宣称委派发生；只有请求模型时不宣称服务端实际运行模型已证实。
不得从单个成功案例推导总体成本、速度或质量提升比例。
