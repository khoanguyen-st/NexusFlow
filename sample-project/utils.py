"""
Utility Functions
Collection of helper functions for the sample project.
"""

from typing import List


def greet(name: str) -> str:
    """
    Generate a greeting message.
    
    Args:
        name: The name to greet
        
    Returns:
        Greeting message string
    """
    return f"Hello, {name}! Welcome to NexusFlow AI."


def calculate_sum(numbers: List[int]) -> int:
    """
    Calculate the sum of a list of numbers.
    
    Args:
        numbers: List of integers to sum
        
    Returns:
        Sum of all numbers
    """
    return sum(numbers)


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a number as currency.
    
    Args:
        amount: The amount to format
        currency: Currency code (default: USD)
        
    Returns:
        Formatted currency string
    """
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"
