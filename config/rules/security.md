# Security Rules

## Mandatory Checks Before Commit

- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] User input is validated
- [ ] SQL queries use parameterized statements
- [ ] HTML output is sanitized (XSS prevention)
- [ ] CSRF protection is enabled
- [ ] Authentication/authorization verified
- [ ] Rate limiting on endpoints
- [ ] Error messages don't expose sensitive data

## Secret Management

❌ Wrong:
```javascript
const apiKey = "sk-proj-xxxxx"
```

✅ Correct:
```javascript
const apiKey = process.env.OPENAI_API_KEY
if (!apiKey) throw new Error("OPENAI_API_KEY not configured")
```

## Security Response Protocol

When security issue discovered:
1. STOP work immediately
2. Use security-reviewer agent
3. Fix critical issues before proceeding
4. Rotate any compromised secrets
5. Review codebase for similar vulnerabilities
