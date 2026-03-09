"""
Smart Site Analyzer - 使用 ScrapeGraphAI + LLM 智能分析小说网站结构
用法:
  python smart_analyzer.py toc <URL>       # 分析目录页结构（选择器+示例章节）
  python smart_analyzer.py chapter <URL>   # 分析章节页，识别正文结构
  python smart_analyzer.py script <URL>    # 生成基础爬虫脚本

环境变量:
  SCRAPEGRAPH_API_KEY   - LLM API 密钥 (必需)
  SCRAPEGRAPH_BASE_URL  - OpenAI 兼容端点 (默认: https://open.bigmodel.cn/api/paas/v4/)
  SCRAPEGRAPH_MODEL     - 模型名称 (默认: GLM-4.7)
"""

import sys
import os
import json


def get_config():
    api_key = os.environ.get("SCRAPEGRAPH_API_KEY", "")
    if not api_key:
        print("错误: 请设置 SCRAPEGRAPH_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)
    base_url = os.environ.get("SCRAPEGRAPH_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/")
    model = os.environ.get("SCRAPEGRAPH_MODEL", "GLM-4.7")
    return {
        "llm": {
            "api_key": api_key,
            "model": f"openai/{model}",
            "base_url": base_url,
        },
        "verbose": False,
        "headless": True,
    }


def analyze_toc(url):
    """分析目录页结构：识别选择器模式，提取示例章节"""
    from scrapegraphai.graphs import SmartScraperGraph

    prompt = (
        "分析这个网络小说目录页面的HTML结构，返回以下信息：\n"
        "1. title: 小说标题\n"
        "2. author: 作者名\n"
        "3. description: 简介（前200字）\n"
        "4. selectors: {\n"
        "     chapter_list_container: 包含章节列表的容器CSS选择器,\n"
        "     chapter_link: 章节链接的CSS选择器（如 'div.index_box a'),\n"
        "     chapter_title_in_link: 链接内标题文本的提取方式\n"
        "   }\n"
        "5. sample_chapters: 前5个章节的 {title, url}（URL必须是完整绝对URL）\n"
        "6. url_pattern: 章节URL的规律（如 /n9669bk/1/ 到 /n9669bk/N/）\n"
        "7. site_info: {\n"
        "     language: 页面语言(zh/ja/en/ko),\n"
        "     has_pagination: 目录是否分页,\n"
        "     total_chapters_approx: 大约总章节数,\n"
        "     anti_scraping: 检测到的反爬措施\n"
        "   }"
    )

    graph = SmartScraperGraph(prompt=prompt, source=url, config=get_config())
    return graph.run()


def analyze_chapter(url):
    """分析章节页，识别正文结构和选择器"""
    from scrapegraphai.graphs import SmartScraperGraph

    prompt = (
        "分析这个网络小说章节页面的HTML结构，返回以下信息：\n"
        "1. chapter_title: 本章标题\n"
        "2. content_preview: 正文前200字\n"
        "3. selectors: {\n"
        "     content: 正文区域的CSS选择器（要精确，能唯一定位正文）,\n"
        "     title: 章节标题的CSS选择器,\n"
        "     next_chapter: 下一章链接的CSS选择器,\n"
        "     prev_chapter: 上一章链接的CSS选择器\n"
        "   }\n"
        "4. page_structure: {\n"
        "     has_pagination: 本章是否分页(true/false),\n"
        "     content_loaded_by: 正文加载方式(static_html/ajax/javascript),\n"
        "     encoding: 页面编码\n"
        "   }\n"
        "5. anti_scraping: 检测到的反爬措施（WAF、验证码、登录要求等）\n"
        "6. recommended_method: 推荐的抓取方式(requests/playwright/drissionpage/curl)"
    )

    graph = SmartScraperGraph(prompt=prompt, source=url, config=get_config())
    return graph.run()


def generate_script(url):
    """基于分析结果生成基础爬虫脚本"""
    from scrapegraphai.graphs import ScriptCreatorGraph

    prompt = (
        "这是一个网络小说网站。请生成一个Python爬虫脚本，功能包括：\n"
        "1. 从目录页提取所有章节链接\n"
        "2. 逐章下载正文内容\n"
        "3. 合并所有章节为一个txt文件\n"
        "4. 文件名使用小说标题\n"
        "要求：\n"
        "- 使用 requests + BeautifulSoup\n"
        "- 每章下载间隔1秒（time.sleep(1)）\n"
        "- 使用 UTF-8 编码保存\n"
        "- 包含进度显示\n"
        "- 包含基本错误处理和重试逻辑"
    )

    config = get_config()
    config["library"] = "beautifulsoup"
    graph = ScriptCreatorGraph(prompt=prompt, source=url, config=config)
    return graph.run()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    mode = sys.argv[1]
    url = sys.argv[2]

    handlers = {
        "toc": analyze_toc,
        "chapter": analyze_chapter,
        "script": generate_script,
    }

    if mode not in handlers:
        print(f"未知模式: {mode}，可选: toc, chapter, script", file=sys.stderr)
        sys.exit(1)

    print(f"正在分析: {url} (模式: {mode})", file=sys.stderr)
    result = handlers[mode](url)

    if mode == "script":
        print(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
