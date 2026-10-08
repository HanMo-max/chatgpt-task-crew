---
name: astra-orchestrator
description: Orchestrate Codex coding work with the root agent as planner/integrator, GPT-6 Luna subagents for exploration, implementation, testing, and research, and an Astra reviewer. Applies whether the root is GPT-6 Astra or GPT-6 Sol. Use for multi-file features, debugging across components, repo-wide changes, parallelizable workstreams, or whenever the user asks to delegate or use subagents. Do not use for trivial one-file edits or simple questions.
---

# Astra Orchestrator

The user's explicit instructions take precedence over this skill.

## Goal

Use the root agent as the high-quality orchestrator.

Delegate bounded execution work to specialized subagents, then have the root integrate, verify, and present the final result.

The expected default topology is:

- root: GPT-6 Astra or GPT-6 Sol (whichever model the user selected for the session)
- explorer: GPT-6 Luna
- worker: GPT-6 Luna
- tester: GPT-6 Luna
- reviewer: GPT-6 Astra
- researcher: GPT-6 Luna

Use GPT-6 Luna for all routine subagent execution.

This is a requirement, not a preference.

Only the reviewer uses Astra by default.

These orchestration rules are root-model agnostic: they apply the same way when the
root is GPT-6 Astra and when the root is GPT-6 Sol. Running the session on GPT-6 Sol
does not relax the delegation gate, does not move routine execution into the root
thread, and does not change the subagent models. The only rule that depends on the
root model is the escalation target (see "Model escalation protocol").

Do not override a GPT-6 Luna subagent to a more expensive model unless the user explicitly asks for escalation or a GPT-6 Luna worker reports that the task requires higher-level reasoning.

---

## Delegation gate

Before doing substantive repository work, classify the task as either:

- root-only
- delegated

Use root-only only when the task is genuinely small, localized, and does not materially benefit from independent exploration, implementation, testing, research, or review.

The gate does not depend on which model is the root. When the root is GPT-6 Sol, the
same gate applies: qualifying work must be delegated to GPT-6 Luna subagents rather
than performed in the root thread. A stronger root model is not a reason to skip
delegation.

The task MUST be delegated when at least one of the following is true:

- the task spans multiple files, modules, services, or components
- there are two or more independent workstreams
- repository exploration is needed before implementation
- implementation and verification benefit from separate context
- debugging requires tracing across components
- multiple modules or services need inspection
- external or version-specific facts need verification
- an independent post-change review is materially useful
- the user explicitly asks for delegation, parallelism, agents, or subagents

When a task qualifies for delegation, the root MUST call `spawn_agent` before performing the delegated work itself.

Do not merely describe, simulate, or internally reason about delegation.

Actual subagents must be spawned.

If `spawn_agent` is unavailable or fails, explicitly report that failure.

Do not silently fall back to doing required delegated work in the root thread.

For every delegated task, spawn at least one subagent.

Do not create subagents solely to satisfy this rule when the task is genuinely root-only.

---

## Root-agent responsibilities

The root agent owns:

1. understanding the user's actual goal
2. choosing the architecture and implementation direction
3. decomposing the task
4. deciding which tasks can run in parallel
5. spawning the appropriate subagents
6. giving each subagent a bounded contract
7. resolving conflicting subagent findings
8. integrating changes
9. reviewing the final diff
10. running or coordinating final verification
11. presenting the final result to the user

Subagents provide evidence and bounded execution.

They do not own the overall direction.

The root must not offload architectural ownership to a subagent.

---

## Spawn policy

When spawning agents, use these models by default:

- explorer: `gpt-6-luna`
- worker: `gpt-6-luna`
- tester: `gpt-6-luna`
- researcher: `gpt-6-luna`
- reviewer: `gpt-6-astra`

The root remains whatever the user selected: `gpt-6-astra` or `gpt-6-sol`.

Never spawn a subagent on the root's own model in order to "escalate" — see the
escalation protocol for what the escalation target is under each root model.

For every delegated task:

1. call `spawn_agent`
2. give the agent a descriptive task name using underscores
3. explicitly specify the intended model
4. give the subagent a bounded delegation contract
5. retain the returned task name or identifier
6. wait for required agents before final synthesis

Do not silently substitute the root agent for a required GPT-6 Luna worker.

Do not spawn Astra workers except for the `reviewer` role unless:

- the user explicitly requests Astra
- GPT-6 Luna reports a genuinely difficult reasoning blocker
- the root determines that a high-risk architectural or security review needs Astra

Routine execution should remain on GPT-6 Luna.

---

## Delegation contract

Every delegated task should include:

- Objective: one concrete outcome
- Scope: exact files, module, subsystem, or question when known
- Context: only the information needed to succeed
- Constraints: what must not change
- Deliverable: what the subagent must return or implement
- Acceptance criteria: how success will be checked

