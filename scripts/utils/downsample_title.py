from PIL import Image

# Load the current title (1800x250)
img = Image.open('E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE.png')

print(f"Original size: {img.size}")

# Calculate aspect ratio to maintain proportions
original_width, original_height = img.size
aspect_ratio = original_width / original_height

# Target size around 800x100, but maintain aspect ratio
target_width = 800
target_height = int(target_width / aspect_ratio)

print(f"Target size: {target_width}x{target_height}")

# Downsample using LANCZOS for maximum quality
img_resized = img.resize((target_width, target_height), Image.LANCZOS)

# Save the downsampled version
img_resized.save('E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE_800.png')

print(f"[OK] Downsampled title saved as PHIGEN_TITLE_800.png ({target_width}x{target_height})")
