from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def userInputSaveAsFile(title:str='Select a file to save'):
    """Returns the full path of a user-selected file to save"""
    from tkinter.filedialog import asksaveasfilename
    filename = asksaveasfilename(
        filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
        title=title
        )
    return filename




def saveFillImage(puzzleGrid, blockSize, lineWidth):

    rows = len(puzzleGrid)
    cols = len(puzzleGrid[0])

    # Set canvas dimensions
    canvasWidth = blockSize * cols + lineWidth
    canvasHeight = blockSize * rows + lineWidth
    # PIL create an empty image and draw object to draw on
    # memory only, not visible
    image1 = Image.new("RGB", (canvasWidth, canvasHeight), 'white')
    draw = ImageDraw.Draw(image1)
    # Initialize block colors
    # block_colors = [['#ffffff' if cell != '.' else '#000000' for cell in row] for row in puzzleGrid]
    # Fill blocks with colors
    for i in range(rows):
        for j in range(cols):
            if puzzleGrid[i][j] == '.':
                x1, y1 = j * blockSize + lineWidth, i * blockSize + lineWidth
                x2, y2 = x1 + blockSize, y1 + blockSize
                draw.rectangle(((x1, y1), (x2, y2)), fill='#000000', width=0)
    # Fill in the letters
    # for i in range(rows):
    #     for j in range(cols):
    #         x = int(j * blockSize + (lineWidth) + blockSize / 2)
    #         y = int(i * blockSize + (lineWidth + lineWidth) + blockSize / 2)
    #         draw.text(
    #             (x, y),
    #             text=puzzleGrid[i][j],
    #             fill='#000000',
    #             anchor='mm',
    #             font=ImageFont.truetype('assets\\Monaco.ttf', int(blockSize / 2 + 3))
    #         )
    # Draw grid lines
    for i in range(rows + 1):
        y = i * blockSize# + lineWidth
        draw.line(((0, y), (canvasWidth - lineWidth, y)), fill='#000000', width=lineWidth)
    for j in range(cols + 1):
        x = j * blockSize# + lineWidth
        draw.line(((x, 0), (x, canvasWidth - lineWidth)), fill='#000000', width=lineWidth)
    # PIL image can be saved as .png .jpg .gif or .bmp file (among others)
    outputFile = userInputSaveAsFile()
    if outputFile:
        image1.save(outputFile)
    else:
        return


puzzleGrid = [
    'ALTOS.SHOX.RISP',
	'GEEKE.OUTX.ATHA',
	'GARGO.LESXANSEL',
	'IFSOXN.SXONSALE',
	'..EXCAR.JACO...',
	'XXXC.MPLET.MESS',
	'URBAXOAS.SXWAIL',
	'SEL.SXNAPXM.UDE',
	'PAULXX.TSTXXTED',
	'SPEX.ALSAU.EXXX',
	'...ENDS.FLYXS..',
	'STINTSXF.AXSTAR',
	'HADTOXDAR.ITALL',
	'AMGE.XOKI.DOKIE',
	'DEER.XWES.OPENS'
]    
blockSize = 40
lineWidth = 1

saveFillImage(puzzleGrid, blockSize, lineWidth)