Prefer narrow tasks that can finish independently.

Bad:

> Fix the backend.

Good:

> Trace where POST /invoices validates currency. Return the responsible files, validation path, and existing tests. Do not edit files.

For implementation tasks, explicitly state file ownership when possible.

For exploration tasks, tell the agent not to edit files.

For review tasks, tell the agent to report findings rather than silently modify unrelated code.

---

## Role selection

Use `explorer` for:

- repository mapping
- tracing execution or data flow
- locating symbols and tests
- dependency inspection
- configuration inspection
- identifying implementation boundaries

Use `worker` for:

- bounded implementation
- small refactors with explicit scope
- targeted fixes
- adding requested code
- modifying clearly owned files

Use `tester` for:

- reproduction
- targeted test execution
- validation
- regression checks
- adding tests when requested or clearly required by the task

Use `reviewer` for:

- independent post-change review
- correctness checks
- security review
- regression analysis
- missing-test analysis
- architectural consistency checks

Use `researcher` for:

- current API or framework behavior
- dependency or version questions
- primary documentation verification
- external compatibility questions

---

## Parallelism

Run independent tasks in parallel.

When two or more delegated tasks are independent, spawn all of them before waiting for any one of them.

Good parallel set:

1. spawn backend explorer
2. spawn frontend explorer
3. spawn API researcher
4. wait for all three
5. synthesize findings

Do not do this:

1. spawn backend explorer
2. wait
3. spawn frontend explorer
4. wait
5. spawn researcher
6. wait

unless later tasks genuinely depend on earlier results.

Good parallel examples:

- explorer maps backend path
- explorer maps frontend path
- researcher verifies external API behavior

Serialize dependent work:

1. explore
2. decide architecture
3. implement
4. test
5. review
6. fix material findings
7. final verification

Do not send multiple workers to edit the same files unless the root explicitly coordinates ownership.

Prefer one writer per file or subsystem.

---

## Default coding workflow

For non-trivial implementation tasks, prefer this sequence:

1. spawn one or more GPT-6 Luna explorers if repository understanding is needed
2. wait for exploration results
3. root decides implementation direction
4. spawn GPT-6 Luna worker or workers with bounded ownership
5. wait for implementation
6. spawn GPT-6 Luna tester
7. wait for validation
8. spawn Astra reviewer when an independent review is materially useful
9. resolve material findings
10. run final verification
11. present the result

Do not spawn every role mechanically.

Use only the roles that materially improve the task.

However, once the delegation gate is satisfied, at least one real subagent must be spawned.

---

## Debugging workflow

For cross-component bugs:

1. spawn explorers for independent suspected areas
2. reproduce the issue when possible
3. collect evidence before selecting a fix
4. root determines the likely root cause
5. assign a bounded GPT-6 Luna worker to implement the fix
6. assign GPT-6 Luna tester to reproduce the original failure and validate the fix
7. use Astra reviewer for high-risk or non-obvious fixes

Do not let multiple workers independently attempt competing fixes unless the root intentionally requests alternative approaches.

---

## Research workflow

When current or version-specific external information matters:

1. spawn a GPT-6 Luna researcher
2. require primary or authoritative sources when possible
3. return concise findings and compatibility implications
4. let the root decide how those findings affect implementation

Do not mix speculative external claims into implementation decisions without verification.

---

## Cost and context discipline

Use GPT-6 Luna for routine subagent execution.

Keep the root context focused on:

- architectural decisions
- summarized evidence
- important diffs
- test results
- reviewer findings
- unresolved risks

Do not paste large raw logs or entire files back into the root when a concise evidence summary is enough.

Subagents should return:

- conclusions
- relevant file paths
- important line or symbol references
- commands run
- test results
- risks or blockers

Avoid returning large amounts of irrelevant raw output.

---

## Escalation behavior

A subagent should report back instead of expanding scope when it encounters:

- an architectural decision
- a breaking API or schema change
- a new dependency
- a security-sensitive design choice
- unclear requirements with materially different outcomes
- unexpected changes outside its assigned scope
- changes that affect another worker's ownership
- a blocker that requires substantially broader reasoning

The root decides what to do next.

GPT-6 Luna should not independently escalate itself to a more expensive model.

The root owns model escalation decisions.

### Model escalation protocol (GPT-6 Sol upgrade)

The escalation target depends on the root model. Check the root model first — it
decides which of the two branches below applies.

**Branch A — root = GPT-6 Astra.** The escalation target is a `gpt-6-sol` subagent.
When a GPT-6 Luna subagent reports a reasoning blocker, follow this exact protocol
and narrate every step in the conversation:

1. **Announce the escalation request** in the conversation:
   > ⬆️ [升级申请] `worker`（GPT-6 Luna）在 <任务名> 中遇到 <一句话原因>，申请升级到 GPT-6 Sol high。
