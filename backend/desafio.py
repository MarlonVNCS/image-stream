import numpy as np
from collections import deque
from backend.filtros_frequencias import limiarizacao_global
from backend.filtros import grayscale


def detectar_linha_divisoria(imagem_gray, altura, largura):

    perfil_horizontal = np.mean(imagem_gray, axis=1)
    

    inicio = int(altura * 0.3)
    fim = int(altura * 0.7)
    
    regiao_central = perfil_horizontal[inicio:fim]
    
    if len(regiao_central) == 0:
        return altura // 2  
    
    idx_min_local = np.argmin(regiao_central)
    linha_divisoria = inicio + idx_min_local
    

    linha_pixels = imagem_gray[linha_divisoria, :]
    pixels_escuros = np.sum(linha_pixels < 128)
    
    if pixels_escuros > largura * 0.5:
        return linha_divisoria
    
    for i in range(inicio, fim):
        janela_inicio = max(0, i - 1)
        janela_fim = min(altura, i + 2)
        janela = imagem_gray[janela_inicio:janela_fim, :]
        media_janela = np.mean(janela)
        
        if media_janela < 100:
            pixels_escuros = np.sum(imagem_gray[i, :] < 128)
            if pixels_escuros > largura * 0.4:
                return i
    
    return altura // 2


def rotular_componentes(imagem_bin):

    altura, largura = imagem_bin.shape
    rotulos = np.zeros((altura, largura), dtype=np.int32)
    rotulo_atual = 0
    
    for i in range(altura):
        for j in range(largura):
            if imagem_bin[i, j] > 0 and rotulos[i, j] == 0:
                rotulo_atual += 1
                fila = deque([(i, j)])
                rotulos[i, j] = rotulo_atual
                
                while fila:
                    y, x = fila.popleft()
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:
                                continue
                            ny, nx = y + dy, x + dx
                            if (0 <= ny < altura and 0 <= nx < largura and
                                imagem_bin[ny, nx] > 0 and rotulos[ny, nx] == 0):
                                rotulos[ny, nx] = rotulo_atual
                                fila.append((ny, nx))
    
    return rotulos, rotulo_atual


def scanline_fill(imagem_bin, seed_y, seed_x, novo_valor=255):

    altura, largura = imagem_bin.shape
    resultado = imagem_bin.copy()
    
    if resultado[seed_y, seed_x] == novo_valor:
        return resultado
    
    valor_original = resultado[seed_y, seed_x]
    pilha = [(seed_y, seed_x)]
    
    while pilha:
        y, x = pilha.pop()
        
        if y < 0 or y >= altura or x < 0 or x >= largura:
            continue
        if resultado[y, x] != valor_original:
            continue
        
        x_esq = x
        while x_esq > 0 and resultado[y, x_esq - 1] == valor_original:
            x_esq -= 1
        
        x_dir = x
        while x_dir < largura - 1 and resultado[y, x_dir + 1] == valor_original:
            x_dir += 1
        
        for i in range(x_esq, x_dir + 1):
            resultado[y, i] = novo_valor
        
        for dy in [-1, 1]:
            ny = y + dy
            if 0 <= ny < altura:
                i = x_esq
                while i <= x_dir:
                    if resultado[ny, i] == valor_original:
                        pilha.append((ny, i))
                        while i <= x_dir and resultado[ny, i] == valor_original:
                            i += 1
                    else:
                        i += 1
    
    return resultado


def detectar_circulos_hough(imagem_bin, raio_min, raio_max, threshold):

    altura, largura = imagem_bin.shape
    
    bordas_y, bordas_x = np.where(imagem_bin > 0)
    
    if len(bordas_y) == 0:
        return []
    
    acumulador = {}
    
    for idx in range(len(bordas_y)):
        y = bordas_y[idx]
        x = bordas_x[idx]
        
        for r in range(raio_min, raio_max + 1):
            for theta in np.linspace(0, 2 * np.pi, 16):
                a = int(x - r * np.cos(theta))
                b = int(y - r * np.sin(theta))
                
                if 0 <= a < largura and 0 <= b < altura:
                    chave = (a, b, r)
                    acumulador[chave] = acumulador.get(chave, 0) + 1
    
    circulos = []
    for (a, b, r), votos in acumulador.items():
        if votos >= threshold:
            circulos.append((a, b, r, votos))
    
    circulos.sort(key=lambda x: x[3], reverse=True)
    
    circulos_filtrados = []
    for circulo in circulos:
        a, b, r, votos = circulo
        duplicado = False
        for cf in circulos_filtrados:
            dist = np.sqrt((a - cf[0])**2 + (b - cf[1])**2)
            if dist < r * 0.5:  
                duplicado = True
                break
        if not duplicado:
            circulos_filtrados.append(circulo)
    
    return circulos_filtrados


