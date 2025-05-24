import json

import pytesseract
from PIL import Image

image_path = "data/Pictures/IMG_7789.jpg"

image = Image.open(image_path)

text = pytesseract.image_to_string(image)

text_json = json.dumps({"text": text}, indent=4)
