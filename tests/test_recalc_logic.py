"""Unit tests for recalc.py logic bug fix (or -> and)."""


def test_real_error_passes_through():
    """修复前：真实错误被误判为宏配置错误。修复后：真实错误应原样返回。"""
    error_msg = "Error: permission denied opening file"
    is_macro_error = "Module1" in error_msg and "RecalculateAndSave" not in error_msg
    assert not is_macro_error, "真实错误不应被误判为宏配置错误"


def test_macro_error_detected():
    """宏配置错误应被正确识别。"""
    error_msg = "Module1 not found in Basic library"
    is_macro_error = "Module1" in error_msg and "RecalculateAndSave" not in error_msg
    assert is_macro_error


def test_macro_error_with_recalculate_not_flagged():
    """包含 RecalculateAndSave 的消息不应被视为宏配置错误。"""
    error_msg = "Module1 RecalculateAndSave failed"
    is_macro_error = "Module1" in error_msg and "RecalculateAndSave" not in error_msg
    assert not is_macro_error


def test_old_or_logic_was_broken():
    """证明旧的 or 逻辑确实有 bug。"""
    error_msg = "Error: permission denied opening file"
    old_broken = "Module1" in error_msg or "RecalculateAndSave" not in error_msg
    assert old_broken, "旧逻辑对真实错误也返回 True（这就是 bug）"


def test_file_lock_error_passes_through():
    """文件锁定错误不应被误判为宏配置错误。"""
    error_msg = "Error: file is locked by another process"
    is_macro_error = "Module1" in error_msg and "RecalculateAndSave" not in error_msg
    assert not is_macro_error


def test_empty_error_not_macro_error():
    """空错误消息不应被视为宏配置错误。"""
    error_msg = ""
    is_macro_error = "Module1" in error_msg and "RecalculateAndSave" not in error_msg
    assert not is_macro_error
