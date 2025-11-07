#!/usr/bin/env python3
"""
PhiGEN Password Vault - Fully Functional Application
Secure password manager with AES-256 encryption and tactical UI.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QPushButton, QLabel, QLineEdit,
                              QSpinBox, QTextEdit, QDialog, QDialogButtonBox,
                              QMessageBox, QInputDialog, QListWidget, QListWidgetItem)
from PyQt6.QtGui import QPixmap, QIcon, QFont, QClipboard
from PyQt6.QtCore import Qt, QSize, QTimer, pyqtSignal

# Add TEMPSVG to path for resources
sys.path.insert(0, str(Path(__file__).parent / "TEMPSVG"))
import buttons_rc

# Import backend
from password_vault_backend import PasswordVault, PasswordGenerator, PasswordEntry
