#!/usr/bin/env python3
"""Sync Claude Code skills and config to GitHub repos.

Cross-platform (Windows/macOS/Linux). Single entry point, no rsync dependency.
Usage: python sync_to_github.py [--skills-only] [--config-only] [--dry-run]
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
SKILLS_SRC = HOME / ".claude" / "skills"
SKILLS_DST = HOME / "claude-code-skills"
CONFIG_SRC = HOME / ".claude"
CONFIG_DST = HOME / "claude-code-config"

CONFIG_FILES = ["CLAUDE.md", "settings.json"]
CONFIG_DIRS = ["agents", "commands", "hooks", "plugins", "rules"]

# Directories to never copy (matched against any path component)
EXCLUDE_DIR_NAMES = {
    ".git", ".experimental", ".omc", "node_modules", "__pycache__",
    ".curated", ".system", ".pytest_cache", "tests", "env.d",
}

# plugins/cache contains marketplace downloads (thousands of files, reproducible)
EXCLUDE_SUBDIRS = {
    (CONFIG_DST, "plugins", "cache"),
}

SECRET_PATTERNS = [
    (re.compile(r'"sk-[a-zA-Z0-9_-]{20,}"'), '"YOUR_API_KEY_HERE"'),
    (re.compile(r'"ghp_[a-zA-Z0-9_-]{36,}"'), '"YOUR_GITHUB_TOKEN_HERE"'),
    (re.compile(r'"github_pat_[a-zA-Z0-9_-]{20,}"'), '"YOUR_GITHUB_TOKEN_HERE"'),
    (re.compile(r'"xox[bors]-[a-zA-Z0-9-]+"'), '"YOUR_SLACK_TOKEN_HERE"'),
]


def is_excluded_subdir(path: Path) -> bool:
    """Check if path matches an excluded subdirectory pattern."""
    try:
        rel = path.relative_to(CONFIG_DST)
        parts = rel.parts
        for pattern in EXCLUDE_SUBDIRS:
            if parts[:len(pattern)] == pattern:
                return True
    except ValueError:
        pass
    return False


def mirror_tree(src: Path, dst: Path, dry_run: bool = False) -> list[str]:
    """Mirror src directory into dst. Returns list of change descriptions.

    When dry_run is True, computes what would change without touching the filesystem.
    """
    changes = []
    if not dry_run:
        dst.mkdir(parents=True, exist_ok=True)

    # Collect source items (respecting excludes)
    src_names = set()
    if src.exists():
        for item in src.iterdir():
            if item.name in EXCLUDE_DIR_NAMES:
                continue
            src_names.add(item.name)

    # Remove dst items not present in src (never touch .git)
    if dst.exists():
        for item in dst.iterdir():
            if item.name == ".git" or item.name in src_names:
                continue
            if dry_run:
                changes.append(f"would remove {item.name}")
                continue
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                changes.append(f"removed {item.name}")
            except PermissionError:
                if item.is_dir():
                    for root, dirs, files in os.walk(item, topdown=False):
                        dirs[:] = [d for d in dirs if d != ".git"]
                        for f in files:
                            try:
                                os.remove(os.path.join(root, f))
                            except (PermissionError, OSError):
                                pass
                    changes.append(f"removed {item.name} (partial)")
                else:
                    changes.append(f"skipped {item.name} (locked)")

    # Copy source items to dst
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".omc")
    for name in src_names:
        if dry_run:
            changes.append(f"would sync {name}")
            continue
        s, d = src / name, dst / name
        if s.is_dir():
            if d.exists():
                shutil.rmtree(d, ignore_errors=True)
            shutil.copytree(s, d, ignore=ignore, dirs_exist_ok=True)
            changes.append(f"synced {name}/")
        else:
            shutil.copy2(s, d)
            changes.append(f"synced {name}")

    return changes


def strip_nested_git_dirs(root: Path):
    """Remove .git directories anywhere under root except root/.git itself.

    This prevents 'not a git repository' errors from skills/plugins that
    have their own .git directories (e.g. cloned skills, marketplace cache).
    """
    removed = 0
    for dirpath, dirnames, _ in os.walk(root):
        for d in dirnames:
            if d == ".git" and Path(dirpath) != root:
                target = Path(dirpath) / d
                shutil.rmtree(target, ignore_errors=True)
                removed += 1
    if removed:
        print(f"  Cleaned {removed} nested .git directories")


def clean_secrets(file_path: Path) -> bool:
    """Scrub secret tokens from a file in-place. Returns True if changed."""
    if not file_path.exists():
        return False
    content = file_path.read_text(encoding="utf-8")
    original = content
    for pattern, replacement in SECRET_PATTERNS:
        content = pattern.sub(replacement, content)
    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False


def git_has_changes(repo: Path) -> bool:
    """Check if a git repo has staged or unstaged changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo, capture_output=True, text=True, timeout=30,
    )
    return bool(result.stdout.strip())


def git_commit(repo: Path, message: str):
    """Stage all and commit. Returns True on success, None if nothing to commit, False on error."""
    add_result = subprocess.run(
        ["git", "add", "-A"], cwd=repo, capture_output=True, text=True, timeout=60,
    )
    if add_result.returncode != 0:
        print(f"  [WARN] git add failed: {add_result.stderr.strip()}")
        return False
    # Check if there are actual staged changes
    diff_check = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo, capture_output=True, text=True, timeout=30,
    )
    if diff_check.returncode == 0:
        return None  # nothing to commit
    result = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=repo, capture_output=True, text=True, timeout=30,
    )
    return result.returncode == 0


