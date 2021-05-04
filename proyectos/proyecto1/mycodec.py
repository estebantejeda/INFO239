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

    # Se transforma a byte
    b = bytearray()
    for i in range(0, len(texto_codificado), 8):
        byte = texto_codificado[i:i+8]
        b.append(int(byte, 2))

    #return frame_destranformado

    return b

def decode(b):

    # Se carga el dendograma y se crea el inverso
    a_file = open("data.pkl", "rb")
    new_dendo = pickle.load(a_file)
    a_file.close()
    dendograma_inverso =  {codigo: simbolo for simbolo, codigo in new_dendo.items()}

    # Se toma el texto codificado en bytes y se transforma a una cadena de 1 y 0
    texto_decodificado = [valor for k in range(len(b)) for valor in b[k]]
    texto_decodificado = ''.join(b)

    # Se decodifica con el dendograma inverso
    codigo = ""
    texto = ""
    for bit in texto_decodificado:
        codigo += bit
        if codigo in dendograma_inverso:
            texto += dendograma_inverso[codigo].astype(str)
            texto += " "
            codigo = ""

    mensaje_final = np.array([float(x) for x in texto.split()], dtype=np.float64)
    frame1 = mensaje_final.reshape(480,848)

    # Se agrega la última esperanza para aprobar
    frame_destranformado = inv_transform(frame1)

    #
    # Reemplaza la linea 24...
    #
    #frame_destranformado = inv_transform(frame_ct)
    #frame = np.frombuffer(bytes(memoryview(message)), dtype='uint8').reshape(480, 848)
    
    #
    # ...con tu implementación del bloque receptor: decodificador + transformación inversa
    #
    return frame_destranformado




