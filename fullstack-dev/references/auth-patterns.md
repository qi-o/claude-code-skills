# Auth Patterns

## JWT Strategy

1. Access token: 15min expiry, contains userId + roles
2. Refresh token: 7-day expiry, stored server-side (Redis/DB), httpOnly cookie
3. Auto-refresh: middleware intercepts 401, refreshes, retries

## OAuth Flow

1. Redirect to provider (Google/GitHub/etc.)
2. Receive callback with code
3. Exchange code for tokens
4. Create or find user in DB
5. Issue our own JWT

## Session Strategy

For stateful auth: express-session with Redis store. Best when you need server-side session data.

## Password Hashing

Always use bcrypt (cost factor 12) or Argon2id. Never hash with plain crypto.
