# Resize all images in a folder to 512x512
from PIL import Image
import glob

for img_path in glob.glob("/Users/luisgago/renpy-8.4.1-sdk/Radiology Cases/game/images/breast/**/*.png", recursive=True):
    img = Image.open(img_path)
    img = img.resize((512, 512), Image.LANCZOS)
    img.save(img_path)