"""Tests for Task model."""
import pytest
from datetime import datetime
from src.models import Task


def test_task_creation_with_title_only():
    """Test Task creation with only title."""
    task = Task("Buy milk")
    assert task.title == "Buy milk"
    assert task.description == ""
    assert task.is_complete is False
    assert isinstance(task.created_at, datetime)


def test_task_creation_with_title_and_description():
    """Test Task creation with title and description."""
    task = Task("Buy milk", "From grocery store")
    assert task.title == "Buy milk"
    assert task.description == "From grocery store"
    assert task.is_complete is False


def test_task_empty_title_raises_value_error():
    """Test that empty title raises ValueError."""
    with pytest.raises(ValueError):
        Task("")


def test_task_whitespace_title_raises_value_error():
    """Test that whitespace-only title raises ValueError."""
    with pytest.raises(ValueError):
        Task("   ")
    with pytest.raises(ValueError):
        Task("\t\n")


def test_task_utf8_characters():
    """Test Task with UTF-8 characters (emojis, international)."""
    task = Task("買い物 🛒", "Milk, eggs, bread")
    assert task.title == "買い物 🛒"
    assert task.description == "Milk, eggs, bread"


def test_task_toggle_status():
    """Test Task toggle_status() method."""
    task = Task("Test task")
    assert task.is_complete is False

    task.toggle_status()
    assert task.is_complete is True

    task.toggle_status()
    assert task.is_complete is False


def test_task_display_status():
    """Test Task display_status() method."""
    task = Task("Test task")
    assert task.display_status() == "✗"

    task.toggle_status()
    assert task.display_status() == "✓"


def test_task_str_without_description():
    """Test Task __str__() without description."""
    task = Task("Buy milk")
    assert str(task) == "[✗] Buy milk"


def test_task_str_with_description():
    """Test Task __str__() with description."""
    task = Task("Buy milk", "From store")
    expected = "[✗] Buy milk: From store"
    assert str(task) == expected


def test_task_str_complete_status():
    """Test Task __str__() shows correct status."""
    task = Task("Buy milk")
    task.toggle_status()
    assert str(task) == "[✓] Buy milk"
