"""CLI menu and I/O handling."""
import sys
from src import services


def display_menu() -> None:
    """Print main menu options."""
    print("\n" + "="*32)
    print("    TODO CONSOLE APP - v1.0")
    print("="*32)
    print("\nMain Menu:")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Exit")


def get_choice() -> str:
    """Get and validate user menu selection."""
    choice = input("\nEnter your choice (1-6): ").strip()
    return choice


def display_tasks(tasks: list) -> None:
    """
    Format and print task list with IDs.

    Args:
        tasks: List of Task objects to display
    """
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task}")


def handle_add_task() -> None:
    """Add task flow: prompt inputs, call service, display result."""
    print("\n--- Add New Task ---")

    # Prompt for title
    title = input("Enter task title: ").strip()

    # Prompt for optional description
    description = input("Enter description (optional): ").strip()

    # Call service
    success, message, task = services.add_task(title, description)

    # Display result
    print(f"\n{message}")


def handle_view_tasks() -> None:
    """View tasks flow: call service, display tasks."""
    print("\n--- All Tasks ---")

    # Call service
    success, message, tasks = services.view_all_tasks()

    if not success:
        # No tasks found
        print(f"\n{message}")
    else:
        # Display all tasks
        display_tasks(tasks)


def handle_update_task() -> None:
    """Update task flow: display tasks, prompt for ID and new values."""
    print("\n--- Update Task ---")

    # Get all tasks first
    success, message, tasks = services.view_all_tasks()

    if not success:
        # No tasks found
        print(f"\n{message}")
        return

    # Display all tasks
    display_tasks(tasks)

    # Prompt for task number
    user_input = input("\nEnter task number to update (or press Enter to cancel): ").strip()

    # Check if user wants to cancel
    if not user_input:
        print("\nCancelled.")
        return

    # Validate input is a number
    try:
        user_id = int(user_input)
    except ValueError:
        print("\nError: Please enter a valid number")
        return

    # Convert user ID to index
    task_index = services.user_id_to_index(user_id)

    # Validate index before prompting for updates
    if task_index < 0 or task_index >= services.get_task_count():
        print("\nError: Invalid task number")
        return

    # Get current task to show current values
    current_task = tasks[task_index]

    # Prompt for new title
    print(f"\nCurrent title: {current_task.title}")
    new_title = input("Enter new title (or press Enter to keep current): ").strip()

    # Prompt for new description
    print(f"Current description: {current_task.description}")
    new_description = input("Enter new description (or press Enter to keep current): ").strip()

    # Determine what to update
    title_to_update = new_title if new_title else None
    description_to_update = new_description if new_description else None

    # Call service to update
    success, message, task = services.update_task(
        task_index,
        title=title_to_update,
        description=description_to_update
    )

    # Display result
    print(f"\n{message}")


def handle_delete_task() -> None:
    """Delete task flow: display tasks, prompt for ID, confirm, delete."""
    print("\n--- Delete Task ---")

    # Get all tasks first
    success, message, tasks = services.view_all_tasks()

    if not success:
        # No tasks found
        print(f"\n{message}")
        return

    # Display all tasks
    display_tasks(tasks)

    # Prompt for task number
    user_input = input("\nEnter task number to delete (or press Enter to cancel): ").strip()

    # Check if user wants to cancel
    if not user_input:
        print("\nCancelled.")
        return

    # Validate input is a number
    try:
        user_id = int(user_input)
    except ValueError:
        print("\nError: Please enter a valid number")
        return

    # Convert user ID to index
    task_index = services.user_id_to_index(user_id)

    # Validate index
    if task_index < 0 or task_index >= services.get_task_count():
        print("\nError: Invalid task number")
        return

    # Get task to show for confirmation
    task_to_delete = tasks[task_index]

    # Ask for confirmation
    print(f"\nAre you sure you want to delete: {task_to_delete.title}?")
    confirmation = input("Type 'yes' to confirm: ").strip().lower()

    if confirmation != "yes":
        print("\nCancelled.")
        return

    # Call service to delete
    success, message, task = services.delete_task(task_index)

    # Display result
    print(f"\n{message}")


def handle_toggle_status() -> None:
    """Toggle task status flow: display tasks, prompt for ID, toggle status."""
    print("\n--- Toggle Task Status ---")

    # Get all tasks first
    success, message, tasks = services.view_all_tasks()

    if not success:
        # No tasks found
        print(f"\n{message}")
        return

    # Display all tasks with current status
    display_tasks(tasks)

    # Prompt for task number
    user_input = input("\nEnter task number to toggle (or press Enter to cancel): ").strip()

    # Check if user wants to cancel
    if not user_input:
        print("\nCancelled.")
        return

    # Validate input is a number
    try:
        user_id = int(user_input)
    except ValueError:
        print("\nError: Please enter a valid number")
        return

    # Convert user ID to index
    task_index = services.user_id_to_index(user_id)

    # Call service to toggle
    success, message, task = services.toggle_task_status(task_index)

    # Display result
    print(f"\n{message}")


def route_choice(choice: str) -> bool:
    """
    Route menu choice to appropriate handler.

    Args:
        choice: User's menu selection

    Returns:
        bool: True to continue loop, False to exit
    """
    if choice == "1":
        handle_add_task()
        return True
    elif choice == "2":
        handle_view_tasks()
        return True
    elif choice == "3":
        handle_update_task()
        return True
    elif choice == "4":
        handle_delete_task()
        return True
    elif choice == "5":
        handle_toggle_status()
        return True
    elif choice == "6":
        return False  # Exit
    else:
        print("\nInvalid choice. Please enter 1-6.")
        return True
