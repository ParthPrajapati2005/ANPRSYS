try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\parth\Desktop\ANPR\TFODCourse\Tesseract\tesseract.exe'

text_from_image = pytesseract.image_to_string(Image.open("car2.jpg"),
                                  lang="eng+eng2")
print(text_from_image)