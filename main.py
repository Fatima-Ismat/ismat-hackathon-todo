"""Application entry point."""
import sys
from src import cli


def configure_utf8() -> None:
    """Configure console for UTF-8 output (Windows compatibility)."""
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')


def main() -> None:
    """Main application loop."""
    # Configure UTF-8 encoding
    configure_utf8()

    # Print welcome banner (done by display_menu)

    # Main event loop
    while True:
        cli.display_menu()
        choice = cli.get_choice()

        # Route choice and check if should continue
        should_continue = cli.route_choice(choice)

        if not should_continue:
            break

    # Print goodbye message
    print("\nThank you for using Todo Console App!")
    print("Exiting...\n")


if __name__ == "__main__":
    main()
