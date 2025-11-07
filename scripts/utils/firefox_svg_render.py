"""
Firefox high-res screenshot + downscale for smooth shadows
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from PIL import Image
import time
from pathlib import Path

def firefox_8x_screenshot(svg_path, output_path, final_width=1400, final_height=200):
    """Render at 8× then downscale for smooth anti-aliasing"""

    render_width = final_width * 8
    render_height = final_height * 8

    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Firefox(options=options)

    # Load SVG
    svg_file = Path(svg_path).absolute().as_uri()
    print(f"Loading: {svg_file}")
    driver.get(svg_file)

    # Inject JavaScript to set high resolution
    driver.execute_script(f"""
        document.querySelector('svg').style.width = '{render_width}px';
        document.querySelector('svg').style.height = '{render_height}px';
    """)

    time.sleep(2)  # Let render

    # Screenshot
    temp_file = 'temp_8x.png'
    element = driver.find_element('tag name', 'svg')
    element.screenshot(temp_file)
    driver.quit()

    # Downscale with Lanczos (high quality)
    img = Image.open(temp_file)
    img_resized = img.resize((final_width, final_height), Image.LANCZOS)
    img_resized.save(output_path)

    print(f"[OK] Smooth 8x render: {output_path}")

# Run the conversion
svg_path = r"E:\PythonProjects\PhiGEN\TEMPSVG\phigen_title_xirod_framed.svg"
output_path = r"E:\PythonProjects\PhiGEN\TEMPSVG\PHIGEN_TITLE.png"

firefox_8x_screenshot(svg_path, output_path, final_width=1800, final_height=250)
