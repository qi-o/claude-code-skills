---
name: gitnexus-exploring
description: Navigate unfamiliar code using GitNexus knowledge graph
---

# Exploring Codebases with GitNexus

## When to Use
- "How does authentication work?"
- "What's the project structure?"
- "Show me the main components"
- "Where is the database logic?"
- Understanding code you haven't seen before

## Workflow

```
1. READ gitnexus://repos                          鈫?Discover indexed repos
2. READ gitnexus://repo/{name}/context             鈫?Codebase overview, check staleness
3. gitnexus_query({query: "<what you want to understand>"})  鈫?Find related execution flows
4. gitnexus_context({name: "<symbol>"})            鈫?Deep dive on specific symbol
5. READ gitnexus://repo/{name}/process/{name}      鈫?Trace full execution flow
```

> If step 2 says "Index is stale" 鈫?run `npx gitnexus analyze` in terminal.

## Checklist

```
- [ ] READ gitnexus://repo/{name}/context
- [ ] gitnexus_query for the concept you want to understand
- [ ] Review returned processes (execution flows)
- [ ] gitnexus_context on key symbols for callers/callees
- [ ] READ process resource for full execution traces
- [ ] Read source files for implementation details
```

## Resources

| Resource | What you get |
|----------|-------------|
| `gitnexus://repo/{name}/context` | Stats, staleness warning (~150 tokens) |
| `gitnexus://repo/{name}/clusters` | All functional areas with cohesion scores (~300 tokens) |
| `gitnexus://repo/{name}/cluster/{name}` | Area members with file paths (~500 tokens) |
| `gitnexus://repo/{name}/process/{name}` | Step-by-step execution trace (~200 tokens) |

## Tools

**gitnexus_query** 鈥?find execution flows related to a concept:
```
gitnexus_query({query: "payment processing"})
鈫?Processes: CheckoutFlow, RefundFlow, WebhookHandler
鈫?Symbols grouped by flow with file locations
```

**gitnexus_context** 鈥?360-degree view of a symbol:
```
gitnexus_context({name: "validateUser"})
鈫?Incoming calls: loginHandler, apiMiddleware
鈫?Outgoing calls: checkToken, getUserById
鈫?Processes: LoginFlow (step 2/5), TokenRefresh (step 1/3)
```

## Example: "How does payment processing work?"

```
1. READ gitnexus://repo/my-app/context       鈫?918 symbols, 45 processes
2. gitnexus_query({query: "payment processing"})
   鈫?CheckoutFlow: processPayment 鈫?validateCard 鈫?chargeStripe
   鈫?RefundFlow: initiateRefund 鈫?calculateRefund 鈫?processRefund
3. gitnexus_context({name: "processPayment"})
   鈫?Incoming: checkoutHandler, webhookHandler
   鈫?Outgoing: validateCard, chargeStripe, saveTransaction
4. Read src/payments/processor.ts for implementation details
```
