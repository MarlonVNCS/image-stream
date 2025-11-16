"""
DETECTOR DE DOMINÓ
==================

Este módulo implementa detecção de dominós em imagens RGB/ARGB usando:

1. ROTULAÇÃO DE COMPONENTES CONECTADOS
   - Identifica regiões conectadas (pontos do dominó)
   - BFS com 8-conectividade

2. SCANLINE FILL
   - Preenchimento de regiões por linha de varredura
   - Usado para processar áreas detectadas

3. EQUAÇÃO GERAL DA CIRCUNFERÊNCIA: (x - a)² + (y - b)² = r²
   - Verifica se componentes são realmente círculos
   - Calcula distância de cada pixel ao centróide: d = √[(x - cx)² + (y - cy)²]
   - Círculos verdadeiros têm distâncias consistentes (baixo desvio padrão)
   - Coeficiente de variação = desvio_padrão / média < 0.35
   - Aspect ratio (altura/largura) ≈ 1.0 para círculos

4. DETECÇÃO DE LINHA DIVISÓRIA
   - Identifica linha preta/cinza que separa as duas metades
   - Análise de perfil de intensidade horizontal
   - Remove região da linha para evitar detecção como ponto

CRITÉRIOS DE VALIDAÇÃO PARA CÍRCULOS:
- Raio dentro do range esperado (adaptativo ao tamanho da imagem)
- Área mínima: π × raio_min²
- Coeficiente de variação das distâncias < 0.35 (forma circular)
- Aspect ratio entre 0.7 e 1.4 (não muito alongado)
- Distância da linha divisória > raio_min/2
- Não é muito alongado (exclui linhas)
"""

import numpy as np
from collections import deque
from backend.filtros_frequencias import limiarizacao_global
from backend.filtros import grayscale


def detectar_linha_divisoria(imagem_gray, altura, largura):
    """
    Detecta a linha divisória horizontal do dominó.
    Procura por linhas com alta concentração de pixels escuros.
    """
    # Analisa o perfil de intensidade horizontal (média de cada linha)
    perfil_horizontal = np.mean(imagem_gray, axis=1)
    
    # Procura por linhas escuras (baixa intensidade)
    # A linha divisória deve estar na região central (entre 30% e 70% da altura)
    inicio = int(altura * 0.3)
    fim = int(altura * 0.7)
    
    # Encontra a linha mais escura na região central
    regiao_central = perfil_horizontal[inicio:fim]
    
    if len(regiao_central) == 0:
        return altura // 2  # Fallback: meio da imagem
    
    # Índice da linha mais escura (menor valor médio)
    idx_min_local = np.argmin(regiao_central)
    linha_divisoria = inicio + idx_min_local
    
    # Verifica se há uma linha horizontal consistente
    # Conta quantos pixels escuros tem nessa linha
    linha_pixels = imagem_gray[linha_divisoria, :]
    pixels_escuros = np.sum(linha_pixels < 128)
    
    # Se mais de 50% da linha é escura, é uma boa candidata
    if pixels_escuros > largura * 0.5:
        return linha_divisoria
    
    # Tenta encontrar uma região de várias linhas escuras consecutivas
    for i in range(inicio, fim):
        # Verifica uma janela de 3 linhas
        janela_inicio = max(0, i - 1)
        janela_fim = min(altura, i + 2)
        janela = imagem_gray[janela_inicio:janela_fim, :]
        media_janela = np.mean(janela)
        
        # Se a janela é escura (< 100), pode ser a linha divisória
        if media_janela < 100:
            # Conta pixels escuros na linha central
            pixels_escuros = np.sum(imagem_gray[i, :] < 128)
            if pixels_escuros > largura * 0.4:
                return i
    
    # Fallback: retorna o meio da imagem
    return altura // 2


