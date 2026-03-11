---
name: crewai-developer
description: Comprehensive CrewAI 框架指南，用于构建协作 AI 代理团队和结构化工作流程。在使用 CrewAI 开发多代理系统、创建自主 AI 团队、编排流程、实现具有角色和工具的代理或构建生产就绪的 AI 自动化时使用。对于构建智能代理系统、任务自动化和复杂 AI 工作流程的开发人员至关重要。
version: 1.0.0
metadata:
  category: workflow-automation
---

# CrewAI 开发者指南

## 概述

CrewAI 是一个轻量级、快速的 Python 框架，用于构建协作 AI 代理团队和结构化工作流程。它使开发人员能够创建具有特定角色、工具和目标的自主 AI 代理，这些代理协同工作以应对复杂任务。此技能涵盖了 Crews（自主协作）、Flows（结构化编排）、代理、任务和企业部署。

## 核心概念

### 代理：专业团队成员

代理是具有特定角色、目标和能力的自主 AI 单元。

```python
from crewai import Agent

# 创建一个研究代理
researcher = Agent(
    role='高级研究分析师',
    goal='揭示 AI 和数据科学的前沿发展',
    backstory="""你是一个领先科技智库的专家。
    你的专长在于识别 AI、数据科学和机器学习中的新兴趋势和技术。""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, scrape_tool]
)

# 创建一个写作代理
writer = Agent(
    role='技术内容策略师',
    goal='撰写关于技术进步的引人入胜的内容',
    backstory="""你是一位著名的内容策略师，以
    你对技术和创新的深刻见解和引人入胜的文章而闻名。
    你将复杂的概念转化为引人入胜的叙述。""",
    verbose=True,
    allow_delegation=True,
    tools=[write_tool]
)
```

#### 代理关键属性

```python
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

### 任务：单个分配

任务定义了代理需要完成的具体工作。

```python
from crewai import Task

# 研究任务
research_task = Task(
    description="""对 AI 最新进展进行全面分析。
    识别关键趋势、突破性技术和潜在行业影响。
    将你的发现汇编成详细报告。""",
    expected_output='关于 AI 进展的全面 3 段报告',
    agent=researcher,
    tools=[search_tool],
    output_file='research_report.md'
)

# 写作任务
write_task = Task(
    description="""使用研究分析师的报告，撰写一篇引人入胜的博客文章，
    突出最重要的 AI 进展。
    使其对普通读者易于理解和引人入胜。""",
    expected_output='关于 AI 进展的 4 段博客文章',
    agent=writer,
    context=[research_task],  # 依赖于 research_task 的输出
    output_file='blog_post.md'
)
```

#### 任务关键属性

```python
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

### 团队：组织代理团队

团队编排代理共同朝着共同目标工作。

```python
from crewai import Crew, Process

# 创建一个团队
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # 或 Process.hierarchical
    verbose=True,
    memory=True,
    cache=True,
    max_rpm=10,
    share_crew=False
)

# 启动团队
result = crew.kickoff()
print(result)

# 使用自定义输入启动
result = crew.kickoff(inputs={
    'topic': '人工智能',
    'audience': '开发者'
})
```

#### 过程类型

```python
# 顺序过程（任务一个接一个运行）
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.sequential
)

# 层级过程（经理向代理委派任务）
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    process=Process.hierarchical,
    manager_llm='gpt-4'  # 层级过程所需
)
```

### 流程：结构化工作流编排

流程提供事件驱动的、确定性的执行路径控制。

```python
from crewai.flow.flow import Flow, listen, start

class BlogPostFlow(Flow):

    @start()
    def fetch_topic(self):
        """入口点 - 获取要写的主题"""
        print("开始生成博客文章")
        return "2024 年的 AI 进展"

    @listen(fetch_topic)
    def research_topic(self, topic):
        """研究主题"""
        print(f"研究中：{topic}")
        # 与团队集成以进行自主研究
        research_crew = Crew(
            agents=[researcher],
            tasks=[research_task]
        )
        result = research_crew.kickoff(inputs={'topic': topic})
        return result

    @listen(research_topic)
    def write_blog_post(self, research_data):
        """撰写博客文章"""
        print("正在撰写博客文章...")
        write_crew = Crew(
            agents=[writer],
            tasks=[write_task]
        )
        result = write_crew.kickoff(inputs={'research': research_data})
        return result

    @listen(write_blog_post)
    def finalize(self, blog_post):
        """最终确定并保存"""
        print("博客文章完成！")
        return blog_post

# 执行流程
flow = BlogPostFlow()
result = flow.kickoff()
```

