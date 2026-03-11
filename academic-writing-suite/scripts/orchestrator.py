#!/usr/bin/env python3
"""
Academic Writing Suite Orchestrator

CLI tool to coordinate the academic writing workflow.

Commands:
    init    - Initialize project directory structure
    search  - Run paper searches across databases
    figures - Generate publication figures
    status  - Check project progress

Usage:
    python orchestrator.py init "Research Topic"
    python orchestrator.py search "transformer attention"
    python orchestrator.py figures
    python orchestrator.py status
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Default paths
DOWNLOADS_DIR = Path.home() / "Downloads" / "academic-writing"
SKILLS_DIR = Path.home() / ".claude" / "skills"
PAPER_SEARCH_SCRIPT = SKILLS_DIR / "paper-search" / "scripts" / "search.py"


def init_project(topic: str, base_dir: Path = DOWNLOADS_DIR) -> Path:
    """Initialize project directory structure."""
    # Sanitize topic for directory name
    safe_topic = "".join(c if c.isalnum() or c in " -_" else "_" for c in topic)
    safe_topic = safe_topic.strip().replace(" ", "_")[:50]

    project_dir = base_dir / safe_topic
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    subdirs = [
        "01_文献调研",
        "01_文献调研/papers",
        "02_提纲",
        "03_草稿",
        "04_图表",
        "05_输出",
    ]
    for subdir in subdirs:
        (project_dir / subdir).mkdir(exist_ok=True)

    # Create initial files
    requirements_file = project_dir / "00_需求分析.md"
    if not requirements_file.exists():
        requirements_file.write_text(f"""# 写作需求分析

## 基本信息
- **项目主题**：{topic}
- **创建时间**：{datetime.now().strftime("%Y-%m-%d %H:%M")}
- **文档类型**：[论文/报告/申请书]
- **目标发表**：[期刊名/会议名/机构]

## 格式要求
- **字数限制**：
- **页数限制**：
- **引用格式**：[APA/IEEE/Nature/...]

## 图表需求
- [ ] 方法流程图
- [ ] 数据图表
- [ ] 结果对比表
- [ ] 其他：

## 时间节点
- **截止日期**：
- **里程碑**：
  - [ ] 文献调研完成
  - [ ] 提纲确定
  - [ ] 初稿完成
  - [ ] 图表完成
  - [ ] 终稿提交

## 备注

""", encoding="utf-8")

    # Create project config
    config_file = project_dir / ".project.json"
    config = {
        "topic": topic,
        "created": datetime.now().isoformat(),
        "phase": "init",
        "searches": [],
        "figures": [],
    }
    config_file.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Project initialized: {project_dir}")
    print(f"\nDirectory structure created:")
    for subdir in subdirs:
        print(f"  {subdir}/")
    print(f"\nNext steps:")
    print(f"  1. Edit 00_需求分析.md to define requirements")
    print(f"  2. Run: python orchestrator.py search '<keywords>'")

    return project_dir


def search_papers(keywords: str, databases: list = None, max_results: int = 10):
    """Search academic databases for papers."""
    if databases is None:
        databases = ["arxiv", "semantic"]

    if not PAPER_SEARCH_SCRIPT.exists():
        print(f"Error: paper-search script not found at {PAPER_SEARCH_SCRIPT}")
        print("Please ensure paper-search skill is installed.")
        sys.exit(1)

    results = {}
    for db in databases:
        print(f"\nSearching {db} for: {keywords}")
        try:
            result = subprocess.run(
                [sys.executable, str(PAPER_SEARCH_SCRIPT), db, keywords, "--max", str(max_results)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print(result.stdout)
                results[db] = result.stdout
            else:
                print(f"Error searching {db}: {result.stderr}")
        except Exception as e:
            print(f"Error running search: {e}")

    return results


def generate_figures(project_dir: Path = None):
    """Generate publication figures using pub-figures templates."""
    print("Figure generation helper")
    print("\nTo generate figures, use the pub-figures skill directly:")
    print("\n  1. Prepare your data in Python/CSV format")
    print("  2. Use pub-figures templates for:")
    print("     - Multi-panel figures (2x2, 1x3 layouts)")
    print("     - Forest plots")
    print("     - Heatmaps")
    print("     - Grouped bar charts")
    print("\nExample:")
    print("  python -c \"import matplotlib.pyplot as plt; ...\"")
    print("\nSee pub-figures SKILL.md for detailed templates.")


def check_status(project_dir: Path = None):
    """Check project progress and status."""
    if project_dir is None:
        # Find most recent project
        if not DOWNLOADS_DIR.exists():
            print("No projects found. Run 'init' first.")
            return

        projects = [d for d in DOWNLOADS_DIR.iterdir() if d.is_dir()]
        if not projects:
            print("No projects found. Run 'init' first.")
            return

        project_dir = max(projects, key=lambda p: p.stat().st_mtime)

    config_file = project_dir / ".project.json"
    if not config_file.exists():
        print(f"Not a valid project directory: {project_dir}")
        return

    config = json.loads(config_file.read_text(encoding="utf-8"))

    print(f"Project: {config['topic']}")
    print(f"Created: {config['created']}")
    print(f"Current Phase: {config['phase']}")
    print("\nDirectory contents:")

    # Check each phase directory
    phases = [
        ("00_需求分析.md", "Phase 1: 需求分析"),
        ("01_文献调研", "Phase 2: 文献调研"),
        ("02_提纲", "Phase 3: 提纲设计"),
        ("03_草稿", "Phase 4: 内容撰写"),
        ("04_图表", "Phase 4: 图表生成"),
        ("05_输出", "Phase 5: 整合输出"),
    ]

    for path, phase_name in phases:
        full_path = project_dir / path
        if full_path.exists():
            if full_path.is_file():
                size = full_path.stat().st_size
                status = "✅" if size > 100 else "⚠️ (empty)"
            else:
                files = list(full_path.iterdir())
                status = f"✅ ({len(files)} files)" if files else "⚠️ (empty)"
        else:
            status = "❌ (missing)"
        print(f"  {phase_name}: {status}")


def main():
    parser = argparse.ArgumentParser(
        description="Academic Writing Suite Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Initialize a new project
    python orchestrator.py init "Transformer Attention Mechanisms"

    # Search for papers
    python orchestrator.py search "attention mechanism" --db arxiv semantic

    # Check project status
    python orchestrator.py status
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize project directory")
    init_parser.add_argument("topic", help="Research topic/title")

    # search command
    search_parser = subparsers.add_parser("search", help="Search academic databases")
    search_parser.add_argument("keywords", help="Search keywords")
    search_parser.add_argument("--db", nargs="+", default=["arxiv", "semantic"],
                               help="Databases to search (arxiv, pubmed, semantic, biorxiv)")
    search_parser.add_argument("--max", type=int, default=10, help="Max results per database")

    # figures command
    figures_parser = subparsers.add_parser("figures", help="Generate publication figures")
    figures_parser.add_argument("--project", help="Project directory path")

    # status command
    status_parser = subparsers.add_parser("status", help="Check project progress")
    status_parser.add_argument("--project", help="Project directory path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "init":
        init_project(args.topic)

    elif args.command == "search":
        search_papers(args.keywords, args.db, args.max)

    elif args.command == "figures":
        project_dir = Path(args.project) if args.project else None
        generate_figures(project_dir)

    elif args.command == "status":
        project_dir = Path(args.project) if args.project else None
        check_status(project_dir)


if __name__ == "__main__":
    main()
