# Syosetu (syosetu.com / 灏忚瀹躲伀銇倣銇?

## 缃戠珯鐗圭偣
- 绫诲瀷锛氶潤鎬佸唴瀹?- 鍙嶇埇锛氭棤鐗规畩闄愬埗锛屼絾闇€鎺у埗璇锋眰棰戠巼
- URL鏍煎紡锛歚https://ncode.syosetu.com/{ncode}/` (鐩綍) `/{ncode}/{chapter}/` (绔犺妭)

## 閫夋嫨鍣?
| 鍏冪礌 | 閫夋嫨鍣?|
|------|--------|
| 灏忚鏍囬 | `.novel_title` |
| 浣滆€?| `.novel_writername a` |
| 绔犺妭鍒楄〃 | `.index_box a` |
| 姝ｆ枃 | `#novel_honbun` |
| 鍓嶈█ | `#novel_p` |
| 鍚庤 | `#novel_a` |

## 绀轰緥浠ｇ爜

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
    # 鍓嶈█
    preface = soup.select_one('#novel_p')
    if preface:
        parts.append(preface.get_text('\n', strip=True))

    # 姝ｆ枃
    body = soup.select_one('#novel_honbun')
    if body:
        parts.append(body.get_text('\n', strip=True))

    # 鍚庤
    afterword = soup.select_one('#novel_a')
    if afterword:
        parts.append(afterword.get_text('\n', strip=True))

    return '\n\n'.join(parts)
```

## 娉ㄦ剰浜嬮」
- 寤鸿寤惰繜1-2绉?绔?- 鐭瘒灏忚URL鏍煎紡涓嶅悓锛歚https://ncode.syosetu.com/{ncode}/`锛堟棤绔犺妭锛?