#### 流程状态管理

```python
from crewai.flow.flow import Flow, listen, start
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
        # 研究逻辑
        self.state.research = "研究结果..."
        return self.state.research

    @listen(research)
    def write_draft(self, research):
        self.state.draft = "草稿内容..."
        return self.state.draft

# 访问状态
flow = ArticleFlow()
flow.kickoff()
print(flow.state.topic)
print(flow.state.research)
```

#### 路由模式

```python
from crewai.flow.flow import Flow, listen, start, router

class ContentFlow(Flow):

    @start()
    def categorize_content(self):
        return "技术"  # 或 "市场营销", "博客"

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

## 工具：扩展代理能力

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
    SeleniumScrapingTool, # 浏览器自动化
    YoutubeChannelSearchTool, # YouTube 搜索
    YoutubeVideoSearchTool   # YouTube 视频搜索
)

# 使用工具
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
file_tool = FileReadTool()

agent = Agent(
    role='研究员',
    tools=[search_tool, scrape_tool, file_tool]
)
```

### 自定义工具

```python
from crewai_tools import BaseTool

class MyCustomTool(BaseTool):
    name: str = "自定义工具名称"
    description: str = "工具功能的清晰描述"

    def _run(self, argument: str) -> str:
        # 实现
        result = perform_operation(argument)
        return result

# 使用自定义工具
custom_tool = MyCustomTool()
agent = Agent(
    role='专家',
    tools=[custom_tool]
)
```

### 函数作为工具

```python
from crewai import Agent

def calculate_sum(a: int, b: int) -> int:
    """计算两个数字的和"""
    return a + b

agent = Agent(
    role='计算器',
    tools=[calculate_sum]  # 直接传递函数
)
```

## 记忆：从过去的交互中学习

```python
from crewai import Crew, Agent, Task

# 启用团队记忆
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    memory=True,  # 启用所有记忆类型
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

## 知识：RAG 集成

```python
from crewai import Agent, Crew, Task, knowledge

# 创建知识源
docs_knowledge = knowledge.StringKnowledgeSource(
    content="公司政策和程序...",
    metadata={"source": "policy_docs"}
)

# 在代理中使用知识
agent = Agent(
    role='政策专家',
    goal='回答有关公司政策的问题',
    backstory='公司政策方面的专家',
    knowledge_sources=[docs_knowledge]
)

# 从文件加载知识
pdf_knowledge = knowledge.PDFKnowledgeSource(
    file_path='./documents/handbook.pdf'
)

txt_knowledge = knowledge.TextKnowledgeSource(
    file_path='./documents/faq.txt'
)

agent = Agent(
    role='支持代理',
    knowledge_sources=[pdf_knowledge, txt_knowledge]
)
```

## 使用 Pydantic 进行结构化输出

```python
from pydantic import BaseModel
from crewai import Task, Agent

class BlogPost(BaseModel):
    title: str
    content: str
    tags: list[str]
    word_count: int

# 带有结构化输出的任务
write_task = Task(
    description='撰写关于 AI 的博客文章',
    expected_output='包含标题、内容、标签和字数的博客文章',
    agent=writer,
    output_pydantic=BlogPost
)

# 执行并获取结构化输出
result = crew.kickoff()
blog_post: BlogPost = write_task.output.pydantic
print(blog_post.title)
print(blog_post.tags)
```

## 训练：提高性能

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2]
)

# 训练循环
crew.train(
    n_iterations=10,
    inputs={'topic': 'AI'},
    filename='trained_crew.pkl'
)

# 加载训练好的团队
trained_crew = Crew.load('trained_crew.pkl')
```

## 人工干预

```python
from crewai import Task

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

## 测试团队

```python
from crewai import Crew
import pytest

def test_research_crew():
    # 设置
    crew = Crew(
        agents=[researcher],
        tasks=[research_task]
    )

    # 执行
    result = crew.kickoff(inputs={'topic': 'AI'})

    # 断言
    assert result is not None
    assert 'AI' in result
    assert len(result) > 100

def test_crew_with_mock():
    # 模拟代理行为以进行测试
    mock_agent = Agent(
        role='模拟代理',
        goal='返回测试数据',
        backstory='测试代理'
    )

    mock_task = Task(
        description='测试任务',
        expected_output='测试输出',
        agent=mock_agent
    )

    crew = Crew(agents=[mock_agent], tasks=[mock_task])
    result = crew.kickoff()

    assert result == '测试输出'
