import numpy as np

def criar_elemento_estruturante(forma='quadrado', tamanho=3):

    if tamanho % 2 == 0:
        tamanho += 1
    
    if forma == 'quadrado':
        return np.ones((tamanho, tamanho), dtype=np.uint8)
    elif forma == 'cruz':
        elemento = np.zeros((tamanho, tamanho), dtype=np.uint8)
        centro = tamanho // 2
        elemento[centro, :] = 1
        elemento[:, centro] = 1
        return elemento
    else:
        raise ValueError("Forma deve ser 'quadrado' ou 'cruz'")

def erosao(imagem, elemento_estruturante):
  
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        for canal in range(3):
            resultado[:,:,canal] = erosao(imagem[:,:,canal], elemento_estruturante)
        return resultado
    
    altura, largura = imagem.shape
    ee_altura, ee_largura = elemento_estruturante.shape
    pad_h = ee_altura // 2
    pad_w = ee_largura // 2
    
    imagem_pad = np.pad(imagem, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    resultado = np.zeros_like(imagem)
    
    for i in range(altura):
        for j in range(largura):
            regiao = imagem_pad[i:i+ee_altura, j:j+ee_largura]
            resultado[i,j] = np.min(regiao[elemento_estruturante == 1])
            
    return resultado

def dilatacao(imagem, elemento_estruturante):
  
    if len(imagem.shape) == 3:
        resultado = np.zeros_like(imagem)
        for canal in range(3):
            resultado[:,:,canal] = dilatacao(imagem[:,:,canal], elemento_estruturante)
        return resultado
    
    altura, largura = imagem.shape
    ee_altura, ee_largura = elemento_estruturante.shape
    pad_h = ee_altura // 2
    pad_w = ee_largura // 2
    
    imagem_pad = np.pad(imagem, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    resultado = np.zeros_like(imagem)
    
    # Aplicar dilatação
    for i in range(altura):
        for j in range(largura):
            regiao = imagem_pad[i:i+ee_altura, j:j+ee_largura]
            resultado[i,j] = np.max(regiao[elemento_estruturante == 1])
            
    return resultado

def abertura(imagem, elemento_estruturante):
    
    return dilatacao(erosao(imagem, elemento_estruturante), elemento_estruturante)

def fechamento(imagem, elemento_estruturante):
    
    return erosao(dilatacao(imagem, elemento_estruturante), elemento_estruturante)