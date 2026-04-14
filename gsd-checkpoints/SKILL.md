---
name: gsd-checkpoints
description: >
  Automation-first checkpoint system from GSD v1. Auto-verify what can be automated,
  present decisions when needed, request human action only for truly manual steps.
  Trigger: "/gsd-checkpoints", "checkpoint", "verify-checkpoint"
user-invocable: true
allowed-tools: "Read, Write, Edit, Bash, Glob, Grep"
---

# GSD Checkpoints — Automation-First Verification

## Purpose

Structure the interaction between agent automation and human judgment. The agent automates everything it can, then presents clean checkpoints for human decisions or verification.

## The 90/9/1 Rule

| Checkpoint Type | Frequency | Purpose |
|----------------|-----------|---------|
| `human-verify` | 90% | Agent automated everything. Human confirms visual/functional correctness. |
| `decision` | 9% | Human makes a choice between options (tech stack, architecture, UX). |
| `human-action` | 1% | Truly unavoidable manual step (auth gate, email link, 2FA, physical action). |

## Golden Rules

1. **If the agent CAN run it, the agent RUNS it.** No asking user to run commands.
2. **Agent sets up the verification environment** — starts dev servers, seeds databases, opens browsers.
3. **User only does what requires human judgment** — visual checks, UX evaluation, architectural decisions.
4. **Secrets come from user, automation from agent.**
5. **One checkpoint at end of flow is better than many checkpoints throughout.**

## Checkpoint Types

### `human-verify` (90% of checkpoints)

Agent has automated everything and prepared the verification environment.

**Agent MUST do before presenting:**
- Start dev server if needed (Next.js, Vite, Django, etc.)
- Seed test data
- Navigate to the relevant page/endpoint
- Run automated tests and report results

**Present to user:**
```
═════════════════════════════════════════════════════════
  CHECKPOINT: Verification Required
═════════════════════════════════════════════════════════
Progress: [X/Y] tasks complete

## What was built:
[Brief description of what was implemented]

## Automated verification results:
- ✅ Tests: [X/Y passing]
- ✅ Lint: [no errors]
- ✅ Type check: [clean]

## Verify manually:
1. Open [URL] in browser
2. [Specific action to test]
3. Expected: [what should happen]

────────────────────────────────────────────────────────
→ Type "approved" to continue, or describe any issues
────────────────────────────────────────────────────────
```

### `decision` (9% of checkpoints)

Human needs to choose between options.

**Present to user:**
```
═════════════════════════════════════════════════════════
  CHECKPOINT: Decision Required
═════════════════════════════════════════════════════════
Context: [why this decision is needed]

## Option A: [name]
- Pros: [...]
- Cons: [...]

## Option B: [name]
- Pros: [...]
- Cons: [...]

────────────────────────────────────────────────────────
→ Type "A" or "B" (or describe your preference)
────────────────────────────────────────────────────────
```

### `human-action` (1% of checkpoints)

Truly unavoidable manual step.

**Use ONLY for:**
- Authentication gates (OAuth flows, 2FA)
- Email verification links
- Physical device interactions
- External service configuration that requires browser access

**Auth Gate Pattern:**
1. Agent attempts automated action
2. Hits 401/403 or auth error
3. Dynamically creates `human-action` checkpoint
4. User authenticates manually
5. Agent retries the automated action

**Present to user:**
```
═════════════════════════════════════════════════════════
  CHECKPOINT: Manual Action Required
═════════════════════════════════════════════════════════
The agent cannot automate this step.

## Action needed:
[Specific manual step, e.g., "Log in to X service in your browser"]

## Why:
[Reason this requires human action, e.g., "OAuth flow requires browser redirect"]

## After completing:
Type "done" and the agent will retry the automated action.
────────────────────────────────────────────────────────
```

## Anti-Patterns (Forbidden)

- ❌ **Never** ask user to start dev servers — agent starts them
- ❌ **Never** ask user to run CLI commands — agent runs them
- ❌ **Never** ask user to copy values between services — use APIs/env vars
- ❌ **Never** create too many checkpoints — batch verification at end of flow
- ❌ **Never** use vague verification ("check it works") — always specify URLs, steps, expected outcomes
- ❌ **Never** ask user to install packages — agent installs them
- ❌ **Never** ask user to create files — agent creates them

## Dev Server Automation Patterns

### Next.js / React
```bash
npm run dev &  # background start
sleep 3        # wait for ready
curl -s http://localhost:3000 > /dev/null  # verify ready
```

### Vite
```bash
npm run dev &
sleep 2
curl -s http://localhost:5173 > /dev/null
```

### Express / FastAPI / Django
```bash
npm run start / python manage.py runserver &
sleep 2
curl -s http://localhost:8000/health > /dev/null
```

## Integration with OMC

| OMC Component | Integration |
|--------------|-------------|
| `ultrawork` | Checkpoints fire after parallel execution completes |
| `ralph` | Checkpoints are natural ralph pause points |
| `autopilot` | Auto-mode approves `human-verify` automatically, stops for `decision` and `human-action` |
| `verifier` agent | Uses checkpoint format for presenting verification results |
| `state_write` | Checkpoint state saved to `.omc/state/` for recovery |

## Workflow Integration

```
Implement → Run automated tests → Verify must_haves (per goal-verification.md) → Present checkpoint
                                                         ↓
                                                    User responds
                                                         ↓
                                              Approved → Continue
                                              Issues → Fix → Re-verify → New checkpoint
```


## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### Known Fixes & Workarounds
- OMC 更新不会覆盖 ~/.claude/rules/ 下的文件（installer 零代码路径写入此目录）——创建新规则文件是安全的
- OMC 的 prunePluginDuplicateAgents() 仅匹配 plugin agent 名称 + OMC frontmatter 的文件——用户自定义 agent 文件保留，修改 verifier.md/planner.md/executor.md 是安全的
- Codex review 发现的关键冲突模式：新规则的自动修复上限（3次）必须与 independent-review.md 的 3x retry 规则对齐，不能写成 move on 而要写成 STOP and escalate
- Rule 2 Missing from plan 的 YAGNI 边界：只有 spec/user request 明确提过的才能 auto-add，agent 自己推断的需求要问用户确认

---

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| Checkpoint 类型选择 | 需要决定是 `human-verify`、`decision` 还是 `human-action` | 确认该步骤是否真正需要人工参与，避免将可自动化步骤误标为人工 |
| 批量审批风险 | autopilot 模式自动审批 `human-verify` checkpoint | 如果任务涉及破坏性操作（删除数据、覆盖文件），即使 autopilot 模式也应暂停确认 |
| 验证环境未就绪 | dev server 启动失败或测试数据库 seed 失败 | 确认是否跳过自动化验证直接展示 checkpoint，还是等待环境修复 |

---

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| Dev server 启动失败 | `curl` 健康检查返回非 200 或超时 | 检查端口占用/依赖缺失，尝试修复；3 次失败后降级为 `human-action` checkpoint |
| 自动化测试全部失败 | 测试套件 0 通过 | 不展示 checkpoint，直接报告失败并切换到调试模式 |
| 用户长时间未响应 | checkpoint 等待超过合理时间 | 保存当前状态到 `.omc/state/`，提示用户可随时恢复 |
| OMC 状态写入失败 | `state_write` 返回错误 | 检查 `.omc/state/` 目录权限，创建目录后重试；失败则仅保留内存状态 |