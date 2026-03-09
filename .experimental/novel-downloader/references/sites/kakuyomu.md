# Kakuyomu (kakuyomu.jp)

## 缃戠珯鐗圭偣
- 绫诲瀷锛氶潤鎬佸唴瀹?- 鍙嶇埇锛氭棤鐗规畩闄愬埗
- URL鏍煎紡锛歚https://kakuyomu.jp/works/{work_id}` (鐩綍)

## 閫夋嫨鍣?
| 鍏冪礌 | 閫夋嫨鍣?|
|------|--------|
| 灏忚鏍囬 | `#workTitle a` |
| 浣滆€?| `#workAuthor-activityName a` |
| 绔犺妭鍒楄〃 | `.widget-toc-episode a` |
| 姝ｆ枃 | `.widget-episodeBody` |

## 绀轰緥浠ｇ爜

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
        # 澶勭悊ruby鏍囩锛堟棩璇敞闊筹級
        for ruby in body.find_all('ruby'):
            # 淇濈暀姹夊瓧锛岀Щ闄ゆ敞闊?            rb = ruby.find('rb')
            if rb:
                ruby.replace_with(rb.get_text())

        # 澶勭悊鎹㈣
        for br in body.find_all('br'):
            br.replace_with('\n')

        return body.get_text().strip()
    return ""
```

## Ruby鏍囩澶勭悊
Kakuyomu浣跨敤ruby鏍囩涓烘眽瀛楁坊鍔犲亣鍚嶆敞闊筹細
```html
<ruby><rb>鐣颁笘鐣?/rb><rp>(</rp><rt>銇勩仜銇嬨亜</rt><rp>)</rp></ruby>
```

鍙€夋嫨锛?1. 鍙繚鐣欐眽瀛楋紙涓婅堪浠ｇ爜锛?2. 淇濈暀娉ㄩ煶锛歚f"{rb.text}({rt.text})"`
