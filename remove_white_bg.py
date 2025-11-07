from PIL import Image
import numpy as np

# Load the image
img = Image.open('E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE.png').convert('RGBA')
data = np.array(img)

# Get the color channels
red, green, blue, alpha = data.T

# Find white or light gray areas (more aggressive threshold)
# This will catch anything that's very light
white_areas = (red > 240) & (green > 240) & (blue > 240)

# Make white areas transparent
data[..., 3][white_areas.T] = 0

# Save the result
result = Image.fromarray(data)
result.save('E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE.png')

print('White areas removed successfully!')
