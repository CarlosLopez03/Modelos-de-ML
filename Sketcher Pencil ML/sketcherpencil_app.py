# Importación de dependencia
# Importación de la dependencias necesarias
# Instación -> !pip install streamlit
import streamlit as st
import numpy as np
from PIL import Image
import cv2

# Función para los reescalados
def dodgeV2(x, y):
    return cv2.divide(x, 255 - y, scale=256)


# Creando función para procesar la imagen
def pencilsketch(inp_img):
    img_gray = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
    final_img = dodgeV2(img_gray, img_smoothing)
    return final_img


# Estableciendo el titulo y la descripción
st.title("App de Sketch Pencil")
st.write("Esta app es para ayudar a convertir tus fotos a Pencil Sketches")

# Creando los parametros
file_image = st.sidebar.file_uploader(
    "Sube tu fotos", type=['jpeg', 'jpg', 'png'])

# Estableciendo condición
if file_image is None:
    st.write("Debe subir una imagen")
else:
    input_img = Image.open(file_image)
    final_sketch = pencilsketch(np.array(input_img))
    st.write("** Su foto **")
    st.image(input_img, use_column_width=True)
    st.write("** Sketch Pencil **")
    st.image(final_sketch, use_column_width=True)
