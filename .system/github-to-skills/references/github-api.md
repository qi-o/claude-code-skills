# GitHub API Quick Reference

Quick reference for GitHub REST API v3 endpoints used by repo2skill.

## Base URL

```
https://api.github.com
```

## Common Endpoints

### Repository Metadata

```bash
GET /repos/{owner}/{repo}
```

**Response fields:**
- `name`: Repository name
- `description`: Repository description
- `stargazers_count`: Star count
- `forks_count`: Fork count
- `language`: Primary language
- `default_branch`: Default branch (main/master)
- `homepage`: Homepage URL
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

**Example:**
```bash
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/vercel/next.js
```

### README Content

```bash
GET /repos/{owner}/{repo}/readme
```

**Response fields:**
- `content`: Base64-encoded content
- `encoding`: Always "base64"
- `name`: Filename (README.md)
- `path`: Path to file
- `sha`: Blob SHA

**Example:**
```bash
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/vercel/next.js/readme
```

### File Tree

```bash
GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1
```

**Response fields:**
- `tree`: Array of file objects
- `sha`: Tree SHA
- `truncated`: True if response was truncated

**Example:**
```bash
curl -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/vercel/next.js/git/trees/main?recursive=1"
```

### File Content

```bash
GET /repos/{owner}/{repo}/contents/{path}
```

**Response fields:**
- `content`: Base64-encoded content
- `encoding`: "base64" or "none"
- `name`: Filename
- `path`: File path
- `sha`: Blob SHA
- `size`: File size in bytes

**Example:**
```bash
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/vercel/next.js/contents/package.json
```

## Authentication

Optional but recommended for higher rate limits.

```bash
curl -H "Authorization: token YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/owner/repo
```

Or via environment:
```bash
export GITHUB_TOKEN=your_token
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo
```

## Rate Limits

**Unauthenticated:**
- 60 requests per hour
- Check headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

**Authenticated:**
- 5,000 requests per hour
- Same headers apply

**Check rate limit:**
```bash
curl -I https://api.github.com/repos/vercel/next.js
```

## Raw Content URLs

For direct file access (bypassing API):

```
https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}
```

**Example:**
```
https://raw.githubusercontent.com/vercel/next.js/main/README.md
```

## Mirror Endpoints

Alternative API endpoints (for rate limit issues):

1. `https://gh.api.888888888.xyz`
2. `https://gh-proxy.com/api/github`
3. `https://api.fastgit.org`
4. `https://api.kgithub.com`
5. `https://githubapi.muicss.com`
6. `https://github.91chi.fun`
7. `https://mirror.ghproxy.com`

**Raw mirrors:**
1. `https://raw.fastgit.org`
2. `https://raw.kgithub.com`

## Common HTTP Status Codes

- `200 OK`: Success
- `404 Not Found`: Resource doesn't exist
- `403 Forbidden`: Rate limit exceeded or private repo
- `429 Too Many Requests`: Rate limit exceeded

## Error Response Format

```json
{
  "message": "Not Found",
  "documentation_url": "https://docs.github.com/rest"
}
```
