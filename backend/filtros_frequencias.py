import numpy as np
from PIL import Image
import cv2  #para alguns filtros adicionais


def filtro_mediana(imagem, tamanho_kernel=3):
    if tamanho_kernel % 2 == 0:
        tamanho_kernel += 1
    
    pad = tamanho_kernel // 2
    
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        for canal in range(3):
            padded = np.pad(imagem[:,:,canal], pad, mode='reflect')
            temp = np.zeros_like(imagem[:,:,canal])
            
            for i in range(imagem.shape[0]):
                for j in range(imagem.shape[1]):
                    vizinhanca = padded[i:i+tamanho_kernel, j:j+tamanho_kernel]
                    temp[i,j] = np.median(vizinhanca)
            
            resultado[:,:,canal] = temp
        return resultado
    else:
        padded = np.pad(imagem, pad, mode='reflect')
        resultado = np.zeros_like(imagem)
        
        for i in range(imagem.shape[0]):
            for j in range(imagem.shape[1]):
                vizinhanca = padded[i:i+tamanho_kernel, j:j+tamanho_kernel]
                resultado[i,j] = np.median(vizinhanca)
        
        return resultado

def filtro_gaussiano(imagem, sigma=1.0):

    tamanho_kernel = int(6 * sigma + 1)
    if tamanho_kernel % 2 == 0:
        tamanho_kernel += 1
    
    x = np.linspace(-(tamanho_kernel//2), tamanho_kernel//2, tamanho_kernel)
    x, y = np.meshgrid(x, x)
    kernel = np.exp(-(x**2 + y**2)/(2*sigma**2))
    kernel = kernel / kernel.sum()  
    
    pad = tamanho_kernel // 2
    
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        for canal in range(3):
            padded = np.pad(imagem[:,:,canal], pad, mode='reflect')
            temp = np.zeros_like(imagem[:,:,canal])
            
            for i in range(imagem.shape[0]):
                for j in range(imagem.shape[1]):
                    vizinhanca = padded[i:i+tamanho_kernel, j:j+tamanho_kernel]
                    temp[i,j] = np.sum(vizinhanca * kernel)
            
            resultado[:,:,canal] = temp
        return resultado.astype(np.uint8)
    else:
        padded = np.pad(imagem, pad, mode='reflect')
        resultado = np.zeros_like(imagem)
        
        for i in range(imagem.shape[0]):
            for j in range(imagem.shape[1]):
                vizinhanca = padded[i:i+tamanho_kernel, j:j+tamanho_kernel]
                resultado[i,j] = np.sum(vizinhanca * kernel)
        
        return resultado.astype(np.uint8)

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

