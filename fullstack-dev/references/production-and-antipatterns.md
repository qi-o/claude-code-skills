# Production Hardening, Anti-Patterns & Common Issues

## Production Hardening

**Health Checks:**
```typescript
app.get('/health', (req, res) => res.json({ status: 'ok' }));  // liveness
app.get('/ready', async (req, res) => {  // readiness
  const checks = { database: await checkDb(), redis: await checkRedis() };
  const ok = Object.values(checks).every(c => c.status === 'ok');
  res.status(ok ? 200 : 503).json({ status: ok ? 'ok' : 'degraded', checks });
});
```

**Graceful Shutdown:**
```typescript
process.on('SIGTERM', async () => {
  server.close();
  await drainConnections();
  await closeDatabase();
  process.exit(0);
});
```

**Security Checklist:**
```
✅ CORS: explicit origins (never '*' in production)
✅ Security headers (helmet / equivalent)
✅ Rate limiting on public endpoints
✅ Input validation on ALL endpoints (trust nothing)
✅ HTTPS enforced
❌ Never expose internal errors to clients
```

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---------|--------------|
| Business logic in routes/controllers | Move to service layer |
| `process.env` scattered everywhere | Centralized typed config |
| `console.log` for logging | Structured JSON logger |
| Generic `Error('oops')` | Typed error hierarchy |
| Direct DB calls in controllers | Repository pattern |
| No input validation | Validate at boundary (Zod/Pydantic) |
| Catching errors silently | Log + rethrow or return error |
| No health check endpoints | `/health` + `/ready` |
| Hardcoded config/secrets | Environment variables |
| No graceful shutdown | Handle SIGTERM properly |
| Hardcode API URL in frontend | Environment variable (`NEXT_PUBLIC_API_URL`) |
| Store JWT in localStorage | Memory + httpOnly refresh cookie |
| Show raw API errors to users | Map to human-readable messages |
| Retry 4xx errors | Only retry 5xx (server failures) |
| Skip loading states | Skeleton/spinner while fetching |
| Upload large files through API server | Presigned URL → direct to S3 |
| Poll for real-time data | SSE or WebSocket |
| Duplicate types frontend + backend | Shared types, tRPC, or OpenAPI codegen |

## Common Issues

**Issue 1: "Where does this business rule go?"**
- HTTP (request parsing, status codes) → controller
- Business decisions (pricing, permissions) → service
- Database → repository

**Issue 2: "Service is getting too big"** (>500 lines, 20+ methods)
- Split by sub-domain: `OrderService` → `OrderCreationService` + `OrderFulfillmentService` + `OrderQueryService`

**Issue 3: "Tests are slow because they hit the database"**
- Unit tests: mock repository layer
- Integration tests: test containers or transaction rollback
- Never mock service layer in integration tests
