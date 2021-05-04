import numpy as np
import cv2 as cv
import heapq
from scipy import fftpack as fft
from fnc import *
import pickle
import ast

#Función que elimina el ruido de la imagen
def denoise(frame):
    #Elimina el ruido impulsivo(sal y pimienta) y ruido periodico
    frame_filtrado = elimina_ruido(frame)
    return frame_filtrado

def code(frame_filtrado):
    #Transformacion -> camnbiar la representacion de los datos-> disminuir la redunciancia y correlacion de los datos
    frame_tr = transformacion(frame_filtrado)
    #Cuantización
    
    frame_ct = cuantizacion(frame_tr,80)

    # frame_ct se convierte en un vector
    frame_ct = frame_ct.ravel()    

    # Se lee el dendograma 
    a_file = open("data.pkl", "rb")
    new_dendo = pickle.load(a_file)
    a_file.close()

    # Se codifica el frame
    texto_codificado = ""
    for num in frame_ct:
        texto_codificado += new_dendo[num]

    # Realizamos padding si es necesario
    padding = 0
    while(len(texto_codificado)%8 != 0):
        padding = padding +1
        texto_codificado = texto_codificado + '0'

    # Se transforma a byte
    b = bytearray()
    for i in range(0, len(texto_codificado), 8):
        byte = texto_codificado[i:i+8]
        b.append(int(byte, 2))

    # Enviamos la información del bytearray junto con el padding por medio de Pickle
    b_enviado = pickle.dumps([padding, bytes(b)])

    #return frame_destranformado

    return b_enviado

def decode(message):

    # Se carga el dendograma y se crea el inverso
    a_file = open("data.pkl", "rb")
    new_dendo = pickle.load(a_file)
    a_file.close()
    dendograma_inverso =  {codigo: simbolo for simbolo, codigo in new_dendo.items()}

    # decodificamos el mensaje con pickle
    b_recibido = pickle.loads(message)
    padding_recibido = b_recibido[0]
    bytes_recibido = b_recibido[1]

    # Se toma el texto codificado en bytes y se transforma a una cadena de 1 y 0
    frame_recibido = ""
    for i in range (0, len(bytes_recibido)):
        frame_recibido += "{0:08b}".format(bytes_recibido[i])

    # Eliminamos el padding
    frame_recibido = frame_recibido[0:len(frame_recibido)-padding_recibido]

    # Se decodifica con el dendograma inverso
    codigo = ""
    texto = ""
    for bit in frame_recibido:
        codigo += bit
        if codigo in dendograma_inverso:
            texto += str(dendograma_inverso[codigo])
            texto += " "
            codigo = ""

    frame_final = np.array([float(x) for x in texto.split()], dtype=np.float64)
    frame_final = frame_final.reshape(480,848)

    # Se agrega la última esperanza para aprobar
    frame_destranformado = inv_transform(frame_final)

    return frame_destranformado




