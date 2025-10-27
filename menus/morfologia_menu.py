import tkinter as tk
from backend.morfologiaMatematica import (
    criar_elemento_estruturante, erosao,
    dilatacao, abertura, fechamento, afinamento
)
from .utils import janela_base

def criar_menu_morfologia(root, callback, image_manager):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Dilatação", command=lambda: dilatacao_janela(image_manager))
    menu.add_command(label="Erosão", command=lambda: erosao_janela(image_manager))
    menu.add_command(label="Abertura", command=lambda: abertura_janela(image_manager))
    menu.add_command(label="Fechamento", command=lambda: fechamento_janela(image_manager))
    menu.add_command(label="Afinamento", command=lambda: afinamento_janela(image_manager))
    return menu

def criar_controles_elemento_estruturante(janela):
    #controles para o elemento estruturante
    label_forma = tk.Label(janela, text="Forma do elemento estruturante:")
    label_forma.pack()
    
    forma_var = tk.StringVar(value="quadrado")
    tk.Radiobutton(janela, text="Quadrado", variable=forma_var, value="quadrado").pack()
    tk.Radiobutton(janela, text="Cruz", variable=forma_var, value="cruz").pack()
    
    label_tamanho = tk.Label(janela, text="Tamanho (3, 5, 7, ...):")
    label_tamanho.pack()
    input_tamanho = tk.Entry(janela)
    input_tamanho.insert(0, "3")
    input_tamanho.pack()
    
    return forma_var, input_tamanho

def dilatacao_janela(image_manager):
    janela = janela_base("Dilatação", altura=300)
    forma_var, input_tamanho = criar_controles_elemento_estruturante(janela)
    
    botao = tk.Button(janela, text="Aplicar",
                     command=lambda: aplicar_dilatacao(image_manager,
                                                     forma_var.get(),
                                                     input_tamanho.get()))
    botao.pack(pady=10)

def erosao_janela(image_manager):
    janela = janela_base("Erosão", altura=300)
    forma_var, input_tamanho = criar_controles_elemento_estruturante(janela)
    
    botao = tk.Button(janela, text="Aplicar",
                     command=lambda: aplicar_erosao(image_manager,
                                                  forma_var.get(),
                                                  input_tamanho.get()))
    botao.pack(pady=10)

def abertura_janela(image_manager):
    janela = janela_base("Abertura", altura=300)
    forma_var, input_tamanho = criar_controles_elemento_estruturante(janela)
    
    botao = tk.Button(janela, text="Aplicar",
                     command=lambda: aplicar_abertura(image_manager,
                                                    forma_var.get(),
                                                    input_tamanho.get()))
    botao.pack(pady=10)

def fechamento_janela(image_manager):
    janela = janela_base("Fechamento", altura=300)
    forma_var, input_tamanho = criar_controles_elemento_estruturante(janela)
    
    botao = tk.Button(janela, text="Aplicar",
                     command=lambda: aplicar_fechamento(image_manager,
                                                      forma_var.get(),
                                                      input_tamanho.get()))
    botao.pack(pady=10)

def afinamento_janela(image_manager):
    janela = janela_base("Afinamento", altura=280)
    
    label_algoritmo = tk.Label(janela, text="(Algoritmo: Zhang-Suen)", 
                              font=("Arial", 8))
    label_algoritmo.pack(pady=5)
    
    label_iteracoes = tk.Label(janela, text="Número de iterações:")
    label_iteracoes.pack(pady=5)
    
    input_iteracoes = tk.Entry(janela)
    input_iteracoes.insert(0, "10")
    input_iteracoes.pack(pady=5)
    
    label_info = tk.Label(janela, text="(Use -1 para iterações até convergência)", 
                         font=("Arial", 8), fg="gray")
    label_info.pack()
    
    botao = tk.Button(janela, text="Aplicar",
                     command=lambda: aplicar_afinamento(image_manager,
                                                       input_iteracoes.get()))
    botao.pack(pady=10)

def validar_tamanho(tamanho_str):
    try:
        tamanho = int(tamanho_str)
        if tamanho < 3:
            tamanho = 3
        elif tamanho % 2 == 0:
            tamanho += 1
        return tamanho
    except ValueError:
        return 3

def aplicar_dilatacao(image_manager, forma, tamanho):
    tamanho = validar_tamanho(tamanho)
    elemento = criar_elemento_estruturante(forma, tamanho)
    
    edi_matrix = image_manager.get_edited_matrix()
    matrix = dilatacao(edi_matrix, elemento)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def aplicar_erosao(image_manager, forma, tamanho):
    tamanho = validar_tamanho(tamanho)
    elemento = criar_elemento_estruturante(forma, tamanho)
    
    edi_matrix = image_manager.get_edited_matrix()
    matrix = erosao(edi_matrix, elemento)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def aplicar_abertura(image_manager, forma, tamanho):
    tamanho = validar_tamanho(tamanho)
    elemento = criar_elemento_estruturante(forma, tamanho)
    
    edi_matrix = image_manager.get_edited_matrix()
    matrix = abertura(edi_matrix, elemento)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def aplicar_fechamento(image_manager, forma, tamanho):
    tamanho = validar_tamanho(tamanho)
    elemento = criar_elemento_estruturante(forma, tamanho)
    
    edi_matrix = image_manager.get_edited_matrix()
    matrix = fechamento(edi_matrix, elemento)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def aplicar_afinamento(image_manager, iteracoes_str):
    try:
        iteracoes = int(iteracoes_str)
    except ValueError:
        iteracoes = 10
    
    edi_matrix = image_manager.get_edited_matrix()
    matrix = afinamento(edi_matrix, iteracoes)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()