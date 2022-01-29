import re
import cv2
import pytesseract
from pytesseract import Output
from mrz import *

# pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

# read image file
IMAGE_PATH = 'images/test3.jpg'

# gets the machine readable zone (MRZ) of the passport
images = getROI(IMAGE_PATH)
print(len(images))

# empty list to store lines of text gotten from the MRZ
lines = []

# get text from MRZ and store in lines list
for img in images:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    d = pytesseract.image_to_data(img, output_type=Output().DICT)
    lines.append(constructString(d['text']))

# pattern matching to find user and document data
pattern = r'P(<|[A-Z])([A-Z]{3})([A-Z]{2,})<{1,2}([A-Z]{2,})<{1,2}([A-Z]{2,})*'
user_data = re.compile(pattern)
passport_data = {}

for line in lines:
    # print(line)
    if user_data.search(line) is not None:
        # print(user_data.search(line).group())
        nationality = user_data.search(line).group(2)
        surname = user_data.search(line).group(3)
        first_name = user_data.search(line).group(4)
        other_name = user_data.search(line).group(5)
        if other_name is not None:
            print(f'Nationality: {nationality}\nSurname: {surname}\nOther Names(s): {first_name} {other_name}')
        else:
            print(f'Nationality: {nationality}\nSurname: {surname}\nOther Names(s): {first_name}')

pattern = r'([A-Z]{1,3})?(\d{6,9})(<)*(\d)?([A-Z]{3})(\d{7})(F|M)(\d{7})'
user_numbers = re.compile(pattern)

prefix = ''

data = {}
for line in lines:
    if user_numbers.search(line) is not None:
        # print(line)
        if user_numbers.search(line).group(1) is not None:
            prefix = user_numbers.search(line).group(1)[-1]
        number = user_numbers.search(line).group(2)[:8]
        # Document Number
        data['id_no'] = prefix + number if prefix is not None else number

        nationality = user_numbers.search(line).group(5)
        data['nationality'] = nationality

        dob = user_numbers.search(line).group(6)[:6]
        data['d.o.b'] = dob

        gender = user_numbers.search(line).group(7)
        data['gender'] = gender

        exp = user_numbers.search(line).group(8)[:6]
        data['expiry'] = exp

        print(f'Document Number: {prefix}{number}\nNationality: {nationality}\nD.O.B: {dob}\nGender: {gender}\nDocument Exp: {exp}')

        # return data