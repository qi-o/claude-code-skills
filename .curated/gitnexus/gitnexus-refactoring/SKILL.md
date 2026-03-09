---
name: gitnexus-refactoring
description: Plan safe refactors using blast radius and dependency mapping
---

# Refactoring with GitNexus

## When to Use
- "Rename this function safely"
- "Extract this into a module"
- "Split this service"
- "Move this to a new file"
- Any task involving renaming, extracting, splitting, or restructuring code

## Workflow

```
1. gitnexus_impact({target: "X", direction: "upstream"})  鈫?Map all dependents
2. gitnexus_query({query: "X"})                            鈫?Find execution flows involving X
3. gitnexus_context({name: "X"})                           鈫?See all incoming/outgoing refs
4. Plan update order: interfaces 鈫?implementations 鈫?callers 鈫?tests
```

> If "Index is stale" 鈫?run `npx gitnexus analyze` in terminal.

## Checklists

### Rename Symbol
```
- [ ] gitnexus_rename({symbol_name: "oldName", new_name: "newName", dry_run: true}) 鈥?preview all edits
- [ ] Review graph edits (high confidence) and ast_search edits (review carefully)
- [ ] If satisfied: gitnexus_rename({..., dry_run: false}) 鈥?apply edits
- [ ] gitnexus_detect_changes() 鈥?verify only expected files changed
- [ ] Run tests for affected processes
```

### Extract Module
```
- [ ] gitnexus_context({name: target}) 鈥?see all incoming/outgoing refs
- [ ] gitnexus_impact({target, direction: "upstream"}) 鈥?find all external callers
- [ ] Define new module interface
- [ ] Extract code, update imports
- [ ] gitnexus_detect_changes() 鈥?verify affected scope
- [ ] Run tests for affected processes
```

### Split Function/Service
```
- [ ] gitnexus_context({name: target}) 鈥?understand all callees
- [ ] Group callees by responsibility
- [ ] gitnexus_impact({target, direction: "upstream"}) 鈥?map callers to update
- [ ] Create new functions/services
- [ ] Update callers
- [ ] gitnexus_detect_changes() 鈥?verify affected scope
- [ ] Run tests for affected processes
```

## Tools

**gitnexus_rename** 鈥?automated multi-file rename:
```
gitnexus_rename({symbol_name: "validateUser", new_name: "authenticateUser", dry_run: true})
鈫?12 edits across 8 files
鈫?10 graph edits (high confidence), 2 ast_search edits (review)
鈫?Changes: [{file_path, edits: [{line, old_text, new_text, confidence}]}]
```

**gitnexus_impact** 鈥?map all dependents first:
```
gitnexus_impact({target: "validateUser", direction: "upstream"})
鈫?d=1: loginHandler, apiMiddleware, testUtils
鈫?Affected Processes: LoginFlow, TokenRefresh
```

**gitnexus_detect_changes** 鈥?verify your changes after refactoring:
```
gitnexus_detect_changes({scope: "all"})
鈫?Changed: 8 files, 12 symbols
鈫?Affected processes: LoginFlow, TokenRefresh
鈫?Risk: MEDIUM
```

**gitnexus_cypher** 鈥?custom reference queries:
```cypher
MATCH (caller)-[:CodeRelation {type: 'CALLS'}]->(f:Function {name: "validateUser"})
RETURN caller.name, caller.filePath ORDER BY caller.filePath
```

## Risk Rules

| Risk Factor | Mitigation |
|-------------|------------|
| Many callers (>5) | Use gitnexus_rename for automated updates |
| Cross-area refs | Use detect_changes after to verify scope |
| String/dynamic refs | gitnexus_query to find them |
| External/public API | Version and deprecate properly |

## Example: Rename `validateUser` to `authenticateUser`

```
1. gitnexus_rename({symbol_name: "validateUser", new_name: "authenticateUser", dry_run: true})
   鈫?12 edits: 10 graph (safe), 2 ast_search (review)
   鈫?Files: validator.ts, login.ts, middleware.ts, config.json...

2. Review ast_search edits (config.json: dynamic reference!)

3. gitnexus_rename({symbol_name: "validateUser", new_name: "authenticateUser", dry_run: false})
   鈫?Applied 12 edits across 8 files

4. gitnexus_detect_changes({scope: "all"})
   鈫?Affected: LoginFlow, TokenRefresh
   鈫?Risk: MEDIUM 鈥?run tests for these flows
```
