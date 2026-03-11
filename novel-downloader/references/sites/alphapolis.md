# Alphapolis (alphapolis.co.jp)

## 2025年1月更新：AWS WAF保护

**重要变更**：Alphapolis现已启用AWS WAF保护，直接使用requests会返回202状态码。

### 解决方案：使用Playwright

```bash
pip install playwright beautifulsoup4
playwright install chromium
```

使用 `scripts/alphapolis.py` 脚本，该脚本使用Playwright浏览器自动化绕过WAF。

## 网站特点
- 类型：AJAX动态加载 + AWS WAF保护
- 反爬机制：WAF + CSRF Token + Session检测
- 正文选择器：`#novelBody`

## 旧版方案（无WAF时可用）

如果WAF未触发，可使用requests方案：
- 关键：每章使用独立session
- API：`POST /novel/episode_body`
- 需要：X-XSRF-TOKEN头

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 202状态码 | AWS WAF | 使用Playwright |
| 419 | XSRF-TOKEN缺失 | 添加X-XSRF-TOKEN头 |
| 前N章空 | 共用session | 每章新建session |
| token找不到 | 先访问了目录页 | 直接访问章节页 |
