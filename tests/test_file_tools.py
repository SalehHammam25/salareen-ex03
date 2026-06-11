"""Tests for src/tools/file_tools.py — no LLM calls, no API keys needed."""

from __future__ import annotations

import pytest

from src.tools.file_tools import (
    FileToolError,
    append_text,
    ensure_parent_dir,
    read_text,
    write_text,
)


def test_ensure_parent_dir_creates_nested_dirs(tmp_path):
    target = tmp_path / "a" / "b" / "c" / "file.txt"
    result = ensure_parent_dir(target)
    assert result == target
    assert target.parent.is_dir()


def test_ensure_parent_dir_accepts_string(tmp_path):
    target = str(tmp_path / "sub" / "file.txt")
    result = ensure_parent_dir(target)
    assert result.parent.is_dir()


def test_write_text_creates_file(tmp_path):
    p = tmp_path / "out.txt"
    write_text(p, "hello world")
    assert p.read_text(encoding="utf-8") == "hello world"


def test_write_text_creates_parent_dirs(tmp_path):
    p = tmp_path / "deep" / "nested" / "file.txt"
    write_text(p, "content")
    assert p.exists()
    assert p.read_text(encoding="utf-8") == "content"


def test_write_text_overwrites_existing(tmp_path):
    p = tmp_path / "file.txt"
    write_text(p, "first")
    write_text(p, "second")
    assert p.read_text(encoding="utf-8") == "second"


def test_write_text_handles_utf8_content(tmp_path):
    p = tmp_path / "hebrew.txt"
    content = "שלום עולם — Human-in-the-Loop"
    write_text(p, content)
    assert p.read_text(encoding="utf-8") == content


def test_read_text_returns_content(tmp_path):
    p = tmp_path / "input.txt"
    p.write_text("read me", encoding="utf-8")
    assert read_text(p) == "read me"


def test_read_text_raises_on_missing_file(tmp_path):
    with pytest.raises(FileToolError, match="not found"):
        read_text(tmp_path / "nonexistent.txt")


def test_append_text_creates_file_when_missing(tmp_path):
    p = tmp_path / "log.txt"
    append_text(p, "line1\n")
    assert p.read_text(encoding="utf-8") == "line1\n"


def test_append_text_adds_to_existing_content(tmp_path):
    p = tmp_path / "log.txt"
    write_text(p, "line1\n")
    append_text(p, "line2\n")
    assert p.read_text(encoding="utf-8") == "line1\nline2\n"


def test_append_text_creates_parent_dirs(tmp_path):
    p = tmp_path / "nested" / "log.txt"
    append_text(p, "entry")
    assert p.exists()
    assert p.read_text(encoding="utf-8") == "entry"
