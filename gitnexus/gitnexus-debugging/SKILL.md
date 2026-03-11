---
name: gitnexus-debugging
description: Trace bugs through call chains using knowledge graph
---

# Debugging with GitNexus

## When to Use
- "Why is this function failing?"
- "Trace where this error comes from"
- "Who calls this method?"
- "This endpoint returns 500"
- Investigating bugs, errors, or unexpected behavior

## Workflow

```
1. gitnexus_query({query: "<error or symptom>"})            鈫?Find related execution flows
2. gitnexus_context({name: "<suspect>"})                    鈫?See callers/callees/processes
3. READ gitnexus://repo/{name}/process/{name}                鈫?Trace execution flow
4. gitnexus_cypher({query: "MATCH path..."})                 鈫?Custom traces if needed
```

> If "Index is stale" 鈫?run `npx gitnexus analyze` in terminal.

## Checklist

```
- [ ] Understand the symptom (error message, unexpected behavior)
- [ ] gitnexus_query for error text or related code
- [ ] Identify the suspect function from returned processes
- [ ] gitnexus_context to see callers and callees
- [ ] Trace execution flow via process resource if applicable
- [ ] gitnexus_cypher for custom call chain traces if needed
- [ ] Read source files to confirm root cause
```

## Debugging Patterns

| Symptom | GitNexus Approach |
|---------|-------------------|
| Error message | `gitnexus_query` for error text 鈫?`context` on throw sites |
| Wrong return value | `context` on the function 鈫?trace callees for data flow |
| Intermittent failure | `context` 鈫?look for external calls, async deps |
| Performance issue | `context` 鈫?find symbols with many callers (hot paths) |
| Recent regression | `detect_changes` to see what your changes affect |

## Tools

**gitnexus_query** 鈥?find code related to error:
```
gitnexus_query({query: "payment validation error"})
鈫?Processes: CheckoutFlow, ErrorHandling
鈫?Symbols: validatePayment, handlePaymentError, PaymentException
```

**gitnexus_context** 鈥?full context for a suspect:
```
gitnexus_context({name: "validatePayment"})
鈫?Incoming calls: processCheckout, webhookHandler
鈫?Outgoing calls: verifyCard, fetchRates (external API!)
鈫?Processes: CheckoutFlow (step 3/7)
```

**gitnexus_cypher** 鈥?custom call chain traces:
```cypher
MATCH path = (a)-[:CodeRelation {type: 'CALLS'}*1..2]->(b:Function {name: "validatePayment"})
RETURN [n IN nodes(path) | n.name] AS chain
```

## Example: "Payment endpoint returns 500 intermittently"

```
1. gitnexus_query({query: "payment error handling"})
   鈫?Processes: CheckoutFlow, ErrorHandling
   鈫?Symbols: validatePayment, handlePaymentError

2. gitnexus_context({name: "validatePayment"})
   鈫?Outgoing calls: verifyCard, fetchRates (external API!)

3. READ gitnexus://repo/my-app/process/CheckoutFlow
   鈫?Step 3: validatePayment 鈫?calls fetchRates (external)

4. Root cause: fetchRates calls external API without proper timeout
```
