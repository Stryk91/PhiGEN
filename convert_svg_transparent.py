from cairosvg import svg2png

# Convert SVG to PNG with transparent background
svg2png(
    url='E:/PythonProjects/PhiGEN/TEMPSVG/phigen_title_complete_paths.svg',
    write_to='E:/PythonProjects/PhiGEN/TEMPSVG/PHIGEN_TITLE.png',
    output_width=1800,  # High resolution for quality
    background_color='transparent'
)

print('PNG generated with transparent background!')
