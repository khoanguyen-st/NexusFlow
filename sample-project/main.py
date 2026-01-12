"""
Sample Python Application
This is a sample project for testing NexusFlow AI indexing.
"""

from utils import greet, calculate_sum


def main():
    """Main entry point."""
    name = "NexusFlow"
    print(greet(name))
    
    numbers = [1, 2, 3, 4, 5]
    total = calculate_sum(numbers)
    print(f"Sum of {numbers} = {total}")


if __name__ == "__main__":
    main()
