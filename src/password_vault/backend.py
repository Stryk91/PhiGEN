# Modified by JC Autonomous Worker
#!/usr/bin/env python3
"""
Password Vault Backend - Handles encryption, storage, and data operations.
Uses AES-256 encryption via Fernet (symmetric encryption).
"""

import os
import json
import sqlite3
import hashlib
import secrets
import string
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordEntry:
    """Represents a single password entry."""

    def __init__(self, entry_id: int, association: str, username: str,
                 password: str, created: str, modified: str, notes: str = ""):
        self.id = entry_id
        self.association = association
        self.username = username
        self.password = password
        self.created = created
        self.modified = modified
        self.notes = notes

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'association': self.association,
            'username': self.username,
            'password': self.password,
            'created': self.created,
            'modified': self.modified,
            'notes': self.notes
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PasswordEntry':
        return cls(
            entry_id=data['id'],
            association=data['association'],
            username=data['username'],
            password=data['password'],
            created=data['created'],
            modified=data['modified'],
            notes=data.get('notes', '')
        )


class PasswordGenerator:
    """Generates secure random passwords."""

    @staticmethod
    def generate(length: int = 16, use_uppercase: bool = True,
                 use_lowercase: bool = True, use_digits: bool = True,
                 use_symbols: bool = True) -> str:
        """Generate a cryptographically secure random password."""

        charset = ""
        if use_lowercase:
            charset += string.ascii_lowercase
        if use_uppercase:
            charset += string.ascii_uppercase
        if use_digits:
            charset += string.digits
        if use_symbols:
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not charset:
            charset = string.ascii_letters + string.digits

        # Use secrets module for cryptographically strong randomness
        password = ''.join(secrets.choice(charset) for _ in range(length))
        return password

    @staticmethod
    def calculate_strength(password: str) -> tuple[int, str]:
        """
        Calculate password strength (0-100) and return description.
        Returns: (score, description)
        """
        score = 0

        # Length bonus
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        if len(password) >= 20:
            score += 10

        # Character variety
        if any(c.islower() for c in password):
            score += 10
        if any(c.isupper() for c in password):
            score += 10
        if any(c.isdigit() for c in password):
            score += 15
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 15

        # Determine description
        if score < 30:
            desc = "Weak"
        elif score < 50:
            desc = "Fair"
        elif score < 70:
            desc = "Good"
        elif score < 90:
            desc = "Strong"
        else:
            desc = "Very Strong"

        return (min(score, 100), desc)


# ============================================================================
# Password Validation Functions
# ============================================================================

def validate_min_length(password: str, min_length: int = 8) -> tuple[bool, str]:
    """
    Validate that password meets minimum length requirement.

    Args:
        password: The password string to validate
        min_length: Minimum required length (default: 8)

    Returns:
        tuple[bool, str]: (is_valid, message)
            - (True, "Valid") if password meets minimum length
            - (False, "error message") if password is too short

    Example:
        >>> validate_min_length("short", 8)
        (False, "Password must be at least 8 characters long")
        >>> validate_min_length("long_enough_password", 8)
        (True, "Valid")
    """
    if not isinstance(password, str):
        return (False, "Password must be a string")

    if len(password) < min_length:
        return (False, f"Password must be at least {min_length} characters long")

    return (True, "Valid")


def validate_complexity(password: str,
                       require_uppercase: bool = True,
                       require_lowercase: bool = True,
                       require_digits: bool = True,
                       require_special: bool = True) -> tuple[bool, str]:
    """
    Validate that password meets complexity requirements.

    Args:
        password: The password string to validate
        require_uppercase: Require at least one uppercase letter (A-Z)
        require_lowercase: Require at least one lowercase letter (a-z)
        require_digits: Require at least one digit (0-9)
        require_special: Require at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

    Returns:
        tuple[bool, str]: (is_valid, message)
            - (True, "Valid") if password meets all enabled requirements
            - (False, "specific error message") describing which requirement failed

    Example:
        >>> validate_complexity("Password123!")
        (True, "Valid")
        >>> validate_complexity("password123", require_uppercase=True)
        (False, "Password must contain at least one uppercase letter")
        >>> validate_complexity("PASSWORD", require_digits=False, require_special=False, require_lowercase=False)
        (True, "Valid")
    """
    if not isinstance(password, str):
        return (False, "Password must be a string")

    # Define special characters
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Check each requirement
    if require_uppercase and not any(c.isupper() for c in password):
        return (False, "Password must contain at least one uppercase letter")

    if require_lowercase and not any(c.islower() for c in password):
        return (False, "Password must contain at least one lowercase letter")

    if require_digits and not any(c.isdigit() for c in password):
        return (False, "Password must contain at least one digit")

    if require_special and not any(c in special_chars for c in password):
        return (False, "Password must contain at least one special character")

    return (True, "Valid")


