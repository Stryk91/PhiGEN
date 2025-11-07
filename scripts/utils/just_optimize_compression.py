from PIL import Image

# Just optimize compression on the HIGH-RES file, don't resize
img = Image.open('E:/PythonProjects/PhiGEN/TEMPSVG/FINALTITLEFORUSE.png')
print(f"Keeping full resolution: {img.size}")

# Save with optimized compression only
img.save('E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE_FINAL.png', 'PNG', optimize=True, compress_level=9)
print("Done - high-res file saved as PHIGEN_TITLE_FINAL.png")
