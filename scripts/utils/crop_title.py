from PIL import Image
import numpy as np

# Load the original image
img = Image.open('E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE.png').convert('RGBA')
data = np.array(img)

# Find non-white pixels (anything that's not pure white)
# We'll look for pixels that are not white (RGB < 250)
red, green, blue, alpha = data.T
not_white = (red < 250) | (green < 250) | (blue < 250)

# Find the bounding box of non-white content
rows = np.any(not_white, axis=1)
cols = np.any(not_white, axis=0)

if rows.any() and cols.any():
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    # Crop to the bounding box
    cropped = img.crop((cmin, rmin, cmax + 1, rmax + 1))

    # Now make any remaining white areas transparent
    data_cropped = np.array(cropped)
    red, green, blue, alpha = data_cropped.T
    white_areas = (red > 245) & (green > 245) & (blue > 245)
    data_cropped[..., 3][white_areas.T] = 0

    # Save the result
    result = Image.fromarray(data_cropped)
    result.save('E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE.png')

    print(f'Image cropped and white areas removed! New size: {result.size}')
else:
    print('No content found')
