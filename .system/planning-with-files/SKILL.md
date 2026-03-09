---
name: planning-with-files
description: Transforms workflow to use Manus-style persistent markdown files for planning, progress tracking, and knowledge storage. Use when starting complex tasks, multi-step projects, research tasks, or when the user mentions planning, organizing work, tracking progress, or wants structured output.
version: 2.19.0
github_url: https://github.com/OthmanAdi/planning-with-files
github_hash: 7b55095bce7624011ec118e6a6029e37ec8a1ea2
license: MIT
metadata:
  category: workflow-automation
---

# Planning with Files (v2.15.1)

Work like Manus: Use persistent markdown files as your "working memory on disk."

> **Why This Pattern?** On December 29, 2025, Meta acquired Manus for $2 billion. Their secret? Context engineering - using markdown files as "working memory on disk."

## What's New in v2.15.1

- **Session catchup false-positive fix** - Bug fix for session recovery (thanks @gydx6!)

### Previous: v2.15.0

- **`/plan:status` command** - Shows planning progress at a glance
- **OpenCode compatibility fix** - Improved OpenCode IDE support with dedicated scripts
- **2-Action Rule** - Save discoveries to file every 2 browse/search actions
- **3-Strike Error Protocol** - Full 3-attempt escalation protocol for error handling
- **Never Repeat Failures** - `if action_failed: next_action != same_action`
- **Read vs Write Decision Matrix** - 6-scenario decision matrix for read/write operations
- **5-Question Reboot Test** - Context management self-check checklist
- **File Location Guidance** - Clear distinction between skill directory and project directory
- **Anti-Patterns expanded** - Added "Repeat failed actions" and "Create files in skill directory"

### Previous: v2.14.0
- Pi Agent support - Full integration with Pi Agent IDE
- Cursor hooks - preToolUse, postToolUse, and stop hooks
- OpenClaw - Moltbot renamed to OpenClaw (.moltbot/ 鈫?.openclaw/)
- Bug fixes - Codex skill paths, check-complete scripts, stop hook errors
- Plan Cascade - Enhanced plan management feature

### Previous: v2.13.0
- Moltbot rebrand (formerly Clawd CLI)
- AdaL CLI / Sylph AI support
- `/plan` command for easier autocomplete
- Kiro steering files support
- Continue IDE support
- Session recovery after `/clear`

## Quick Start

Before ANY complex task:

1. **Create `task_plan.md`** in the working directory
2. **Define phases** with checkboxes
3. **Update after each phase** - mark [x] and change status
4. **Read before deciding** - refresh goals in attention window

## The 3-File Pattern

For every non-trivial task, create THREE files:

| File | Purpose | When to Update |
|------|---------|----------------|
| `task_plan.md` | Track phases and progress | After each phase |
| `notes.md` | Store findings and research | During research |
| `[deliverable].md` | Final output | At completion |

## Core Workflow

```
Loop 1: Create task_plan.md with goal and phases
Loop 2: Research 鈫?save to notes.md 鈫?update task_plan.md
Loop 3: Read notes.md 鈫?create deliverable 鈫?update task_plan.md
Loop 4: Deliver final output
```

### The Loop in Detail

**Before each major action:**
```bash
Read task_plan.md  # Refresh goals in attention window
```

**After each phase:**
```bash
Edit task_plan.md  # Mark [x], update status
```

**When storing information:**
```bash
Write notes.md     # Don't stuff context, store in file
```

## task_plan.md Template

Create this file FIRST for any complex task:

```markdown
# Task Plan: [Brief Description]

## Goal
[One sentence describing the end state]

## Phases
- [ ] Phase 1: Plan and setup
- [ ] Phase 2: Research/gather information
- [ ] Phase 3: Execute/build
- [ ] Phase 4: Review and deliver

## Key Questions
1. [Question to answer]
2. [Question to answer]

## Decisions Made
- [Decision]: [Rationale]

## Errors Encountered
- [Error]: [Resolution]

## Status
**Currently in Phase X** - [What I'm doing now]
```

## notes.md Template

For research and findings:

```markdown
# Notes: [Topic]

## Sources

### Source 1: [Name]
- URL: [link]
- Key points:
  - [Finding]
  - [Finding]

## Synthesized Findings

### [Category]
- [Finding]
- [Finding]
```

## Critical Rules

### 1. ALWAYS Create Plan First
Never start a complex task without `task_plan.md`. This is non-negotiable.

### 2. Read Before Decide
Before any major decision, read the plan file. This keeps goals in your attention window.

### 3. Update After Act
After completing any phase, immediately update the plan file:
- Mark completed phases with [x]
- Update the Status section
- Log any errors encountered

### 4. Store, Don't Stuff
Large outputs go to files, not context. Keep only paths in working memory.

### 5. Log All Errors
Every error goes in the "Errors Encountered" section. This builds knowledge for future tasks.

### 6. 2-Action Rule
After every 2 browse/search operations, immediately save your discoveries to a file. Do not accumulate findings only in context -- persist them to disk regularly.

```
action_count = 0
for each browse/search action:
    action_count += 1
    if action_count >= 2:
        save findings to notes.md
        action_count = 0
```

### 7. 3-Strike Error Protocol
When an action fails, follow this escalation protocol:

