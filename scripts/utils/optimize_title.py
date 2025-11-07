from PIL import Image
import os

# Load the super high-res FINALTITLEFORUSE.png (7144x1224)
img = Image.open('E:/PythonProjects/PhiGEN/TEMPSVG/FINALTITLEFORUSE.png')

print(f"Source dimensions: {img.size} (super high resolution)")

# Calculate aspect ratio
original_width, original_height = img.size
aspect_ratio = original_width / original_height

# Downsample to program-friendly size (let's try 1200px width - good balance)
target_width = 1200
target_height = int(target_width / aspect_ratio)

print(f"Target dimensions: {target_width}x{target_height}")

# Downsample using LANCZOS from the super high-res source = excellent quality
img_resized = img.resize((target_width, target_height), Image.LANCZOS)

# Save with optimized PNG compression
output_path = 'E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE_PREVIEW.png'
img_resized.save(output_path, 'PNG', optimize=True, compress_level=9)

# Get file size
new_size = os.path.getsize(output_path) / 1024

print(f"File size: {new_size:.1f} KB")
print(f"\n[OK] High-quality downsampled title saved as PHIGEN_TITLE_PREVIEW.png")
print(f"Starting from {original_width}x{original_height} ensures excellent quality!")
print(f"This is a PREVIEW - not yet applied to the program")
