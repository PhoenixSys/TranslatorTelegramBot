from PIL import Image
import pytesseract

result = pytesseract.image_to_string(
    Image.open(f'AgACAgQAAxkBAAOzYiONHyOprDwpfmj0Jvblf0s62y8AAm23MRtnxhhRnCgyYLkPXPYBAAMCAAN5AAMjBA.jpg'))
print(result)
