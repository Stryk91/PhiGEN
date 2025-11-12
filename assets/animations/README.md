# Tactical Satellite Scan Animation

**CIA/FBI-style wireframe topographical satellite view of Central Victoria**

## Files

### Animated GIFs
- `central_victoria_tactical_scan.gif` - Standard version (330 KB)
- `central_victoria_tactical_scan_hq.gif` - High quality version (330 KB)

### PNG Frames (800x600, 150 DPI)
1. `topo_frame_1.png` - Wide view
2. `topo_frame_2.png` - Zoom in / Scanning
3. `topo_frame_3.png` - Target lock
4. `topo_frame_4.png` - Enhanced detail
5. `topo_frame_5.png` - Maximum resolution
6. `topo_frame_6.png` - Scan complete / Confirmed

### SVG Source Files
Located in `svg_source/` directory for easy editing

## Technical Details

**Location**: Central Victoria, Australia
- Latitude: -37.8136° S
- Longitude: 144.9631° E

**Theme**: PhiVector Matrix
- Background: Soft black (#0D0D0D)
- Primary wireframe: Bright green (#00FF00)
- Secondary: Medium green (#00EE00, #00DD00)
- Dimmed elements: Dark green (#00AA00)

**Animation Timing**:
- Frame 1: 0.8 seconds (initial view)
- Frames 2-5: 0.4 seconds each (zoom/scan progression)
- Frame 6: 1.2 seconds (hold on confirmed)
- Loop: Infinite

**Visual Style**:
- Wireframe topographical contour lines
- Tactical grid overlay
- 3D perspective wireframe base
- Targeting reticle with crosshairs
- Lock-on brackets
- Coordinate data overlay
- Progressive zoom effect
- Scanning line animation

## Usage

Perfect for:
- Hacker/tactical aesthetic backgrounds
- Video intros/outros
- Presentation slides
- Desktop wallpapers (animated)
- Social media content
- Cybersecurity/tech demos

## Customization

To modify:
1. Edit SVG files in `svg_source/`
2. Regenerate PNGs:
   ```bash
   convert -density 150 -background "#0D0D0D" svg_source/topo_frame_X.svg topo_frame_X.png
   ```
3. Recreate GIF:
   ```bash
   convert -delay 80 topo_frame_1.png \
           -delay 40 topo_frame_{2..5}.png \
           -delay 120 topo_frame_6.png \
           -loop 0 output.gif
   ```

---

**Created with**: PhiGEN Tactical Design System
**Font**: White Rabbit (monospace)
**Color Palette**: PhiVector Matrix Soft Fade
