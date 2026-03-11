# Syosetu (syosetu.com / 小説家になろう)

## 网站特点
- 类型：静态内容
- 反爬：无特殊限制，但需控制请求频率
- URL格式：`https://ncode.syosetu.com/{ncode}/` (目录) `/{ncode}/{chapter}/` (章节)

## 选择器

| 元素 | 选择器 |
|------|--------|
| 小说标题 | `.novel_title` |
| 作者 | `.novel_writername a` |
| 章节列表 | `.index_box a` |
| 正文 | `#novel_honbun` |
| 前言 | `#novel_p` |
| 后记 | `#novel_a` |

## 示例代码

```python
BASE_URL = "https://ncode.syosetu.com"

def get_chapter_list():
    resp = requests.get(NOVEL_URL, headers=HEADERS)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    title = soup.select_one('.novel_title').get_text(strip=True)
    author = soup.select_one('.novel_writername a').get_text(strip=True)

    chapters = []
    for link in soup.select('.index_box a'):
        href = link.get('href', '')
        chapters.append({
            'url': BASE_URL + href,
            'title': link.get_text(strip=True)
        })
    return title, author, chapters

def get_chapter_content(url):
    resp = requests.get(url, headers=HEADERS)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    parts = []
    # 前言
    preface = soup.select_one('#novel_p')
    if preface:
        parts.append(preface.get_text('\n', strip=True))

    # 正文
    body = soup.select_one('#novel_honbun')
    if body:
        parts.append(body.get_text('\n', strip=True))

    # 后记
    afterword = soup.select_one('#novel_a')
    if afterword:
        parts.append(afterword.get_text('\n', strip=True))

    return '\n\n'.join(parts)
```

## 注意事项
- 建议延迟1-2秒/章
- 短篇小说URL格式不同：`https://ncode.syosetu.com/{ncode}/`（无章节）
