#!/usr/bin/env python3
"""
Qt Designer .ui File Layout Analyzer
Analyzes Qt Designer .ui files and explains layout structure, size policies, and potential issues
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Tuple, Dict

class UILayoutAnalyzer:
    def __init__(self, ui_file_path):
        self.ui_file_path = Path(ui_file_path)
        self.tree = None
        self.root = None
        self.issues = []
        self.info = []
        
    def load_file(self):
        """Load and parse the .ui file"""
        try:
            self.tree = ET.parse(self.ui_file_path)
            self.root = self.tree.getroot()
            return True
        except ET.ParseError as e:
            print(f"❌ Error parsing XML: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ File not found: {self.ui_file_path}")
            return False
    
    def analyze_layout_structure(self, element=None, depth=0):
        """Recursively analyze layout structure"""
        if element is None:
            element = self.root
        
        indent = "  " * depth
        
        # Check for widgets
        for widget in element.findall('.//widget'):
            widget_class = widget.get('class', 'Unknown')
            widget_name = widget.get('name', 'unnamed')
            
            # Check if widget has geometry (absolute positioning)
            geometry = widget.find('./property[@name="geometry"]')
            if geometry is not None and depth == 0:
                rect = geometry.find('rect')
                if rect is not None:
                    x = rect.find('x').text if rect.find('x') is not None else '?'
                    y = rect.find('y').text if rect.find('y') is not None else '?'
                    w = rect.find('width').text if rect.find('width') is not None else '?'
                    h = rect.find('height').text if rect.find('height') is not None else '?'
                    
                    # Check if this widget is in a layout
                    parent_layout = self._find_parent_layout(widget)
                    if parent_layout is None:
                        self.issues.append(
                            f"⚠️  {widget_class} '{widget_name}' uses absolute positioning "
                            f"(x:{x}, y:{y}, w:{w}, h:{h}) and is NOT in a layout"
                        )
        
        # Check for layouts
        for layout in element.findall('.//layout'):
            layout_class = layout.get('class', 'Unknown')
            layout_name = layout.get('name', 'unnamed')
            
            self.info.append(f"{indent}📐 {layout_class} '{layout_name}'")
            
            # Analyze layout properties
            spacing = layout.find("./property[@name='spacing']")
            if spacing is not None:
                spacing_val = spacing.find('number')
                if spacing_val is not None:
                    self.info.append(f"{indent}   Spacing: {spacing_val.text}px")
            
            # Check for items in layout
            items = layout.findall('./item')
            self.info.append(f"{indent}   Items: {len(items)}")
            
            # Recursively analyze children
            for item in items:
                child_widget = item.find('./widget')
                if child_widget is not None:
                    self._analyze_widget_in_layout(child_widget, depth + 1)
    
    def _find_parent_layout(self, widget_element):
        """Check if widget has a parent layout"""
        parent = widget_element
        for _ in range(10):  # Safety limit
            parent = self._find_parent(parent)
            if parent is None:
                return None
            if parent.tag == 'layout':
                return parent
        return None
    
    def _find_parent(self, element):
        """Find parent of an element (ElementTree doesn't have parent pointers)"""
        for parent in self.root.iter():
            if element in list(parent):
                return parent
        return None
    
    def _analyze_widget_in_layout(self, widget, depth):
        """Analyze a widget that's inside a layout"""
        indent = "  " * depth
        widget_class = widget.get('class', 'Unknown')
        widget_name = widget.get('name', 'unnamed')
        
        # Get size policy
        size_policy = widget.find("./property[@name='sizePolicy']")
        if size_policy is not None:
            hsizetype = size_policy.find(".//sizepolicy[@hsizetype]")
            vsizetype = size_policy.find(".//sizepolicy[@vsizetype]")
            
            h_policy = hsizetype.get('hsizetype') if hsizetype is not None else 'Unknown'
            v_policy = vsizetype.get('vsizetype') if vsizetype is not None else 'Unknown'
            
            self.info.append(
                f"{indent}└─ {widget_class} '{widget_name}' "
                f"(H:{h_policy}, V:{v_policy})"
            )
            
            # Check for common size policy issues
            if h_policy == 'Fixed' and v_policy == 'Fixed':
                self.issues.append(
                    f"⚠️  {widget_class} '{widget_name}' has Fixed size policy in both directions - won't resize"
                )
        else:
            self.info.append(f"{indent}└─ {widget_class} '{widget_name}' (default size policy)")
    
    def check_main_window_layout(self):
        """Check if main window has a layout"""
        main_window = self.root.find(".//widget[@class='QMainWindow']")
        if main_window is not None:
            central_widget = main_window.find(".//widget[@class='QWidget']")
            if central_widget is not None:
                layout = central_widget.find('./layout')
                if layout is None:
                    self.issues.append(
                        "❌ CRITICAL: Central widget has NO layout! "
                        "Window resizing will not work properly."
                    )
                else:
                    layout_class = layout.get('class', 'Unknown')
                    self.info.append(f"✅ Central widget has {layout_class}")
    
    def analyze_size_constraints(self):
        """Check for widgets with size constraints"""
        for widget in self.root.findall('.//widget'):
            widget_class = widget.get('class', 'Unknown')
            widget_name = widget.get('name', 'unnamed')
            
            min_size = widget.find("./property[@name='minimumSize']")
            max_size = widget.find("./property[@name='maximumSize']")
            
            if min_size is not None or max_size is not None:
                constraint_info = []
                
                if min_size is not None:
                    size = min_size.find('./size')
                    if size is not None:
                        w = size.find('width').text if size.find('width') is not None else '?'
                        h = size.find('height').text if size.find('height') is not None else '?'
                        constraint_info.append(f"min:{w}x{h}")
                
                if max_size is not None:
                    size = max_size.find('./size')
                    if size is not None:
                        w = size.find('width').text if size.find('width') is not None else '?'
                        h = size.find('height').text if size.find('height') is not None else '?'
                        constraint_info.append(f"max:{w}x{h}")
                
                self.info.append(
                    f"📏 {widget_class} '{widget_name}' has size constraints: {', '.join(constraint_info)}"
                )
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*70)
        print("🔍 Qt Designer Layout Analysis Report")
        print("="*70)
        print(f"📁 File: {self.ui_file_path}")
        
        # Main window layout check
        print("\n" + "─"*70)
        print("🏗️  Main Window Structure")
        print("─"*70)
        self.check_main_window_layout()
        
        # Layout structure
        print("\n" + "─"*70)
        print("📐 Layout Hierarchy")
        print("─"*70)
        self.analyze_layout_structure()
        
        # Size constraints
        print("\n" + "─"*70)
        print("📏 Size Constraints")
        print("─"*70)
        self.analyze_size_constraints()
        
        # Print info
        if self.info:
            print("\n💡 Layout Information:")
            for info in self.info:
                print(f"   {info}")
        
        # Print issues
        print("\n" + "="*70)
        if self.issues:
            print("⚠️  Issues Found:")
            for issue in self.issues:
                print(f"   {issue}")
            print("\n💡 Recommendations:")
            print("   - Widgets with absolute positioning should be placed in layouts")
            print("   - Use size policies to control resizing behavior")
            print("   - Always apply a layout to the central widget")
        else:
            print("✅ No major issues detected!")
        
        print("="*70)
    
    def get_layout_recommendations(self):
        """Provide specific recommendations for PhiGEN"""
        print("\n" + "="*70)
        print("💡 PhiGEN-Specific Recommendations")
        print("="*70)
        
        recommendations = [
            "1. Main Layout: Use QVBoxLayout on central widget",
            "2. Title: QLabel with Fixed vertical, Expanding horizontal size policy",
            "3. Input fields: QLineEdit with Expanding horizontal size policy",
            "4. Buttons: Use QHBoxLayout or QGridLayout with Expanding policies",
            "5. Custom button images: Set min-width/min-height, use border-image in stylesheet",
            "6. Status bar: QHBoxLayout with Fixed vertical size policy",
            "7. Set margins on main layout: 15-20px for professional spacing",
            "8. Set spacing between widgets: 10-15px",
        ]
        
        for rec in recommendations:
            print(f"   {rec}")


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║        Qt Designer Layout Analyzer                       ║
║        Understand Your UI Structure                      ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Get UI file path
    if len(sys.argv) > 1:
        ui_file = sys.argv[1]
    else:
        ui_file = input("Enter path to .ui file: ").strip().strip('"')
    
    if not ui_file:
        print("❌ No file specified")
        sys.exit(1)
    
    # Analyze
    analyzer = UILayoutAnalyzer(ui_file)
    
    if not analyzer.load_file():
        sys.exit(1)
    
    analyzer.generate_report()
    analyzer.get_layout_recommendations()
    
    print("\n📚 For detailed layout guide, see: QT_DESIGNER_LAYOUT_GUIDE.md")


if __name__ == "__main__":
    main()
