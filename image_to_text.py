from PIL import Image
import pytesseract
from googletrans import Translator

result = pytesseract.image_to_string(
    Image.open(f'AgACAgQAAxkBAAOzYiONHyOprDwpfmj0Jvblf0s62y8AAm23MRtnxhhRnCgyYLkPXPYBAAMCAAN5AAMjBA.jpg'))
print(result)

translation = Translator().translate(result, dest="fa")
print(translation.text)
