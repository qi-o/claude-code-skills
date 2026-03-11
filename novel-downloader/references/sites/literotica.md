# Literotica (literotica.com)

## 网站特点
- 类型：SPA应用，服务端渲染
- 反爬机制：HTTP/2协议问题导致requests/playwright失败
- 正文选择器：`div[class*="_article__content"]`
- 分页：章节内分页，URL格式 `?page=N`

## 解决方案：使用curl

由于HTTP/2协议问题，需要使用curl获取页面：

```python
import subprocess

def fetch_url(url):
    result = subprocess.run([
        'curl', '-s', '-L',
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        '-H', 'Accept: text/html,application/xhtml+xml',
        url
    ], capture_output=True, text=True, timeout=60)
    return result.stdout
```

## URL格式
- 系列页：`https://www.literotica.com/series/se/{slug}`
- 章节页：`https://www.literotica.com/s/{slug}-ch-{num}`
- 分页：`https://www.literotica.com/s/{slug}-ch-{num}?page={page}`

## 选择器

| 元素 | 选择器 |
|------|--------|
| 正文 | `div[class*="_article__content"]` |
| 作者 | `a[href*="/authors/"]` |
| 下一页 | `a[href*="?page=N"]` |

## 注意事项

1. **HTTP/2问题**：requests和playwright都会遇到协议错误，必须使用curl
2. **章节内分页**：每章可能有多页，需要循环获取
3. **分页检测**：通过查找下一页链接判断是否有更多页
4. 建议延迟1秒/章，0.5秒/页

## 脚本

使用 `scripts/literotica.py`，需要修改 `SERIES_URL` 和 `OUTPUT_FILE` 变量