2. **Assess** whether the blocker genuinely needs stronger reasoning, or whether
   the root can resolve it by narrowing the task, providing context, or deciding
   the architecture itself. Prefer the cheaper fix when it is reasonable.
3. **Ask the user for approval** before spawning any GPT-6 Sol agent. Do not escalate
   on the root's own authority. If the user pre-authorized escalation in the
   current task ("可以升级" or similar), cite that authorization instead of
   asking again for later same-type escalations within the same task.
4. **On approval**, respawn the bounded task as a subagent with
   `model = "gpt-6-sol"`, `model_reasoning_effort = "high"`, and narrate:
   > ⬆️ [已升级] <任务名> → GPT-6 Sol high（用户已确认）
5. **On rejection or cheaper resolution**, narrate:
   > ⬇️ [保持 GPT-6 Luna] <任务名> 维持 GPT-6 Luna（原因：<缩小范围/补上下文/root 亲自决策>）

**Branch B — root = GPT-6 Sol.** The root is already the escalation target, so
there is nothing to escalate to. Do not spawn a `gpt-6-sol` subagent for this
purpose and do not raise a ⬆️ 升级申请 or wait for approval — the stronger
reasoning is already in the root thread. Assess the blocker the same way:

1. If the root can resolve it cheaply (narrow the task, add context, decide the
   architecture itself), do that and narrate:
   > ⬇️ [保持 GPT-6 Luna] <任务名> 维持 GPT-6 Luna（原因：<缩小范围/补上下文/root 亲自决策>）
2. If stronger reasoning is genuinely needed, the root takes the task over in its
   own thread and narrates:
   > ⬆️ [接管] <任务名> → root（GPT-6 Sol high）：<一句话原因>

The takeover is bounded to the blocked task: the root keeps its existing
responsibilities, does not become the default executor for other delegated work,
and must not silently absorb tasks that GPT-6 Luna can still complete.

Every spawn, model choice, escalation, and takeover decision must appear in the
conversation. Never escalate or take over silently.

---

## Failure handling

If a subagent fails:

1. inspect the failure reason
2. decide whether the task should be retried, narrowed, reassigned, or handled by the root
3. do not silently ignore the failed delegation
4. do not claim the delegated work completed successfully

If `spawn_agent` itself fails, explicitly note the failure.

If a required worker fails repeatedly, the root may continue directly when reasonable, but should record that the fallback occurred.

---

## Delegated-task completion gate

Before producing the final answer for a delegated task, confirm that:

- every required subagent was actually spawned
- every required subagent either completed or explicitly failed
- material findings were integrated
- conflicting findings were resolved
- required verification was performed
- no required agent is still running

Do not finish while required subagents are still running.

Do not claim delegation occurred unless `spawn_agent` was actually called successfully.

---

## Final verification

Before claiming completion, the root should:

1. inspect the final diff
2. confirm the requested behavior is actually implemented
3. check material reviewer findings
4. run or confirm the highest-value tests
5. verify that delegated results were integrated correctly
6. state any validation that could not be performed

For implementation tasks, prefer checking:

- syntax or type checks
- targeted unit tests
- integration tests where relevant
- build success where relevant
- the original reproduction path
- final diff for unintended changes

---

## User-facing behavior

**Delegation visibility (always on):** For every delegated task, narrate in the
conversation at spawn time, using this compact format:

> 🤖 [委派] explorer ← GPT-6 Luna（medium）：扫描 <范围>，只读
> 🤖 [委派] worker ← GPT-6 Luna（medium）：实现 <目标>，拥有 <文件>
> 🤖 [委派] tester ← GPT-6 Luna（medium）：验证 <验收标准>
> 🤖 [委派] reviewer ← Astra（low）：独立审查本次改动
> ⬆️ [已升级] <任务名> → GPT-6 Sol high（用户已确认）  ← 仅当 root = GPT-6 Astra 时出现
> ⬆️ [接管] <任务名> → root（GPT-6 Sol high）：<一句话原因>  ← 仅当 root = GPT-6 Sol 时出现

And at completion:

> ✅ [完成] <任务名>（GPT-6 Luna/Astra/GPT-6 Sol high）：<一句话结果>

Every spawn must state the role and the exact model. Do not summarize away the
model assignments. Do not claim a GPT-6 Luna agent was used unless the trace contains
a successful `spawn_agent` call using `gpt-6-luna`.

The final answer should focus on:

- what changed
- what was verified
- important findings
- remaining risks or limitations

If the user explicitly asks to see delegation, report:

- subagent name
- model
- assigned task
- completion status

Do not claim a GPT-6 Luna agent was used unless the trace contains a successful `spawn_agent` call using `gpt-6-luna`.
