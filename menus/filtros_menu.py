import tkinter as tk
from backend import filtros
from .utils import janela_base

def criar_menu_filtros(root, callback, image_manager):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Brilho e contraste", command=lambda: brilho_contraste_janela(image_manager))
    menu.add_command(label="Grayscale", command=lambda: grayscale_janela(image_manager))
    menu.add_command(label="Passa-baixa", command=lambda: callback("Passa-baixa"))
    menu.add_command(label="Passa-alta", command=lambda: callback("Passa-alta"))
    menu.add_command(label="Threshold e afinamento", command=lambda: callback("Threshold e afinamento"))
    return menu

def brilho_contraste_janela(image_manager):
    janela = janela_base("Brilho e Contraste")
    
    label_brilho = tk.Label(janela, text="Brilho:")
    label_brilho.pack()
    input_brilho = tk.Entry(janela)
    input_brilho.pack()
    
    label_contraste = tk.Label(janela, text="Contraste:")
    label_contraste.pack()
    input_contraste = tk.Entry(janela)
    input_contraste.pack()
    
    botao = tk.Button(janela, text="Aplicar", command=lambda: aplicar_brilho_contraste(image_manager, input_brilho.get(), input_contraste.get()))
    botao.pack(pady=10)

def aplicar_brilho_contraste(image_manager, brilho, contraste):
    try:
        brilho = float(brilho)
    except ValueError:
        brilho = 0.0
    try:
        contraste = float(contraste)
    except ValueError:
        contraste = 1.0
    image_manager.load_image()
    edi_matrix = image_manager.get_edited_matrix()
    matrix = filtros.brilho_contraste(edi_matrix, brilho, contraste)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def grayscale_janela(image_manager):
    janela = janela_base("Grayscale")
    botao = tk.Button(janela, text="Aplicar", command=lambda: aplicar_grayscale(image_manager))
    botao.pack(pady=10)
def aplicar_grayscale(image_manager):
    image_manager.load_image()
    edi_matrix = image_manager.get_edited_matrix()
    matrix = filtros.grayscale(edi_matrix)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()