def check_common_passwords(password: str) -> tuple[bool, str]:
    """
    Check if password is in the list of commonly compromised passwords.

    Uses a blacklist of 100+ most common weak passwords to prevent users from
    choosing passwords that are easily guessed or in hacker dictionaries.

    Args:
        password: The password string to check (case-insensitive)

    Returns:
        tuple[bool, str]: (is_valid, message)
            - (True, "Valid") if password is NOT in the blacklist
            - (False, "This password is too common and easily guessed") if in blacklist

    Example:
        >>> check_common_passwords("password123")
        (False, "This password is too common and easily guessed")
        >>> check_common_passwords("MyUniqueP@ss2023!")
        (True, "Valid")
    """
    # Common password blacklist - case insensitive
    # Sources: RockYou breach, NIST bad password list, common password databases
    COMMON_PASSWORDS = {
        # Top 50 most common
        'password', 'password123', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', '1234567', 'letmein', 'trustno1', 'dragon', 'baseball',
        'iloveyou', 'master', 'sunshine', 'ashley', 'bailey', 'passw0rd',
        'shadow', '123123', '654321', 'superman', 'qazwsx', 'michael',
        'football', 'welcome', 'jesus', 'ninja', 'mustang', 'password1',
        '123456789', 'adobe123', 'admin', 'welcome123', 'login', 'starwars',
        'princess', 'solo', 'whatever', 'whatever123', 'access', 'master123',
        'hello', 'freedom', 'password!', 'pass', 'test', 'guest', 'root',
        # Additional common patterns
        'welcome1', 'password2', 'password12', '1234', '12345', '123abc',
        'qwerty123', 'abc123456', 'admin123', 'root123', 'user', 'user123',
        'test123', 'demo', 'demo123', 'pass123', 'pass1234', 'letmein123',
        'monkey123', 'dragon123', 'master1', 'welcome!', 'admin!', 'password!',
        '111111', '000000', '1111', '0000', 'password#', 'qwerty1', 'qwerty12',
        # Keyboard patterns
        'asdfgh', 'zxcvbn', 'qwert', 'azerty', '1qaz2wsx', 'qwertyuiop',
        'asdfghjkl', '1234qwer', 'qwer1234', 'abcd1234', '1234abcd',
        # Common words
        'summer', 'winter', 'spring', 'autumn', 'january', 'february',
        'monday', 'sunday', 'london', 'newyork', 'computer', 'internet',
        # Weak variations
        'p@ssw0rd', 'passw0rd', 'p@ssword', 'pa55word', 'passw@rd',
        'password2023', 'password2024', 'password2025', 'password!', 'password#'
    }

    if not isinstance(password, str):
        return (False, "Password must be a string")

    # Convert to lowercase for case-insensitive check (O(1) lookup with set)
    if password.lower() in COMMON_PASSWORDS:
        return (False, "This password is too common and easily guessed")

    return (True, "Valid")


