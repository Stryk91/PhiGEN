from PIL import Image
import xml.etree.ElementTree as ET

# Try using Inkscape if available, otherwise use a Python library
import subprocess
import os

# Check if Inkscape is available
inkscape_paths = [
    r"C:\Program Files\Inkscape\bin\inkscape.exe",
    r"C:\Program Files (x86)\Inkscape\bin\inkscape.exe",
]

inkscape_exe = None
for path in inkscape_paths:
    if os.path.exists(path):
        inkscape_exe = path
        break

if inkscape_exe:
    # Use Inkscape for high-quality conversion with transparency
    subprocess.run([
        inkscape_exe,
        "E:/PythonProjects/PhiGEN/TEMPSVG/phigen_title_complete_paths.svg",
        "--export-type=png",
        "--export-filename=E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE.png",
        "--export-width=1800",
        "--export-background-opacity=0"
    ], check=True)
    print("PNG generated with Inkscape!")
else:
    print("Inkscape not found. Please install Inkscape or use another method.")
