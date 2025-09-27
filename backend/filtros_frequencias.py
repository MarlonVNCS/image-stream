import numpy as np
from scipy import ndimage
from PIL import Image
import cv2  #para alguns filtros adicionais


def filtro_mediana(imagem, tamanho_kernel=3):
    
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        for canal in range(3):
            resultado[:,:,canal] = ndimage.median_filter(imagem[:,:,canal], 
                                                       size=tamanho_kernel)
        return resultado
    else:
        return ndimage.median_filter(imagem, size=tamanho_kernel)


def filtro_gaussiano(imagem, sigma=1.0):
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        for canal in range(3):
            resultado[:,:,canal] = ndimage.gaussian_filter(imagem[:,:,canal], 
                                                         sigma=sigma)
        return resultado
    else:
        return ndimage.gaussian_filter(imagem, sigma=sigma)

def filtro_laplaciano(imagem, ksize=3):

    if imagem.dtype != np.uint8:
        imagem = np.clip(imagem, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3:
        imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
        bordas = cv2.Laplacian(imagem_gray, cv2.CV_64F, ksize=ksize)
        bordas = np.absolute(bordas)
        bordas = np.clip(bordas, 0, 255).astype(np.uint8)
        return cv2.cvtColor(bordas, cv2.COLOR_GRAY2RGB)
    else:
        bordas = cv2.Laplacian(imagem, cv2.CV_64F, ksize=ksize)
        return np.absolute(bordas).clip(0, 255).astype(np.uint8)

def filtro_sobel(imagem, direcao='ambos', ksize=3):

    if imagem.dtype != np.uint8:
        imagem = np.clip(imagem, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3:
        imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
    else:
        imagem_gray = imagem
    
    if direcao == 'x':
        grad_x = cv2.Sobel(imagem_gray, cv2.CV_64F, 1, 0, ksize=ksize)
        grad = np.absolute(grad_x)
    elif direcao == 'y':
        grad_y = cv2.Sobel(imagem_gray, cv2.CV_64F, 0, 1, ksize=ksize)
        grad = np.absolute(grad_y)
    else: 
        grad_x = cv2.Sobel(imagem_gray, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(imagem_gray, cv2.CV_64F, 0, 1, ksize=ksize)
        grad = np.sqrt(grad_x**2 + grad_y**2)
    
    grad = np.clip(grad, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3:
        return cv2.cvtColor(grad, cv2.COLOR_GRAY2RGB)
    return grad

def limiarizacao_global(imagem, limiar=127, valor_max=255):
  
    if imagem.dtype != np.uint8:
        imagem = np.clip(imagem, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3:
        imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
    else:
        imagem_gray = imagem
    
    _, resultado = cv2.threshold(imagem_gray, limiar, valor_max, cv2.THRESH_BINARY)
    
    if len(imagem.shape) == 3:
        return cv2.cvtColor(resultado, cv2.COLOR_GRAY2RGB)
    return resultado

