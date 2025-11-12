#!/usr/bin/env python3
"""
PhiGEN System Status Monitor
Real-time status dashboard for all PhiGEN components
"""

import sys
import os
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLabel, QTextEdit, QPlainTextEdit, QFrame,
    QMessageBox
)
from PyQt6.QtGui import QFont, QColor, QPalette, QTextCursor, QFontDatabase
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QPoint


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
        font = QFont("Xolonium", 10, QFont.Weight.Bold)
        self.setFont(font)

        # Enable button click for process control
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

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

        # For window dragging
        self.dragging = False
        self.drag_position = QPoint()

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

        # Frameless window for custom dark title bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Get background image path
        assets_dir = Path(__file__).parent / "assets"
        bg_image = assets_dir / "circuit_background_opacity_20.png"

        # Dark terminal-style theme with circuit background
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #0a0e14;
                background-image: url({bg_image.as_posix()});
                background-repeat: repeat;
            }}
            QLabel {{
                color: #00ff00;
                font-family: 'Consolas', monospace;
                background: transparent;
            }}
            QPlainTextEdit {{
                background-color: rgba(10, 14, 20, 0.9);
                color: #00ff00;
                border: 2px solid #00ff00;
                font-family: 'Consolas', monospace;
                font-size: 10pt;
                padding: 5px;
            }}
            QFrame {{
                background: transparent;
            }}
        """)

        # Central widget with transparent background
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Custom title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 255, 0, 0.15);
                border-bottom: 2px solid #00ff00;
            }
        """)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        # Title text
        self.title_label = QLabel("⚡ PhiGEN SYSTEM STATUS MONITOR ⚡")
        self.title_label.setFont(QFont("Xirod", 12, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #00ff00; background: transparent; border: none;")
        title_layout.addWidget(self.title_label)

        # Window control buttons
        minimize_btn = QPushButton("_")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 255, 0, 0.2);
                color: #00ff00;
                border: 1px solid #00ff00;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 0.4);
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(minimize_btn)

        close_btn = QPushButton("X")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 0.3);
                color: #ff0000;
                border: 1px solid #ff0000;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.6);
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)

        main_layout.addWidget(title_bar)

        # Content area with padding
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        main_layout.addWidget(content_widget)

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
            btn.clicked.connect(lambda checked, m=module_id: self.handle_module_click(m))
            self.module_buttons[module_id] = btn
            row = i // 3
            col = i % 3
            modules_layout.addWidget(btn, row, col)

        content_layout.addWidget(modules_frame)

        # Terminal output section
        terminal_label = QLabel("▼ SYSTEM LOG ▼")
        terminal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        terminal_label.setFont(QFont("White Rabbit", 12, QFont.Weight.Bold))
        content_layout.addWidget(terminal_label)

        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setMinimumHeight(200)
        self.terminal_output.setMaximumBlockCount(500)  # Limit scrollback
        content_layout.addWidget(self.terminal_output)

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
        content_layout.addWidget(self.status_label)

        # Store title bar for mouse events
        self.title_bar = title_bar

    def log(self, message):
        """Add message to terminal output"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.signals.log_message.emit(f"[{timestamp}] {message}")

    def append_log(self, message):
        """Append log message (called from signal)"""
        self.terminal_output.appendPlainText(message)
        # Auto-scroll to bottom
        cursor = self.terminal_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal_output.setTextCursor(cursor)

    def update_module_status(self, module_name, is_active):
        """Update module status indicator"""
        if module_name in self.module_buttons:
            self.module_buttons[module_name].set_active(is_active)

    def show_confirmation_dialog(self, title, message):
        """Show custom-themed confirmation dialog"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        # Apply PhiGEN dark theme to dialog
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #0a0e14;
                color: #00ff00;
                font-family: 'Xolonium';
                font-size: 12pt;
            }
            QLabel {
                color: #00ff00;
                background: transparent;
            }
            QPushButton {
                background-color: rgba(0, 255, 0, 0.2);
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 0.4);
                border: 2px solid #00ff66;
            }
            QPushButton:pressed {
                background-color: rgba(0, 255, 0, 0.6);
            }
        """)

        return msg_box.exec() == QMessageBox.StandardButton.Yes

    def handle_module_click(self, module_id):
        """Handle module button click - start or stop process"""
        is_active = self.module_buttons[module_id].is_active

        if is_active:
            # Confirm stop
            if self.show_confirmation_dialog(
                "Stop Process",
                f"Stop {module_id.upper()}?\n\nThis will terminate the running process."
            ):
                self.stop_process(module_id)
        else:
            # Start process
            self.start_process(module_id)

    def start_process(self, module_id):
        """Start a PhiGEN module process"""
        self.log(f"Starting {module_id}...")

        project_root = Path(__file__).parent.parent.parent
        env_file = project_root / ".env"

        # Load environment variables from .env
        env = os.environ.copy()
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env[key.strip()] = value.strip()

        commands = {
            "discord-bot": ["python", "-m", "src.phigen.bots.discord_bot_mcp_enhanced"],
            "ollama": ["docker", "start", "phigen-ollama"],  # Start Docker container
            "ai-api": None,  # Module doesn't exist yet
            "dc-bridge": ["python", "-m", "src.phigen.bots.discord_mcp_bridge"],
            "ai-reviewer": None,  # Module doesn't exist yet
            "ai-logs": None,  # Module doesn't exist yet
        }

        if module_id in commands:
            cmd = commands[module_id]
            if cmd is None:
                self.log(f"⚠ {module_id} not implemented yet or needs manual setup")
                return

            try:
                # Start process in background with environment
                subprocess.Popen(
                    cmd,
                    cwd=project_root,
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.log(f"✓ {module_id} started successfully")
                # Status will update on next monitoring cycle
            except Exception as e:
                self.log(f"✗ Failed to start {module_id}: {e}")
        else:
            self.log(f"⚠ No start command configured for {module_id}")

    def stop_process(self, module_id):
        """Stop a PhiGEN module process"""
        self.log(f"Stopping {module_id}...")

        # Special handling for Docker containers
        if module_id == "ollama":
            try:
                subprocess.run(
                    ["docker", "stop", "phigen-ollama"],
                    check=False,
                    timeout=10
                )
                self.log(f"✓ {module_id} Docker container stopped")
                return
            except Exception as e:
                self.log(f"✗ Failed to stop {module_id} container: {e}")
                return

        # Process name patterns to match for local processes
        patterns = {
            "discord-bot": "discord_bot_mcp_enhanced",
            "ai-api": "api_server",
            "dc-bridge": "discord_mcp_bridge",
            "ai-reviewer": "ai_reviewer",
            "ai-logs": "ai_log_analyzer",
        }

        if module_id in patterns:
            try:
                # Kill matching processes
                subprocess.run(
                    ["pkill", "-f", patterns[module_id]],
                    check=False
                )
                self.log(f"✓ {module_id} stopped")
            except Exception as e:
                self.log(f"✗ Failed to stop {module_id}: {e}")
        else:
            self.log(f"⚠ No stop pattern configured for {module_id}")

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

    def check_process_running(self, pattern):
        """Check if a process matching pattern is running"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", pattern],
                capture_output=True,
                text=True,
                timeout=2
            )
            return bool(result.stdout.strip())
        except:
            return False

    def check_all_statuses(self):
        """Check status of all modules"""
        # Check both Docker containers and local processes
        statuses = {
            "discord-bot": (
                self.check_docker_container("phigen-discord-multimodel") or
                self.check_process_running("discord_bot_mcp_enhanced")
            ),
            "ollama": (
                self.check_docker_container("phigen-ollama") or
                self.check_ollama_native()
            ),
            "ai-api": (
                self.check_docker_container("phigen-ai-api") or
                self.check_process_running("api_server")
            ),
            "ai-reviewer": (
                self.check_docker_container("phigen-ai-reviewer") or
                self.check_process_running("ai_reviewer")
            ),
            "ai-logs": (
                self.check_docker_container("phigen-ai-logs") or
                self.check_process_running("ai_log_analyzer")
            ),
            "dc-bridge": (
                self.check_process_running("discord_mcp_bridge") or
                self.check_dc_bridge()
            ),
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
            # Try localhost first (works on native Linux)
            try:
                urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
                return True
            except:
                pass

            # Try Windows host IP (for WSL)
            try:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if 'nameserver' in line:
                            host_ip = line.split()[1]
                            urllib.request.urlopen(f"http://{host_ip}:11434/api/tags", timeout=2)
                            return True
            except:
                pass

            return False
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

    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if click is on title bar area (top 40 pixels)
            if event.position().y() <= 40:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()


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
