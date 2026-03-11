# Syosetu R18 (novel18.syosetu.com)

## 网站特点
- 类型：静态内容
- 年龄验证：需要设置 `over18=yes` cookie
- 与普通syosetu.com选择器不同

## 关键配置

```python
# 设置年龄验证cookie
session.cookies.set('over18', 'yes', domain='.syosetu.com')
```

## 选择器

| 元素 | 选择器 |
|------|--------|
| 小说标题 | `.novel_title, .p-novel__title` |
| 作者 | `.novel_writername a, .p-novel__author a` |
| 章节列表 | `.index_box a, .p-eplist__sublist a` |
| 正文 | `.p-novel__body` (R18站) 或 `#novel_honbun` (普通站) |
| 前言 | `#novel_p` |
| 后记 | `#novel_a` |

## 注意事项

1. **R18站使用不同选择器**：`.p-novel__body` 而非 `#novel_honbun`
2. **需要年龄验证cookie**：否则会重定向到验证页面
3. 建议延迟1秒/章

## 脚本

使用 `scripts/syosetu_r18.py`
