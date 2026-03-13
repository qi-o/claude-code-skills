#!/usr/bin/env python3
"""
create_skill.py - Enhanced skill scaffolding with multi-platform support and enhanced metadata.

Supports:
- Multi-platform repository sources (GitHub, GitLab, Gitee)
- Enhanced metadata with platform-specific fields
- Mirror tracking for GitHub repositories
- Comprehensive skill structure

Usage:
    python create_skill.py <json_info_file> <output_skills_dir>
    python create_skill.py repo_info.json ~/.config/opencode/skills
"""

import sys

# 配置 UTF-8 输出（解决 Windows GBK 编码问题）
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
        sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')
except (AttributeError, Exception):
    pass

import os
import json
import datetime
import re
from typing import Dict


def sanitize_name(name: str) -> str:
    """
    Convert repository name to kebab-case for skill naming.

    Args:
        name: Original repository name

    Returns:
        Sanitized name in kebab-case
    """
    # Replace spaces and special characters with hyphens
    name = re.sub(r'[^a-zA-Z0-9\-_]+', '-', name)
    # Convert to lowercase
    name = name.lower()
    # Remove consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    # Ensure name is not empty
    if not name:
        name = "unknown-skill"
    return name


def determine_url_field(repo_info: Dict) -> str:
    """
    Determine the appropriate URL field based on platform.

    Args:
        repo_info: Repository information dictionary

    Returns:
        URL field name (github_url, gitlab_url, or gitee_url)
    """
    platform = repo_info.get('platform', 'github')
    url_map = {
        'github': 'github_url',
        'gitlab': 'gitlab_url',
        'gitee': 'gitee_url'
    }
    return url_map.get(platform, 'github_url')


