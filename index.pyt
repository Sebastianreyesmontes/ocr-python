import cv2
import pytesseract
import os
import re
from PIL import Image
import numpy as np

# Ruta donde esta el tesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Lee la imagen
image = cv2.imread('solo.jpg')

# Aplicacion del desenfoque Gaussian a la imagen
img = cv2.GaussianBlur(image, (5, 5), 0)

# Separador el texto del fondo
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
coords = cv2.findNonZero(thresh)
x, y, w, h = cv2.boundingRect(coords)
text = thresh[y:y+h, x:x+w]

# Escalar la imagen
(h, w) = text.shape[:2]
r = 1000.0 / w
dim = (1000, int(h * r))
text = cv2.resize(text, tuple(np.round(dim).astype(int)), interpolation=cv2.INTER_AREA)

# Guardar la imagen en escala  gris
gray_file = 'temp.jpg'
cv2.imwrite(gray_file, text)

# oem "es el motor del tesseract" psm"es el formato del texto" eng"es el idioma"
config ='--oem 3  --psm 6-- --l eng--'
# Utilice  pytesseract para convertir en escala gris al texto
text = pytesseract.image_to_string(Image.open(gray_file))

#Esto era para realizar una  prueba pero no funciono  hasta al final del IF 
date_flight_regex = r'(\d{2}[A-Z]{3}\d{2}[-\s]?\d{2}[-\s]?\d{4})(?:.*\n)*(\d{2}\w{3}\d{4})'
match = re.search(date_flight_regex, text)

if match:
    date = match.group(1)
    flight_number = match.group(2)
    print(f'Date: {date}')
    print(f'Flight Number: {flight_number}')
else:
    print('Date and/or flight number not found.')

registration_regex = r'AN\s+(\w{3}\/\w{3}\s+\w{3})'
date_regex = r'\d{2}[A-Z]{3}\d{2}'

registration_match = re.search(registration_regex, text)
if registration_match:
    registration = registration_match.group(1)
    print(f'Registration: {registration}')

#Sale un archio txt
with open('solo.txt', 'w') as f:
 f.write(text)

# Elimina el archivo en escala gris
os.remove(gray_file)

# imprime el texto
print(text)




