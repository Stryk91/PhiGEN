#!/usr/bin/env python3
"""
PhiGEN Password Vault - IMPROVED RESPONSIVE VERSION
Same functionality and visual design, but with better layout management for proper resizing
"""

import os

# *** DPI FIX - MUST BE FIRST, BEFORE ANY Qt IMPORTS ***
# Prevent Windows DPI scaling from affecting window size
# This ensures window opens at exactly 1125×740 pixels regardless of display scaling
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"

import sys
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QGridLayout, QPushButton, QLabel, QLineEdit,
                              QSpinBox, QMessageBox, QInputDialog, QFileDialog,
                              QListWidget, QListWidgetItem, QSizePolicy)
from PyQt6.QtGui import QPixmap, QIcon, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QSize, QTimer, QPoint

# Import the compiled resource file
sys.path.insert(0, str(Path(__file__).parent / "TEMPSVG"))
import buttons_rc

# Add parent directory to path for backend import
sys.path.insert(0, str(Path(__file__).parent.parent))

# Backend import
try:
    from .backend import PasswordVault, PasswordGenerator
except ImportError:
    from password_vault.backend import PasswordVault, PasswordGenerator


class PasswordVaultComplete(QMainWindow):
    def __init__(self):
        super().__init__()

        # Frameless window for custom dark title bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # For window dragging
        self.dragging = False
        self.drag_position = QPoint()

        self.setWindowTitle("PhiGEN Password Vault - Improved Responsive")

        # Get the absolute path to the TEMPSVG directory (for background image)
        self.assets_dir = Path(__file__).parent

        # Set subtle circuit board background (opacity increased by 5%)
        background_path = str(self.assets_dir / "circuit_background_opacity_15.png").replace("\\", "/")
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #0a0a0a;
                background-image: url({background_path});
                background-repeat: no-repeat;
                background-position: center center;
            }}
        """)

        # Set window size constraints - locked to 1125×740 minimum
        # Default/initial window size: 1125×740
        self.resize(1125, 740)

        # Minimum window size: 1125×740 (cannot be resized smaller)
        self.setMinimumSize(1125, 740)

        # Maximum window size: Unrestricted (can grow larger)
        self.setMaximumSize(16777215, 16777215)

        # Enable resize grip for making window larger
        self.statusBar().setSizeGripEnabled(True)

        # Backend instance
        self.vault = PasswordVault()

        # Auto-lock timer (5 minutes)
        self.auto_lock_timer = QTimer()
        self.auto_lock_timer.timeout.connect(self.auto_lock)
        self.auto_lock_timer.setInterval(300000)  # 5 minutes

        # Clipboard clear timer
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.clear_clipboard)

        # Store current entries for retrieval
        self.current_entries = []

        # Build UI first
        self.setup_ui()

        # Then handle master password flow
        self.initialize_master_flow()

        # Initial list load (if unlocked)
        self.refresh_password_list()

        # Start auto-lock timer if unlocked
        if not self.vault.is_locked:
            self.auto_lock_timer.start()

    def setup_ui(self):
        """Setup main UI with IMPROVED layouts."""
        central = QWidget()
        # *** IMPROVED: Set size policy for proper expansion ***
        central.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        # *** OPTIMIZED: Reduced spacing to prevent clipping ***
        main_layout.setSpacing(6)  # Reduced from 8
        main_layout.setContentsMargins(12, 10, 12, 10)  # Reduced margins

        # Custom title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 255, 0, 0.15);
                border-bottom: 2px solid #00ff00;
            }
        """)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 0, 10, 0)

        # Title text
        self.title_label_bar = QLabel("⚡ PhiGEN PASSWORD VAULT ⚡")
        self.title_label_bar.setFont(QFont("Xirod", 12, QFont.Weight.Bold))
        self.title_label_bar.setStyleSheet("color: #00ff00;")
        title_bar_layout.addWidget(self.title_label_bar)

        title_bar_layout.addStretch()

        # Window control buttons
        minimize_btn = QPushButton("_")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 0, 0.2);
                color: #00ff00;
                border: 1px solid #00ff00;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 0.3);
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)

        close_btn = QPushButton("X")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 0.2);
                color: #ff0000;
                border: 1px solid #ff0000;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.4);
            }
        """)
        close_btn.clicked.connect(self.close)

        title_bar_layout.addWidget(minimize_btn)
        title_bar_layout.addWidget(close_btn)

        main_layout.addWidget(title_bar)

        # Title - Fixed height with high-res scaling
        title_label = QLabel()
        # Load BLENDED title image
        blended_pixmap = QPixmap(str(self.assets_dir / "PHIGEN_TITLE_BLENDED.png"))
        if not blended_pixmap.isNull():
            # Scale to appropriate display size using Qt's high-quality transformation
            display_height = 100  # Display height for title
            aspect_ratio = blended_pixmap.width() / blended_pixmap.height()
            display_width = int(display_height * aspect_ratio)

            display_pixmap = blended_pixmap.scaled(
                display_width,
                display_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            title_label.setPixmap(display_pixmap)
        else:
            # Fallback to old title if blended one not found
            title_pixmap = QPixmap(":/ui/title_password_vault_ultra_smooth.png")
            title_label.setPixmap(title_pixmap)

        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setScaledContents(False)
        # *** IMPROVED: Fixed vertical size policy ***
        title_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        # *** STRETCH FACTOR 0: Title never shrinks ***
        main_layout.addWidget(title_label, 0)

        # Input section
        inputs_layout = QVBoxLayout()
        # *** OPTIMIZED: Reduced spacing to save vertical space ***
        inputs_layout.setSpacing(4)

        # Association input
        assoc_label = QLabel("Association (e.g., gmail.com):")
        assoc_label.setStyleSheet("color: #6fff4a; font-size: 11px;")
        # *** IMPROVED: Minimum vertical size policy ***
        assoc_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        inputs_layout.addWidget(assoc_label)

        self.assoc_input = QLineEdit()
        self.assoc_input.setPlaceholderText("Website or service name")
        # *** OPTIMIZED: Reduced height from 50px to 40px ***
        self.assoc_input.setMinimumHeight(40)
        self.assoc_input.setMaximumHeight(40)
        # *** IMPROVED: Expanding horizontal, fixed vertical ***
        self.assoc_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.assoc_input.textChanged.connect(self.reset_auto_lock_timer)
        self.assoc_input.setStyleSheet(f"""
            QLineEdit {{
                border-image: url({self.assets_dir / 'text_input_9slice_ultra_smooth.png'}) 20 20 20 20 stretch;
                padding: 8px 40px;
                background-color: rgba(10, 15, 10, 0.95);
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 13px;
            }}
            QLineEdit::placeholder {{ color: rgba(57, 255, 20, 0.3); }}
        """)
        inputs_layout.addWidget(self.assoc_input)

        # Username input
        user_label = QLabel("Username / Email:")
        user_label.setStyleSheet("color: #6fff4a; font-size: 11px;")
        user_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        inputs_layout.addWidget(user_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or email address")
        # *** OPTIMIZED: Reduced height from 50px to 40px ***
        self.username_input.setMinimumHeight(40)
        self.username_input.setMaximumHeight(40)
        # *** IMPROVED: Expanding horizontal, fixed vertical ***
        self.username_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.username_input.textChanged.connect(self.reset_auto_lock_timer)
        self.username_input.setStyleSheet(self.assoc_input.styleSheet())
        inputs_layout.addWidget(self.username_input)

        # Password input with show/hide button
        pass_label = QLabel("Password:")
        pass_label.setStyleSheet("color: #6fff4a; font-size: 11px;")
        pass_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        inputs_layout.addWidget(pass_label)

        password_row = QHBoxLayout()
        password_row.setSpacing(8)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Generated password will appear here")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        # *** OPTIMIZED: Reduced height from 50px to 40px ***
        self.password_input.setMinimumHeight(40)
        self.password_input.setMaximumHeight(40)
        # *** IMPROVED: Expanding horizontal to fill space ***
        self.password_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.password_input.textChanged.connect(self.on_password_changed)
        self.password_input.setStyleSheet(self.assoc_input.styleSheet())
        password_row.addWidget(self.password_input)

        # Show/Hide button - Fixed size (match input height)
        # Uses lock/unlock icons to match PhiGEN's aesthetic
        self.show_hide_btn = QPushButton()
        # *** OPTIMIZED: Match input field height ***
        self.show_hide_btn.setFixedSize(40, 40)
        # *** IMPROVED: Fixed size policy ***
        self.show_hide_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # Set icon paths for toggle
        self.lock_icon_path = str(self.assets_dir / "icon_locked.png")
        self.unlock_icon_path = str(self.assets_dir / "icon_unlocked.png")
        # Start with unlock icon (password visible by default for password manager)
        self.show_hide_btn.setIcon(QIcon(self.unlock_icon_path))
        self.show_hide_btn.setIconSize(QSize(32, 32))
        self.show_hide_btn.clicked.connect(self.toggle_password_visibility)
        self.show_hide_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                border: 2px solid #39ff14;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: rgba(57, 255, 20, 0.2); }
        """)
        password_row.addWidget(self.show_hide_btn)
        inputs_layout.addLayout(password_row)

        # Password strength indicator
        self.strength_label = QLabel("")
        # *** FIX 1: Remove any potential borders/underlines ***
        self.strength_label.setStyleSheet("color: #6fff4a; font-size: 10px; font-style: italic; border: none; text-decoration: none;")
        self.strength_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        inputs_layout.addWidget(self.strength_label)

        # *** FIX 1: Add small spacer to visually separate password section from length section ***
        inputs_layout.addSpacing(8)

        # Password length row - NOW WITH GENERATE AND SAVE BUTTONS
        # *** TASK 2: Move Generate/Save buttons to this row to save vertical space ***
        length_layout = QHBoxLayout()
        length_layout.setSpacing(10)
        # *** FIX 1: Set alignment to prevent visual artifacts ***
        length_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        length_label = QLabel("Password Length:")
        length_label.setStyleSheet("color: #6fff4a; font-size: 12px;")
        # *** IMPROVED: Minimum horizontal size policy ***
        length_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        length_layout.addWidget(length_label)

        self.length_spinbox = QSpinBox()
        self.length_spinbox.setMinimum(8)
        self.length_spinbox.setMaximum(128)
        self.length_spinbox.setValue(16)
        self.length_spinbox.setFixedSize(100, 40)
        # *** IMPROVED: Fixed size policy ***
        self.length_spinbox.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.length_spinbox.valueChanged.connect(self.reset_auto_lock_timer)
        self.length_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #1a1a1a;
                border: 2px solid #39ff14;
                border-radius: 5px;
                color: #39ff14;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 18px;
                border-left: 1px solid #39ff14;
                background-color: #0d0d0d;
            }
            QSpinBox::up-arrow { border: 4px solid transparent; border-bottom: 6px solid #39ff14; }
            QSpinBox::down-arrow { border: 4px solid transparent; border-top: 6px solid #39ff14; }
        """)
        length_layout.addWidget(self.length_spinbox)

        # *** TASK 2: Add spacer to push Generate/Save buttons to the right ***
        length_layout.addStretch()

        # *** TASK 2: Add GENERATE button to this row (saves vertical space!) ***
        self.btn_generate = QPushButton()
        self.btn_generate.setIcon(QIcon(":/buttons/generate_v2_ultra_smooth.png"))
        self.btn_generate.setIconSize(QSize(220, 80))
        self.btn_generate.setFixedSize(220, 80)
        self.btn_generate.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_generate.clicked.connect(self.on_generate)
        self.btn_generate.setStyleSheet("""
            QPushButton { border: none; background: transparent; }
            QPushButton:pressed { transform: scale(0.95); }
        """)
        length_layout.addWidget(self.btn_generate)

        # *** TASK 2: Add SAVE button to this row ***
        self.btn_save = QPushButton()
        self.btn_save.setIcon(QIcon(":/buttons/save_v2_ultra_smooth.png"))
        self.btn_save.setIconSize(QSize(220, 80))
        self.btn_save.setFixedSize(220, 80)
        self.btn_save.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_save.clicked.connect(self.on_save)
        self.btn_save.setStyleSheet("""
            QPushButton { border: none; background: transparent; }
            QPushButton:pressed { transform: scale(0.95); }
        """)
        length_layout.addWidget(self.btn_save)

        inputs_layout.addLayout(length_layout)

        # *** STRETCH FACTOR 0: Input section never shrinks ***
        main_layout.addLayout(inputs_layout, 0)

        # Password list (INTERACTIVE) - Expanding to fill space
        list_label = QLabel("Stored Passwords (double-click to load):")
        list_label.setStyleSheet("color: #6fff4a; font-size: 13px; font-weight: bold;")
        list_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        # *** STRETCH FACTOR 0: Label never shrinks ***
        main_layout.addWidget(list_label, 0)

        self.password_list = QListWidget()
        # *** TASK 1 & 3: Start at 40px (like inputs), max 100px, then scrollbar ***
        self.password_list.setMinimumHeight(40)  # Matches input field height when empty
        self.password_list.setMaximumHeight(100)  # Stops growing at 100px
        self.password_list.setMinimumWidth(500)
        # *** IMPROVED: Expanding horizontally, but limited vertically by max height ***
        self.password_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # *** CRITICAL: Enable scrollbar when content exceeds 100px ***
        self.password_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.password_list.itemDoubleClicked.connect(self.on_list_item_double_clicked)
        self.password_list.itemClicked.connect(self.reset_auto_lock_timer)
        self.password_list.setStyleSheet(f"""
            QListWidget {{
                border-image: url({self.assets_dir / 'list_panel_9slice_ultra_smooth.png'}) 40 40 40 40 stretch;
                padding: 10px;
                background-color: rgba(5, 10, 6, 0.95);
                color: #39ff14;
                font-family: 'Xolonium', 'Courier New', monospace;
                font-size: 13px;
                font-weight: bold;
            }}
            QListWidget::item {{
                padding: 8px;
                min-height: 20px;
                border-bottom: 1px solid rgba(57, 255, 20, 0.1);
            }}
            QListWidget::item:selected {{
                background-color: rgba(57, 255, 20, 0.3);
                color: #0a0a0a;
            }}
            QListWidget::item:hover {{
                background-color: rgba(57, 255, 20, 0.15);
            }}
            QScrollBar:vertical {{
                border: none;
                background: rgba(10, 10, 10, 0.8);
                width: 12px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #39ff14;
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        # *** STRETCH FACTOR 1: Password list CAN shrink when window gets smaller ***
        main_layout.addWidget(self.password_list, 1)

        # Button section - Single horizontal row (FIX 2: saves more vertical space!)
        # *** FIX 2: Changed from 2x2 grid to single horizontal row ***
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Button configs - 4 buttons in a horizontal row
        button_configs = [
            ("retrieve", ":/buttons/retrieve_v2_ultra_smooth.png", self.on_retrieve),
            ("copy", ":/buttons/copy_v2_ultra_smooth.png", self.on_copy_password),
            ("lock", ":/buttons/lock_v2_ultra_smooth.png", self.on_lock),
            ("set_vault", ":/buttons/set_vault_v2_ultra_smooth.png", self.on_set_vault),
        ]

        self.buttons = {
            "generate": self.btn_generate,  # Already created in length row
            "save": self.btn_save,  # Already created in length row
        }

        for name, icon_path, callback in button_configs:
            btn = QPushButton()
            btn.setObjectName(f"btn_{name}")
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(220, 80))
            btn.setFixedSize(220, 80)
            # *** IMPROVED: Fixed size policy for buttons ***
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton { border: none; background: transparent; }
                QPushButton:pressed { transform: scale(0.95); }
            """)
            buttons_layout.addWidget(btn)
            self.buttons[name] = btn

        # Add UNLOCK button (hidden/shown based on lock state)
        btn_unlock = QPushButton()
        btn_unlock.setObjectName("btn_unlock")
        btn_unlock.setIcon(QIcon(":/buttons/unlock_v2_ultra_smooth.png"))
        btn_unlock.setIconSize(QSize(220, 80))
        btn_unlock.setFixedSize(220, 80)
        btn_unlock.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        btn_unlock.clicked.connect(self.on_unlock)
        btn_unlock.setStyleSheet("""
            QPushButton { border: none; background: transparent; }
            QPushButton:pressed { transform: scale(0.95); }
        """)
        buttons_layout.addWidget(btn_unlock)
        self.buttons["unlock"] = btn_unlock

        # *** IMPROVED: Add stretch to push buttons left ***
        buttons_layout.addStretch()

        # *** STRETCH FACTOR 0: Buttons MUST always stay visible ***
        main_layout.addLayout(buttons_layout, 0)

    # ==== Backend wiring helpers ====
    def initialize_master_flow(self):
        try:
            if not self.vault.has_master_password():
                # First run: set master password
                ok = False
                while not ok:
                    pwd, accepted = QInputDialog.getText(self, "Create Master Password",
                                                        "Enter a new master password (min 8 characters):",
                                                        QLineEdit.EchoMode.Password)
                    if not accepted:
                        QMessageBox.warning(self, "Master Password Required",
                                            "A master password is required to initialize the vault.")
                        continue
                    if len(pwd) < 8:
                        QMessageBox.warning(self, "Weak Password",
                                            "Please choose at least 8 characters.")
                        continue
                    ok = self.vault.set_master_password(pwd)
                    if not ok:
                        QMessageBox.critical(self, "Error", "Failed to set master password.")
                self.set_locked_ui(False)
                QMessageBox.information(self, "Success", "Vault created! Your passwords are now secure.")
            else:
                # Existing vault: prompt unlock
                self.prompt_unlock()
        except Exception as e:
            QMessageBox.critical(self, "Initialization Error", str(e))

    def prompt_unlock(self):
        while self.vault.is_locked:
            pwd, accepted = QInputDialog.getText(self, "Unlock Vault",
                                                "Enter master password:",
                                                QLineEdit.EchoMode.Password)
            if not accepted:
                break
            if self.vault.unlock(pwd):
                self.set_locked_ui(False)
                self.refresh_password_list()
                self.auto_lock_timer.start()
                return
            else:
                QMessageBox.warning(self, "Unlock Failed", "Incorrect master password.")
        self.set_locked_ui(self.vault.is_locked)

    def set_locked_ui(self, locked: bool):
        """Disable/enable UI elements based on lock state."""
        for w in [self.assoc_input, self.username_input, self.password_input,
                  self.length_spinbox, self.show_hide_btn]:
            w.setEnabled(not locked)

        # Show/hide appropriate buttons based on lock state
        for name, btn in self.buttons.items():
            if locked:
                # When locked: only unlock button enabled, rest disabled
                btn.setEnabled(name == "unlock")
                btn.setVisible(name == "unlock" or name != "lock")  # Hide lock, show unlock
                if name == "unlock":
                    btn.setVisible(True)
                elif name == "lock":
                    btn.setVisible(False)
            else:
                # When unlocked: all buttons except unlock enabled
                btn.setEnabled(name != "unlock")
                btn.setVisible(name != "unlock")  # Hide unlock, show lock
                if name == "lock":
                    btn.setVisible(True)

        if locked:
            self.password_list.clear()
            item = QListWidgetItem("[Vault Locked] Click UNLOCK button to access")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.password_list.addItem(item)
            self.strength_label.setText("")

    def refresh_password_list(self):
        """Refresh the password list display."""
        self.password_list.clear()
        if self.vault.is_locked:
            return

        try:
            self.current_entries = self.vault.get_all_passwords()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load entries: {e}")
            return

        if not self.current_entries:
            item = QListWidgetItem("No passwords stored yet. Click GENERATE to create one!")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.password_list.addItem(item)
            return

        # Add entries to list
        for entry in self.current_entries:
            masked = "*" * min(16, len(entry.password))
            display_text = f"{entry.association:25s}  |  {entry.username:25s}  |  {masked}"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, entry.id)
            self.password_list.addItem(item)

    # ==== Button callbacks ====
    def on_generate(self):
        """Generate new password."""
        try:
            length = self.length_spinbox.value()
            password = PasswordGenerator.generate(length)
            self.password_input.setText(password)
            self.reset_auto_lock_timer()

            score, strength = PasswordGenerator.calculate_strength(password)
            QMessageBox.information(self, "Password Generated",
                                   f"Generated {length}-character password\nStrength: {strength} ({score}/100)")
        except Exception as e:
            QMessageBox.warning(self, "Generate Error", str(e))

    def on_save(self):
        """Save current password to vault."""
        if self.vault.is_locked:
            QMessageBox.information(self, "Locked", "Unlock the vault first.")
            self.prompt_unlock()
            return

        assoc = self.assoc_input.text().strip()
        user = self.username_input.text().strip()
        pwd = self.password_input.text()

        if not assoc or not user or not pwd:
            QMessageBox.information(self, "Missing Data",
                                   "Association, username, and password are required.")
            return

        try:
            self.vault.add_password(assoc, user, pwd)
            self.refresh_password_list()
            # Clear input fields
            self.assoc_input.clear()
            self.username_input.clear()
            self.password_input.clear()
            self.strength_label.setText("")
            QMessageBox.information(self, "Saved", f"Password for {assoc} saved successfully!")
            self.reset_auto_lock_timer()
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def on_retrieve(self):
        """Retrieve/load selected password from list."""
        current_item = self.password_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection",
                               "Please select a password from the list or double-click an entry.")
            return

        entry_id = current_item.data(Qt.ItemDataRole.UserRole)
        if entry_id is None:
            return

        try:
            entry = self.vault.get_password_by_id(entry_id)
            if entry:
                self.assoc_input.setText(entry.association)
                self.username_input.setText(entry.username)
                self.password_input.setText(entry.password)
                QMessageBox.information(self, "Retrieved",
                                       f"Loaded password for {entry.association}")
                self.reset_auto_lock_timer()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve: {str(e)}")

    def on_copy_password(self):
        """Copy password to clipboard with auto-clear."""
        password = self.password_input.text()

        if not password:
            # Try to copy from selected list item
            current_item = self.password_list.currentItem()
            if current_item:
                entry_id = current_item.data(Qt.ItemDataRole.UserRole)
                if entry_id:
                    try:
                        entry = self.vault.get_password_by_id(entry_id)
                        if entry:
                            password = entry.password
                    except:
                        pass

        if password:
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            QMessageBox.information(self, "Copied",
                                   "Password copied to clipboard!\nWill auto-clear in 30 seconds.")

            # Clear clipboard after 30 seconds
            self.clipboard_timer.start(30000)
            self.reset_auto_lock_timer()
        else:
            QMessageBox.warning(self, "No Password", "No password to copy!")

    def on_list_item_double_clicked(self, item):
        """Handle double-click on list item."""
        entry_id = item.data(Qt.ItemDataRole.UserRole)
        if entry_id is None:
            return

        # Show options dialog
        reply = QMessageBox.question(self, "Password Entry Options",
                                     "What would you like to do?",
                                     QMessageBox.StandardButton.Open |
                                     QMessageBox.StandardButton.Close |
                                     QMessageBox.StandardButton.Cancel)

        if reply == QMessageBox.StandardButton.Open:
            # Load entry
            self.on_retrieve()
        elif reply == QMessageBox.StandardButton.Close:
            # Delete entry
            self.delete_entry(entry_id)

    def delete_entry(self, entry_id):
        """Delete a password entry."""
        reply = QMessageBox.question(self, "Confirm Delete",
                                     "Are you sure you want to delete this password?\nThis cannot be undone!",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.vault.delete_password(entry_id)
                self.refresh_password_list()
                QMessageBox.information(self, "Deleted", "Password entry deleted.")
                self.reset_auto_lock_timer()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {str(e)}")

    def on_lock(self):
        """Lock the vault."""
        reply = QMessageBox.question(self, "Lock Vault",
                                     "Are you sure you want to lock the vault?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.vault.lock()
            self.auto_lock_timer.stop()
            self.set_locked_ui(True)
            QMessageBox.information(self, "Locked", "Vault locked successfully!")

    def on_unlock(self):
        """Unlock the vault."""
        self.prompt_unlock()

    def on_set_vault(self):
        """Change vault database location."""
        reply = QMessageBox.question(
            self,
            "Set Vault Location",
            "Do you want to:\n\n"
            "• Create a NEW vault at a different location?\n"
            "• Open an EXISTING vault file?\n\n"
            "Current vault will be locked.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Yes
        )

        if reply == QMessageBox.StandardButton.Cancel:
            return

        # Lock current vault first
        if not self.vault.is_locked:
            self.vault.lock()
            self.set_locked_ui(True)

        # Get new vault path
        if reply == QMessageBox.StandardButton.Yes:
            # Create new vault
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Create New Vault",
                str(Path.home() / "phigen_vault.db"),
                "Database Files (*.db);;All Files (*)"
            )
        else:
            # Open existing vault
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open Existing Vault",
                str(Path.home()),
                "Database Files (*.db);;All Files (*)"
            )

        if not file_path:
            return  # User cancelled

        try:
            # Create new vault instance with selected path
            self.vault = PasswordVault(vault_path=file_path)
            self.vault.lock()  # Start locked
            self.set_locked_ui(True)
            self.password_list.clear()

            # Show success message
            QMessageBox.information(
                self,
                "Vault Changed",
                f"Vault location set to:\n{file_path}\n\n"
                "Please unlock the vault to access passwords."
            )

            # Prompt to unlock or set master password if new
            if not self.vault.has_master_password():
                reply = QMessageBox.question(
                    self,
                    "New Vault",
                    "This vault has no master password.\n"
                    "Would you like to set one now?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    password, ok = QInputDialog.getText(
                        self,
                        "Set Master Password",
                        "Enter master password for new vault:",
                        QLineEdit.EchoMode.Password
                    )
                    if ok and password:
                        confirm, ok2 = QInputDialog.getText(
                            self,
                            "Confirm Master Password",
                            "Confirm master password:",
                            QLineEdit.EchoMode.Password
                        )
                        if ok2 and password == confirm:
                            if self.vault.set_master_password(password):
                                QMessageBox.information(self, "Success", "Master password set successfully!")
                                self.set_locked_ui(False)
                                self.refresh_password_list()
                            else:
                                QMessageBox.warning(self, "Error", "Failed to set master password.")
                        else:
                            QMessageBox.warning(self, "Error", "Passwords do not match!")
            else:
                self.prompt_unlock()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to change vault location:\n{e}"
            )

    def auto_lock(self):
        """Auto-lock after timeout."""
        self.vault.lock()
        self.auto_lock_timer.stop()
        self.set_locked_ui(True)
        QMessageBox.warning(self, "Auto-Lock", "Vault auto-locked due to inactivity (5 minutes).")

    def reset_auto_lock_timer(self):
        """Reset the auto-lock timer on user activity."""
        if not self.vault.is_locked:
            self.auto_lock_timer.stop()
            self.auto_lock_timer.start()

    def clear_clipboard(self):
        """Clear clipboard after timeout."""
        clipboard = QApplication.clipboard()
        clipboard.clear()
        self.clipboard_timer.stop()

    def toggle_password_visibility(self):
        """Toggle password visibility with lock/unlock icons."""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            # Currently hidden → show password (unlock)
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_hide_btn.setIcon(QIcon(self.unlock_icon_path))
        else:
            # Currently visible → hide password (lock)
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_hide_btn.setIcon(QIcon(self.lock_icon_path))
        self.reset_auto_lock_timer()

    def on_password_changed(self):
        """Update password strength indicator when password changes."""
        password = self.password_input.text()
        if password:
            score, strength = PasswordGenerator.calculate_strength(password)

            # Color based on strength
            if score < 50:
                color = "#ff4444"  # Red
            elif score < 70:
                color = "#ffaa00"  # Orange
            elif score < 90:
                color = "#39ff14"  # Green
            else:
                color = "#00ffff"  # Cyan

            self.strength_label.setText(f"Strength: {strength} ({score}/100)")
            self.strength_label.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: bold;")
        else:
            self.strength_label.setText("")
        self.reset_auto_lock_timer()

    def closeEvent(self, event):
        """Handle window close."""
        if not self.vault.is_locked:
            reply = QMessageBox.question(self, "Exit",
                                        "Do you want to lock the vault before exiting?",
                                        QMessageBox.StandardButton.Yes |
                                        QMessageBox.StandardButton.No |
                                        QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Yes:
                self.vault.lock()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


    def mousePressEvent(self, event):
        """Handle mouse press for window dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Only drag if clicking in the title bar area (top 40 pixels)
            if event.position().y() <= 40:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging."""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Xolonium", 10))

    print("\n" + "="*70)
    print("PhiGEN Password Vault - IMPROVED RESPONSIVE VERSION")
    print("="*70)
    print("Same UI and functionality, but with improved layout management!")
    print("")
    print("Improvements:")
    print("  + Input fields expand with window width")
    print("  + Password list grows/shrinks to fill available space")
    print("  + Better size policies for all widgets")
    print("  + Smooth resizing behavior")
    print("")
    print("Try resizing the window to see the difference!")
    print("="*70 + "\n")

    window = PasswordVaultComplete()
    window.show()

    sys.exit(app.exec())
