# Purple Novel (purple-novel.com)

## 网站特点
- 类型：WordPress站点
- 结构：分页形式，每页一章
- 正文选择器：`article`

## URL格式
- 目录/第一页：`https://purple-novel.com/{slug}/`
- 后续页：`https://purple-novel.com/{slug}/{page}/`

## 选择器

| 元素 | 选择器 |
|------|--------|
| 标题 | `h1.entry-title, h1` |
| 正文 | `article` |

## 注意事项

1. **分页形式**：需要从页面链接中提取最大页数
2. **移除干扰元素**：`script, style, .sharedaddy, .jp-relatedposts, nav, .post-navigation`
3. 作者信息可能需要从标题中提取

## 脚本

使用 `scripts/purple_novel.py`，需要修改 `NOVEL_SLUG` 变量