| Strike | Action |
|--------|--------|
| Strike 1 | Retry with minor adjustment (different parameter, slight variation) |
| Strike 2 | Try a fundamentally different approach to achieve the same goal |
| Strike 3 | Log the blocker in task_plan.md, skip this step, and move to the next phase |

**Never** attempt the same failing action more than 3 times.

### 8. Never Repeat Failures
```
if action_failed:
    next_action != same_action
```
If an action failed, your very next action MUST be different. Do not retry the exact same command, query, or approach. Change something meaningful before retrying.

### 9. Read vs Write Decision Matrix

| Scenario | Action | Why |
|----------|--------|-----|
| Starting a new phase | Read task_plan.md | Refresh goals in attention window |
| Found new information | Write to notes.md | Persist discovery before it leaves context |
| Completed a phase | Edit task_plan.md | Mark progress, update status |
| About to make a decision | Read task_plan.md + notes.md | Ensure decision aligns with goals and findings |
| Error occurred | Edit task_plan.md | Log error immediately for future reference |
| Context window getting full | Write summary to notes.md | Preserve key findings before potential context loss |

### 10. 5-Question Reboot Test
Before starting any new phase, ask yourself these 5 questions. If you cannot answer any of them, re-read the relevant file:

1. **What is the end goal?** (If unclear, read task_plan.md)
2. **What phase am I in?** (If unclear, read task_plan.md)
3. **What have I found so far?** (If unclear, read notes.md)
4. **What errors have I hit?** (If unclear, read task_plan.md)
5. **What is my next action?** (If unclear, read task_plan.md)

## When to Use This Pattern

**Use 3-file pattern for:**
- Multi-step tasks (3+ steps)
- Research tasks
- Building/creating something
- Tasks spanning multiple tool calls
- Anything requiring organization

**Skip for:**
- Simple questions
- Single-file edits
- Quick lookups

## File Location Guidance

**Important:** All planning files (`task_plan.md`, `notes.md`, `[deliverable].md`) must be created in the **project working directory**, NOT in the skill installation directory.

| Location | What Goes Here |
|----------|---------------|
| Skill directory (`.claude/skills/...`) | Skill definition files only (SKILL.md, reference.md, etc.) -- **never modify** |
| Project working directory (`./`) | All task-specific files: task_plan.md, notes.md, deliverables |

**Never** create task files inside the skill directory. The skill directory is read-only reference material.

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Use TodoWrite for persistence | Create `task_plan.md` file |
| State goals once and forget | Re-read plan before each decision |
| Hide errors and retry | Log errors to plan file |
| Stuff everything in context | Store large content in files |
| Start executing immediately | Create plan file FIRST |
| Repeat failed actions unchanged | Change approach after each failure (Never Repeat Failures rule) |
| Create files in skill directory | Always create task files in the project working directory |

## Advanced Patterns

See [reference.md](reference.md) for:
- Attention manipulation techniques
- Error recovery patterns
- Context optimization from Manus

See [examples.md](examples.md) for:
- Real task examples
- Complex workflow patterns

## Session Recovery (v2.2.0+)

When your context window fills up and you run `/clear`, this skill automatically recovers unsynced work from your previous session.

**Session Catchup Commands:**

On Linux/macOS:
```bash
cat task_plan.md notes.md 2>/dev/null || echo "No previous session files found"
```

On Windows:
```powershell
Get-Content task_plan.md, notes.md -ErrorAction SilentlyContinue
```

These commands quickly reload your previous session state into the new context window.

**Optimal Workflow:**
1. Disable auto-compact in Claude Code settings (use full context window)
2. Start a fresh session in your project
3. Run `/planning-with-files` when ready to work on a complex task
4. Work until context fills up (Claude will warn you)
5. Run `/clear` to start fresh
6. The skill automatically recovers your progress from plan files

## Supported IDEs

| IDE | Status | Format |
|-----|--------|--------|
| Claude Code | 鉁?Full Support | Plugin + SKILL.md |
| Gemini CLI | 鉁?Full Support | Agent Skills |
| Moltbot | 鉁?Full Support | Workspace/Local Skills |
| Kiro | 鉁?Full Support | Steering Files |
| Cursor | 鉁?Full Support | Skills |
| Continue | 鉁?Full Support | Skills + Prompt files |
| Kilocode | 鉁?Full Support | Skills |
| OpenCode | 鉁?Full Support | Personal/Project Skill |
| Codex | 鉁?Full Support | Personal Skill |
| FactoryAI Droid | 鉁?Full Support | Workspace/Personal Skill |
| Antigravity | 鉁?Full Support | Workspace/Personal Skill |
| CodeBuddy | 鉁?Full Support | Workspace/Personal Skill |
| AdaL CLI | 鉁?Full Support | Personal/Project Skills |

## The Problem This Solves

Claude Code (and most AI agents) suffer from:
- **Volatile memory** 鈥?TodoWrite tool disappears on context reset
- **Goal drift** 鈥?After 50+ tool calls, original goals get forgotten
- **Hidden errors** 鈥?Failures aren't tracked, so the same mistakes repeat
- **Context stuffing** 鈥?Everything crammed into context instead of stored

## Core Principle

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)

鈫?Anything important gets written to disk.
```
