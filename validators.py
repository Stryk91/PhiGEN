#!/usr/bin/env python3
"""
Password Validation Module
Provides password strength validation with comprehensive checks
"""

import re
from typing import Dict, List, Any


def validate_password_strength(password: str) -> Dict[str, Any]:
    """
    Validate password strength against multiple criteria.

    Checks:
    - Minimum 8 characters
    - At least one uppercase letter (A-Z)
    - At least one lowercase letter (a-z)
    - At least one digit (0-9)
    - At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

    Args:
        password: The password string to validate

    Returns:
        Dictionary with:
        - score: int (0-100) indicating strength
        - failed_requirements: list of str describing failures
        - passed: bool indicating if all requirements met

    Example:
        >>> validate_password_strength("Weak123")
        {'score': 60, 'failed_requirements': ['No special character'], 'passed': False}

        >>> validate_password_strength("Strong@Pass123")
        {'score': 100, 'failed_requirements': [], 'passed': True}
    """
    failed_requirements = []
    score = 0

    # Check minimum length (8 chars)
    if len(password) >= 8:
        score += 20
    else:
        failed_requirements.append(f"Minimum 8 characters (currently {len(password)})")

    # Check for uppercase letter
    if re.search(r'[A-Z]', password):
        score += 20
    else:
        failed_requirements.append("At least one uppercase letter (A-Z)")

    # Check for lowercase letter
    if re.search(r'[a-z]', password):
        score += 20
    else:
        failed_requirements.append("At least one lowercase letter (a-z)")

    # Check for digit
    if re.search(r'[0-9]', password):
        score += 20
    else:
        failed_requirements.append("At least one digit (0-9)")

    # Check for special character
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        score += 20
    else:
        failed_requirements.append("At least one special character (!@#$%^&*...)")

    # Bonus points for length > 12
    if len(password) >= 12:
        score = min(100, score + 10)

    # Bonus points for length > 16
    if len(password) >= 16:
        score = min(100, score + 10)

    return {
        'score': score,
        'failed_requirements': failed_requirements,
        'passed': len(failed_requirements) == 0
    }


if __name__ == '__main__':
    # Test cases
    test_passwords = [
        "weak",
        "weakpass",
        "Weakpass",
        "Weakpass1",
        "Weak@123",
        "Strong@Pass123",
        "VeryStrong@Pass123!Extra"
    ]

    print("Password Strength Validator Tests")
    print("=" * 60)

    for pwd in test_passwords:
        result = validate_password_strength(pwd)
        print(f"\nPassword: '{pwd}'")
        print(f"Score: {result['score']}/100")
        print(f"Passed: {result['passed']}")
        if result['failed_requirements']:
            print("Failed requirements:")
            for req in result['failed_requirements']:
                print(f"  - {req}")
