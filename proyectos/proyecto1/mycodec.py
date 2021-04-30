import numpy as np
import cv2 as cv
from scipy import fftpack as fft

#Función que elimina el ruido de la imagen
def denoise(frame):
    #Elimina el ruido impulsivo(sal y pimienta)
    frame = cv.medianBlur(frame, 5)

    #Eliminamos ruido periodico utilizando una mascara en frecuencia
    f_img = fft.fftshift(fft.fft2(frame))
    esp_fil = f_img*create_mask(f_img.shape, 0.05)
    frame = np.uint8(fft.ifft2(fft.ifftshift(esp_fil)))
    return frame

#mascara en frecuencia
def create_mask(dims, frequency, size=5):
    freq_int = int(frequency*dims[0])
    mask = np.ones(shape=(dims[0], dims[1]))
    mask[dims[0]//2-size-freq_int:dims[0]//2+size-freq_int,
         dims[1]//2-size:dims[1]//2+size] = 0
    mask[dims[0]//2-size+freq_int:dims[0]//2+size+freq_int,
          dims[1]//2-size:dims[1]//2+size] = 0
    return mask


def code(frame):
    #
    # Implementa en esta función el bloque transmisor: Transformación + Cuantización + Codificación de fuente
    #
    return frame


def decode(message):
    #
    # Reemplaza la linea 24...
    #
    frame = np.frombuffer(bytes(memoryview(message)), dtype='uint8').reshape(480, 848)
    #
    # ...con tu implementación del bloque receptor: decodificador + transformación inversa
    #
    return frame