def rotular_componentes(imagem_bin):
    """
    Rotula componentes conectados em uma imagem binária.
    Retorna matriz de rótulos e número de componentes.
    """
    altura, largura = imagem_bin.shape
    rotulos = np.zeros((altura, largura), dtype=np.int32)
    rotulo_atual = 0
    
    for i in range(altura):
        for j in range(largura):
            if imagem_bin[i, j] > 0 and rotulos[i, j] == 0:
                rotulo_atual += 1
                # BFS para rotular todo o componente
                fila = deque([(i, j)])
                rotulos[i, j] = rotulo_atual
                
                while fila:
                    y, x = fila.popleft()
                    # 8-conectividade
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
    """
    Preenche uma região usando o algoritmo Scanline Fill.
    """
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
        
        # Preenche a linha
        x_esq = x
        while x_esq > 0 and resultado[y, x_esq - 1] == valor_original:
            x_esq -= 1
        
        x_dir = x
        while x_dir < largura - 1 and resultado[y, x_dir + 1] == valor_original:
            x_dir += 1
        
        # Preenche a linha atual
        for i in range(x_esq, x_dir + 1):
            resultado[y, i] = novo_valor
        
        # Processa linhas acima e abaixo
        for dy in [-1, 1]:
            ny = y + dy
            if 0 <= ny < altura:
                i = x_esq
                while i <= x_dir:
                    if resultado[ny, i] == valor_original:
                        pilha.append((ny, i))
                        # Pula pixels já processados
                        while i <= x_dir and resultado[ny, i] == valor_original:
                            i += 1
                    else:
                        i += 1
    
    return resultado


def detectar_circulos_hough(imagem_bin, raio_min, raio_max, threshold):
    """
    Detecta círculos usando a Transformada de Hough com equação geral da circunferência:
    (x - a)² + (y - b)² = r²
    """
    altura, largura = imagem_bin.shape
    
    # Encontra bordas (pixels não-zero)
    bordas_y, bordas_x = np.where(imagem_bin > 0)
    
    if len(bordas_y) == 0:
        return []
    
    # Espaço de acumulação [a, b, r]
    acumulador = {}
    
    for idx in range(len(bordas_y)):
        y = bordas_y[idx]
        x = bordas_x[idx]
        
        # Para cada pixel de borda, vota em possíveis centros
        for r in range(raio_min, raio_max + 1):
            # Testa vários ângulos
            for theta in np.linspace(0, 2 * np.pi, 16):
                # Equação da circunferência: centro = (x - r*cos(θ), y - r*sin(θ))
                a = int(x - r * np.cos(theta))
                b = int(y - r * np.sin(theta))
                
                if 0 <= a < largura and 0 <= b < altura:
                    chave = (a, b, r)
                    acumulador[chave] = acumulador.get(chave, 0) + 1
    
    # Encontra círculos com votos acima do threshold
    circulos = []
    for (a, b, r), votos in acumulador.items():
        if votos >= threshold:
            circulos.append((a, b, r, votos))
    
    # Ordena por número de votos e remove duplicatas próximas
    circulos.sort(key=lambda x: x[3], reverse=True)
    
    circulos_filtrados = []
    for circulo in circulos:
        a, b, r, votos = circulo
        duplicado = False
        for cf in circulos_filtrados:
            dist = np.sqrt((a - cf[0])**2 + (b - cf[1])**2)
            if dist < r * 0.5:  # Muito próximo
                duplicado = True
                break
        if not duplicado:
            circulos_filtrados.append(circulo)
    
    return circulos_filtrados


