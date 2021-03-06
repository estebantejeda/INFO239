import numpy as np
import cv2 as cv
import heapq
from scipy import fftpack as fft


def elimina_ruido(frame):
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

def transformacion(frame):
    frame_size = frame.shape
    dct_matrix = np.zeros(shape=frame_size)
    DCT2 = lambda g, norm='ortho': fft.dct(fft.dct(g, axis=0, norm=norm), axis=1, norm=norm)
    # Se recorre el frame en bloques de 8x8
    for i in range(0, frame_size[0], 8):
        for j in range(0, frame_size[1], 8):
            dct_matrix[i:(i+8),j:(j+8)] = DCT2(frame[i:(i+8),j:(j+8)])
    return dct_matrix

#Matriz de cuantizacion

Q = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
              [12, 12, 14, 19, 26, 58, 60, 55],
              [14, 13, 16, 24, 40, 57, 69, 56],
              [14, 17, 22, 29, 51, 87, 80, 62],
              [18, 22, 37, 56, 68, 109, 103, 77],
              [24, 35, 55, 64, 81, 104, 113, 92],
              [49, 64, 78, 87, 103, 121, 120, 101],
              [72, 92, 95, 98, 112, 100, 103, 99]])

def cuantizacion(frame, porcentaje, p_original):
    frame_size = frame.shape
    frame_cuantizado = np.zeros(shape=frame_size)
    nnz = np.zeros(frame.shape)
    if (porcentaje < 50):
        S = 5000/porcentaje
    else:
        S = 200 - 2*porcentaje

    Q_dyn = np.floor((S*Q + 50) / 100)
    Q_dyn[Q_dyn == 0] = 1
    for i in range(0, frame_size[0], 8):
        for j in range(0, frame_size[1], 8):
            frame_cuantizado[i:(i+8), j:(j+8)] = np.round(frame[i:(i+8),j:(j+8)]/Q_dyn)
            nnz[i,j]=np.count_nonzero(frame[i:(i+8), j:(j+8)])

    p_comprimido = np.sum(nnz)*8/1e+6
    print("Peso comprimido: %0.2f MB" % p_comprimido)  
    print("Tasa de compresi??n: %0.2f MB/s" % (p_comprimido / p_original))
    return frame_cuantizado


def inv_transform(frame):
    frame_size = frame.shape
    im_dct = np.zeros(shape=frame_size)
    IDCT2 = lambda G, norm='ortho': fft.idct( fft.idct(G, axis=0, norm=norm), axis=1, norm=norm)
    
    for i in range(0, frame_size[0], 8):
           for j in range(0, frame_size[1], 8): 
                im_dct[i:(i+8), j:(j+8)] = IDCT2(frame[i:(i+8),j:(j+8)])
                
    return np.uint8(im_dct)

