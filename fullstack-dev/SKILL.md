---
github_url: https://github.com/MiniMax-AI/skills
github_hash: 1391b63464d11c985fe8d320fb8ac988f582c0d6
name: fullstack-dev
description: |
  Full-stack backend architecture and frontend-backend integration guide.
  TRIGGER when: building a full-stack app, creating REST API with frontend, scaffolding backend service,
  building todo app, building CRUD app, building real-time app, building chat app,
  Express + React, Next.js API, Node.js backend, Python backend, Go backend,
  designing service layers, implementing error handling, managing config/auth,
  setting up API clients, implementing auth flows, handling file uploads,
  adding real-time features (SSE/WebSocket), hardening for production.
  DO NOT TRIGGER when: pure frontend UI work, pure CSS/styling, database schema only.
license: MIT
metadata:
  category: full-stack
  version: "1.1.0"
  sources:
    - The Twelve-Factor App (12factor.net)
    - Clean Architecture (Robert C. Martin)
    - Domain-Driven Design (Eric Evans)
    - Patterns of Enterprise Application Architecture (Martin Fowler)
    - Martin Fowler (Testing Pyramid, Contract Tests)
    - Google SRE Handbook (Release Engineering)
    - ThoughtWorks Technology Radar
---

# Full-Stack Development Practices

## MANDATORY WORKFLOW — Follow These Steps In Order

**When this skill is triggered, you MUST follow this workflow before writing any code.**

### Step 0: Gather Requirements

Before scaffolding anything, ask the user to clarify (or infer from context):

1. **Stack**: Language/framework for backend and frontend (e.g., Express + React, Django + Vue, Go + HTMX)
2. **Service type**: API-only, full-stack monolith, or microservice?
3. **Database**: SQL (PostgreSQL, SQLite, MySQL) or NoSQL (MongoDB, Redis)?
4. **Integration**: REST, GraphQL, tRPC, or gRPC?
5. **Real-time**: Needed? If yes — SSE, WebSocket, or polling?
6. **Auth**: Needed? If yes — JWT, session, OAuth, or third-party (Clerk, Auth.js)?

If the user has already specified these in their request, skip asking and proceed.

### Step 1: Architectural Decisions

Based on requirements, make and state these decisions before coding:

