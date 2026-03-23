"""Tests for SKILL.md structure: valid YAML frontmatter, required sections."""
from pathlib import Path
import yaml

SKILLS_DIR = Path(__file__).parent.parent
SKILLS = ["pdf", "xlsx", "docx", "pptx"]


def _read_skill(name):
    return (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")


def _parse_frontmatter(content):
    parts = content.split("---", 2)
    assert len(parts) >= 3, "SKILL.md must have YAML frontmatter delimited by ---"
    return yaml.safe_load(parts[1])


def test_yaml_frontmatter_valid():
    """All SKILL.md files must have parseable YAML frontmatter."""
    for skill in SKILLS:
        content = _read_skill(skill)
        fm = _parse_frontmatter(content)
        assert isinstance(fm, dict), f"{skill}/SKILL.md frontmatter should be a dict"
        assert "name" in fm, f"{skill}/SKILL.md frontmatter missing 'name'"


def test_dependencies_section_exists():
    """pdf, xlsx, docx must have a ## Dependencies section."""
    for skill in ["pdf", "xlsx", "docx"]:
        content = _read_skill(skill)
        assert "## Dependencies" in content, f"{skill}/SKILL.md missing ## Dependencies"


def test_markitdown_mentioned():
    """pdf, xlsx, docx must mention markitdown."""
    for skill in ["pdf", "xlsx", "docx"]:
        content = _read_skill(skill)
        assert "markitdown" in content, f"{skill}/SKILL.md missing markitdown reference"


def test_qa_section_exists():
    """pdf, xlsx, docx must have a ## QA section."""
    for skill in ["pdf", "xlsx", "docx"]:
        content = _read_skill(skill)
        assert "## QA" in content, f"{skill}/SKILL.md missing ## QA section"


def test_frontmatter_no_merged_fields():
    """Verify pdf SKILL.md frontmatter no longer has merged version+source field."""
    content = _read_skill("pdf")
    fm = _parse_frontmatter(content)
    version = fm.get("version", "")
    assert "source" not in str(version), \
        "pdf/SKILL.md version field must not contain 'source' (YAML was corrupted)"
