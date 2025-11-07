from PIL import Image

# Load the FINALTITLEFORUSE.png
img = Image.open('E:/PythonProjects/PhiGEN/TEMPSVG/FINALTITLEFORUSE.png')

print(f"Original size: {img.size}")

# Calculate aspect ratio to maintain proportions
original_width, original_height = img.size
aspect_ratio = original_width / original_height

# Keep it at higher resolution for better quality - 2000px width
target_width = 2000
target_height = int(target_width / aspect_ratio)

print(f"Target size: {target_width}x{target_height}")

# Downsample using LANCZOS for maximum quality
img_resized = img.resize((target_width, target_height), Image.LANCZOS)

# Save the downsampled version for preview
img_resized.save('E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE_PREVIEW.png')

print(f"[OK] High-quality downsampled title saved as PHIGEN_TITLE_PREVIEW.png ({target_width}x{target_height})")
print(f"This is a PREVIEW - not yet applied to the program")