| Decision | Options | Reference |
|----------|---------|-----------|
| Project structure | Feature-first (recommended) vs layer-first | [Section 1](#1-project-structure--layering-critical) |
| API client approach | Typed fetch / React Query / tRPC / OpenAPI codegen | [Section 5](#5-api-client-patterns-medium) |
| Auth strategy | JWT + refresh / session / third-party | [Section 6](#6-authentication--middleware-high) |
| Real-time method | Polling / SSE / WebSocket | [Section 11](#11-real-time-patterns-medium) |
| Error handling | Typed error hierarchy + global handler | [Section 3](#3-error-handling--resilience-high) |

Briefly explain each choice (1 sentence per decision).

### Step 2: Scaffold with Checklist

Use the appropriate checklist below. Ensure ALL checked items are implemented — do not skip any.

### Step 3: Implement Following Patterns

Write code following the patterns in this document. Reference specific sections as you implement each part.

### Step 4: Test & Verify

After implementation, run these checks before claiming completion:

1. **Build check**: Ensure both backend and frontend compile without errors
   ```bash
   # Backend
   cd server && npm run build
   # Frontend
   cd client && npm run build
   ```
2. **Start & smoke test**: Start the server, verify key endpoints return expected responses
   ```bash
   # Start server, then test
   curl http://localhost:3000/health
   curl http://localhost:3000/api/<resource>
   ```
3. **Integration check**: Verify frontend can connect to backend (CORS, API base URL, auth flow)
4. **Real-time check** (if applicable): Open two browser tabs, verify changes sync

If any check fails, fix the issue before proceeding.

### Step 5: Handoff Summary

Provide a brief summary to the user:

- **What was built**: List of implemented features and endpoints
- **How to run**: Exact commands to start backend and frontend
- **What's missing / next steps**: Any deferred items, known limitations, or recommended improvements
- **Key files**: List the most important files the user should know about

---

## Scope

**USE this skill when:**
- Building a full-stack application (backend + frontend)
- Scaffolding a new backend service or API
- Designing service layers and module boundaries
- Implementing database access, caching, or background jobs
- Writing error handling, logging, or configuration management
- Reviewing backend code for architectural issues
- Hardening for production
- Setting up API clients, auth flows, file uploads, or real-time features

**NOT for:**
- Pure frontend/UI concerns (use your frontend framework's docs)
- Pure database schema design without backend context

---

## Quick Start — New Backend Service Checklist

- [ ] Project scaffolded with **feature-first** structure
- [ ] Configuration **centralized**, env vars **validated at startup** (fail fast)
- [ ] **Typed error hierarchy** defined (not generic `Error`)
- [ ] **Global error handler** middleware
- [ ] **Structured JSON logging** with request ID propagation
- [ ] Database: **migrations** set up, **connection pooling** configured
- [ ] **Input validation** on all endpoints (Zod / Pydantic / Go validator)
- [ ] **Authentication middleware** in place
- [ ] **Health check** endpoints (`/health`, `/ready`)
- [ ] **Graceful shutdown** handling (SIGTERM)
- [ ] **CORS** configured (explicit origins, not `*`)
- [ ] **Security headers** (helmet or equivalent)
- [ ] `.env.example` committed (no real secrets)

## Quick Start — Frontend-Backend Integration Checklist

- [ ] **API client** configured (typed fetch wrapper, React Query, tRPC, or OpenAPI generated)
- [ ] **Base URL** from environment variable (not hardcoded)
- [ ] **Auth token** attached to requests automatically (interceptor / middleware)
- [ ] **Error handling** — API errors mapped to user-facing messages
- [ ] **Loading states** handled (skeleton/spinner, not blank screen)
- [ ] **Type safety** across the boundary (shared types, OpenAPI, or tRPC)
- [ ] **CORS** configured with explicit origins (not `*` in production)
- [ ] **Refresh token** flow implemented (httpOnly cookie + transparent retry on 401)

---

## Quick Navigation

| Need to… | Jump to |
|----------|---------|
| Organize project folders | [1. Project Structure](#1-project-structure--layering-critical) |
| Manage config + secrets | [2. Configuration](#2-configuration--environment-critical) |
| Handle errors properly | [3. Error Handling](#3-error-handling--resilience-high) |
| Write database code | [4. Database Access Patterns](#4-database-access-patterns-high) |
| Set up API client from frontend | [5. API Client Patterns](#5-api-client-patterns-medium) |
| Add auth middleware | [6. Auth & Middleware](#6-authentication--middleware-high) |
| Set up logging | [7. Logging & Observability](#7-logging--observability-medium-high) |
| Add background jobs | [8. Background Jobs](#8-background-jobs--async-medium) |
| Implement caching | [9. Caching](#9-caching-patterns-medium) |
| Upload files (presigned URL, multipart) | [10. File Upload Patterns](#10-file-upload-patterns-medium) |
| Add real-time features (SSE, WebSocket) | [11. Real-Time Patterns](#11-real-time-patterns-medium) |
| Handle API errors in frontend UI | [12. Cross-Boundary Error Handling](#12-cross-boundary-error-handling-medium) |
| Harden for production | [13. Production Hardening](#13-production-hardening-medium) |
| Design API endpoints | [API Design](references/api-design.md) |
| Design database schema | [Database Schema](references/db-schema.md) |
| Auth flow (JWT, refresh, Next.js SSR, RBAC) | [references/auth-flow.md](references/auth-flow.md) |
| CORS, env vars, environment management | [references/environment-management.md](references/environment-management.md) |

---

## Core Principles (7 Iron Rules)

```
1. ✅ Organize by FEATURE, not by technical layer
2. ✅ Controllers never contain business logic
3. ✅ Services never import HTTP request/response types
4. ✅ All config from env vars, validated at startup, fail fast
5. ✅ Every error is typed, logged, and returns consistent format
6. ✅ All input validated at the boundary — trust nothing from client
7. ✅ Structured JSON logging with request ID — not console.log
```

---

## 1. Project Structure & Layering (CRITICAL)

### Feature-First Organization

```
✅ Feature-first                    ❌ Layer-first
src/                                src/
  orders/                             controllers/
    order.controller.ts                 order.controller.ts
    order.service.ts                    user.controller.ts
    order.repository.ts               services/
    order.dto.ts                        order.service.ts
    order.test.ts                       user.service.ts
  users/                              repositories/
    user.controller.ts                  ...
    user.service.ts
  shared/
    database/
    middleware/
```

### Three-Layer Architecture

```
Controller (HTTP) → Service (Business Logic) → Repository (Data Access)
```

| Layer | Responsibility | ❌ Never |
|-------|---------------|---------|
| Controller | Parse request, validate, call service, format response | Business logic, DB queries |
| Service | Business rules, orchestration, transaction mgmt | HTTP types (req/res), direct DB |
| Repository | Database queries, external API calls | Business logic, HTTP types |

### Dependency Injection (All Languages)

Inject dependencies via constructor — never `new` collaborators inside, never import concrete implementations:
- **TypeScript**: `constructor(private readonly repo: OrderRepository)` (inject interface)
- **Python**: `def __init__(self, repo: OrderRepository)` (type-hint interface)
- **Go**: struct fields as interfaces + `NewXxxService()` constructor
```

---

## 2. Configuration & Environment (CRITICAL)

**Rules:**
```
✅ All config via environment variables (Twelve-Factor)
✅ Validate required vars at startup — fail fast
✅ Type-cast at config layer, not at usage sites
✅ Commit .env.example with dummy values

❌ Never hardcode secrets, URLs, or credentials
❌ Never commit .env files
❌ Never scatter process.env / os.environ throughout code
```

**Examples:**
- TypeScript: `const config = { port: parseInt(process.env.PORT || '3000'), database: { url: requiredEnv('DATABASE_URL') } }`
- Python: `class Settings(BaseSettings): database_url: str; jwt_secret: str` (fails fast if missing)

---

## 3. Error Handling & Resilience (HIGH)

> **For detailed error handling patterns, see [references/error-handling.md](references/error-handling.md)**

**Typed Error Hierarchy:**
```typescript
class AppError extends Error {
  constructor(message: string, public code: string, public statusCode: number) { super(message); }
}
class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`, 'NOT_FOUND', 404);
  }
}
```

**Global Error Handler:** Catch all errors, return structured response for operational errors, log + generic 500 for programming errors.

**Rules:**
```
✅ Typed, domain-specific error classes
✅ Global error handler catches everything
✅ Operational errors → structured response
✅ Programming errors → log + generic 500
✅ Retry transient failures with exponential backoff

❌ Never catch and ignore errors silently
❌ Never return stack traces to client
❌ Never throw generic Error('something')
```

---

## 4. Database Access Patterns (HIGH)

> **For detailed database patterns, migrations, and schema design, see [references/db-schema.md](references/db-schema.md)**

**Migrations Always:** Prisma `migrate dev/deploy`, Alembic `revision --autogenerate` + `upgrade head`, golang-migrate

**N+1 Prevention:**
```typescript
// ❌ N+1: 1 query + N queries
for (const o of orders) { o.items = await db.item.findMany({ where: { orderId: o.id } }); }
// ✅ Single JOIN query
const orders = await db.order.findMany({ include: { items: true } });
```

**Transactions:** Wrap multi-step writes (create + decrement + payment) in `$transaction`.

**Connection Pooling:** Size = `(CPU cores × 2) + spindle_count` (10-20 default). Set timeout. Use PgBouncer for serverless.

---

## 5. API Client Patterns (MEDIUM)

The "glue layer" between frontend and backend. Choose the approach that fits your team and stack.

> **For detailed implementations and code examples, see [references/api-design.md](references/api-design.md)**

**Decision Matrix:**

| Approach | When | Type Safety | Effort |
|----------|------|-------------|--------|
| Typed fetch wrapper | Simple apps, small teams | Manual types | Low |
| React Query + fetch | React apps, server state | Manual types | Medium |
| tRPC | Same team, TypeScript both sides | Automatic | Low |
| OpenAPI generated | Public API, multi-consumer | Automatic | Medium |
| GraphQL codegen | GraphQL APIs | Automatic | Medium |

---

## 6. Authentication & Middleware (HIGH)

> **Full reference:** [references/auth-flow.md](references/auth-flow.md) — JWT bearer flow, automatic token refresh, Next.js SSR, RBAC pattern.

**Standard Middleware Order:**
```
RequestID → Logging → CORS → RateLimit → BodyParse → Auth → Authz → Validation → Handler → ErrorHandler
```

**JWT Rules:**
```
✅ Short expiry access (15min) + refresh token (server-stored)
✅ Minimal claims: userId, roles
✅ Rotate signing keys periodically

❌ Never store tokens in localStorage (XSS risk)
❌ Never pass tokens in URL query params
```

**RBAC Pattern:**
```typescript
function authorize(...roles: Role[]) {
  return (req, res, next) => {
    if (!req.user) throw new UnauthorizedError();
    if (!roles.some(r => req.user.roles.includes(r))) throw new ForbiddenError();
    next();
  };
}
router.delete('/users/:id', authenticate, authorize('admin'), deleteUser);
```

---

## 7. Logging & Observability (MEDIUM-HIGH)

**Structured JSON Logging:**
```typescript
// ✅ Structured — parseable, filterable, alertable
logger.info('Order created', { orderId: order.id, userId: user.id, total: order.total });
// ❌ Unstructured — useless at scale
console.log(`Order created for user ${user.id}`);
```

**Log Levels:** error (immediate attention), warn (unexpected/handled), info (normal ops/audit), debug (dev only)

**Rules:**
```
✅ Request ID in every log entry (propagated via middleware)
✅ Log at layer boundaries (request in, response out, external call)
❌ Never log passwords, tokens, PII, or secrets
❌ Never use console.log in production
```

---

## 8. Background Jobs & Async (MEDIUM)

**Rules:**
```
✅ All jobs must be IDEMPOTENT (same job running twice = same result)
✅ Failed jobs → retry (max 3) → dead letter queue → alert
✅ Workers run as SEPARATE processes (not threads in API server)

❌ Never put long-running tasks in request handlers
❌ Never assume job runs exactly once
```

**Idempotent Pattern:**
```typescript
async function processPayment(data: { orderId: string }) {
  const order = await orderRepo.findById(data.orderId);
  if (order.paymentStatus === 'completed') return;  // already processed
  await paymentGateway.charge(order);
  await orderRepo.updatePaymentStatus(order.id, 'completed');
}
```

---

## 9. Caching Patterns (MEDIUM)

**Cache-Aside (Lazy Loading):**
```typescript
async function getUser(id: string): Promise<User> {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  const user = await userRepo.findById(id);
  if (!user) throw new NotFoundError('User', id);
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 900);  // 15min TTL
  return user;
}
```

**Rules:**
```
✅ ALWAYS set TTL — never cache without expiry
✅ Invalidate on write (delete cache key after update)
✅ Use cache for reads, never for authoritative state

❌ Never cache without TTL (stale data is worse than slow data)
```

**Suggested TTL:** User profile 5-15min, Product catalog 1-5min, Config 30-60sec, Session = match duration

---

## 10. File Upload Patterns (MEDIUM)

> **For presigned URLs, multipart upload, and chunked resumable uploads, see [references/api-design.md](references/api-design.md)**

**Decision Matrix:**

| Method | File Size | Server Load | Complexity |
|--------|-----------|-------------|------------|
| Presigned URL | Any (recommended > 5MB) | None (direct to storage) | Medium |
| Multipart | < 10MB | High (streams through server) | Low |
| Chunked / Resumable | > 100MB | Medium | High |

---

## 11. Real-Time Patterns (MEDIUM)

> **For SSE, WebSocket, and polling implementations, see [references/real-time-patterns.md](references/real-time-patterns.md)**

**Decision Matrix:**

| Method | Direction | Complexity | When |
|--------|-----------|------------|------|
| Polling | Client → Server | Low | Simple status checks, < 10 clients |
| SSE | Server → Client | Medium | Notifications, feeds, AI streaming |
| WebSocket | Bidirectional | High | Chat, collaboration, gaming |

---

## 12. Cross-Boundary Error Handling (MEDIUM)

> **For error mapping code and integration decision trees, see [references/error-handling.md](references/error-handling.md)**

**Rules:**
```
✅ Map every API error code to a human-readable message
✅ Show field-level validation errors next to form inputs
✅ Auto-retry on 5xx (max 3, with backoff), never on 4xx
✅ Redirect to login on 401 (after refresh attempt fails)
✅ Show "offline" banner when fetch fails with TypeError

❌ Never show raw API error messages to users ("NullPointerException")
❌ Never silently swallow errors (show toast or log)
❌ Never retry 4xx errors (client is wrong, retrying won't help)
```

---

> **Production hardening** (health checks, graceful shutdown, security checklist), **anti-patterns** (18-item table), and **common issues** (where to put business rules, service splitting, test speed) → [references/production-and-antipatterns.md](references/production-and-antipatterns.md)

---

## Reference Documents

This skill includes deep-dive references for specialized topics. Read the relevant reference when you need detailed guidance.

| Need to… | Reference |
|----------|-----------|
| Write backend tests (unit, integration, e2e, contract, performance) | [references/testing-strategy.md](references/testing-strategy.md) |
| Validate a release before deployment (6-gate checklist) | [references/release-checklist.md](references/release-checklist.md) |
| Choose a tech stack (language, framework, database, infra) | [references/technology-selection.md](references/technology-selection.md) |
| Build with Django / DRF (models, views, serializers, admin) | [references/django-best-practices.md](references/django-best-practices.md) |
| Design REST/GraphQL/gRPC endpoints (URLs, status codes, pagination) | [references/api-design.md](references/api-design.md) |
| Design database schema, indexes, migrations, multi-tenancy | [references/db-schema.md](references/db-schema.md) |
| Auth flow (JWT bearer, token refresh, Next.js SSR, RBAC, middleware order) | [references/auth-flow.md](references/auth-flow.md) |
| CORS config, env vars per environment, common CORS issues | [references/environment-management.md](references/environment-management.md) |