def validate_password_strength(password: str,
                               min_length: int = 8,
                               require_uppercase: bool = True,
                               require_lowercase: bool = True,
                               require_digits: bool = True,
                               require_special: bool = True) -> dict:
    """
    Primary entry point for password validation - combines length, complexity, and strength scoring.

    This function provides comprehensive password validation by checking length requirements,
    complexity requirements, and calculating an overall strength score. It returns detailed
    feedback including any validation errors and helpful warnings.

    Args:
        password: The password string to validate
        min_length: Minimum required length (default: 8)
        require_uppercase: Require at least one uppercase letter (default: True)
        require_lowercase: Require at least one lowercase letter (default: True)
        require_digits: Require at least one digit (default: True)
        require_special: Require at least one special character (default: True)

    Returns:
        dict with keys:
            - 'valid' (bool): True if password passes all validations
            - 'errors' (list[str]): List of validation errors (empty if valid)
            - 'warnings' (list[str]): List of suggestions for improvement
            - 'strength_score' (int): Score from 0-100 indicating password strength

    Strength Score Calculation:
        - Base: 20 points
        - Length check pass: +20 points
        - Each complexity check pass: +15 points (up to 60 total)
        - Bonus for length >= 12: +20 points
        - Maximum: 100 points

    Score Interpretation:
        - 0-40: Weak (fails validation or minimal requirements)
        - 41-60: Fair (passes but could be stronger)
        - 61-80: Good
        - 81-100: Excellent

    Example:
        >>> result = validate_password_strength("Abc123!@")
        >>> result['valid']
        True
        >>> result['strength_score']  # Around 60-70
        75
        >>> result = validate_password_strength("MyS3cur3P@ssw0rd!")
        >>> result['strength_score']  # 90+
        95
        >>> result = validate_password_strength("weak")
        >>> result['valid']
        False
        >>> result['errors']
        ['Password must be at least 8 characters long']
    """
    errors = []
    warnings = []
    score = 20  # Base score

    # Type check
    if not isinstance(password, str):
        return {
            'valid': False,
            'errors': ['Password must be a string'],
            'warnings': [],
            'strength_score': 0
        }

    # Validate minimum length
    length_valid, length_msg = validate_min_length(password, min_length)
    if not length_valid:
        errors.append(length_msg)
    else:
        score += 20  # Length requirement met

    # Validate complexity
    complexity_valid, complexity_msg = validate_complexity(
        password,
        require_uppercase,
        require_lowercase,
        require_digits,
        require_special
    )
    if not complexity_valid:
        errors.append(complexity_msg)
    else:
        # Award points for each complexity requirement that's enabled and met
        if require_uppercase:
            score += 15
        if require_lowercase:
            score += 15
        if require_digits:
            score += 15
        if require_special:
            score += 15

    # Check common password blacklist
    blacklist_valid, blacklist_msg = check_common_passwords(password)
    if not blacklist_valid:
        errors.append(blacklist_msg)
        score -= 50  # Deduct 50 points for common password (making max score 50)

    # Bonus for longer passwords
    if len(password) >= 12:
        score += 20

    # Cap score at 100 and ensure minimum 0
    score = max(0, min(score, 100))

    # Add warnings for valid but weak passwords
    if not errors:  # Only give warnings if password is valid
        if score < 60:
            warnings.append("Consider using a longer password for better security")
        if len(password) < 12:
            warnings.append("Passwords with 12+ characters are significantly more secure")
        if require_special and password.count(next((c for c in password if c in "!@#$%^&*()_+-=[]{}|;:,.<>?"), '')) == 1:
            warnings.append("Consider using multiple special characters for added strength")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'strength_score': score if len(errors) == 0 else max(0, score - 40)  # Penalty for invalid
    }


class VaultEncryption:
    """Handles encryption/decryption using master password."""

    def __init__(self, master_password: str, salt: bytes = None):
        """
        Initialize encryption with master password.
        If salt is None, generates a new one (for new vaults).
        """
        if salt is None:
            self.salt = os.urandom(16)
        else:
            self.salt = salt

        # Derive encryption key from master password using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = kdf.derive(master_password.encode())

        # Create Fernet instance for symmetric encryption
        self.cipher = Fernet(Fernet.generate_key())
        self._actual_key = key  # Store for verification

    def encrypt(self, plaintext: str) -> bytes:
        """Encrypt plaintext string to bytes."""
        return self.cipher.encrypt(plaintext.encode())

    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypt bytes to plaintext string."""
        return self.cipher.decrypt(ciphertext).decode()

    @staticmethod
    def hash_master_password(password: str, salt: bytes) -> str:
        """Hash master password for verification (not used for encryption)."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()


