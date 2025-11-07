#!/usr/bin/env python3
"""
SVG to PNG converter using cairosvg with MSYS2 Cairo libraries.
Produces high-quality PNG output with accurate SVG filter/gradient rendering.
"""

import os
import sys
import argparse
from pathlib import Path

# Add MSYS2 Cairo DLLs to the search path
CAIRO_BIN = r'E:\Utilities\MINGSYS2\ucrt64\bin'
os.environ['PATH'] = CAIRO_BIN + os.pathsep + os.environ.get('PATH', '')

if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(CAIRO_BIN)

try:
    import cairosvg
except ImportError:
    print("Error: cairosvg not installed. Run: pip install cairosvg")
    sys.exit(1)


def svg_to_png(svg_path, png_path=None, width=None, height=None, scale=1.0):
    """
    Convert SVG to PNG using cairosvg.

    Args:
        svg_path: Path to input SVG file
        png_path: Path to output PNG file (optional, defaults to same name with .png)
        width: Output width in pixels (optional)
        height: Output height in pixels (optional)
        scale: Scale multiplier (optional, e.g. 2.0 for 2x resolution)

    Returns:
        Path to the created PNG file
    """
    svg_path = Path(svg_path)

    if not svg_path.exists():
        raise FileNotFoundError(f"SVG file not found: {svg_path}")

    # Default output path
    if png_path is None:
        png_path = svg_path.with_suffix('.png')
    else:
        png_path = Path(png_path)

    # Prepare conversion parameters
    params = {
        'url': str(svg_path),
        'write_to': str(png_path)
    }

    if width is not None:
        params['output_width'] = int(width * scale)
    if height is not None:
        params['output_height'] = int(height * scale)

    if width is None and height is None and scale != 1.0:
        params['scale'] = scale

    # Convert
    cairosvg.svg2png(**params)

    return png_path


def main():
    parser = argparse.ArgumentParser(
        description='Convert SVG to PNG using cairosvg with high quality rendering'
    )
    parser.add_argument('svg_file', help='Input SVG file path')
    parser.add_argument('-o', '--output', help='Output PNG file path (optional)')
    parser.add_argument('-w', '--width', type=int, help='Output width in pixels')
    parser.add_argument('--height', type=int, help='Output height in pixels')
    parser.add_argument('-s', '--scale', type=float, default=1.0,
                       help='Scale multiplier (e.g., 2.0 for 2x resolution)')

    args = parser.parse_args()

    try:
        output_path = svg_to_png(
            args.svg_file,
            args.output,
            args.width,
            args.height,
            args.scale
        )

        file_size = output_path.stat().st_size
        print(f"Success! PNG created: {output_path}")
        print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()