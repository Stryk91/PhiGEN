#!/usr/bin/env python3
"""
PhiVector Control Bridge - Tactical System Management Hub
Uses pre-rendered high-quality PNG textures (rendered at 2x @ 300 DPI)
With soft fade color palette for eye strain reduction
"""

import os
import sys
from pathlib import Path

# DPI Fix
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QSplitter, QTextEdit, QLabel,
    QPushButton, QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtGui import QFont, QIcon, QPixmap, QImage, QPainter
from PyQt6.QtCore import Qt, QPoint, QSize

# Import soft fade color palette
try:
    from .colors import COLORS, TEXTURE_OPACITIES, INTERACTION_STATES
except ImportError:
    # Direct execution fallback
    from colors import COLORS, TEXTURE_OPACITIES, INTERACTION_STATES


class PhiVectorControlBridge(QMainWindow):
    def __init__(self):
        super().__init__()

        # Frameless window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Window dragging
        self.dragging = False
        self.drag_position = QPoint()

        self.setWindowTitle("PhiVector Control Bridge")

        # Asset directories
        self.old_assets_dir = Path(__file__).parent.parent.parent / "old" / "TEMPSVG"
        self.textures_dir = Path(__file__).parent.parent.parent / "assets" / "textures" / "rendered"

        # Window size
        self.resize(1650, 950)
        self.setMinimumSize(1400, 800)

        self.setup_ui()

    def setup_ui(self):
        """Tactical 3-pane interface with layered textures and soft fade palette."""
        central = QWidget()

        # Multi-layer texture overlay for soft fade effect
        # Layer 1: Carbon fiber (8% opacity)
        # Layer 2: Graphene mesh (4% opacity)
        # Layer 3: Snake scale (3% opacity)
        # Layer 4: Circuit background (10% opacity)
        carbon_path = str(self.textures_dir / "carbon-fibre_2x.png").replace("\\", "/")
        graphene_path = str(self.textures_dir / "graphene-mesh_2x.png").replace("\\", "/")
        snake_path = str(self.textures_dir / "snake-scale_2x.png").replace("\\", "/")
        circuit_path = str(self.old_assets_dir / "circuit_background_opacity_10.png").replace("\\", "/")

        central.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_base']};
                background-image:
                    url({carbon_path}),
                    url({graphene_path}),
                    url({snake_path}),
                    url({circuit_path});
                background-repeat: repeat, repeat, repeat, repeat;
                color: {COLORS['primary']};
            }}
        """)
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Slim title bar - pure black, no gradients
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)

        # Top toolbar with diamond mesh header
        toolbar = self.create_toolbar()
        main_layout.addWidget(toolbar)

        # Main 3-pane splitter
        splitter_container = self.create_three_pane_layout()
        main_layout.addWidget(splitter_container, 1)

        # Status bar with diamond mesh footer
        status_bar = self.create_status_bar()
        main_layout.addWidget(status_bar)

    def create_title_bar(self):
        """Soft black slim title bar with soft fade palette."""
        title_bar = QWidget()
        title_bar.setFixedHeight(28)
        title_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_base']};
                border-bottom: 1px solid {COLORS['primary']};
            }}
        """)

        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(10, 0, 8, 0)
        layout.setSpacing(8)

        # Logo placeholder (will be replaced with banner)
        logo = QLabel("⬢")
        logo.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        logo.setStyleSheet(f"color: {COLORS['primary']}; border: none; background: transparent;")
        layout.addWidget(logo)

        layout.addStretch()

        # Window controls - minimal tactical style with soft fade colors
        for symbol, color, callback in [
            ("─", COLORS['primary'], self.showMinimized),
            ("□", COLORS['primary'], self.toggle_maximize),
            ("×", COLORS['error'], self.close)
        ]:
            btn = QPushButton(symbol)
            btn.setFixedSize(28, 24)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {color};
                    border: 1px solid {color};
                    font-size: {'18px' if symbol == '×' else '14px'};
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2);
                }}
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        return title_bar

    def create_toolbar(self):
        """Toolbar with tactical chrome ribs separator."""
        toolbar = QWidget()
        toolbar.setFixedHeight(60)

        # Soft fade background
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_input']};
                border-bottom: 2px solid {COLORS['border_bright']};
            }}
        """)

        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)

        # System indicators section
        tray_label = QLabel("SYSTEM:")
        tray_label.setFont(QFont("Xolonium", 11, QFont.Weight.Bold))
        tray_label.setStyleSheet(f"color: {COLORS['primary_dim']}; border: none; background: transparent;")
        layout.addWidget(tray_label)

        for name, value, color in [
            ("CPU", "45%", COLORS['success']),
            ("RAM", "62%", COLORS['warning']),
            ("DISK", "78%", COLORS['warning']),
            ("NET", "OK", COLORS['success']),
        ]:
            indicator = self.create_indicator(name, value, color)
            layout.addWidget(indicator)

        layout.addSpacing(30)

        # Chrome rib separator
        sep = self.create_chrome_separator()
        layout.addWidget(sep)

        layout.addSpacing(30)

        # Quick actions
        for label, icon in [("Refresh", "⟳"), ("Health", "✓"), ("Sync", "⇅")]:
            btn = self.create_quick_action_button(label, icon)
            layout.addWidget(btn)

        layout.addStretch()

        # Quick access indicator
        search = QLabel("🔍 QUICK ACCESS")
        search.setFont(QFont("Kanit", 10))
        search.setStyleSheet(f"""
            color: {COLORS['primary_dim']};
            background-color: {INTERACTION_STATES['hover_bg']};
            border: 1px solid {COLORS['border_dim']};
            padding: 8px 20px;
            border-radius: 4px;
        """)
        layout.addWidget(search)

        return toolbar

    def create_three_pane_layout(self):
        """3-pane layout with chrome rib splitters."""
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {COLORS['border_bright']};
                width: 2px;
            }}
            QSplitter::handle:hover {{
                background-color: {COLORS['primary']};
                width: 3px;
            }}
        """)

        # Three panes
        left_pane = self.create_left_pane()
        middle_pane = self.create_middle_pane()
        right_pane = self.create_right_pane()

        main_splitter.addWidget(left_pane)
        main_splitter.addWidget(middle_pane)
        main_splitter.addWidget(right_pane)

        # Splitter sizes
        main_splitter.setSizes([420, 840, 420])

        return main_splitter

    def create_left_pane(self):
        """Left navigation - with hierarchy connectors and icons."""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_input']};
                border-right: 2px solid {COLORS['border_bright']};
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header with diamond mesh accent
        header = QLabel("TOOL INDEX")
        header.setFont(QFont("Xolonium", 14, QFont.Weight.Bold))
        header.setStyleSheet(f"""
            background-color: {INTERACTION_STATES['hover_bg']};
            color: {COLORS['primary']};
            padding: 14px;
            border-bottom: 2px solid {COLORS['primary']};
        """)
        layout.addWidget(header)

        # Navigation tree with enhanced visual feedback using soft fade palette
        tree = QTreeWidget()
        tree.setHeaderHidden(True)
        tree.setFont(QFont("White Rabbit", 11))
        tree.setIndentation(28)  # More space for hierarchy connectors
        tree.setStyleSheet(f"""
            QTreeWidget {{
                background-color: {COLORS['bg_input']};
                color: {INTERACTION_STATES['normal']};
                border: none;
                outline: none;
                padding: 8px;
            }}
            QTreeWidget::item {{
                padding: 10px 8px;
                border: none;
                border-left: 3px solid transparent;
                margin: 2px 4px;
            }}
            QTreeWidget::item:hover {{
                background-color: {INTERACTION_STATES['hover_bg']};
                color: {INTERACTION_STATES['hover']};
                border-left: 3px solid {INTERACTION_STATES['border_hover']};
            }}
            QTreeWidget::item:selected {{
                background-color: {INTERACTION_STATES['selected_bg']};
                color: {INTERACTION_STATES['selected']};
                border-left: 3px solid {INTERACTION_STATES['border_selected']};
                font-weight: bold;
            }}
            QTreeWidget::item:selected:hover {{
                background-color: rgba(0, 238, 0, 0.25);
                border-left: 3px solid {INTERACTION_STATES['border_selected']};
            }}
            QTreeWidget::branch {{
                background-color: transparent;
            }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {{
                border-image: none;
                image: none;
            }}
            QTreeWidget::branch:open:has-children:!has-siblings,
            QTreeWidget::branch:open:has-children:has-siblings {{
                border-image: none;
                image: none;
            }}
        """)

        # Tool icons mapping
        tool_icons = {
            # Dashboard
            "Overview": "📊",
            "Quick Stats": "📈",
            "Alerts": "⚠️",

            # System Tools
            "Password Vault": "🔒",
            "Driver Updater": "💿",
            "Service Manager": "⚙️",
            "Process Monitor": "📊",
            "Disk Cleanup": "🧹",

            # System Health
            "Hardware Monitor": "🖥️",
            "Network Status": "🌐",
            "Storage Analysis": "💾",
            "Performance Metrics": "⚡",

            # Utilities
            "File Browser": "📁",
            "Registry Editor": "📝",
            "Task Scheduler": "⏰",
            "Environment Variables": "🔧",

            # Package Manager
            "Installed Software": "📦",
            "Update Center": "🔄",
            "Repository Manager": "🗃️",

            # Settings
            "Preferences": "⚙️",
            "Themes": "🎨",
            "Hotkeys": "⌨️"
        }

        # Categories with items
        categories = {
            "DASHBOARD": ["Overview", "Quick Stats", "Alerts"],
            "SYSTEM TOOLS": [
                "Password Vault",
                "Driver Updater",
                "Service Manager",
                "Process Monitor",
                "Disk Cleanup"
            ],
            "SYSTEM HEALTH": [
                "Hardware Monitor",
                "Network Status",
                "Storage Analysis",
                "Performance Metrics"
            ],
            "UTILITIES": [
                "File Browser",
                "Registry Editor",
                "Task Scheduler",
                "Environment Variables"
            ],
            "PACKAGE MANAGER": [
                "Installed Software",
                "Update Center",
                "Repository Manager"
            ],
            "SETTINGS": [
                "Preferences",
                "Themes",
                "Hotkeys"
            ]
        }

        for category, items in categories.items():
            # Section separator line
            separator = QTreeWidgetItem(tree, ["─" * 40])
            separator.setFont(0, QFont("Kanit", 8))
            separator.setForeground(0, Qt.GlobalColor.darkGray)
            separator.setFlags(Qt.ItemFlag.NoItemFlags)  # Non-selectable

            # Category header with collapse indicator
            parent = QTreeWidgetItem(tree, [f"▼ {category}"])
            parent.setFont(0, QFont("Xolonium", 12, QFont.Weight.Bold))
            parent.setForeground(0, Qt.GlobalColor.green)  # Bright green for headers

            # Add items with icons and hierarchy connectors
            for idx, item in enumerate(items):
                icon = tool_icons.get(item, "◆")
                is_last = (idx == len(items) - 1)
                connector = "└─" if is_last else "├─"

                child = QTreeWidgetItem(parent, [f"  {connector} {icon} {item}"])
                child.setFont(0, QFont("White Rabbit", 11))
                child.setForeground(0, Qt.GlobalColor.darkGreen)  # Medium green for items

        tree.expandAll()

        # Connect selection signal
        tree.itemClicked.connect(self.on_nav_item_clicked)

        layout.addWidget(tree)

        self.nav_tree = tree
        return container

    def on_nav_item_clicked(self, item, column):
        """Handle navigation tree item clicks."""
        # Get the item text and extract tool name
        text = item.text(0)

        # Skip separators and category headers
        if text.startswith("─") or text.startswith("▼"):
            return

        # Extract tool name (after icon)
        parts = text.split(" ", 3)
        if len(parts) >= 4:
            tool_name = parts[3]
            print(f"[Navigation] Selected: {tool_name}")
            # TODO: Load tool content in middle pane

    def create_middle_pane(self):
        """Middle content viewer - tool cards with brushed metal."""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_base']};
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QLabel("CONTENT VIEWER")
        header.setFont(QFont("Xolonium", 14, QFont.Weight.Bold))
        header.setStyleSheet(f"""
            background-color: {INTERACTION_STATES['hover_bg']};
            color: {COLORS['primary']};
            padding: 14px;
            border-bottom: 2px solid {COLORS['primary']};
        """)
        layout.addWidget(header)

        # Content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {COLORS['bg_base']};
            }}
            QScrollBar:vertical {{
                background: {COLORS['bg_base']};
                width: 16px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['border_bright']};
                min-height: 30px;
                border-radius: 8px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {COLORS['primary']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 28, 28, 28)
        content_layout.setSpacing(22)

        # Direct prompt - no fluff
        prompt = QLabel("Select a tool from the navigation tree")
        prompt.setFont(QFont("White Rabbit", 12))
        prompt.setStyleSheet(f"color: {COLORS['primary_dim']};")
        content_layout.addWidget(prompt)

        content_layout.addSpacing(35)

        # Tool cards
        tools = [
            ("PASSWORD VAULT", "Secure password generation | 23 entries ready", "🔐"),
            ("DRIVER UPDATER", "System drivers current | Last scan: 2h ago", "🔄"),
            ("SERVICE MANAGER", "Windows services control | 142 active", "⚙️"),
            ("SYSTEM MONITOR", "Real-time hardware metrics | All green", "📊"),
        ]

        for title, status, icon in tools:
            card = self.create_tool_card(title, status, icon)
            content_layout.addWidget(card)

        content_layout.addStretch()

        scroll_area.setWidget(content)
        layout.addWidget(scroll_area)

        return container

    def create_right_pane(self):
        """Right actions pane - tactical buttons."""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_input']};
                border-left: 2px solid {COLORS['border_bright']};
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QLabel("ACTIONS")
        header.setFont(QFont("Xolonium", 14, QFont.Weight.Bold))
        header.setStyleSheet(f"""
            background-color: {INTERACTION_STATES['hover_bg']};
            color: {COLORS['primary']};
            padding: 14px;
            border-bottom: 2px solid {COLORS['primary']};
        """)
        layout.addWidget(header)

        # Action area
        action_container = QWidget()
        action_layout = QVBoxLayout(action_container)
        action_layout.setContentsMargins(20, 20, 20, 20)
        action_layout.setSpacing(14)

        # Context
        context = QLabel("No item selected")
        context.setFont(QFont("White Rabbit", 11))
        context.setStyleSheet(f"""
            color: {COLORS['primary_dim']};
            background-color: {INTERACTION_STATES['hover_bg']};
            padding: 14px;
            border-radius: 4px;
            border: 1px solid {COLORS['border_dim']};
        """)
        action_layout.addWidget(context)

        action_layout.addSpacing(28)

        # Action label
        action_label = QLabel("AVAILABLE ACTIONS")
        action_label.setFont(QFont("Xolonium", 11, QFont.Weight.Bold))
        action_label.setStyleSheet(f"color: {COLORS['primary']};")
        action_layout.addWidget(action_label)

        # Action buttons with Kanit
        for action in ["Execute", "Configure", "View Details", "Export Data", "Refresh"]:
            btn = QPushButton(action)
            btn.setFont(QFont("Kanit", 12))
            btn.setMinimumHeight(48)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {INTERACTION_STATES['hover_bg']};
                    color: {COLORS['primary']};
                    border: 2px solid {COLORS['border_dim']};
                    border-radius: 6px;
                    padding: 12px;
                    text-align: left;
                    padding-left: 20px;
                }}
                QPushButton:hover {{
                    background-color: rgba(0, 238, 0, 0.18);
                    border: 2px solid {COLORS['border_bright']};
                }}
                QPushButton:pressed {{
                    background-color: {INTERACTION_STATES['selected_bg']};
                }}
            """)
            action_layout.addWidget(btn)

        action_layout.addStretch()

        # Properties
        props_label = QLabel("PROPERTIES")
        props_label.setFont(QFont("Xolonium", 11, QFont.Weight.Bold))
        props_label.setStyleSheet(f"color: {COLORS['primary']};")
        action_layout.addWidget(props_label)

        props_text = QTextEdit()
        props_text.setReadOnly(True)
        props_text.setMaximumHeight(170)
        props_text.setFont(QFont("White Rabbit", 10))
        props_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: rgba(10, 10, 10, 0.9);
                color: {COLORS['primary_dim']};
                border: 1px solid {COLORS['border_dim']};
                border-radius: 4px;
                padding: 12px;
            }}
        """)
        props_text.setPlainText("Name: None\nType: None\nStatus: Idle\nLast Modified: N/A")
        action_layout.addWidget(props_text)

        layout.addWidget(action_container)

        return container

    def create_status_bar(self):
        """Bottom status bar with soft fade palette."""
        status_bar = QWidget()
        status_bar.setFixedHeight(34)
        status_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_input']};
                border-top: 2px solid {COLORS['border_bright']};
            }}
        """)

        layout = QHBoxLayout(status_bar)
        layout.setContentsMargins(20, 0, 20, 0)

        status = QLabel("Ready")
        status.setFont(QFont("White Rabbit", 10))
        status.setStyleSheet(f"color: {COLORS['primary_dim']}; border: none;")
        layout.addWidget(status)

        layout.addStretch()

        version = QLabel("PhiVector v1.0.0")
        version.setFont(QFont("White Rabbit", 10))
        version.setStyleSheet(f"color: {COLORS['primary_dim']}; border: none;")
        layout.addWidget(version)

        return status_bar

    def create_chrome_separator(self):
        """Chrome rib tactical separator."""
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFixedHeight(40)
        sep.setFixedWidth(2)
        sep.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['border_bright']};
                border: none;
            }}
        """)
        return sep

    def create_indicator(self, name, value, color):
        """System indicator with tactical styling."""
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {INTERACTION_STATES['hover_bg']};
                border: 1px solid {COLORS['border_dim']};
                border-radius: 4px;
            }}
        """)

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        name_label = QLabel(name)
        name_label.setFont(QFont("Kanit", 10, QFont.Weight.Bold))
        name_label.setStyleSheet(f"color: {COLORS['primary_dim']}; border: none; background: transparent;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Kanit", 10, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color}; border: none; background: transparent;")

        layout.addWidget(name_label)
        layout.addWidget(value_label)

        return widget

    def create_quick_action_button(self, label, icon):
        """Tactical quick action button."""
        btn = QPushButton(f"{icon} {label}")
        btn.setFont(QFont("Kanit", 11))
        btn.setMinimumWidth(115)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {INTERACTION_STATES['hover_bg']};
                color: {COLORS['primary']};
                border: 1px solid {COLORS['border_dim']};
                border-radius: 5px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 238, 0, 0.22);
                border: 1px solid {COLORS['border_bright']};
            }}
            QPushButton:pressed {{
                background-color: {INTERACTION_STATES['selected_bg']};
            }}
        """)
        return btn

    def create_tool_card(self, title, status, icon):
        """Tool card with brushed metal texture hint."""
        card = QWidget()
        card.setMinimumHeight(95)
        card.setStyleSheet(f"""
            QWidget {{
                background-color: {INTERACTION_STATES['hover_bg']};
                border: 1px solid {COLORS['border_dim']};
                border-radius: 6px;
            }}
            QWidget:hover {{
                background-color: rgba(0, 238, 0, 0.15);
                border: 1px solid {COLORS['border_bright']};
            }}
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 14, 20, 14)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 36))
        icon_label.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(icon_label)

        layout.addSpacing(20)

        # Text
        text_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Xolonium", 14, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {COLORS['primary']}; border: none; background: transparent;")
        text_layout.addWidget(title_label)

        status_label = QLabel(status)
        status_label.setFont(QFont("White Rabbit", 11))
        status_label.setStyleSheet(f"color: {COLORS['primary_dim']}; border: none; background: transparent;")
        text_layout.addWidget(status_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        return card

    def toggle_maximize(self):
        """Toggle window maximize."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        """Window dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() <= 28:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        """Window dragging."""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Window dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("White Rabbit", 11))

    window = PhiVectorControlBridge()
    window.show()

    sys.exit(app.exec())