def detectar_retangulo_domino(imagem_gray):
    """
    Detecta se existe um retângulo vertical (formato de dominó) na imagem.
    Retorna (encontrado, bordas) onde bordas = (x_min, y_min, x_max, y_max).
    """
    altura, largura = imagem_gray.shape
    
    # Aplica threshold adaptativo para detectar bordas usando função existente
    # Procura por pixels escuros (bordas do dominó)
    media_global = np.mean(imagem_gray)
    limiar = min(150, media_global * 0.7)
    # Usa limiarização global com inversão (< limiar vira branco)
    imagem_bin = 255 - limiarizacao_global(imagem_gray, limiar=limiar, valor_max=255)
    
    # Se muito poucos pixels escuros, não há dominó
    pixels_escuros = np.sum(imagem_bin > 0)
    total_pixels = altura * largura
    if pixels_escuros < total_pixels * 0.05:  # Menos de 5% escuro
        return False, None
    
    # Encontra componentes conectados
    rotulos, num_componentes = rotular_componentes(imagem_bin)
    
    if num_componentes == 0:
        return False, None
    
    # Procura pelo maior componente que pareça um retângulo vertical
    melhor_candidato = None
    melhor_score = 0
    
    for rotulo in range(1, num_componentes + 1):
        y_coords, x_coords = np.where(rotulos == rotulo)
        
        if len(y_coords) < 100:  # Muito pequeno para ser um dominó
            continue
        
        # Calcula bounding box
        y_min, y_max = np.min(y_coords), np.max(y_coords)
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        
        altura_comp = y_max - y_min + 1
        largura_comp = x_max - x_min + 1
        area_comp = len(y_coords)
        
        # Verifica tamanhos mínimos
        if largura_comp < 20 or altura_comp < 40:
            continue
        
        # Aspect ratio: dominó em pé tem altura > largura (tipicamente 1.4 a 2.5)
        aspect_ratio = altura_comp / largura_comp
        
        # Dominó DEVE ser vertical
        if aspect_ratio < 1.2:  # Não é vertical o suficiente
            continue
        
        # Área do componente vs área do bounding box
        area_bbox = altura_comp * largura_comp
        ocupacao = area_comp / area_bbox if area_bbox > 0 else 0
        
        # Verifica se ocupa uma parte significativa da imagem (5% a 95%)
        area_imagem = altura * largura
        proporcao_imagem = area_comp / area_imagem
        
        # Ajuste: aceita componentes menores (pode ser apenas a borda do dominó)
        if proporcao_imagem < 0.03 or proporcao_imagem > 0.98:
            continue
        
        # Score baseado em múltiplos critérios
        score = 0
        
        # Critério 1: Aspect ratio ideal (1.5 a 2.3 para dominó)
        if 1.5 <= aspect_ratio <= 2.3:
            score += 40
        elif 1.3 <= aspect_ratio <= 2.8:
            score += 20
        else:
            score += 5
        
        # Critério 2: Ocupação alta (retângulo preenchido) OU borda (ocupação baixa mas bounding box grande)
        if ocupacao > 0.75:
            score += 30
        elif ocupacao > 0.5:
            score += 20
        elif ocupacao > 0.3:
            score += 15
        elif ocupacao > 0.08 and area_bbox > area_imagem * 0.3:  # Borda de retângulo grande
            score += 25
        
        # Critério 3: Tamanho razoável em relação à imagem
        # Bounding box deve ser significativo (> 30% da imagem)
        proporcao_bbox = area_bbox / area_imagem
        if proporcao_bbox > 0.5:
            score += 30
        elif proporcao_bbox > 0.3:
            score += 20
        elif proporcao_bbox > 0.2:
            score += 10
        
        # Atualiza melhor candidato
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
    
    # Score mínimo de 60 para considerar como dominó
    if melhor_candidato is not None and melhor_score >= 60:
        return True, melhor_candidato['bordas']
    
    return False, None


