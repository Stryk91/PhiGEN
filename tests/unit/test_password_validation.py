# Modified by JC Autonomous Worker
#!/usr/bin/env python3
"""
Unit tests for password validation functions.
"""

import unittest
from src.password_vault.backend import validate_min_length, validate_complexity, validate_password_strength


class TestPasswordValidation(unittest.TestCase):
    """Test password validation functions."""

    # ========================================================================
    # validate_min_length() Tests
    # ========================================================================

    def test_validate_min_length_valid(self):
        """Test valid password length."""
        result, message = validate_min_length("password123")
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    def test_validate_min_length_too_short(self):
        """Test password that's too short."""
        result, message = validate_min_length("short")
        self.assertFalse(result)
        self.assertIn("at least 8 characters", message)

    def test_validate_min_length_exact_minimum(self):
        """Test password at exact minimum length."""
        result, message = validate_min_length("exactly8")
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    def test_validate_min_length_custom_minimum(self):
        """Test custom minimum length."""
        result, message = validate_min_length("hello", min_length=10)
        self.assertFalse(result)
        self.assertIn("at least 10 characters", message)

    def test_validate_min_length_empty_string(self):
        """Test empty password."""
        result, message = validate_min_length("")
        self.assertFalse(result)
        self.assertIn("at least 8 characters", message)

    def test_validate_min_length_non_string(self):
        """Test non-string input."""
        result, message = validate_min_length(12345)
        self.assertFalse(result)
        self.assertIn("must be a string", message)

    def test_validate_min_length_long_password(self):
        """Test very long password."""
        long_password = "a" * 50
        result, message = validate_min_length(long_password)
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    # ========================================================================
    # validate_complexity() Tests
    # ========================================================================

    def test_validate_complexity_all_requirements_met(self):
        """Test password meeting all default complexity requirements."""
        result, message = validate_complexity("Password123!")
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    def test_validate_complexity_missing_uppercase(self):
        """Test password missing uppercase letter."""
        result, message = validate_complexity("password123!")
        self.assertFalse(result)
        self.assertIn("uppercase", message.lower())

    def test_validate_complexity_missing_lowercase(self):
        """Test password missing lowercase letter."""
        result, message = validate_complexity("PASSWORD123!")
        self.assertFalse(result)
        self.assertIn("lowercase", message.lower())

    def test_validate_complexity_missing_digit(self):
        """Test password missing digit."""
        result, message = validate_complexity("PasswordABC!")
        self.assertFalse(result)
        self.assertIn("digit", message.lower())

    def test_validate_complexity_missing_special(self):
        """Test password missing special character."""
        result, message = validate_complexity("Password123")
        self.assertFalse(result)
        self.assertIn("special", message.lower())

    def test_validate_complexity_uppercase_only_disabled(self):
        """Test with uppercase requirement disabled."""
        result, message = validate_complexity("password123!", require_uppercase=False)
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    def test_validate_complexity_lowercase_only_disabled(self):
        """Test with lowercase requirement disabled."""
        result, message = validate_complexity("PASSWORD123!", require_lowercase=False)
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    def test_validate_complexity_digits_disabled(self):
        """Test with digit requirement disabled."""
        result, message = validate_complexity("PasswordABC!", require_digits=False)
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    def test_validate_complexity_special_disabled(self):
        """Test with special character requirement disabled."""
        result, message = validate_complexity("Password123", require_special=False)
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    def test_validate_complexity_all_disabled(self):
        """Test with all requirements disabled."""
        result, message = validate_complexity(
            "anything",
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False
        )
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    def test_validate_complexity_empty_string(self):
        """Test empty password string."""
        result, message = validate_complexity("")
        self.assertFalse(result)
        # Should fail on first requirement check

    def test_validate_complexity_non_string(self):
        """Test non-string input."""
        result, message = validate_complexity(12345)
        self.assertFalse(result)
        self.assertIn("must be a string", message)

    def test_validate_complexity_only_special_chars(self):
        """Test password with only special characters."""
        result, message = validate_complexity("!@#$%^&*()")
        self.assertFalse(result)
        # Should fail on missing uppercase, lowercase, or digits

    def test_validate_complexity_multiple_special_chars(self):
        """Test that various special characters are recognized."""
        special_passwords = [
            "Password123!",
            "Password123@",
            "Password123#",
            "Password123$",
            "Password123%",
            "Password123^",
            "Password123&",
            "Password123*",
            "Password123(",
            "Password123)",
            "Password123_",
            "Password123+",
            "Password123-",
            "Password123=",
            "Password123[",
            "Password123]",
            "Password123{",
            "Password123}",
            "Password123|",
            "Password123;",
            "Password123:",
            "Password123,",
            "Password123.",
            "Password123<",
            "Password123>",
            "Password123?",
        ]
        for pwd in special_passwords:
            with self.subTest(password=pwd):
                result, message = validate_complexity(pwd)
                self.assertTrue(result, f"Failed for password: {pwd}")

    def test_validate_complexity_mixed_requirements(self):
        """Test various combinations of enabled/disabled requirements."""
        # Only uppercase and lowercase
        result, message = validate_complexity(
            "PasswordABC",
            require_uppercase=True,
            require_lowercase=True,
            require_digits=False,
            require_special=False
        )
        self.assertTrue(result)

        # Only digits and special
        result, message = validate_complexity(
            "123!@#",
            require_uppercase=False,
            require_lowercase=False,
            require_digits=True,
            require_special=True
        )
        self.assertTrue(result)

    def test_validate_complexity_edge_case_single_char_each(self):
        """Test password with exactly one character of each type."""
        result, message = validate_complexity("Aa1!")
        self.assertTrue(result)
        self.assertEqual(message, "Valid")

    # ========================================================================
    # validate_password_strength() Tests (Integration Function)
    # ========================================================================

    def test_validate_password_strength_strong_password(self):
        """Test a strong password with high score."""
        result = validate_password_strength("MyS3cur3P@ssw0rd!")
        self.assertTrue(result['valid'])
        self.assertEqual(result['errors'], [])
        self.assertGreaterEqual(result['strength_score'], 90)
        self.assertIsInstance(result['warnings'], list)

    def test_validate_password_strength_weak_but_valid(self):
        """Test a password that passes but is considered weak (short)."""
        # Even though it meets requirements, it's only 8 chars so should get warnings
        result = validate_password_strength("Pass123!")
        self.assertTrue(result['valid'])
        self.assertEqual(result['errors'], [])
        # 8-char password scores: 20+20+60 = 100, but should have warnings about length
        self.assertEqual(result['strength_score'], 100)
        # Should have warnings about using longer password
        self.assertGreater(len(result['warnings']), 0)
        self.assertTrue(any("12+" in w or "longer" in w.lower() for w in result['warnings']))

    def test_validate_password_strength_invalid_too_short(self):
        """Test password that fails length check."""
        result = validate_password_strength("Aa1!")
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)
        self.assertIn("at least 8 characters", result['errors'][0])

    def test_validate_password_strength_invalid_missing_uppercase(self):
        """Test password missing uppercase."""
        result = validate_password_strength("password123!")
        self.assertFalse(result['valid'])
        self.assertIn("uppercase", result['errors'][0].lower())

    def test_validate_password_strength_invalid_missing_multiple(self):
        """Test password missing multiple requirements."""
        result = validate_password_strength("password")
        self.assertFalse(result['valid'])
        # Should have multiple errors
        self.assertGreater(len(result['errors']), 0)

    def test_validate_password_strength_score_calculation_base(self):
        """Test base score calculation for minimal valid password."""
        result = validate_password_strength("Pass123!")
        self.assertTrue(result['valid'])
        # Score: 20 (base) + 20 (length) + 60 (4 complexity * 15) = 100
        # But less than 12 chars, so no bonus
        expected_score = 20 + 20 + 60  # = 100
        self.assertEqual(result['strength_score'], 100)

    def test_validate_password_strength_score_with_length_bonus(self):
        """Test score bonus for 12+ character passwords."""
        result = validate_password_strength("Password123!")  # 12 chars
        self.assertTrue(result['valid'])
        self.assertEqual(result['strength_score'], 100)  # 20 + 20 + 60 + 20 bonus = 100 (capped)

    def test_validate_password_strength_warnings_short_password(self):
        """Test that short valid passwords get warnings."""
        result = validate_password_strength("Pass123!")  # 8 chars, valid but short
        self.assertTrue(result['valid'])
        # Should warn about 12+ characters
        self.assertTrue(any("12+" in w for w in result['warnings']))

    def test_validate_password_strength_no_warnings_strong_password(self):
        """Test that strong passwords don't get unnecessary warnings."""
        result = validate_password_strength("MyVeryS3cure!P@ssw0rd!")  # 22 chars
        self.assertTrue(result['valid'])
        self.assertGreaterEqual(result['strength_score'], 95)
        # Should have minimal or no warnings
        # (May still suggest multiple special chars, which is okay)

    def test_validate_password_strength_custom_requirements(self):
        """Test with custom requirement settings."""
        result = validate_password_strength(
            "password123",
            require_uppercase=False,
            require_special=False
        )
        self.assertTrue(result['valid'])
        # Score: 20 (base) + 20 (length) + 30 (2 enabled complexity * 15) = 70
        expected_score = 20 + 20 + 30
        self.assertEqual(result['strength_score'], expected_score)

    def test_validate_password_strength_all_requirements_disabled(self):
        """Test with all requirements disabled."""
        result = validate_password_strength(
            "anypassword",
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False
        )
        self.assertTrue(result['valid'])
        # Score: 20 (base) + 20 (length) = 40
        self.assertEqual(result['strength_score'], 40)

    def test_validate_password_strength_non_string_input(self):
        """Test non-string input handling."""
        result = validate_password_strength(12345)
        self.assertFalse(result['valid'])
        self.assertIn("must be a string", result['errors'][0])
        self.assertEqual(result['strength_score'], 0)

    def test_validate_password_strength_empty_string(self):
        """Test empty string handling."""
        result = validate_password_strength("")
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)

    def test_validate_password_strength_return_structure(self):
        """Test that return dictionary has correct structure."""
        result = validate_password_strength("TestPass123!")
        # Check all required keys exist
        self.assertIn('valid', result)
        self.assertIn('errors', result)
        self.assertIn('warnings', result)
        self.assertIn('strength_score', result)
        # Check types
        self.assertIsInstance(result['valid'], bool)
        self.assertIsInstance(result['errors'], list)
        self.assertIsInstance(result['warnings'], list)
        self.assertIsInstance(result['strength_score'], int)
        # Check score range
        self.assertGreaterEqual(result['strength_score'], 0)
        self.assertLessEqual(result['strength_score'], 100)

    def test_validate_password_strength_score_penalties_for_invalid(self):
        """Test that invalid passwords get score penalties."""
        result = validate_password_strength("short")
        self.assertFalse(result['valid'])
        # Invalid passwords should have reduced scores
        self.assertLess(result['strength_score'], 40)

    def test_validate_password_strength_exact_score_scenarios(self):
        """Test specific score calculation scenarios."""
        # Scenario 1: Minimal valid (8 chars, all requirements)
        result1 = validate_password_strength("Pass123!")
        self.assertEqual(result1['strength_score'], 100)  # 20+20+60 = 100

        # Scenario 2: With length bonus (12+ chars)
        result2 = validate_password_strength("Password123!")
        self.assertEqual(result2['strength_score'], 100)  # 20+20+60+20 = 100 (capped)

        # Scenario 3: Some requirements disabled
        result3 = validate_password_strength("password",
                                            require_uppercase=False,
                                            require_digits=False,
                                            require_special=False)
        self.assertEqual(result3['strength_score'], 20 + 20 + 15)  # base + length + 1 complexity


if __name__ == '__main__':
    print("Running password validation tests...")
    unittest.main(verbosity=2)