def detectar_retangulo_domino(imagem_gray):

    altura, largura = imagem_gray.shape
    

    media_global = np.mean(imagem_gray)
    limiar = min(150, media_global * 0.7)
    imagem_bin = 255 - limiarizacao_global(imagem_gray, limiar=limiar, valor_max=255)
    
    pixels_escuros = np.sum(imagem_bin > 0)
    total_pixels = altura * largura
    if pixels_escuros < total_pixels * 0.05:  
        return False, None
    
    rotulos, num_componentes = rotular_componentes(imagem_bin)
    
    if num_componentes == 0:
        return False, None
    
    melhor_candidato = None
    melhor_score = 0
    
    for rotulo in range(1, num_componentes + 1):
        y_coords, x_coords = np.where(rotulos == rotulo)
        
        if len(y_coords) < 100:  
            continue
        
        y_min, y_max = np.min(y_coords), np.max(y_coords)
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        
        altura_comp = y_max - y_min + 1
        largura_comp = x_max - x_min + 1
        area_comp = len(y_coords)
        
        if largura_comp < 20 or altura_comp < 40:
            continue
        
        aspect_ratio = altura_comp / largura_comp
        
        if aspect_ratio < 1.2:  
            continue
        
        area_bbox = altura_comp * largura_comp
        ocupacao = area_comp / area_bbox if area_bbox > 0 else 0
        
        area_imagem = altura * largura
        proporcao_imagem = area_comp / area_imagem
        
        if proporcao_imagem < 0.03 or proporcao_imagem > 0.98:
            continue
        
        score = 0
        
        if 1.5 <= aspect_ratio <= 2.3:
            score += 40
        elif 1.3 <= aspect_ratio <= 2.8:
            score += 20
        else:
            score += 5
        
        if ocupacao > 0.75:
            score += 30
        elif ocupacao > 0.5:
            score += 20
        elif ocupacao > 0.3:
            score += 15
        elif ocupacao > 0.08 and area_bbox > area_imagem * 0.3: 
            score += 25
        

        proporcao_bbox = area_bbox / area_imagem
        if proporcao_bbox > 0.5:
            score += 30
        elif proporcao_bbox > 0.3:
            score += 20
        elif proporcao_bbox > 0.2:
            score += 10
        
        if score > melhor_score:
            melhor_score = score
            melhor_candidato = {
                'bordas': (x_min, y_min, x_max, y_max),
                'aspect_ratio': aspect_ratio,
                'ocupacao': ocupacao,
                'score': score,
                'area': area_comp,
                'proporcao': proporcao_imagem
            }
    
    if melhor_candidato is not None and melhor_score >= 60:
        return True, melhor_candidato['bordas']
    
    return False, None


def detectar_domino(image_manager):

    matriz = image_manager.get_edited_matrix()
    
    if matriz is None:
        return -1, -1
    
    if len(matriz.shape) == 3:
        matriz_gray_rgb = grayscale(matriz[:, :, :3] if matriz.shape[2] == 4 else matriz)
        imagem_gray = matriz_gray_rgb[:, :, 0]
    else:
        imagem_gray = matriz.copy()
    
    altura, largura = imagem_gray.shape
    tamanho_imagem = max(altura, largura)
    
    encontrou_domino, bordas = detectar_retangulo_domino(imagem_gray)
    
    if not encontrou_domino:
        return -1, -1
    
    linha_divisoria_y = detectar_linha_divisoria(imagem_gray, altura, largura)
    
    if tamanho_imagem < 200:
        raio_min = 2
        raio_max = int(tamanho_imagem * 0.3)  
        limiar_bin = 128
    elif tamanho_imagem < 500:
        raio_min = 3
        raio_max = int(tamanho_imagem * 0.15)
        limiar_bin = 128
    else:
        raio_min = 5
        raio_max = int(tamanho_imagem * 0.1)
        limiar_bin = 128

    imagem_bin = 255 - limiarizacao_global(imagem_gray, limiar=limiar_bin, valor_max=255)

    margem_linha = max(2, int(tamanho_imagem * 0.02))
    imagem_bin[max(0, linha_divisoria_y - margem_linha):min(altura, linha_divisoria_y + margem_linha), :] = 0
    
    rotulos, num_componentes = rotular_componentes(imagem_bin)
    
    componentes_info = []
    
    for rotulo in range(1, num_componentes + 1):
        mascara = (rotulos == rotulo).astype(np.uint8) * 255
        y_coords, x_coords = np.where(mascara > 0)
        
        if len(y_coords) < 5:  
            continue
        
        cy = int(np.mean(y_coords))
        cx = int(np.mean(x_coords))
        
        area = len(y_coords)
        

        distancias = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
        raio_medio = np.mean(distancias)
        desvio_raio = np.std(distancias)
        

        if raio_medio > 0:
            coef_variacao = desvio_raio / raio_medio
        else:
            coef_variacao = 1.0
        
        y_min, y_max = np.min(y_coords), np.max(y_coords)
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        altura_comp = y_max - y_min + 1
        largura_comp = x_max - x_min + 1
        
        if largura_comp > 0:
            aspect_ratio = altura_comp / largura_comp
        else:
            aspect_ratio = 0
        
        distancia_linha = abs(cy - linha_divisoria_y)
        
        componentes_info.append({
            'rotulo': rotulo,
            'centro': (cx, cy),
            'raio': raio_medio,
            'area': area,
            'coef_variacao': coef_variacao,
            'aspect_ratio': aspect_ratio,
            'distancia_linha': distancia_linha
        })
    
    circulos = []
    for comp in componentes_info:
        raio_ok = raio_min <= comp['raio'] <= raio_max
        
        area_ok = comp['area'] >= np.pi * raio_min**2

        circular_ok = comp['coef_variacao'] < 0.45
        

        aspect_ok = 0.6 <= comp['aspect_ratio'] <= 1.7

        longe_linha = comp['distancia_linha'] > raio_min * 0.5
        

        if comp['raio'] > 0:
            razao_area_raio = comp['area'] / (comp['raio'] ** 2)
            nao_alongado = razao_area_raio > 1.5 
        else:
            nao_alongado = False
        
        if raio_ok and area_ok and circular_ok and aspect_ok and longe_linha and nao_alongado:
            circulos.append(comp)
    
    if len(circulos) == 0:
        return 0, 0
    

    pontos_superior = sum(1 for c in circulos if c['centro'][1] < linha_divisoria_y)
    pontos_inferior = sum(1 for c in circulos if c['centro'][1] > linha_divisoria_y)
    
    return pontos_superior, pontos_inferior