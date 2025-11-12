#!/usr/bin/env python3
"""
PhiGEN Asset Renderer - Pre-render SVG textures to high-quality PNGs
Run once when SVG assets change, not at runtime.

Usage:
    python scripts/utils/render_svg_assets.py
"""

import sys
from pathlib import Path
from io import BytesIO

try:
    import cairosvg
    from PIL import Image
except ImportError:
    print("ERROR: Missing dependencies. Install with:")
    print("  pip install cairosvg pillow")
    sys.exit(1)


def render_svg_to_png(svg_path: Path, output_path: Path, scale: int = 2, dpi: int = 300):
    """
    Render SVG to high-quality PNG using Cairo.

    Args:
        svg_path: Path to source SVG file
        output_path: Path to output PNG file
        scale: Rendering scale (2 = 2x supersampling)
        dpi: DPI for rendering (300 = high quality)
    """
    if not svg_path.exists():
        print(f"[SKIP] {svg_path.name} - file not found")
        return False

    try:
        # Read SVG to get dimensions
        with open(svg_path, 'rb') as f:
            svg_data = f.read()

        # Render at 2x scale with high DPI for supersampling
        png_bytes = cairosvg.svg2png(
            bytestring=svg_data,
            scale=scale,
            dpi=dpi
        )

        # Save directly
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(png_bytes)

        # Get file size for reporting
        size_kb = len(png_bytes) / 1024

        print(f"[DONE] {svg_path.name:30s} → {output_path.name:35s} ({size_kb:6.1f} KB)")
        return True

    except Exception as e:
        print(f"[FAIL] {svg_path.name} - {e}")
        return False


def main():
    """Pre-render all tactical SVG textures to high-quality PNGs."""

    print("=" * 80)
    print("PhiGEN Asset Renderer - Cairo SVG to PNG (2x @ 300 DPI)")
    print("=" * 80)
    print()

    # Paths
    project_root = Path(__file__).parent.parent.parent
    svg_dir = project_root / "old" / "TEMPSVG"
    output_dir = project_root / "assets" / "textures" / "rendered"

    # SVG textures to render
    textures = [
        # Tactical textures (original SVGs)
        "brushed_metal_dark.svg",
        "chrome_ribs.svg",
        "diamond_mesh.svg",
        "bee_sting_brackets.svg",

        # Circuit backgrounds (if SVG versions exist)
        "circuit_background.svg",
        "circuit_background_tileable.svg",
    ]

    print(f"Source directory:  {svg_dir}")
    print(f"Output directory:  {output_dir}")
    print()
    print("Rendering textures...")
    print("-" * 80)

    success_count = 0
    total_count = 0

    for texture_name in textures:
        svg_path = svg_dir / texture_name
        output_name = texture_name.replace('.svg', '_2x.png')
        output_path = output_dir / output_name

        total_count += 1
        if render_svg_to_png(svg_path, output_path, scale=2, dpi=300):
            success_count += 1

    print("-" * 80)
    print()
    print(f"Complete: {success_count}/{total_count} textures rendered successfully")
    print()
    print("Output location:")
    print(f"  {output_dir}")
    print()
    print("These pre-rendered PNGs can now be used in the app at runtime.")
    print("No need to render SVGs during app execution.")
    print("=" * 80)


if __name__ == "__main__":
    main()
