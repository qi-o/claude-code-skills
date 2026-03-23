"""Tests for pdf script fixes: directory creation and argument validation."""
import subprocess
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).parent.parent / "pdf" / "scripts"


def test_convert_creates_output_dir(tmp_path):
    """convert_pdf_to_images should auto-create a non-existent output directory."""
    import importlib.util
    import os

    script = SCRIPTS_DIR / "convert_pdf_to_images.py"
    spec = importlib.util.spec_from_file_location("convert_pdf_to_images", script)
    mod = importlib.util.module_from_spec(spec)

    # Patch convert_from_path so we don't need a real PDF
    import unittest.mock as mock
    with mock.patch.dict("sys.modules", {"pdf2image": mock.MagicMock()}):
        spec.loader.exec_module(mod)

    output_dir = str(tmp_path / "new_subdir" / "images")
    assert not Path(output_dir).exists()

    # Patch convert_from_path to return empty list (no pages)
    with mock.patch("pdf2image.convert_from_path", return_value=[]):
        mod.convert("fake.pdf", output_dir)

    assert Path(output_dir).exists(), "Output directory should have been created"


def test_check_fillable_fields_no_args():
    """No args should exit non-zero without crashing."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "check_fillable_fields.py")],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_check_fillable_fields_missing_file():
    """Non-existent file should exit non-zero with error on stderr."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "check_fillable_fields.py"), "nonexistent.pdf"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert result.stderr.strip() != ""
