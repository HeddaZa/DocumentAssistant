from PIL import Image
import pytesseract
import json

image_path = 'data/Pictures/IMG_7789.jpg'

image = Image.open(image_path)

text = pytesseract.image_to_string(image)

text_json = json.dumps({"text": text}, indent=4)

print(text_json)

# # Optionally, save the JSON to a file
# with open('output.json', 'w') as json_file:
#     json_file.write(text_json)