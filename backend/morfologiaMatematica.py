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

def afinamento(imagem, max_iteracoes=-1):
    """Aplica algoritmo de afinamento morfológico (Zhang-Suen simplificado).
    
    Args:
        imagem: matriz da imagem (pode ser colorida ou grayscale)
        max_iteracoes: número máximo de iterações (-1 para convergência completa)
    
    Returns:
        matriz com a imagem afinada (esqueleto)
    """
    # Converte para escala de cinza se necessário
    if len(imagem.shape) == 3:
        imagem_gray = np.mean(imagem, axis=2).astype(np.uint8)
    else:
        imagem_gray = imagem.copy()
    
    # Binariza: pixels pretos (<127) = 1 (objeto), pixels brancos (>=127) = 0 (fundo)
    # Inverte porque normalmente texto/objeto é preto em fundo branco
    imagem_bin = (imagem_gray < 127).astype(np.uint8)
    
    def get_vizinhos(img, i, j):
        """Retorna os 8 vizinhos em ordem: P2, P3, P4, P5, P6, P7, P8, P9
        P9 P2 P3
        P8 P1 P4
        P7 P6 P5
        """
        return [
            img[i-1, j],   # P2 (Norte)
            img[i-1, j+1], # P3 (Nordeste)
            img[i, j+1],   # P4 (Leste)
            img[i+1, j+1], # P5 (Sudeste)
            img[i+1, j],   # P6 (Sul)
            img[i+1, j-1], # P7 (Sudoeste)
            img[i, j-1],   # P8 (Oeste)
            img[i-1, j-1]  # P9 (Noroeste)
        ]
    
    def contar_vizinhos(vizinhos):
        """Conta quantos vizinhos são 1 (objeto)"""
        return sum(vizinhos)
    
    def contar_transicoes(vizinhos):
        """Conta transições de 0->1 nos vizinhos (circular)"""
        vizinhos_circular = vizinhos + [vizinhos[0]]
        transicoes = 0
        for k in range(len(vizinhos)):
            if vizinhos_circular[k] == 0 and vizinhos_circular[k+1] == 1:
                transicoes += 1
        return transicoes
    
    resultado = imagem_bin.copy()
    altura, largura = resultado.shape
    iteracao = 0
    
    while True:
        if max_iteracoes != -1 and iteracao >= max_iteracoes:
            break
        
        mudou = False
        
        # Sub-iteração 1
        marcados1 = []
        for i in range(1, altura-1):
            for j in range(1, largura-1):
                if resultado[i, j] == 1:  # Apenas pixels do objeto
                    vizinhos = get_vizinhos(resultado, i, j)
                    P2, P3, P4, P5, P6, P7, P8, P9 = vizinhos
                    
                    # Condições do algoritmo Zhang-Suen (sub-iteração 1)
                    B = contar_vizinhos(vizinhos)  # Número de vizinhos != 0
                    A = contar_transicoes(vizinhos)  # Número de transições 0->1
                    
                    # Condições para remover o pixel
                    if (2 <= B <= 6 and 
                        A == 1 and 
                        P2 * P4 * P6 == 0 and 
                        P4 * P6 * P8 == 0):
                        marcados1.append((i, j))
        
        # Remove pixels marcados na sub-iteração 1
        for i, j in marcados1:
            resultado[i, j] = 0
            mudou = True
        
        # Sub-iteração 2
        marcados2 = []
        for i in range(1, altura-1):
            for j in range(1, largura-1):
                if resultado[i, j] == 1:  # Apenas pixels do objeto
                    vizinhos = get_vizinhos(resultado, i, j)
                    P2, P3, P4, P5, P6, P7, P8, P9 = vizinhos
                    
                    # Condições do algoritmo Zhang-Suen (sub-iteração 2)
                    B = contar_vizinhos(vizinhos)
                    A = contar_transicoes(vizinhos)
                    
                    # Condições para remover o pixel (diferentes da sub-iteração 1)
                    if (2 <= B <= 6 and 
                        A == 1 and 
                        P2 * P4 * P8 == 0 and 
                        P2 * P6 * P8 == 0):
                        marcados2.append((i, j))
        
        # Remove pixels marcados na sub-iteração 2
        for i, j in marcados2:
            resultado[i, j] = 0
            mudou = True
        
        # Para se não houve mudanças
        if not mudou:
            break
        
        iteracao += 1
    
    # Converte de volta para 0-255 e inverte (1 vira preto=0, 0 vira branco=255)
    resultado = ((1 - resultado) * 255).astype(np.uint8)
    
    # Se imagem original era colorida, retorna RGB
    if len(imagem.shape) == 3:
        resultado_rgb = np.stack([resultado, resultado, resultado], axis=2)
        return resultado_rgb
    
    return resultado