def create_skill(repo_info: Dict, output_dir: str) -> str:
    """
    Create a skill directory structure with enhanced SKILL.md.

    Args:
        repo_info: Repository information from fetch_repo_info.py
        output_dir: Base directory for skills

    Returns:
        Path to created skill directory
    """
    # Extract repository information
    repo_name = repo_info['name']
    platform = repo_info.get('platform', 'github')
    metadata = repo_info.get('metadata', {})

    # Sanitize name for skill directory
    skill_name = sanitize_name(repo_name)
    skill_path = os.path.join(output_dir, skill_name)

    # Determine URL field based on platform
    url_field = determine_url_field(repo_info)

    # Create directory structure
    os.makedirs(os.path.join(skill_path, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(skill_path, "references"), exist_ok=True)
    os.makedirs(os.path.join(skill_path, "assets"), exist_ok=True)

    # Get metadata fields
    stars = metadata.get('stars', 0)
    language = metadata.get('language', 'Unknown')
    mirror_used = metadata.get('mirror_used', 'unknown')
    description = metadata.get('description', f'Skill wrapper for {repo_name}')

    # Extract tags from README content
    readme = repo_info.get('readme', '')
    tags = extract_tags(readme, language)

    # Generate YAML frontmatter
    frontmatter = generate_frontmatter(
        skill_name=skill_name,
        description=description,
        repo_info=repo_info,
        url_field=url_field,
        stars=stars,
        language=language,
        mirror_used=mirror_used,
        tags=tags
    )

    # Generate SKILL.md content
    skill_md_content = frontmatter + generate_skill_content(repo_info, metadata)

    # Write SKILL.md
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write(skill_md_content)

    # Create wrapper script
    create_wrapper_script(skill_path, repo_name)

    # Create .gitkeep for empty directories
    for dir_name in ["references", "assets"]:
        gitkeep_path = os.path.join(skill_path, dir_name, ".gitkeep")
        with open(gitkeep_path, "w") as f:
            f.write("")

    return skill_path


def extract_tags(readme: str, language: str) -> list:
    """
    Extract relevant tags from README content.

    Args:
        readme: README content
        language: Primary programming language

    Returns:
        List of tags
    """
    tags = [language.lower()] if language and language != 'Unknown' else []

    # Common technology keywords to look for
    tech_keywords = [
        'api', 'cli', 'web', 'framework', 'library', 'tool',
        'machine-learning', 'ml', 'ai', 'deep-learning',
        'react', 'vue', 'angular', 'nodejs', 'python',
        'testing', 'automation', 'docker', 'kubernetes',
        'database', 'frontend', 'backend', 'fullstack'
    ]

    readme_lower = readme.lower()
    for keyword in tech_keywords:
        if keyword in readme_lower:
            tags.append(keyword)

    # Deduplicate and limit to 10 tags
    tags = list(set(tags))[:10]

    return tags


def generate_frontmatter(
    skill_name: str,
    description: str,
    repo_info: Dict,
    url_field: str,
    stars: int,
    language: str,
    mirror_used: str,
    tags: list
) -> str:
    """
    Generate YAML frontmatter for SKILL.md.

    Args:
        skill_name: Sanitized skill name
        description: Skill description
        repo_info: Repository information
        url_field: Appropriate URL field for platform
        stars: Repository star count
        language: Primary programming language
        mirror_used: Mirror used for fetching (GitHub)
        tags: Extracted tags

    Returns:
        YAML frontmatter string
    """
    now = datetime.datetime.now().isoformat()

    frontmatter = f"""---
name: {skill_name}
description: {description}
license: {repo_info.get('license', 'unknown')}
{url_field}: {repo_info['url']}
github_hash: {repo_info['latest_hash']}
version: 0.1.0
created_at: {now}
platform: {repo_info.get('platform', 'github')}
source: {repo_info['url']}
stars: {stars}
language: {language}
entry_point: scripts/wrapper.py
dependencies: []
tags: {json.dumps(tags, ensure_ascii=False)}
mirror_used: {mirror_used}
---

"""
    return frontmatter


def generate_skill_content(repo_info: Dict, metadata: Dict) -> str:
    """
    Generate the main content for SKILL.md.

    Args:
        repo_info: Repository information
        metadata: Repository metadata

    Returns:
        SKILL.md content string
    """
    repo_name = repo_info['name']
    qualified_name = repo_info.get('qualified_name', repo_name)
    platform = repo_info.get('platform', 'github').capitalize()
    readme = repo_info.get('readme', '')

    # Get default branch
    default_branch = metadata.get('default_branch', 'main')

    content = f"""# {repo_name} Skill

This skill wraps the capabilities of [{repo_name}]({repo_info['url']}), hosted on {platform}.

## Overview

{metadata.get('description', f'The {repo_name} tool from {qualified_name}.')}

**Repository Statistics:**
- ⭐ Stars: {metadata.get('stars', 0):,}
- 🍴 Forks: {metadata.get('forks', 0):,}
- 💻 Language: {metadata.get('language', 'Unknown')}
- 🌿 Default Branch: {default_branch}

## Quick Start

> **Note**: This is an auto-generated skill. Review the installation and usage instructions below, and refer to the [original repository]({repo_info['url']}) for the most up-to-date information.

### Prerequisites

Ensure you have the following installed:
"""

    # Add platform-specific prerequisites
    language = metadata.get('language', '').lower()
    if 'python' in language:
        content += "- Python 3.8 or higher\n- pip (Python package manager)\n"
    elif 'javascript' in language or 'typescript' in language:
        content += "- Node.js 16 or higher\n- npm, yarn, or pnpm\n"
    elif 'go' in language:
        content += "- Go 1.18 or higher\n"
    elif 'rust' in language:
        content += "- Rust 1.65 or higher\n- Cargo\n"

    content += f"""
### Installation

Follow the installation instructions from the original repository:

"""

    # Add README excerpt if available
    if readme:
        # Try to extract installation section
        install_match = re.search(
            r'##+[ \t]*Installation.*?(?=\n##+|\Z)',
            readme,
            re.DOTALL | re.IGNORECASE
        )
        if install_match:
            content += install_match.group(0).strip() + "\n\n"
        else:
            # Add first 500 chars of README as fallback
            content += f"""
See the [original README]({repo_info['url']}) for detailed installation instructions.

**Excerpt from README:**

```markdown
{readme[:500]}...
```
"""
    else:
        content += f"""
Please refer to the [original repository]({repo_info['url']}) for installation instructions.
"""

    content += """
## Usage

This skill provides a Python wrapper to interface with the tool.

### Basic Usage

"""

    # Try to extract usage examples
    if readme:
        usage_match = re.search(
            r'##+[ \t]*(Usage|Getting Started|Quick Start).*?(?=\n##+|\Z)',
            readme,
            re.DOTALL | re.IGNORECASE
        )
        if usage_match:
            content += usage_match.group(0).strip() + "\n\n"

    content += f"""
### Using the Wrapper

The wrapper script in `scripts/wrapper.py` provides a Python interface to the tool.

```python
from scripts.wrapper import main

# Call the main function
main()
```

## API Reference

"""

    # Try to extract API documentation
    if readme:
        api_match = re.search(
            r'##+[ \t]*(API|API Reference|Documentation).*?(?=\n##+|\Z)',
            readme,
            re.DOTALL | re.IGNORECASE
        )
        if api_match:
            content += api_match.group(0).strip() + "\n\n"
        else:
            content += f"""
For detailed API documentation, please refer to the [original repository]({repo_info['url']}).
"""
    else:
        content += f"""
Please refer to the [original repository]({repo_info['url']}) for API documentation.
"""

    content += f"""
## Configuration

If the tool requires configuration, set up the necessary environment variables or configuration files as specified in the [original documentation]({repo_info['url']}).

## Development

To contribute or modify this skill:

1. **Clone the original repository:**
   ```bash
   git clone {repo_info['url']}
   cd {repo_name}
   ```

2. **Review the implementation:**
   - Check `scripts/wrapper.py` for the wrapper implementation
   - Modify as needed for your use case

3. **Test your changes:**
   ```bash
   python scripts/wrapper.py --help
   ```

## Troubleshooting

### Common Issues

1. **Installation fails**
   - Ensure all prerequisites are installed
   - Check the [original repository's issues]({repo_info['url']}/issues) for similar problems

2. **Import errors**
   - Verify dependencies are correctly installed
   - Check Python/node version compatibility

3. **Performance issues**
   - Refer to the original documentation for optimization tips

## Resources

- **Original Repository**: [{repo_name}]({repo_info['url']})
- **Documentation**: Check the repository's wiki or docs folder
- **Issues**: [{repo_name} Issues]({repo_info['url']}/issues)
- **Contributing**: [{repo_name} Contributing Guide]({repo_info['url']}/blob/{default_branch}/CONTRIBUTING.md)

## Metadata

- **Generated**: {datetime.datetime.now().isoformat()}
- **Source Commit**: {repo_info['latest_hash']}
- **Platform**: {repo_info.get('platform', 'github')}
- **Mirror Used**: {metadata.get('mirror_used', 'N/A')}

---

> **Auto-generated by**: repo-to-skills v2.0.0
> **Source**: {qualified_name} on {platform}
> **Last Updated**: {datetime.datetime.now().strftime('%Y-%m-%d')}
"""
    return content


def create_wrapper_script(skill_path: str, repo_name: str) -> None:
    """
    Create a placeholder wrapper script.

    Args:
        skill_path: Path to skill directory
        repo_name: Repository name
    """
    wrapper_content = f"""#!/usr/bin/env python3
\"\"\"
wrapper.py - Wrapper script for {repo_name}.

This script provides a Python interface to the {repo_name} tool.
Implement the actual invocation logic based on the tool's usage.
\"\"\"

import sys
import subprocess
from typing import List


def main(args: List[str] = None) -> int:
    \"\"\"
    Main entry point for the wrapper.

    Args:
        args: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code
    \"\"\"
    if args is None:
        args = sys.argv[1:]

    # TODO: Implement actual invocation logic here
    # Example implementations for different types of tools:

    # For CLI tools:
    # return subprocess.run(['{repo_name}', *args]).returncode

    # For Python libraries:
    # import {repo_name}
    # {repo_name}.main()

    # For Node.js tools:
    # return subprocess.run(['npx', '{repo_name}', *args]).returncode

    print(f\"This is a placeholder wrapper for {repo_name}.\")
    print(f\"Received args: {{args}}\")
    print(\"\\nTODO: Implement the actual invocation logic in scripts/wrapper.py\")
    return 0


if __name__ == \"__main__\":
    sys.exit(main())
"""

    wrapper_path = os.path.join(skill_path, "scripts", "wrapper.py")
    with open(wrapper_path, "w", encoding="utf-8") as f:
        f.write(wrapper_content)

    # Make wrapper executable on Unix systems
    try:
        os.chmod(wrapper_path, 0o755)
    except (OSError, AttributeError):
        pass  # Windows or no chmod support


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 3:
        print("Usage: python create_skill.py <json_info_file> <output_skills_dir>")
        print("\nExample:")
        print("  python create_skill.py repo_info.json ~/.config/opencode/skills")
        sys.exit(1)

    json_file = sys.argv[1]
    output_dir = sys.argv[2]

    # Read repository info
    with open(json_file, 'r', encoding='utf-8') as f:
        repo_info = json.load(f)

    # Validate repository info
    if 'error' in repo_info:
        print(f"Error: {repo_info['error']}", file=sys.stderr)
        if 'suggestions' in repo_info:
            print("\nSuggestions:", file=sys.stderr)
            for s in repo_info['suggestions']:
                print(f"  - {s}", file=sys.stderr)
        sys.exit(1)

    # Create skill
    try:
        skill_path = create_skill(repo_info, output_dir)

        print(f"✅ Skill created successfully!")
        print(f"   Location: {skill_path}")
        print(f"   Name: {os.path.basename(skill_path)}")
        print(f"   Platform: {repo_info.get('platform', 'github').capitalize()}")
        print(f"   Commit: {repo_info['latest_hash'][:8]}")
        print("\nNext steps:")
        print("1. Review SKILL.md and refine the description")
        print("2. Implement the actual logic in scripts/wrapper.py")
        print("3. Test the skill by invoking it in OpenCode/Claude Code")

    except Exception as e:
        print(f"Error creating skill: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