def detectar_domino(image_manager):
    """
    Detecta dominó em uma imagem RGB ou ARGB.
    Retorna (num_pontos_superior, num_pontos_inferior).
    """
    matriz = image_manager.get_edited_matrix()
    
    if matriz is None:
        return -1, -1
    
    # Converte para escala de cinza usando função existente
    if len(matriz.shape) == 3:
        # Usa a função grayscale que retorna RGB (3 canais iguais)
        matriz_gray_rgb = grayscale(matriz[:, :, :3] if matriz.shape[2] == 4 else matriz)
        # Extrai apenas um canal (todos são iguais)
        imagem_gray = matriz_gray_rgb[:, :, 0]
    else:
        imagem_gray = matriz.copy()
    
    altura, largura = imagem_gray.shape
    tamanho_imagem = max(altura, largura)
    
    # VALIDAÇÃO INICIAL: Detecta se existe um retângulo vertical (dominó)
    encontrou_domino, bordas = detectar_retangulo_domino(imagem_gray)
    
    if not encontrou_domino:
        # Não é um dominó - retorna -1, -1 para indicar que não há dominó na imagem
        return -1, -1
    
    # Detecta a linha divisória do dominó ANTES de processar os pontos
    linha_divisoria_y = detectar_linha_divisoria(imagem_gray, altura, largura)
    
    # Parâmetros adaptativos baseados no tamanho da imagem
    if tamanho_imagem < 200:
        raio_min = 2
        raio_max = int(tamanho_imagem * 0.3)  # 30% do tamanho para imagens pequenas
        limiar_bin = 128
    elif tamanho_imagem < 500:
        raio_min = 3
        raio_max = int(tamanho_imagem * 0.15)
        limiar_bin = 128
    else:
        raio_min = 5
        raio_max = int(tamanho_imagem * 0.1)
        limiar_bin = 128
    
    # Binarização (círculos são escuros, fundo é claro) usando função existente
    # Inverte porque queremos pixels escuros como brancos (objetos)
    imagem_bin = 255 - limiarizacao_global(imagem_gray, limiar=limiar_bin, valor_max=255)
    
    # Remove a região da linha divisória para não detectar como ponto
    # Cria uma máscara excluindo alguns pixels ao redor da linha
    margem_linha = max(2, int(tamanho_imagem * 0.02))
    imagem_bin[max(0, linha_divisoria_y - margem_linha):min(altura, linha_divisoria_y + margem_linha), :] = 0
    
    # Rotula componentes conectados
    rotulos, num_componentes = rotular_componentes(imagem_bin)
    
    # Analisa cada componente para ver se é um círculo usando a equação da circunferência
    componentes_info = []
    
    for rotulo in range(1, num_componentes + 1):
        mascara = (rotulos == rotulo).astype(np.uint8) * 255
        y_coords, x_coords = np.where(mascara > 0)
        
        if len(y_coords) < 5:  # Componente muito pequeno
            continue
        
        # Calcula centróide
        cy = int(np.mean(y_coords))
        cx = int(np.mean(x_coords))
        
        # Área do componente
        area = len(y_coords)
        
        # VERIFICAÇÃO CRÍTICA: Usa a equação da circunferência (x - a)² + (y - b)² = r²
        # Calcula a distância de cada pixel ao centro
        distancias = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
        raio_medio = np.mean(distancias)
        desvio_raio = np.std(distancias)
        
        # Para ser um círculo, as distâncias devem ser consistentes (baixo desvio)
        # Coeficiente de variação: desvio / média
        if raio_medio > 0:
            coef_variacao = desvio_raio / raio_medio
        else:
            coef_variacao = 1.0
        
        # Calcula aspect ratio (largura vs altura)
        y_min, y_max = np.min(y_coords), np.max(y_coords)
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        altura_comp = y_max - y_min + 1
        largura_comp = x_max - x_min + 1
        
        if largura_comp > 0:
            aspect_ratio = altura_comp / largura_comp
        else:
            aspect_ratio = 0
        
        # Verifica se está muito próximo da linha divisória
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
    
    # Filtra componentes que são REALMENTE círculos usando critérios rigorosos
    circulos = []
    for comp in componentes_info:
        # Critério 1: Tamanho do raio dentro do range esperado
        raio_ok = raio_min <= comp['raio'] <= raio_max
        
        # Critério 2: Área mínima
        area_ok = comp['area'] >= np.pi * raio_min**2
        
        # Critério 3: Baixa variação de distâncias (forma circular consistente)
        # Círculos têm coeficiente de variação < 0.45 (relaxado para imagens reais)
        circular_ok = comp['coef_variacao'] < 0.45
        
        # Critério 4: Aspect ratio próximo de 1 (largura ≈ altura)
        # Círculos têm aspect ratio entre 0.6 e 1.7 (mais tolerante)
        aspect_ok = 0.6 <= comp['aspect_ratio'] <= 1.7
        
        # Critério 5: Não está muito próximo da linha divisória
        # Deve estar a pelo menos metade do raio de distância
        longe_linha = comp['distancia_linha'] > raio_min * 0.5
        
        # Critério 6: Não é muito alongado (exclui linhas)
        # Verifica a razão área/raio² - círculos têm ~π ≈ 3.14
        if comp['raio'] > 0:
            razao_area_raio = comp['area'] / (comp['raio'] ** 2)
            nao_alongado = razao_area_raio > 1.5  # Aceita formas mais ou menos compactas
        else:
            nao_alongado = False
        
        # Aceita apenas se passar em TODOS os critérios
        if raio_ok and area_ok and circular_ok and aspect_ok and longe_linha and nao_alongado:
            circulos.append(comp)
    
    if len(circulos) == 0:
        return 0, 0
    
    # Usa a linha divisória detectada para separar os pontos
    # Pontos acima da linha = parte superior
    # Pontos abaixo da linha = parte inferior
    pontos_superior = sum(1 for c in circulos if c['centro'][1] < linha_divisoria_y)
    pontos_inferior = sum(1 for c in circulos if c['centro'][1] > linha_divisoria_y)
    
    return pontos_superior, pontos_inferior