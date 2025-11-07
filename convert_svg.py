import os
import sys

# Add MSYS2 bin to PATH so cairocffi can find libcairo-2.dll
os.environ['PATH'] = r'E:\Utilities\MINGSYS2\ucrt64\bin' + os.pathsep + os.environ.get('PATH', '')

import cairosvg

svg_path = sys.argv[1]
output_path = sys.argv[2]
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

cairosvg.svg2png(url=svg_path, write_to=output_path, scale=scale)
print(f"Rendered {svg_path} to {output_path} at {scale}x scale")