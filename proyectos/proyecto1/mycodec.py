import numpy as np
import cv2 as cv
import heapq
from scipy import fftpack as fft
from fnc import *

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

    frame_destranformado = inv_transform(frame_ct)
    
    
    return frame_destranformado


def decode(message):
    #
    # Reemplaza la linea 24...
    #
    #frame_destranformado = inv_transform(frame_ct)
    frame = np.frombuffer(bytes(memoryview(message)), dtype='uint8').reshape(480, 848)
    
    #
    # ...con tu implementación del bloque receptor: decodificador + transformación inversa
    #
    return frame




