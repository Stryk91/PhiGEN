# PhiVector Texture Pack

Production-ready tactical textures for PhiVector Control Bridge UI.

## Textures Included

1. **carbon-fibre.svg** - Twill-inspired carbon fiber weave (16x16px tile)
2. **chrome-vein.svg** - Metallic highlight veins (128x128px tile)
3. **snake-scale.svg** - Organic metallic scales (48x28px tile)
4. **graphene-mesh.svg** - Hexagonal lattice pattern (24x20.7846px tile)
5. **mesh-ultra.svg** - Ultra-fine crosshatch grid (8x8px tile)
6. **textures-sprite.svg** - Combined sprite for inline SVG usage

## Usage

### Option A: CSS Background (Recommended)

```css
:root {
  --tex-carbon: url('/assets/textures/carbon-fibre.svg');
  --tex-graphene: url('/assets/textures/graphene-mesh.svg');
  --tex-chrome: url('/assets/textures/chrome-vein.svg');
}

.app-surface {
  background-color: #0D0D0D; /* Soft black base */
  background-image:
    var(--tex-chrome),
    var(--tex-graphene),
    var(--tex-carbon);
  background-repeat: repeat;
  background-size:
    220px 220px,  /* chrome vein */
    48px 41.57px, /* graphene */
    16px 16px;    /* carbon fibre */
  background-blend-mode: screen, overlay, multiply;
}
```

### Option B: Inline SVG with Sprite

Include `textures-sprite.svg` once, then reference patterns:

```html
<svg viewBox="0 0 100 100" style="position:fixed;inset:0;pointer-events:none">
  <rect width="100%" height="100%" fill="url(#tex-carbon-fibre)" opacity="0.25"/>
  <rect width="100%" height="100%" fill="url(#tex-graphene)" opacity="0.15"/>
  <rect width="100%" height="100%" fill="url(#tex-chrome-vein)" opacity="0.18"/>
</svg>
```

## Recommended Layer Stack

```
Layer 1: Carbon fiber - 8-10% opacity (base structure)
Layer 2: Graphene mesh - 3-5% opacity (detail)
Layer 3: Chrome vein - 2-4% opacity (highlights)
Layer 4: Mesh ultra - 2-3% opacity (micro-texture)
```

## Color Palette Integration

Base colors for PhiVector:
- Background base: `#0D0D0D` (soft black)
- Panel background: `#151515`
- Primary green: `#00EE00`
- Dimmed green: `#00AA00`
- Accent teal: `#00FFAA`

## Pre-rendering to PNG

Use Cairo to render high-quality PNGs:

```python
# render_textures.py
import cairo

def render_svg_to_png(svg_path, png_path, scale=2, dpi=300):
    # Render at 2x with 300 DPI for crisp display
    pass

# Batch render all textures
textures = ['carbon-fibre', 'chrome-vein', 'snake-scale', 'graphene-mesh', 'mesh-ultra']
for tex in textures:
    render_svg_to_png(f'{tex}.svg', f'{tex}_2x.png', scale=2, dpi=300)
```

## Performance Tips

- Pre-render SVGs to PNG for production (use build script)
- Keep background-size close to native tile size
- Use texture caching in PySide6
- Layer no more than 3-4 textures for optimal performance

## License

Part of PhiVector Control Bridge by PhiGEN project.
