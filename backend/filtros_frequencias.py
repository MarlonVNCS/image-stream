import numpy as np

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
        imagem_gray = np.mean(imagem, axis=2).astype(np.uint8)
    else:
        imagem_gray = imagem
        
    if ksize == 3:
        kernel = np.array([[0, 1, 0],
                          [1, -4, 1],
                          [0, 1, 0]])
    else:  
        kernel = np.array([[0, 0, 1, 0, 0],
                          [0, 1, 2, 1, 0],
                          [1, 2, -16, 2, 1],
                          [0, 1, 2, 1, 0],
                          [0, 0, 1, 0, 0]])
    
    pad = ksize // 2
    padded = np.pad(imagem_gray, pad, mode='reflect')
    bordas = np.zeros_like(imagem_gray, dtype=np.float64)
    
    for i in range(imagem_gray.shape[0]):
        for j in range(imagem_gray.shape[1]):
            vizinhanca = padded[i:i+ksize, j:j+ksize]
            bordas[i,j] = np.sum(vizinhanca * kernel)
    
    bordas = np.absolute(bordas)
    bordas = np.clip(bordas, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3:
        return np.stack((bordas,)*3, axis=-1)
    return bordas

def filtro_sobel(imagem, direcao='ambos', ksize=3):
    if imagem.dtype != np.uint8:
        imagem = np.clip(imagem, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3:
        imagem_gray = np.mean(imagem, axis=2).astype(np.uint8)
    else:
        imagem_gray = imagem
    
    if ksize == 3:
        kernel_x = np.array([[-1, 0, 1],
                           [-2, 0, 2],
                           [-1, 0, 1]])
        kernel_y = np.array([[-1, -2, -1],
                           [0, 0, 0],
                           [1, 2, 1]])
    else:  
        kernel_x = np.array([[-1, -2, 0, 2, 1],
                           [-4, -8, 0, 8, 4],
                           [-6, -12, 0, 12, 6],
                           [-4, -8, 0, 8, 4],
                           [-1, -2, 0, 2, 1]])
        kernel_y = kernel_x.T
    
    pad = ksize // 2
    padded = np.pad(imagem_gray, pad, mode='reflect')
    grad_x = np.zeros_like(imagem_gray, dtype=np.float64)
    grad_y = np.zeros_like(imagem_gray, dtype=np.float64)
    
    for i in range(imagem_gray.shape[0]):
        for j in range(imagem_gray.shape[1]):
            vizinhanca = padded[i:i+ksize, j:j+ksize]
            if direcao in ['x', 'ambos']:
                grad_x[i,j] = np.sum(vizinhanca * kernel_x)
            if direcao in ['y', 'ambos']:
                grad_y[i,j] = np.sum(vizinhanca * kernel_y)
    
    if direcao == 'x':
        grad = np.absolute(grad_x)
    elif direcao == 'y':
        grad = np.absolute(grad_y)
    else:
        grad = np.sqrt(grad_x**2 + grad_y**2)
    
    grad = np.clip(grad, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3:
        return np.stack((grad,)*3, axis=-1)
    return grad

def limiarizacao_global(imagem, limiar=127, valor_max=255):
    if imagem.dtype != np.uint8:
        imagem = np.clip(imagem, 0, 255).astype(np.uint8)
    
    if len(imagem.shape) == 3:
        imagem_gray = np.mean(imagem, axis=2).astype(np.uint8)
    else:
        imagem_gray = imagem
    
    resultado = np.where(imagem_gray >= limiar, valor_max, 0).astype(np.uint8)
    
    if len(imagem.shape) == 3:
        return np.stack((resultado,)*3, axis=-1)
    return resultado

