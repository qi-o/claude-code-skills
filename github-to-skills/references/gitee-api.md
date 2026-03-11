# Gitee API Quick Reference

Quick reference for Gitee REST API v5 endpoints used by repo2skill.

## Base URL

```
https://gitee.com/api/v5
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
- `default_branch`: Default branch (usually master)
- `homepage`: Homepage URL
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

**Example:**
```bash
curl https://gitee.com/api/v5/repos/mindspore/docs
```

### README Content

```bash
GET /repos/{owner}/{repo}/contents/{path}?ref={branch}
```

**Response fields:**
- `content`: Base64-encoded content
- `encoding`: "base64"
- `name`: Filename
- `path`: File path
- `sha`: Blob SHA

**Example:**
```bash
curl "https://gitee.com/api/v5/repos/mindspore/docs/contents/README.md?ref=master"
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
curl "https://gitee.com/api/v5/repos/mindspore/docs/git/trees/master?recursive=1"
```

### Branch List

```bash
GET /repos/{owner}/{repo}/branches
```

**Example:**
```bash
curl https://gitee.com/api/v5/repos/mindspore/docs/branches
```

## Authentication

Optional via Access Token:

```bash
curl -H "Authorization: token your_token" \
  https://gitee.com/api/v5/repos/user/repo
```

Or via query parameter:
```bash
curl "https://gitee.com/api/v5/repos/user/repo?access_token=your_token"
```

## Rate Limits

**Authenticated:**
- Approximately 5,000 requests per hour

**Unauthenticated:**
- Approximately 100 requests per hour (varies)

## Raw Content URLs

For direct file access:

```
https://gitee.com/{owner}/{repo}/raw/{branch}/{path}
```

**Example:**
```
https://gitee.com/mindspore/docs/raw/master/README.md
```

## Differences from GitHub

1. **Default branch**: Gitee often uses `master` instead of `main`
2. **API version**: Gitee uses v5 (GitHub uses v3)
3. **Rate limits**: Generally more generous for authenticated users
4. **Content encoding**: Similar to GitHub (base64 for API)

## Common HTTP Status Codes

- `200 OK`: Success
- `404 Not Found`: Resource doesn't exist
- `403 Forbidden`: Private repo or rate limit
- `429 Too Many Requests`: Rate limit exceeded

## Error Response Format

```json
{
  "message": "Not Found",
  "documentation_url": "https://gitee.com/api/v5/"
}
```
