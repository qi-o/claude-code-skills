---
name: fullstack-dev
description: Full-stack backend architecture and frontend-backend integration. REST API design, auth flows (JWT, session, OAuth), real-time features (SSE, WebSocket), database integration (SQL/NoSQL), production hardening. Trigger when user mentions backend, fullstack, REST API, database design, or real-time features.
type: skill
github_url: https://github.com/MiniMax-AI/skills
github_hash: b4c7c3fcd4d8c1f6e2a3d7b9c5e1f4a8d2b7c3e9
version: 1.0.0
---

# Full-Stack Development

End-to-end backend architecture and frontend-backend integration. Follow the mandatory 5-step workflow.

## Mandatory 5-Step Workflow

### Step 0: Gather Requirements
Clarify (or infer):
1. **Stack**: Language/framework (Express+React, Django+Vue, Go+HTMX)
2. **Service type**: API-only, full-stack monolith, or microservice?
3. **Database**: SQL (PostgreSQL, SQLite, MySQL) or NoSQL (MongoDB, Redis)?
4. **Integration**: REST, GraphQL, tRPC, or gRPC?
5. **Real-time**: SSE, WebSocket, or polling?
6. **Auth**: JWT, session, OAuth, or third-party (Clerk, Auth.js)?

### Step 1: Architectural Decisions
State decisions before coding: project structure, API client approach, auth strategy, real-time method, error handling approach.

### Step 2: Scaffold with Checklist
Use the appropriate checklist below. ALL items must be implemented.

### Step 3: Implement Following Patterns
Write code referencing specific sections of this skill.

### Step 4: Test & Verify
- Build check (both backend and frontend compile)
- Start & smoke test (verify key endpoints)
- Integration check (frontend-backend connection)
- Real-time check (if applicable)

### Step 5: Handoff Summary
- What was built, how to run, what's missing, key files

## 7 Iron Rules

```
1. Organize by FEATURE, not by technical layer
2. Controllers never contain business logic
3. Services never import HTTP request/response types
4. All config from env vars, validated at startup, fail fast
5. Every error is typed, logged, and returns consistent format
6. All input validated at the boundary -- trust nothing from client
7. Structured JSON logging with request ID -- not console.log
```

## Three-Layer Architecture

```
Controller (HTTP) -> Service (Business Logic) -> Repository (Data Access)
```

| Layer | Responsibility | Never |
|-------|---------------|-------|
| Controller | Parse request, validate, call service, format response | Business logic, DB queries |
| Service | Business rules, orchestration, transaction management | HTTP types (req/res), direct DB |
| Repository | Database queries, external API calls | Business logic, HTTP types |

## Error Handling Patterns

### TypeScript

```typescript
class AppError extends Error {
    constructor(
        public readonly message: string,
        public readonly code: string,
        public readonly statusCode: number,
        public readonly isOperational: boolean = true,
    ) { super(message); }
}
class NotFoundError extends AppError {
    constructor(resource: string, id: string) {
        super(`${resource} not found: ${id}`, 'NOT_FOUND', 404);
    }
}
class ValidationError extends AppError {
    constructor(public readonly errors: FieldError[]) {
        super('Validation failed', 'VALIDATION_ERROR', 422);
    }
}
```

### Global Error Handler (Express)

```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
    if (err instanceof AppError && err.isOperational) {
        return res.status(err.statusCode).json({
            title: err.code,
            status: err.statusCode,
            detail: err.message,
            request_id: req.id,
        });
    }
    logger.error('Unexpected error', { error: err.message, stack: err.stack, request_id: req.id });
    res.status(500).json({ title: 'Internal Error', status: 500, request_id: req.id });
});
```

## Real-Time Patterns

### SSE (Server-Sent Events)
One-way server->client. Best for notifications, live feeds, streaming AI responses.

```typescript
app.get('/stream', (req, res) => {
    res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    });
    // Send events with res.write('data: ...\n\n');
});
```

### WebSocket
Bidirectional. Best for chat, collaborative editing, gaming.

### When to Choose

| Scenario | Recommendation |
|----------|---------------|
| Notifications | SSE |
| Live AI streaming | SSE |
| Chat | WebSocket |
| Collaborative editing | WebSocket |
| Simple status polling | Polling |

## Auth Patterns

### JWT with Refresh Tokens

```typescript
// Access token: short expiry (15min), minimal claims
const accessToken = jwt.sign(
    { userId, roles },
    JWT_SECRET,
    { expiresIn: '15m' }
);

// Refresh token: server-stored, httpOnly cookie
const refreshToken = crypto.randomBytes(64).toString('hex');
await refreshTokenStore.set(userId, refreshToken, EXPIRY_7_DAYS);
```

### NEVER
- Store tokens in localStorage (XSS risk)
- Put sensitive data in JWT payload (it's base64, not encrypted)
- Use `console.log` for auth events

## Validation

Use Zod (TypeScript) or Pydantic (Python) at the boundary:

```typescript
import { z } from 'zod';
const CreateUserSchema = z.object({
    email: z.string().email(),
    password: z.string().min(8),
    role: z.enum(['user', 'admin']).default('user'),
});
type CreateUserInput = z.infer<typeof CreateUserSchema>;
```

## Configuration

```typescript
// config.ts
import { z } from 'zod';
const configSchema = z.object({
    PORT: z.number().default(3000),
    DATABASE_URL: z.string().url(),
    JWT_SECRET: z.string().min(32),
    NODE_ENV: z.enum(['development', 'production']).default('development'),
});
export const config = configSchema.parse(process.env);
```
