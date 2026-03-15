# CrewAI 代码示例参考

## 目录

1. [Agent 完整属性](#agent-完整属性)
2. [Task 完整属性](#task-完整属性)
3. [Crew 过程类型](#crew-过程类型)
4. [Flow 模式](#flow-模式)
5. [工具：内置与自定义](#工具内置与自定义)
6. [记忆配置](#记忆配置)
7. [知识 RAG 集成](#知识-rag-集成)
8. [结构化输出 Pydantic](#结构化输出-pydantic)
9. [训练与人工干预](#训练与人工干预)
10. [测试模式](#测试模式)
11. [自定义 LLM](#自定义-llm)
12. [异步执行](#异步执行)
13. [回调与事件](#回调与事件)
14. [企业部署配置](#企业部署配置)
15. [YAML 配置](#yaml-配置)
16. [常见模式](#常见模式)

---

## Agent 完整属性

```python
from crewai import Agent

researcher = Agent(
    role='高级研究分析师',
    goal='揭示 AI 和数据科学的前沿发展',
    backstory="""你是一个领先科技智库的专家。
    你的专长在于识别 AI、数据科学和机器学习中的新兴趋势和技术。""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool]
)

# 完整属性列表
agent = Agent(
    role='角色名称',              # 代理的职位名称
    goal='具体目标',             # 代理旨在实现的目标
    backstory='背景故事',        # 背景和专长
    verbose=True,                # 启用详细日志
    allow_delegation=False,      # 是否可以将任务委派给其他代理
    tools=[tool1, tool2],       # 可用工具
    llm=custom_llm,             # 自定义 LLM 配置
    max_iter=15,                # 任务的最大迭代次数
    max_rpm=10,                 # 限制速率（每分钟请求数）
    memory=True,                # 启用记忆
    cache=True,                 # 启用响应缓存
    system_template="template",  # 自定义系统提示模板
    prompt_template="template",  # 自定义提示模板
    response_template="template" # 自定义响应模板
)
```

---

## Task 完整属性

```python
from crewai import Task

research_task = Task(
    description="""对 AI 最新进展进行全面分析。
    识别关键趋势、突破性技术和潜在行业影响。
    将你的发现汇编成详细报告。""",
    expected_output='关于 AI 进展的全面 3 段报告',
    agent=researcher,
    tools=[search_tool],
    output_file='research_report.md'
)

# 完整属性列表
task = Task(
    description='详细的任务描述',
    expected_output='清晰的输出格式',
    agent=agent_instance,
    tools=[tool1, tool2],           # 任务特定工具
    context=[previous_task],        # 依赖关系
    async_execution=False,          # 异步执行
    output_json=OutputClass,        # 结构化输出（Pydantic）
    output_pydantic=OutputClass,    # Pydantic 验证
    output_file='result.txt',       # 将输出保存到文件
    callback=callback_function,     # 完成时的回调
    human_input=False              # 请求人类反馈
)
```

---

## Crew 过程类型

```python
from crewai import Crew, Process

# 顺序过程（任务一个接一个运行）
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True,
    memory=True,
    cache=True,
    max_rpm=10,
    share_crew=False
)

# 层级过程（经理向代理委派任务）
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.hierarchical,
    manager_llm='gpt-4'  # 层级过程所需
)

# 启动方式
result = crew.kickoff()
result = crew.kickoff(inputs={'topic': '人工智能', 'audience': '开发者'})
```

---

## Flow 模式

### 基础 Flow

```python
from crewai.flow.flow import Flow, listen, start

class BlogPostFlow(Flow):

    @start()
    def fetch_topic(self):
        return "2024 年的 AI 进展"

    @listen(fetch_topic)
    def research_topic(self, topic):
        research_crew = Crew(agents=[researcher], tasks=[research_task])
        return research_crew.kickoff(inputs={'topic': topic})

    @listen(research_topic)
    def write_blog_post(self, research_data):
        write_crew = Crew(agents=[writer], tasks=[write_task])
        return write_crew.kickoff(inputs={'research': research_data})

    @listen(write_blog_post)
    def finalize(self, blog_post):
        return blog_post

flow = BlogPostFlow()
result = flow.kickoff()
```

### Flow 状态管理

```python
from pydantic import BaseModel

class ArticleState(BaseModel):
    topic: str = ""
    research: str = ""
    draft: str = ""
    final: str = ""

class ArticleFlow(Flow[ArticleState]):

    @start()
    def set_topic(self):
        self.state.topic = "AI 伦理"
        return self.state.topic

    @listen(set_topic)
    def research(self, topic):
        self.state.research = "研究结果..."
        return self.state.research

    @listen(research)
    def write_draft(self, research):
        self.state.draft = "草稿内容..."
        return self.state.draft

flow = ArticleFlow()
flow.kickoff()
print(flow.state.topic)
```

### 路由模式

```python
from crewai.flow.flow import Flow, listen, start, router

class ContentFlow(Flow):

    @start()
    def categorize_content(self):
        return "技术"

    @router(categorize_content)
    def route_content(self, category):
        if category == "技术":
            return "write_technical"
        elif category == "市场营销":
            return "write_marketing"
        else:
            return "write_blog"

    @listen("write_technical")
    def write_technical_doc(self):
        return "技术文档..."

    @listen("write_marketing")
    def write_marketing_copy(self):
        return "市场内容..."

    @listen("write_blog")
    def write_blog_post(self):
        return "博客文章..."
```

---

## 工具：内置与自定义

### 内置工具

```python
from crewai_tools import (
    SerperDevTool,      # Google 搜索
    ScrapeWebsiteTool,  # 网络爬虫
    FileReadTool,       # 读取文件
    DirectoryReadTool,  # 读取目录
    CodeDocsSearchTool, # 搜索代码文档
    CSVSearchTool,      # 搜索 CSV 文件
    JSONSearchTool,     # 搜索 JSON 文件
    MDXSearchTool,      # 搜索 MDX 文件
    PDFSearchTool,      # 搜索 PDF 文件
    TXTSearchTool,      # 搜索文本文件
    WebsiteSearchTool,  # 搜索网站
    SeleniumScrapingTool,       # 浏览器自动化
    YoutubeChannelSearchTool,   # YouTube 搜索
    YoutubeVideoSearchTool      # YouTube 视频搜索
)

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
agent = Agent(role='研究员', tools=[search_tool, scrape_tool])
```

### 自定义工具（类方式）

```python
from crewai_tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "自定义工具名称"
    description: str = "工具功能的清晰描述"

    def _run(self, argument: str) -> str:
        result = perform_operation(argument)
        return result

custom_tool = MyCustomTool()
agent = Agent(role='专家', tools=[custom_tool])
```

### 函数作为工具

```python
def calculate_sum(a: int, b: int) -> int:
    """计算两个数字的和"""
    return a + b

agent = Agent(role='计算器', tools=[calculate_sum])
```

---

## 记忆配置

```python
# 启用所有记忆类型
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,
    verbose=True
)

# 配置特定记忆类型
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,
    memory_config={
        'short_term': True,   # 在单次运行内记忆
        'long_term': True,    # 跨运行记忆
        'entity': True        # 记忆实体（人、地点）
    }
)
```

---

## 知识 RAG 集成

```python
from crewai import Agent, knowledge

# 字符串知识源
docs_knowledge = knowledge.StringKnowledgeSource(
    content="公司政策和程序...",
    metadata={"source": "policy_docs"}
)

# PDF 知识源
pdf_knowledge = knowledge.PDFKnowledgeSource(
    file_path='./documents/handbook.pdf'
)

# 文本文件知识源
txt_knowledge = knowledge.TextKnowledgeSource(
    file_path='./documents/faq.txt'
)

agent = Agent(
    role='支持代理',
    knowledge_sources=[pdf_knowledge, txt_knowledge]
)
```

---

## 结构化输出 Pydantic

```python
from pydantic import BaseModel
from crewai import Task

class BlogPost(BaseModel):
    title: str
    content: str
    tags: list[str]
    word_count: int

write_task = Task(
    description='撰写关于 AI 的博客文章',
    expected_output='包含标题、内容、标签和字数的博客文章',
    agent=writer,
    output_pydantic=BlogPost
)

result = crew.kickoff()
blog_post: BlogPost = write_task.output.pydantic
print(blog_post.title)
print(blog_post.tags)
```

---

## 训练与人工干预

### 训练

```python
crew = Crew(agents=[agent1, agent2], tasks=[task1, task2])

crew.train(
    n_iterations=10,
    inputs={'topic': 'AI'},
    filename='trained_crew.pkl'
)

trained_crew = Crew.load('trained_crew.pkl')
```

### 人工干预

```python
# 需要人类输入的任务
review_task = Task(
    description='审核草稿并提供反馈',
    expected_output='批准的草稿或修订反馈',
    agent=editor,
    human_input=True  # 将暂停并请求输入
)

# 条件性人类输入
task = Task(
    description='生成报告',
    expected_output='最终报告',
    agent=analyst,
    callback=lambda output: validate_output(output),
    human_input=True if needs_review else False
)
```

---

## 测试模式

```python
import pytest
from crewai import Crew

def test_research_crew():
    crew = Crew(agents=[researcher], tasks=[research_task])
    result = crew.kickoff(inputs={'topic': 'AI'})
    assert result is not None
    assert 'AI' in result
    assert len(result) > 100

def test_crew_with_mock():
    mock_agent = Agent(role='模拟代理', goal='返回测试数据', backstory='测试代理')
    mock_task = Task(description='测试任务', expected_output='测试输出', agent=mock_agent)
    crew = Crew(agents=[mock_agent], tasks=[mock_task])
    result = crew.kickoff()
    assert result == '测试输出'
```

---

## 自定义 LLM

```python
from langchain_openai import ChatOpenAI
from crewai import Agent, Crew

custom_llm = ChatOpenAI(
    model='gpt-4-turbo-preview',
    temperature=0.7,
    max_tokens=2000
)

agent = Agent(role='写手', llm=custom_llm)

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    manager_llm=custom_llm  # 用于层级过程
)
```

---

## 异步执行

```python
from crewai import Crew

crew = Crew(agents=[agent1, agent2], tasks=[task1, task2])

# 异步启动
async def run_crew():
    result = await crew.kickoff_async(inputs={'topic': 'AI'})
    return result

# 并行批量执行
inputs_list = [
    {'topic': 'AI'},
    {'topic': 'ML'},
    {'topic': '数据科学'}
]
results = crew.kickoff_for_each(inputs=inputs_list)
```

---

## 回调与事件

```python
def on_task_complete(output):
    print(f"任务完成，输出为：{output}")

def on_task_error(error):
    print(f"任务失败，错误为：{error}")

task = Task(
    description='分析数据',
    expected_output='分析报告',
    agent=analyst,
    callback=on_task_complete
)

# 代理级回调
agent = Agent(
    role='分析师',
    step_callback=lambda step: print(f"代理步骤：{step}"),
    task_callback=on_task_complete
)
```

---

## 企业部署配置

### 环境变量

```python
import os

os.environ['OPENAI_API_KEY'] = 'your-key'
os.environ['SERPER_API_KEY'] = 'your-key'
os.environ['CREWAI_API_KEY'] = 'your-enterprise-key'  # CrewAI+（企业版）
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_API_KEY'] = 'your-langchain-key'
```

### 项目结构

```
my_crew_project/
├── src/
│   └── my_crew_project/
│       ├── __init__.py
│       ├── main.py
│       ├── crew.py
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── tools/
│           └── custom_tool.py
├── tests/
│   └── test_crew.py
├── pyproject.toml
└── README.md
```

---

## YAML 配置

**agents.yaml**
```yaml
researcher:
  role: >
    高级研究分析师
  goal: >
    揭示 {topic} 的前沿发展
  backstory: >
    你是一位对 {topic} 有深刻了解的专家研究员

writer:
  role: >
    内容撰写者
  goal: >
    创建关于 {topic} 的引人入胜的内容
  backstory: >
    你是一位能够使复杂主题易于理解的熟练写手
```

**tasks.yaml**
```yaml
research_task:
  description: >
    对 {topic} 进行全面研究
  expected_output: >
    一份包含关键发现的详细研究报告
  agent: researcher

writing_task:
  description: >
    根据研究撰写文章
  expected_output: >
    一篇结构良好的文章
  agent: writer
  context:
    - research_task
```

---

## 常见模式

### 研究和写作管道

```python
researcher = Agent(role='研究员', ...)
analyst = Agent(role='分析师', ...)
writer = Agent(role='写手', ...)
editor = Agent(role='编辑', ...)

research = Task(agent=researcher, ...)
analysis = Task(agent=analyst, context=[research], ...)
draft = Task(agent=writer, context=[analysis], ...)
final = Task(agent=editor, context=[draft], ...)

crew = Crew(
    agents=[researcher, analyst, writer, editor],
    tasks=[research, analysis, draft, final],
    process=Process.sequential
)
```

### 多阶段审批流程

```python
class ApprovalFlow(Flow):

    @start()
    def create_draft(self):
        return draft_content

    @listen(create_draft)
    def request_review(self, draft):
        return review_request

    @router(request_review)
    def check_approval(self, review):
        if review.approved:
            return "finalize"
        else:
            return "revise"

    @listen("revise")
    def revise_draft(self):
        return revised_draft

    @listen("finalize")
    def finalize_content(self):
        return final_content
```