def ensure_repo(path: Path, name: str) -> bool:
    """Verify a git repo exists at path."""
    if (path / ".git").is_dir():
        return True
    print(f"  [ERROR] {name} not found at {path}")
    print(f"  Fix: git clone <your-remote> {path}")
    return False


def build_commit_msg(label: str, changes: list[str]) -> str:
    """Build a concise commit message from change list."""
    date = datetime.now().strftime("%Y-%m-%d")
    lines = [f"{label} {date}"]
    # Show up to 15 changes, group if too many
    if len(changes) <= 15:
        for c in changes:
            lines.append(f"- {c}")
    else:
        for c in changes[:10]:
            lines.append(f"- {c}")
        lines.append(f"- ... and {len(changes) - 10} more")
    return "\n".join(lines)


def sync_skills(dry_run: bool = False) -> bool:
    """Sync skills repo. Returns True if changes were detected."""
    print("\n[Skills]")
    changes = mirror_tree(SKILLS_SRC, SKILLS_DST, dry_run=dry_run)
    if not dry_run:
        strip_nested_git_dirs(SKILLS_DST)
    if changes:
        for c in changes:
            print(f"  {c}")
    else:
        print("  No changes")
    return bool(changes)


def sync_config(dry_run: bool = False) -> bool:
    """Sync config repo. Returns True if changes were detected."""
    print("\n[Config]")
    changes = []

    # Individual files
    for f in CONFIG_FILES:
        src_f = CONFIG_SRC / f
        dst_f = CONFIG_DST / f
        if src_f.exists():
            if dry_run:
                changes.append(f"would sync {f}")
            else:
                dst_f.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_f, dst_f)
                changes.append(f"synced {f}")

    # Directories
    for d in CONFIG_DIRS:
        src_d = CONFIG_SRC / d
        dst_d = CONFIG_DST / d
        if not src_d.exists():
            continue
        dir_changes = mirror_tree(src_d, dst_d, dry_run=dry_run)
        changes.extend(dir_changes)

    # Exclude plugins/cache from tracking
    cache_dir = CONFIG_DST / "plugins" / "cache"
    if cache_dir.exists() and not dry_run:
        gitignore = CONFIG_DST / ".gitignore"
        content = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
        if "plugins/cache" not in content:
            if content and not content.endswith("\n"):
                content += "\n"
            content += "plugins/cache/\n"
            gitignore.write_text(content, encoding="utf-8")
            changes.append("updated .gitignore (plugins/cache)")

    # Clean secrets
    if not dry_run:
        settings = CONFIG_DST / "settings.json"
        if clean_secrets(settings):
            changes.append("cleaned secrets in settings.json")

    if changes:
        for c in changes:
            print(f"  {c}")
    else:
        print("  No changes")
    return bool(changes)


def main():
    parser = argparse.ArgumentParser(description="Sync skills and config to GitHub repos")
    parser.add_argument("--skills-only", action="store_true", help="Only sync skills repo")
    parser.add_argument("--config-only", action="store_true", help="Only sync config repo")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without committing")
    args = parser.parse_args()

    print("=" * 50)
    print("sync-to-github")
    print("=" * 50)

    # Verify repos (only check what will be synced)
    print("\n[1/3] Checking repos...")
    if not args.config_only and not ensure_repo(SKILLS_DST, "claude-code-skills"):
        return 1
    if not args.skills_only and not ensure_repo(CONFIG_DST, "claude-code-config"):
        return 1

    # Sync
    print("\n[2/3] Syncing files...")
    skills_changed = False
    config_changed = False

    if not args.config_only:
        skills_changed = sync_skills(dry_run=args.dry_run)
    if not args.skills_only:
        config_changed = sync_config(dry_run=args.dry_run)

    if args.dry_run:
        print("\n[dry-run] No commits made.")
        return 0

    # Commit
    print("\n[3/3] Committing...")
    commits = 0

    if skills_changed:
        changes = []
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-status", "--diff-filter=ADMR"],
            cwd=SKILLS_DST, capture_output=True, text=True, timeout=30,
        )
        # Fall back to status if no staged changes yet
        if not result.stdout.strip():
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=SKILLS_DST, capture_output=True, text=True, timeout=30,
            )
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                # Extract filename from status line
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    changes.append(parts[1])

        msg = build_commit_msg("sync skills", changes[:20])
        result = git_commit(SKILLS_DST, msg)
        if result is True:
            print("  [OK] claude-code-skills committed")
            commits += 1
        elif result is None:
            print("  claude-code-skills: up to date (no changes)")
        else:
            print("  [FAIL] claude-code-skills commit failed")
    else:
        print("  claude-code-skills: up to date")

    if config_changed:
        changes = []
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=CONFIG_DST, capture_output=True, text=True, timeout=30,
        )
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    changes.append(parts[1])

        msg = build_commit_msg("sync config", changes[:20])
        result = git_commit(CONFIG_DST, msg)
        if result is True:
            print("  [OK] claude-code-config committed")
            commits += 1
        elif result is None:
            print("  claude-code-config: up to date (no changes)")
        else:
            print("  [FAIL] claude-code-config commit failed")
    else:
        print("  claude-code-config: up to date")

    # Summary
    print("\n" + "=" * 50)
    if commits:
        print(f"Done. {commits} repo(s) committed.")
        print("Push via GitHub Desktop when ready.")
    else:
        print("Done. Everything up to date.")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
