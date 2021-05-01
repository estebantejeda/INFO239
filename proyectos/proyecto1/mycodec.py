import numpy as np
import cv2 as cv
import heapq
from scipy import fftpack as fft

#Función que elimina el ruido de la imagen
def denoise(frame):
    #Elimina el ruido impulsivo(sal y pimienta)
    frame = cv.medianBlur(frame, 5)

    #Eliminamos ruido periodico utilizando una mascara en frecuencia
    f_img = fft.fftshift(fft.fft2(frame))
    esp_fil = f_img*create_mask(f_img.shape, 0.04)
    frame = np.uint8(fft.ifft2(fft.ifftshift(esp_fil)))
    return frame

#mascara en frecuencia
def create_mask(dims, frequency, size=3):
    freq_int = int(frequency*dims[0])
    mask = np.ones(shape=(dims[0], dims[1]))
    mask[dims[0]//2-size-freq_int:dims[0]//2+size-freq_int,
         dims[1]//2-size:dims[1]//2+size] = 0
    mask[dims[0]//2-size+freq_int:dims[0]//2+size+freq_int,
          dims[1]//2-size:dims[1]//2+size] = 0
    return mask


def code(frame):
    #Transformacion -> camnbiar la representacion de los datos-> disminuir la redunciancia y correlacion de los datos

    frame_size = frame.shape
    dct_matrix = np.zeros(shape=frame_size)

    DCT2 = lambda g, norm='ortho': fft.dct(fft.dct(g, axis=0, norm=norm), axis=1, norm=norm)
    # Se recorre el frame en bloques de 8x8
    for i in range(0, frame_size[0], 8):
        for j in range(0, frame_size[1], 8):
            dct_matrix[i:(i+8),j:(j+8)] = DCT2(frame[i:(i+8),j:(j+8)])


    #Cuantización
    #usando el algoritmo JPGE cuantizamos en el espacio de las frecuencias
    #operacion de redondeo o truncamiento

    #El nivel de cuantización de JPEG se controla como
    # un valor denominado tipicamente como calidad que va entre 0 y 100
    #A mayor calidad se aplica menor cuantización, resultando en un archivo más pesado
    Q = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
              [12, 12, 14, 19, 26, 58, 60, 55],
              [14, 13, 16, 24, 40, 57, 69, 56],
              [14, 17, 22, 29, 51, 87, 80, 62],
              [18, 22, 37, 56, 68, 109, 103, 77],
              [24, 35, 55, 64, 81, 104, 113, 92],
              [49, 64, 78, 87, 103, 121, 120, 101],
              [72, 92, 95, 98, 112, 100, 103, 99]])

    im_dct = np.zeros(shape=frame_size)
   # nnz = np.zeros(dct_matrix.shape) #
    #porcentaje de cuantizacion?
    IDCT2 = lambda G, norm='ortho': fft.idct( fft.idct(G, axis=0, norm=norm), axis=1, norm=norm)
    porcentaje = 90
    if (porcentaje < 50):
        S = 5000/porcentaje
    else:
        S = 200 - 2*porcentaje

    Q_dyn = np.floor((S*Q + 50) / 100)
    Q_dyn[Q_dyn == 0] = 1
    for i in range(0, frame_size[0], 8):
        for j in range(0, frame_size[1], 8):
            quant = np.round(dct_matrix[i:(i+8),j:(j+8)]/Q_dyn)
            im_dct[i:(i+8),j:(j+8)] = IDCT2(quant)

    frame = np.uint8(im_dct)



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
