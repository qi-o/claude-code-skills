# GitLab API Quick Reference

Quick reference for GitLab REST API v4 endpoints used by repo2skill.

## Base URL

```
https://gitlab.com/api/v4
```

## Common Endpoints

### Repository Metadata

```bash
GET /projects/{id}
```

**Note:** `{id}` must be URL-encoded as `{owner}%2F{repo}`

**Response fields:**
- `name`: Project name
- `description`: Project description
- `star_count`: Star count
- `forks_count`: Fork count
- `default_branch`: Default branch
- `web_url`: Project URL
- `created_at`: Creation timestamp
- `last_activity_at`: Last activity timestamp

**Example:**
```bash
curl "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab"
```

### README Content

```bash
GET /projects/{id}/repository/files/README.md/raw?ref={branch}
```

**Note:** Returns raw content (not base64-encoded)

**Example:**
```bash
curl "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/repository/files/README.md/raw?ref=main"
```

### File Tree

```bash
GET /projects/{id}/repository/tree?recursive=1
```

**Response fields:**
- Array of file objects with:
  - `id`: SHA
  - `name`: Filename
  - `type`: "tree" (directory) or "blob" (file)
  - `path`: File path
  - `mode`: File mode

**Example:**
```bash
curl "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/repository/tree?recursive=1&per_page=100"
```

### File Content

```bash
GET /projects/{id}/repository/files/{file_path}/raw?ref={branch}
```

**Note:** File path must be URL-encoded (slashes become %2F)

**Example:**
```bash
curl "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/repository/files/package.json/raw?ref=main"
```

### Branch List

```bash
GET /projects/{id}/repository/branches
```

**Example:**
```bash
curl "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/repository/branches"
```

## Authentication

Optional via Personal Access Token:

```bash
curl --header "PRIVATE-TOKEN: your_token" \
  "https://gitlab.com/api/v4/projects/user%2Frepo"
```

Or via environment:
```bash
export GITLAB_TOKEN=your_token
curl --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/user%2Frepo"
```

## Rate Limits

**Unauthenticated:**
- Approximately 60 requests per minute (varies)

**Authenticated:**
- Higher limits (varies by plan)

**Check headers:**
- `RateLimit-Remaining`
- `RateLimit-Reset`

## Pagination

GitLab uses Link header for pagination:

```bash
curl -I "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab/repository/tree?per_page=100"
```

**Response headers:**
- `X-Total`: Total items
- `X-Total-Pages`: Total pages
- `X-Per-Page`: Items per page
- `X-Page`: Current page

## Raw Content URLs

For direct file access:

```
https://gitlab.com/{owner}/{repo}/-/raw/{branch}/{path}
```

**Example:**
```
https://gitlab.com/gitlab-org/gitlab/-/raw/main/README.md
```

## Mirror Endpoints

Alternative API endpoint:

1. `https://gl.gitmirror.com/api/v4`

## URL Encoding

Project paths with slashes must be URL-encoded:

```
owner/repo 鈫?owner%2Frepo
group/subgroup/project 鈫?group%2Fsubgroup%2Fproject
```

## Common HTTP Status Codes

- `200 OK`: Success
- `404 Not Found`: Resource doesn't exist
- `403 Forbidden`: Insufficient permissions
- `429 Too Many Requests`: Rate limit exceeded

## Error Response Format

```json
{
  "message": "404 Project Not Found",
  "documentation_url": "https://docs.gitlab.com/ee/api/"
}
```
