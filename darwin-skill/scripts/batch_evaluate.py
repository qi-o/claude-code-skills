#!/usr/bin/env python
"""
Darwin Skill Batch Evaluator — static analysis of SKILL.md files.
Scores dimensions 1-7 based on the darwin-skill rubric.
Outputs TSV to stdout.
"""
import os
import re
import sys
import json
from datetime import datetime

SKILLS_DIR = os.path.expanduser("~/.claude/skills")

def read_frontmatter(content):
    """Extract YAML frontmatter from SKILL.md content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[1].strip()
    return ""

def parse_frontmatter(fm_text):
    """Simple YAML frontmatter parser (no pyyaml dependency)."""
    result = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            result[key] = val
    return result

def score_frontmatter(fm):
    """D1: Frontmatter quality (weight 8)."""
    score = 5  # baseline
    if fm.get("name"):
        score += 1
    desc = fm.get("description", "")
    if desc:
        score += 1
        if len(desc) > 20:
            score += 1
        # Check for trigger words in description
        if any(t in desc.lower() for t in ["trigger", "触发", "when", "use when", "用于"]):
            score += 1
    if len(desc) <= 1024:
        score += 1
    return min(score, 10)

def score_workflow(content):
    """D2: Workflow clarity (weight 15)."""
    score = 3
    # Check for numbered steps
    step_patterns = [
        r"(?:^|\n)\s*(?:Step|步骤)\s*\d",
        r"(?:^|\n)\s*\d+\.\s",
        r"(?:^|\n)\s*###\s*(?:Step|Phase|阶段|步骤)",
        r"(?:^|\n)##\s*(?:Step|Phase|阶段|步骤)\s",
    ]
    for pat in step_patterns:
        if re.search(pat, content, re.MULTILINE | re.IGNORECASE):
            score += 2
            break

    # Check for input/output specs
    io_patterns = [r"输入[:：]", r"输出[:：]", r"input[:：]", r"output[:：]", r"参数[:：]", r"返回"]
    io_count = sum(1 for p in io_patterns if re.search(p, content, re.IGNORECASE))
    score += min(io_count, 2)

    # Check for code blocks (executable steps)
    code_blocks = len(re.findall(r"```", content)) // 2
    if code_blocks >= 3:
        score += 2
    elif code_blocks >= 1:
        score += 1

    # Check for clear section structure
    sections = len(re.findall(r"^##", content, re.MULTILINE))
    if sections >= 4:
        score += 1

    return min(score, 10)

def score_boundary(content):
    """D3: Boundary conditions (weight 10)."""
    score = 3
    boundary_signals = [
        r"错误处理|error.?handl|异常|fallback|回退|备选",
        r"边界|edge.?case|corner.?case|边界条件",
        r"失败|失败时|on.?fail|on.?error|catch|except",
        r"超时|timeout|retry|重试",
        r"如果.*不存在|if.*not.*exist|if.*missing|不存在则",
    ]
    matches = sum(1 for p in boundary_signals if re.search(p, content, re.IGNORECASE))
    score += min(matches, 4)

    # Check for explicit error/fallback section
    if re.search(r"^##.*(?:错误|异常|边界|Error|Fallback|回退)", content, re.MULTILINE | re.IGNORECASE):
        score += 2

    return min(score, 10)

def score_checkpoints(content):
    """D4: Checkpoint design (weight 7)."""
    score = 3
    cp_signals = [
        r"确认|confirm|用户确认|pause|暂停",
        r"AskUserQuestion|询问用户",
        r"STOP|停止|等待",
        r"检查点|checkpoint",
    ]
    matches = sum(1 for p in cp_signals if re.search(p, content, re.IGNORECASE))
    score += min(matches, 4)

    # Check for explicit checkpoint sections
    if re.search(r"^##.*(?:检查|确认|Checkpoint|验证)", content, re.MULTILINE | re.IGNORECASE):
        score += 2

    return min(score, 10)

def score_specificity(content):
    """D5: Instruction specificity (weight 15)."""
    score = 3

    # Check for specific parameters/flags
    param_patterns = [r"--\w+", r"-[a-z]\b", r"参数[:：]", r"\{\{.*\}\}"]
    param_count = sum(1 for p in param_patterns if re.search(p, content))
    score += min(param_count, 2)

    # Check for examples
    if re.search(r"示例|example|比如|例如", content, re.IGNORECASE):
        score += 2

    # Check for file paths (specific)
    if re.search(r"~/.*/", content) or re.search(r"[A-Z]:\\", content):
        score += 1

    # Check for format specifications
    fmt_patterns = [r"格式[:：]", r"JSON|TSV|CSV|Markdown", r"```json", r"```yaml", r"```bash"]
    fmt_count = sum(1 for p in fmt_patterns if re.search(p, content, re.IGNORECASE))
    score += min(fmt_count, 2)

    # Check for concrete commands
    if re.search(r"(?:python|node|npm|npx|pip|git|curl|bash)\s+", content):
        score += 1

    return min(score, 10)

def score_resources(content, skill_dir):
    """D6: Resource integration (weight 5)."""
    score = 5  # neutral baseline
    referenced_files = []

    # Find references to scripts, templates, etc.
    ref_patterns = [
        r"scripts/[\w.-]+",
        r"templates/[\w.-]+",
        r"references/[\w.-]+",
        r"\./[\w.-]+\.(?:py|js|mjs|sh|json)",
    ]
    for pat in ref_patterns:
        for m in re.finditer(pat, content):
            referenced_files.append(m.group())

    if referenced_files:
        existing = 0
        for rf in referenced_files:
            full_path = os.path.join(skill_dir, rf)
            if os.path.exists(full_path):
                existing += 1
        if referenced_files:
            ratio = existing / len(referenced_files)
            score = int(3 + ratio * 7)

    # Check if scripts dir exists
    scripts_dir = os.path.join(skill_dir, "scripts")
    if os.path.isdir(scripts_dir):
        scripts = os.listdir(scripts_dir)
        if scripts:
            score = max(score, 7)

    return min(score, 10)

def score_architecture(content):
    """D7: Overall architecture (weight 15)."""
    score = 4

    # Check for structured sections
    h2_count = len(re.findall(r"^## ", content, re.MULTILINE))
    h3_count = len(re.findall(r"^### ", content, re.MULTILINE))
    if h2_count >= 3:
        score += 1
    if h3_count >= 3:
        score += 1

    # Check for tables (structured data)
    table_count = len(re.findall(r"\|.+\|", content))
    if table_count >= 5:
        score += 2
    elif table_count >= 2:
        score += 1

    # Check for clear intro/purpose
    if re.search(r"^#.*\n\n.*(?:本|this|这个|该)", content, re.MULTILINE):
        score += 1

    # Check not too verbose (>2000 lines is probably bloated)
    lines = content.count("\n")
    if lines < 500:
        score += 1

    # Check for usage/invoke section
    if re.search(r"^##.*(?:使用|调用|Usage|Usage|触发)", content, re.MULTILINE | re.IGNORECASE):
        score += 1

    return min(score, 10)

def evaluate_skill(skill_dir):
    """Evaluate a single skill and return scores."""
    skill_file = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_file):
        return None

    with open(skill_file, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    fm_text = read_frontmatter(content)
    fm = parse_frontmatter(fm_text)

    d1 = score_frontmatter(fm)
    d2 = score_workflow(content)
    d3 = score_boundary(content)
    d4 = score_checkpoints(content)
    d5 = score_specificity(content)
    d6 = score_resources(content, skill_dir)
    d7 = score_architecture(content)

    # Weighted total
    total = (d1*8 + d2*15 + d3*10 + d4*7 + d5*15 + d6*5 + d7*15) / 10

    dims = {"D1": d1, "D2": d2, "D3": d3, "D4": d4, "D5": d5, "D6": d6, "D7": d7}
    weakest = min(dims, key=dims.get)
    dim_names = {
        "D1": "Frontmatter", "D2": "Workflow", "D3": "Boundary",
        "D4": "Checkpoint", "D5": "Specificity", "D6": "Resources", "D7": "Architecture"
    }

    return {
        "name": fm.get("name", os.path.basename(skill_dir)),
        "scores": dims,
        "total": round(total, 1),
        "weakest": weakest,
        "weakest_name": dim_names[weakest],
        "weakest_score": dims[weakest],
        "line_count": content.count("\n"),
    }

def main():
    # Scan all skills
    skills = []
    for entry in sorted(os.listdir(SKILLS_DIR)):
        skill_dir = os.path.join(SKILLS_DIR, entry)
        if not os.path.isdir(skill_dir):
            continue
        result = evaluate_skill(skill_dir)
        if result:
            skills.append(result)

    # Sort by total score ascending (worst first)
    skills.sort(key=lambda s: s["total"])

    # Output as TSV
    print(f"skill\tD1\tD2\tD3\tD4\tD5\tD6\tD7\ttotal\tweakest\tweakest_score\tlines")
    for s in skills:
        d = s["scores"]
        print(f"{s['name']}\t{d['D1']}\t{d['D2']}\t{d['D3']}\t{d['D4']}\t{d['D5']}\t{d['D6']}\t{d['D7']}\t{s['total']}\t{s['weakest_name']}\t{s['weakest_score']}\t{s['line_count']}")

    # Summary
    print(f"\n# Total: {len(skills)} skills evaluated")
    if skills:
        avg = round(sum(s['total'] for s in skills) / len(skills), 1)
        print(f"# Average score: {avg}")
        print(f"# Lowest 10:")
        for s in skills[:10]:
            print(f"#   {s['name']}: {s['total']} (weakest: {s['weakest_name']}={s['weakest_score']})")

if __name__ == "__main__":
    main()
