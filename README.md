Uma aplicação para processamento digital de imagens desenvolvida como projeto da disciplina de Processamento Digital de Imagens da Universidade Feevale.

## Desenvolvedores

- Júlia Nathalie Schmitz
- Marlon Vinicius Gonçalves

## Requisitos

Para executar a aplicação, você precisa ter instalado:

- Python 3.x
- As seguintes bibliotecas Python:
  ```bash
  pip install pillow numpy
  ```
  
Obs: O `tkinter` já vem incluído na instalação padrão do Python.

## Como Executar

1. Clone o repositório ou baixe os arquivos
2. Instale as dependências conforme descrito acima
3. Execute o arquivo principal:
   ```bash
   python main.py
   ```

## Funcionalidades

A aplicação oferece diversas funcionalidades de processamento de imagens:

### Arquivo
- Abrir imagem
- Salvar imagem
- Informações sobre o projeto

### Transformações Geométricas
- Translação
- Rotação
- Espelhamento
- Aumento/Diminuição de escala

### Filtros
- Ajuste de brilho e contraste
- Conversão para escala de cinza
- Filtro passa-baixa
- Filtro passa-alta
- Threshold e afinamento

### Morfologia Matemática
- Dilatação
- Erosão
- Abertura
- Fechamento

### Extração de Características
- Funcionalidades de extração de características da imagem

## Interface

A interface é dividida em duas áreas principais:
- Área da imagem original
- Área da imagem modificada

As modificações são visualizadas em tempo real e podem ser salvas em diversos formatos de arquivo (PNG, JPEG, BMP, TIFF)" 
