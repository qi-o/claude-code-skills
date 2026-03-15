---
name: crewai-developer
description: CrewAI 框架完整指南，用于构建协作 AI 代理团队和结构化工作流程。当用户提到"CrewAI"、"多代理系统"、"AI团队"、"代理编排"、"crewai crew"、"crewai flow"、"multi-agent"、"agent orchestration"、"build a crew"时使用。Do NOT use for general agent orchestration unrelated to CrewAI (use role-orchestrator or oh-my-claudecode agents instead).
version: 1.0.0
metadata:
  category: workflow-automation
---

# CrewAI 开发者指南

## 概述

CrewAI 是一个轻量级、快速的 Python 框架，用于构建协作 AI 代理团队和结构化工作流程。支持两种模式：
- **Crews**：自主协作，代理共同完成目标
- **Flows**：结构化编排，事件驱动的确定性执行路径

## 核心概念速查

| 概念 | 说明 | 关键参数 |
|------|------|---------|
| `Agent` | 具有角色/目标/工具的自主 AI 单元 | `role`, `goal`, `backstory`, `tools`, `llm` |
| `Task` | 代理需要完成的具体工作 | `description`, `expected_output`, `agent`, `context` |
| `Crew` | 编排代理团队朝共同目标工作 | `agents`, `tasks`, `process`, `memory` |
| `Flow` | 事件驱动的工作流，用 `@start`/`@listen`/`@router` 装饰器 | 状态管理、路由控制 |

## 安装

```bash
uv pip install crewai crewai-tools   # 推荐
pip install crewai crewai-tools
pip install 'crewai[all]'            # 所有扩展
```

## 重要导入

```python
from crewai import Agent, Task, Crew, Process
from crewai.flow.flow import Flow, listen, start, router
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel
```

## 最小示例

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(role='研究员', goal='收集信息', backstory='专业研究员')
writer = Agent(role='写手', goal='撰写内容', backstory='专业写手')

research_task = Task(description='研究 AI 趋势', expected_output='研究报告', agent=researcher)
write_task = Task(description='撰写文章', expected_output='博客文章', agent=writer, context=[research_task])

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task], process=Process.sequential)
result = crew.kickoff()
```

## 过程类型

| 类型 | 说明 | 何时使用 |
|------|------|---------|
| `Process.sequential` | 任务按顺序执行 | 默认，线性工作流 |
| `Process.hierarchical` | 经理代理委派任务 | 复杂协调，需设 `manager_llm` |

## Flow 装饰器

| 装饰器 | 说明 |
|--------|------|
| `@start()` | 流程入口点 |
| `@listen(method)` | 监听指定方法完成后触发 |
| `@router(method)` | 根据返回值路由到不同分支 |

## 工具类型

| 类型 | 示例 |
|------|------|
| 内置工具 | `SerperDevTool`, `ScrapeWebsiteTool`, `FileReadTool`, `PDFSearchTool` |
| 自定义类 | 继承 `BaseTool`，实现 `_run()` |
| 函数工具 | 直接传递 Python 函数 |

## 最佳实践

**代理设计**
- 提供清晰、具体的角色和详细背景故事
- 限制工具至必要范围（工具过多会导致混淆）
- 代理数量 3-5 个为最佳

**任务设计**
- 编写清晰可操作的描述，指定预期输出格式
- 用 `context=[prev_task]` 设置任务依赖
- 对关键决策启用 `human_input=True`

**团队组织**
- 从顺序过程开始，复杂协调再用层级
- 启用 `memory=True` 保留上下文
- 设置合理的 `max_rpm` 速率限制

## CLI 命令

```bash
crewai create crew my_project   # 创建新项目
crewai create flow my_flow      # 创建流程
crewai install                  # 安装依赖
crewai run                      # 运行项目
crewai train                    # 训练团队
crewai replay <task_id>         # 重播任务
crewai test                     # 测试团队
```

## 参考文件

详细代码示例请参见 `references/code_examples.md`，包含：
- Agent/Task/Crew/Flow 完整属性和代码示例
- 内置工具列表与自定义工具实现
- 记忆配置、知识 RAG 集成
- 结构化输出（Pydantic）、训练、人工干预
- 测试模式、自定义 LLM、异步执行
- 回调与事件、企业部署配置
- YAML 配置文件示例
- 研究写作管道、多阶段审批流程等常见模式

## 资源

- 官方文档: https://docs.crewai.com/
- API 参考: https://docs.crewai.com/api-reference
- GitHub: https://github.com/joaomdmoura/crewAI
- 社区论坛: https://community.crewai.com/
