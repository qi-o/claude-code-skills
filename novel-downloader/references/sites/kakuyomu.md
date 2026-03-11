# Kakuyomu (kakuyomu.jp)

## 网站特点
- 类型：静态内容
- 反爬：无特殊限制
- URL格式：`https://kakuyomu.jp/works/{work_id}` (目录)

## 选择器

| 元素 | 选择器 |
|------|--------|
| 小说标题 | `#workTitle a` |
| 作者 | `#workAuthor-activityName a` |
| 章节列表 | `.widget-toc-episode a` |
| 正文 | `.widget-episodeBody` |

## 示例代码

```python
BASE_URL = "https://kakuyomu.jp"

def get_chapter_list():
    resp = requests.get(NOVEL_URL, headers=HEADERS)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    title = soup.select_one('#workTitle a').get_text(strip=True)
    author = soup.select_one('#workAuthor-activityName a').get_text(strip=True)

    chapters = []
    for link in soup.select('.widget-toc-episode a'):
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

    body = soup.select_one('.widget-episodeBody')
    if body:
        # 处理ruby标签（日语注音）
        for ruby in body.find_all('ruby'):
            # 保留汉字，移除注音
            rb = ruby.find('rb')
            if rb:
                ruby.replace_with(rb.get_text())

        # 处理换行
        for br in body.find_all('br'):
            br.replace_with('\n')

        return body.get_text().strip()
    return ""
```

## Ruby标签处理
Kakuyomu使用ruby标签为汉字添加假名注音：
```html
<ruby><rb>異世界</rb><rp>(</rp><rt>いせかい</rt><rp>)</rp></ruby>
```

可选择：
1. 只保留汉字（上述代码）
2. 保留注音：`f"{rb.text}({rt.text})"`
