from docx import Document
import string
x=0
doc = Document('C:/Users/serem/Desktop/Laba3.docx')


def detect_latin_letters(paragraph):
    latin_letters = set(string.ascii_letters)
    x % 2 != 0
    char_count = 0
    for run in paragraph.runs:
        if any(char in latin_letters for char in run.text):
            print(f"YES:  '{paragraph.text}'")
            break
    else:
        print(f"NO:  '{paragraph.text}'")

    char_count = len(paragraph.text)

    #print(f"Количество символов в строке '{paragraph.text}': {char_count}")


for paragraph in doc.paragraphs:
    detect_latin_letters(paragraph)