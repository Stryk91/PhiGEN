from PIL import Image
import numpy as np

# Load the image
img = Image.open('E:/PythonProjects/PhiGEN/TEMPSVG/Final_Title_Draft.png').convert('RGBA')
data = np.array(img)

print(f"Original size: {img.size}")

# Get the color channels
red, green, blue, alpha = data.T

# More aggressive: remove anything that looks like background
# This includes white and very light colors
light_bg = (red > 200) & (green > 200) & (blue > 200)

# Make light background areas transparent
data[..., 3][light_bg.T] = 0

# Create result image
result = Image.fromarray(data)

# Save the result
result.save('E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE.png')

print(f'Background removed! Image saved')
print(f'Final size: {result.size}')
