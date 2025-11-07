#!/usr/bin/env python3
"""
PhiGEN System Status Monitor
Real-time status dashboard for all PhiGEN components
"""

import sys
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QTextEdit, QFrame
)
from PyQt6.QtGui import QFont, QColor, QPalette, QTextCursor
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject


class StatusSignals(QObject):
    """Signals for updating UI from background threads"""
    log_message = pyqtSignal(str)
    status_update = pyqtSignal(str, bool)  # module_name, is_active


class ModuleButton(QPushButton):
    """Status indicator button for a PhiGEN module"""

    def __init__(self, module_name, display_name):
        super().__init__(display_name)
        self.module_name = module_name
        self.is_active = False

        # Set fixed size
        self.setFixedSize(200, 80)

        # Terminal-style font
        font = QFont("Consolas", 10, QFont.Weight.Bold)
        self.setFont(font)

        # Initial state (inactive/greyscale)
        self.set_active(False)

    def set_active(self, active):
        """Update button appearance based on active state"""
        self.is_active = active

        if active:
            # Illuminated - green glow
            self.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:0, y2:1,
                        stop:0 #00ff00,
                        stop:1 #00aa00
                    );
                    color: #001100;
                    border: 2px solid #00ff00;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:0, y2:1,
                        stop:0 #00ff66,
                        stop:1 #00cc00
                    );
                    border: 2px solid #00ff66;
                }
            """)
        else:
            # Greyscale - inactive/error
            self.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:0, y2:1,
                        stop:0 #555555,
                        stop:1 #333333
                    );
                    color: #999999;
                    border: 2px solid #444444;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:0, y2:1,
                        stop:0 #666666,
                        stop:1 #444444
                    );
                }
            """)


class PhiGENStatusMonitor(QMainWindow):
    """Main status monitor window"""

    def __init__(self):
        super().__init__()
        self.signals = StatusSignals()
        self.module_buttons = {}
        self.init_ui()

        # Connect signals
        self.signals.log_message.connect(self.append_log)
        self.signals.status_update.connect(self.update_module_status)

        # Start monitoring
        self.start_monitoring()

        self.log("PhiGEN Status Monitor initialized")
        self.log("=" * 80)

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("PhiGEN System Status Monitor")
        self.setGeometry(100, 100, 900, 700)

        # Dark terminal-style theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0e14;
            }
            QLabel {
                color: #00ff00;
                font-family: 'Consolas', monospace;
            }
            QTextEdit {
                background-color: #0a0e14;
                color: #00ff00;
                border: 2px solid #00ff00;
                font-family: 'Consolas', monospace;
                font-size: 10pt;
                padding: 5px;
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        header = QLabel("⚡ PhiGEN SYSTEM STATUS ⚡")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        header.setStyleSheet("color: #00ff00; padding: 10px;")
        main_layout.addWidget(header)

        # Module status grid
        modules_frame = QFrame()
        modules_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        modules_layout = QGridLayout(modules_frame)
        modules_layout.setSpacing(10)

        # Define modules
        modules = [
            ("discord-bot", "Discord Bot\n(Multi-Model)"),
            ("ollama", "Ollama\n(AI Models)"),
            ("ai-api", "REST API\n(Port 8000)"),
            ("dc-bridge", "DC Bridge\n(Watch & Send)"),
            ("ai-reviewer", "AI Code\nReviewer"),
            ("ai-logs", "AI Log\nAnalyzer"),
        ]

        # Create module buttons in grid
        for i, (module_id, display_name) in enumerate(modules):
            btn = ModuleButton(module_id, display_name)
            self.module_buttons[module_id] = btn
            row = i // 3
            col = i % 3
            modules_layout.addWidget(btn, row, col)

        main_layout.addWidget(modules_frame)

        # Terminal output section
        terminal_label = QLabel("▼ SYSTEM LOG ▼")
        terminal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        terminal_label.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        main_layout.addWidget(terminal_label)

        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setMinimumHeight(200)
        self.terminal_output.setMaximumBlockCount(500)  # Limit scrollback
        main_layout.addWidget(self.terminal_output)

        # Status bar
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #1a1e24;
                color: #00ff00;
                padding: 8px;
                border: 1px solid #00ff00;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.status_label)

    def log(self, message):
        """Add message to terminal output"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.signals.log_message.emit(f"[{timestamp}] {message}")

    def append_log(self, message):
        """Append log message (called from signal)"""
        self.terminal_output.append(message)
        # Auto-scroll to bottom
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal_output.setTextCursor(cursor)

    def update_module_status(self, module_name, is_active):
        """Update module status indicator"""
        if module_name in self.module_buttons:
            self.module_buttons[module_name].set_active(is_active)

    def check_docker_container(self, container_name):
        """Check if Docker container is running"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={container_name}",
                 "--format", "{{.Status}}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            status = result.stdout.strip()
            return bool(status and "Up" in status)
        except Exception as e:
            self.log(f"Error checking {container_name}: {e}")
            return False

    def check_dc_bridge(self):
        """Check if DC Bridge Python process is running"""
        try:
            # Windows
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq python.exe"],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Check if watch_and_send_to_dc is in process list
            if "python.exe" in result.stdout:
                # Further check command line
                result2 = subprocess.run(
                    ["wmic", "process", "where", "name='python.exe'",
                     "get", "commandline"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return "watch_and_send_to_dc" in result2.stdout
            return False
        except Exception:
            return False

    def check_all_statuses(self):
        """Check status of all modules"""
        # Docker containers
        statuses = {
            "discord-bot": self.check_docker_container("phigen-discord-multimodel"),
            "ollama": self.check_docker_container("phigen-ollama") or self.check_ollama_native(),
            "ai-api": self.check_docker_container("phigen-ai-api"),
            "ai-reviewer": self.check_docker_container("phigen-ai-reviewer"),
            "ai-logs": self.check_docker_container("phigen-ai-logs"),
            "dc-bridge": self.check_dc_bridge(),
        }

        # Update UI
        for module, is_active in statuses.items():
            self.signals.status_update.emit(module, is_active)

        # Update status bar
        active_count = sum(statuses.values())
        total_count = len(statuses)
        self.status_label.setText(
            f"Active: {active_count}/{total_count} modules"
        )

        return statuses

    def check_ollama_native(self):
        """Check if Ollama is running natively (not in Docker)"""
        try:
            import urllib.request
            urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
            return True
        except:
            return False

    def monitoring_thread(self):
        """Background thread for monitoring services"""
        self.log("Starting monitoring thread...")

        while True:
            try:
                statuses = self.check_all_statuses()

                # Log status changes
                if hasattr(self, 'last_statuses'):
                    for module, is_active in statuses.items():
                        if self.last_statuses.get(module) != is_active:
                            status_str = "ONLINE" if is_active else "OFFLINE"
                            self.log(f"{module.upper()}: {status_str}")

                self.last_statuses = statuses

            except Exception as e:
                self.log(f"Monitoring error: {e}")

            time.sleep(5)  # Check every 5 seconds

    def start_monitoring(self):
        """Start the monitoring background thread"""
        monitor = threading.Thread(target=self.monitoring_thread, daemon=True)
        monitor.start()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Create and show window
    monitor = PhiGENStatusMonitor()
    monitor.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