```

## 自定义 LLMs

```python
from langchain_openai import ChatOpenAI
from crewai import Agent, Crew

# 使用自定义 LLM
custom_llm = ChatOpenAI(
    model='gpt-4-turbo-preview',
    temperature=0.7,
    max_tokens=2000
)

agent = Agent(
    role='写手',
    llm=custom_llm
)

# 团队级 LLM
crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    manager_llm=custom_llm  # 用于层级过程
)
```

## 异步执行

```python
from crewai import Crew

crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2]
)

# 异步启动
async def run_crew():
    result = await crew.kickoff_async(inputs={'topic': 'AI'})
    return result

# 为每个启动（并行执行）
inputs_list = [
    {'topic': 'AI'},
    {'topic': 'ML'},
    {'topic': '数据科学'}
]

results = crew.kickoff_for_each(inputs=inputs_list)
```

## 回调和事件监听器

```python
from crewai import Task, Agent

def on_task_complete(output):
    print(f"任务完成，输出为：{output}")
    # 记录、通知或处理输出

def on_task_error(error):
    print(f"任务失败，错误为：{error}")
    # 处理错误、重试或通知

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

## 企业部署

### 环境配置

```python
import os

# API 密钥
os.environ['OPENAI_API_KEY'] = 'your-key'
os.environ['SERPER_API_KEY'] = 'your-key'

# CrewAI+（企业版）
os.environ['CREWAI_API_KEY'] = 'your-enterprise-key'

# 可观察性
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

### YAML 配置

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

## 最佳实践

### 代理设计

✅ **良好实践**：
- 为代理提供清晰、具体的角色
- 提供详细的背景故事以提供上下文
- 限制工具至必要的范围
- 启用经理的委派功能
- 在开发过程中使用详细模式

❌ **避免**：
- 模糊或重叠的角色
- 工具过多（会导致混淆）
- 缺失背景故事
- 目标过于复杂

### 任务设计

✅ **良好实践**：
- 编写清晰、可操作的描述
- 指定预期输出格式
- 设置适当的任务依赖关系
- 使用上下文进行任务链
- 对关键决策启用人类输入

❌ **避免**：
- 模糊的描述
- 缺失预期输出
- 循环依赖
- 单个任务过于复杂

### 团队组织

✅ **良好实践**：
- 从顺序过程开始
- 对复杂协调使用层级
- 启用记忆以保留上下文
- 设置合理的速率限制
- 首先用小数据集进行测试

❌ **避免**：
- 代理过多（3-5 个为最佳）
- 未经测试的复杂层级
- 在多步骤流程中禁用记忆
- 不设置速率限制

## 常见模式

### 研究和写作管道

```python
# 1. 研究代理收集信息
# 2. 分析师代理处理数据
# 3. 写作代理创建内容
# 4. 编辑代理审核和完善

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
        # 生成初步草稿
        return draft_content

    @listen(create_draft)
    def request_review(self, draft):
        # 发送审核请求
        return review_request

    @router(request_review)
    def check_approval(self, review):
        if review.approved:
            return "finalize"
        else:
            return "revise"

    @listen("revise")
    def revise_draft(self):
        # 修订并循环回去
        return revised_draft

    @listen("finalize")
    def finalize_content(self):
        return final_content
```

## 快速参考

### 安装

```bash
# 使用 uv（推荐）
uv pip install crewai crewai-tools

# 使用 pip
pip install crewai crewai-tools

# 安装所有扩展
pip install 'crewai[all]'
```

### CLI 命令

```bash
# 创建新项目
crewai create crew my_project

# 创建流程
crewai create flow my_flow

# 安装依赖
crewai install

# 运行项目
crewai run

# 训练团队
crewai train

# 重播任务
crewai replay <task_id>

# 测试团队
crewai test
```

### 重要导入

```python
from crewai import Agent, Task, Crew, Process
from crewai.flow.flow import Flow, listen, start, router
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel
```

## 资源

有关高级模式、集成示例和故障排除：
- 官方文档: https://docs.crewai.com/
- API 参考: https://docs.crewai.com/api-reference
- GitHub: https://github.com/joaomdmoura/crewAI
- 社区论坛: https://community.crewai.com/

### 扩展参考
请参见 `references/advanced_patterns.md` 以获取：
- MCP（模型上下文协议）集成
- 可观察性和追踪设置
- 生产部署策略
- 高级流程模式
- 性能优化