"""Task model for todo application."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        title: The main task description (required, non-empty)
        description: Optional detailed information
        is_complete: Completion status (default: False)
        created_at: Task creation timestamp (auto-generated)
    """
    title: str
    description: str = ""
    is_complete: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate and clean task data after initialization."""
        self.title = self.title.strip()
        self.description = self.description.strip()

        if not self.title:
            raise ValueError("Task title cannot be empty")

    def toggle_status(self) -> None:
        """Toggle completion status between complete and incomplete."""
        self.is_complete = not self.is_complete

    def display_status(self) -> str:
        """Return visual status indicator for display."""
        return "✓" if self.is_complete else "✗"

    def __str__(self) -> str:
        """Human-readable string representation."""
        status = self.display_status()
        if self.description:
            return f"[{status}] {self.title}: {self.description}"
        return f"[{status}] {self.title}"
