# Error Handling Patterns

## Error Hierarchy

Base class that all errors extend. Each error has: `message`, `code`, `statusCode`, `isOperational`.

## Logging

Always use structured JSON logging with request ID:

```typescript
logger.info('User created', { requestId: req.id, userId: result.id, email: result.email });
logger.error('Database connection failed', { requestId: req.id, error: err.message, stack: err.stack });
```

Never use `console.log` in production code.

## Error Response Format

```json
{
    "title": "VALIDATION_ERROR",
    "status": 422,
    "detail": "Validation failed",
    "request_id": "abc-123-def",
    "errors": [
        { "field": "email", "message": "Invalid email format" }
    ]
}
```