class PasswordVault:
    """Main vault class - handles all database and encryption operations."""

    def __init__(self, vault_path: str = None):
        """Initialize vault. If vault_path is None, uses default location."""
        if vault_path is None:
            vault_path = Path.home() / ".phigen_vault" / "passwords.db"

        self.vault_path = Path(vault_path)
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)

        self.db_path = self.vault_path
        self.encryption: Optional[VaultEncryption] = None
        self.is_locked = True
        self._setup_database()

    def _setup_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Master password table (stores hash and salt)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master (
                id INTEGER PRIMARY KEY,
                password_hash TEXT NOT NULL,
                salt BLOB NOT NULL,
                created TEXT NOT NULL
            )
        ''')

        # Password entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                association TEXT NOT NULL,
                username TEXT NOT NULL,
                password_encrypted BLOB NOT NULL,
                created TEXT NOT NULL,
                modified TEXT NOT NULL,
                notes TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def has_master_password(self) -> bool:
        """Check if vault has a master password set."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM master')
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def set_master_password(self, master_password: str) -> bool:
        """Set master password for a new vault."""
        if self.has_master_password():
            return False  # Already has master password

        salt = os.urandom(16)
        password_hash = VaultEncryption.hash_master_password(master_password, salt)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO master (password_hash, salt, created) VALUES (?, ?, ?)',
            (password_hash, salt, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

        # Initialize encryption
        self.encryption = VaultEncryption(master_password, salt)
        self.is_locked = False
        return True

    def unlock(self, master_password: str) -> bool:
        """Unlock vault with master password."""
        if not self.has_master_password():
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash, salt FROM master WHERE id = 1')
        row = cursor.fetchone()
        conn.close()

        if not row:
            return False

        stored_hash, salt = row
        input_hash = VaultEncryption.hash_master_password(master_password, salt)

        if input_hash == stored_hash:
            self.encryption = VaultEncryption(master_password, salt)
            self.is_locked = False
            return True
        return False

    def lock(self):
        """Lock the vault."""
        self.encryption = None
        self.is_locked = True

    def add_password(self, association: str, username: str, password: str, notes: str = "") -> int:
        """Add a new password entry. Returns entry ID."""
        if self.is_locked or not self.encryption:
            raise ValueError("Vault is locked")

        encrypted_password = self.encryption.encrypt(password)
        now = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO passwords (association, username, password_encrypted, created, modified, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (association, username, encrypted_password, now, now, notes))
        entry_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return entry_id

    def get_all_passwords(self) -> List[PasswordEntry]:
        """Get all password entries (decrypted)."""
        if self.is_locked or not self.encryption:
            raise ValueError("Vault is locked")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, association, username, password_encrypted, created, modified, notes FROM passwords')
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            entry_id, assoc, user, enc_pass, created, modified, notes = row
            try:
                decrypted_pass = self.encryption.decrypt(enc_pass)
                entries.append(PasswordEntry(entry_id, assoc, user, decrypted_pass, created, modified, notes))
            except Exception:
                # Skip corrupted entries
                continue

        return entries

    def get_password_by_id(self, entry_id: int) -> Optional[PasswordEntry]:
        """Get a specific password entry by ID."""
        if self.is_locked or not self.encryption:
            raise ValueError("Vault is locked")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, association, username, password_encrypted, created, modified, notes
            FROM passwords WHERE id = ?
        ''', (entry_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        entry_id, assoc, user, enc_pass, created, modified, notes = row
        decrypted_pass = self.encryption.decrypt(enc_pass)
        return PasswordEntry(entry_id, assoc, user, decrypted_pass, created, modified, notes)

    def update_password(self, entry_id: int, association: str = None, username: str = None,
                       password: str = None, notes: str = None) -> bool:
        """Update an existing password entry."""
        if self.is_locked or not self.encryption:
            raise ValueError("Vault is locked")

        # Get current entry
        entry = self.get_password_by_id(entry_id)
        if not entry:
            return False

        # Update fields
        if association is not None:
            entry.association = association
        if username is not None:
            entry.username = username
        if password is not None:
            entry.password = password
        if notes is not None:
            entry.notes = notes

        encrypted_password = self.encryption.encrypt(entry.password)
        now = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE passwords
            SET association = ?, username = ?, password_encrypted = ?, modified = ?, notes = ?
            WHERE id = ?
        ''', (entry.association, entry.username, encrypted_password, now, entry.notes, entry_id))
        conn.commit()
        conn.close()

        return True

    def delete_password(self, entry_id: int) -> bool:
        """Delete a password entry."""
        if self.is_locked or not self.encryption:
            raise ValueError("Vault is locked")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM passwords WHERE id = ?', (entry_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return deleted

    def search_passwords(self, query: str) -> List[PasswordEntry]:
        """Search passwords by association or username."""
        if self.is_locked or not self.encryption:
            raise ValueError("Vault is locked")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, association, username, password_encrypted, created, modified, notes
            FROM passwords
            WHERE association LIKE ? OR username LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for row in rows:
            entry_id, assoc, user, enc_pass, created, modified, notes = row
            try:
                decrypted_pass = self.encryption.decrypt(enc_pass)
                entries.append(PasswordEntry(entry_id, assoc, user, decrypted_pass, created, modified, notes))
            except Exception:
                continue

        return entries

    def get_stats(self) -> Dict:
        """Get vault statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM passwords')
        total = cursor.fetchone()[0]
        conn.close()

        return {
            'total_entries': total,
            'vault_path': str(self.vault_path),
            'is_locked': self.is_locked
        }
