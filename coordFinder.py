import os
import fitz
import matplotlib.pyplot as plt

from utils import resource_path


doc = fitz.open(resource_path(os.path.join("origonalPDFs", "Sage MinSurg Consent.pdf")))
page = doc[1]
pix = page.get_pixmap(dpi=150)
img = pix.tobytes("png")

import io
from PIL import Image
image = Image.open(io.BytesIO(img))

fig, ax = plt.subplots()
ax.imshow(image)

scale = 150 / 72  # dpi vs PDF points

def onclick(event):
    if event.xdata is not None:
        pdf_x = event.xdata / scale
        pdf_y = event.ydata / scale
        print(f"x={pdf_x:.0f}, y={pdf_y:.0f}")

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()