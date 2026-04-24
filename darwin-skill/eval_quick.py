#!/usr/bin/env python
"""Quick structural evaluation of all skills against darwin-skill rubric dimensions 1-7."""
import os, re, json

SKILLS_DIR = os.path.expanduser("~/.claude/skills")
results = []

def read_frontmatter(content):
    """Extract YAML frontmatter from SKILL.md content."""
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm

def score_skill(name, path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None

    fm = read_frontmatter(content)
    body = content
    # Strip frontmatter for body analysis
    body_clean = re.sub(r'^---\s*\n.*?\n---', '', body, count=1, flags=re.DOTALL).strip()
    lines = body_clean.split('\n')
    word_count = len(body_clean.split())

    # D1: Frontmatter quality (8)
    d1 = 5
    if fm.get('name'): d1 += 1
    desc = fm.get('description', '')
    if desc:
        if len(desc) > 20: d1 += 1
        if any(t in desc.lower() for t in ['trigger', 'use when', '触发', '使用']): d1 += 1
        if len(desc) <= 1024: d1 += 1
    if d1 > 10: d1 = 10

    # D2: Workflow clarity (15)
    d2 = 3
    step_markers = len(re.findall(r'(?:^|\n)\s*(?:Step|步骤|Phase|阶段|###?\s*(?:\d+|Step|步骤))', body_clean, re.IGNORECASE))
    if step_markers >= 3: d2 += 3
    elif step_markers >= 1: d2 += 1
    numbered_steps = len(re.findall(r'(?:^|\n)\s*\d+[\.\)]\s', body_clean))
    if numbered_steps >= 3: d2 += 2
    if '```' in body_clean: d2 += 1  # has code examples
    if d2 > 10: d2 = 10

    # D3: Boundary conditions (10)
    d3 = 3
    error_keywords = len(re.findall(r'(?:error|错误|失败|fail|fallback|异常|如果.*失败|edge.?case|边界|timeout|超时|回退|回滚|rollback|revert)', body_clean, re.IGNORECASE))
    if error_keywords >= 5: d3 += 3
    elif error_keywords >= 2: d3 += 1
    # Detect structured error/boundary tables (markdown tables with error/fallback columns)
    error_table_rows = len(re.findall(r'\|.*(?:错误|失败|error|回退|fallback|异常|边界).*\|', body_clean, re.IGNORECASE))
    if error_table_rows >= 3: d3 += 3
    elif error_table_rows >= 1: d3 += 1
    # Detect dedicated boundary/error sections
    has_boundary_section = bool(re.search(r'^##\s+.*(?:边界|异常|错误处理|Error|Fallback|边界条件)', body_clean, re.MULTILINE | re.IGNORECASE))
    if has_boundary_section: d3 += 2
    if '```bash' in body_clean or '```python' in body_clean: d3 += 1
    if d3 > 10: d3 = 10

    # D4: Checkpoint design (7)
    d4 = 3
    confirm_keywords = len(re.findall(r'(?:确认|confirm|暂停|pause|检查点|checkpoint|AskUserQuestion|用户确认|等.*确认|询问|approval|approve)', body_clean, re.IGNORECASE))
    if confirm_keywords >= 3: d4 += 3
    elif confirm_keywords >= 1: d4 += 1
    # Detect structured checkpoint/confirmation tables
    checkpoint_table_rows = len(re.findall(r'\|.*(?:确认|检查点|checkpoint|用户确认|AskUserQuestion|暂停).*\|', body_clean, re.IGNORECASE))
    if checkpoint_table_rows >= 2: d4 += 3
    elif checkpoint_table_rows >= 1: d4 += 1
    # Detect dedicated checkpoint sections
    has_checkpoint_section = bool(re.search(r'^##\s+.*(?:检查点|checkpoint|确认|用户确认)', body_clean, re.MULTILINE | re.IGNORECASE))
    if has_checkpoint_section: d4 += 1
    if d4 > 10: d4 = 10

    # D5: Instruction specificity (15)
    d5 = 3
    has_commands = bool(re.search(r'```(?:bash|python|sh)', body_clean))
    has_paths = bool(re.search(r'~?/.*?\.(?:py|js|ts|sh|json|md|yaml)', body_clean))
    has_params = bool(re.search(r'(?:参数|--?\w+|parameter|flag|option)', body_clean, re.IGNORECASE))
    has_examples = body_clean.count('```') >= 2
    if has_commands: d5 += 2
    if has_paths: d5 += 1
    if has_params: d5 += 1
    if has_examples: d5 += 2
    if d5 > 10: d5 = 10

    # D6: Resource integration (5)
    d6 = 3
    has_scripts = os.path.isdir(os.path.join(os.path.dirname(path), 'scripts'))
    has_refs = os.path.isdir(os.path.join(os.path.dirname(path), 'references'))
    mentions_scripts = bool(re.search(r'scripts/', body_clean))
    mentions_refs = bool(re.search(r'references/', body_clean))
    if has_scripts or mentions_scripts: d6 += 2
    if has_refs or mentions_refs: d6 += 2
    if d6 > 10: d6 = 10

    # D7: Overall architecture (15)
    d7 = 4
    has_sections = len(re.findall(r'^##?\s+', body_clean, re.MULTILINE))
    if has_sections >= 4: d7 += 2
    if has_sections >= 8: d7 += 1
    has_table = '|' in body_clean and '---' in body_clean
    if has_table: d7 += 1
    # Penalize bloat
    if word_count < 200: d7 -= 1
    elif word_count > 5000: d7 -= 1
    if d7 > 10: d7 = 10
    if d7 < 1: d7 = 1

    total = round((d1*8 + d2*15 + d3*10 + d4*7 + d5*15 + d6*5 + d7*15) / 10, 1)

    dims = {'D1': d1, 'D2': d2, 'D3': d3, 'D4': d4, 'D5': d5, 'D6': d6, 'D7': d7}
    weakest = min(dims, key=dims.get)
    reasons = {
        'D1': 'frontmatter缺少触发词或description不完整',
        'D2': 'workflow缺少明确步骤或步骤不足',
        'D3': '缺少异常处理或边界条件',
        'D4': '缺少用户确认检查点',
        'D5': '指令模糊，缺少具体参数/示例',
        'D6': 'scripts/references引用缺失',
        'D7': '结构不清晰或过于冗长'
    }

    return {
        'name': name,
        'scores': dims,
        'total': total,
        'weakest': weakest,
        'reason': reasons[weakest],
        'word_count': word_count
    }

# Scan all skills
for entry in sorted(os.listdir(SKILLS_DIR)):
    skill_path = os.path.join(SKILLS_DIR, entry)
    skill_md = os.path.join(skill_path, 'SKILL.md')
    if os.path.isdir(skill_path) and os.path.exists(skill_md):
        r = score_skill(entry, skill_md)
        if r:
            results.append(r)

# Also check root SKILL.md
root_md = os.path.join(SKILLS_DIR, 'SKILL.md')
if os.path.exists(root_md):
    r = score_skill('_root_', root_md)
    if r:
        results.append(r)

# Sort by total ascending (weakest first)
results.sort(key=lambda x: x['total'])

# Output
print(f"{'Skill':<35} {'D1':>3} {'D2':>3} {'D3':>3} {'D4':>3} {'D5':>3} {'D6':>3} {'D7':>3} {'TOTAL':>6} {'Weakest':>4} {'Reason'}")
print('-' * 120)
for r in results:
    s = r['scores']
    print(f"{r['name']:<35} {s['D1']:>3} {s['D2']:>3} {s['D3']:>3} {s['D4']:>3} {s['D5']:>3} {s['D6']:>3} {s['D7']:>3} {r['total']:>6} {r['weakest']:>4} {r['reason']}")

# Bottom 10
print('\n=== BOTTOM 10 (candidates for optimization) ===')
for r in results[:10]:
    s = r['scores']
    print(f"{r['name']:<35} {r['total']:>6} | weakest: {r['weakest']} ({r['reason']})")

# Stats
totals = [r['total'] for r in results]
print(f'\nTotal skills: {len(results)}')
print(f'Average score: {sum(totals)/len(totals):.1f}')
print(f'Min: {min(totals):.1f} | Max: {max(totals):.1f}')
