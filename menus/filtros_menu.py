import tkinter as tk
import tkinter as tk
from backend import filtros
from backend.filtros_frequencias import (
    filtro_mediana, filtro_gaussiano, 
    filtro_laplaciano, filtro_sobel,
    limiarizacao_global
)
from .utils import janela_base

def criar_menu_filtros(root, callback, image_manager):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Brilho e contraste", command=lambda: brilho_contraste_janela(image_manager))
    menu.add_command(label="Grayscale", command=lambda: grayscale_janela(image_manager))
    
    submenu_pb = tk.Menu(menu, tearoff=0)
    submenu_pb.add_command(label="Mediana", command=lambda: filtro_mediana_janela(image_manager))
    submenu_pb.add_command(label="Gaussiano", command=lambda: filtro_gaussiano_janela(image_manager))
    menu.add_cascade(label="Passa-baixa", menu=submenu_pb)
    
    submenu_pa = tk.Menu(menu, tearoff=0)
    submenu_pa.add_command(label="Laplaciano", command=lambda: filtro_laplaciano_janela(image_manager))
    submenu_pa.add_command(label="Sobel", command=lambda: filtro_sobel_janela(image_manager))
    menu.add_cascade(label="Passa-alta", menu=submenu_pa)
    
    # Opção de limiarização
    menu.add_command(label="Limiarização", command=lambda: limiarizacao_global_janela(image_manager))
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

def filtro_mediana_janela(image_manager):
    janela = janela_base("Filtro de Mediana")
    
    label_kernel = tk.Label(janela, text="Tamanho do kernel (3, 5, 7, ...):")
    label_kernel.pack()
    input_kernel = tk.Entry(janela)
    input_kernel.insert(0, "3") 
    input_kernel.pack()
    
    botao = tk.Button(janela, text="Aplicar", command=lambda: aplicar_filtro_mediana(image_manager, input_kernel.get()))
    botao.pack(pady=10)

def aplicar_filtro_mediana(image_manager, kernel_size):
    try:
        kernel_size = int(kernel_size)
        if kernel_size % 2 == 0:  
            kernel_size += 1
    except ValueError:
        kernel_size = 3
    
    image_manager.load_image()
    edi_matrix = image_manager.get_edited_matrix()
    matrix = filtro_mediana(edi_matrix, tamanho_kernel=kernel_size)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def filtro_gaussiano_janela(image_manager):
    janela = janela_base("Filtro Gaussiano")
    
    label_sigma = tk.Label(janela, text="Sigma (desvio padrão):")
    label_sigma.pack()
    input_sigma = tk.Entry(janela)
    input_sigma.insert(0, "1.0")  
    input_sigma.pack()
    
    botao = tk.Button(janela, text="Aplicar", command=lambda: aplicar_filtro_gaussiano(image_manager, input_sigma.get()))
    botao.pack(pady=10)

def aplicar_filtro_gaussiano(image_manager, sigma):
    try:
        sigma = float(sigma)
    except ValueError:
        sigma = 1.0
    
    image_manager.load_image()
    edi_matrix = image_manager.get_edited_matrix()
    matrix = filtro_gaussiano(edi_matrix, sigma=sigma)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def filtro_laplaciano_janela(image_manager):
    janela = janela_base("Filtro Laplaciano")
    
    label_kernel = tk.Label(janela, text="Tamanho do kernel (3 ou 5):")
    label_kernel.pack()
    input_kernel = tk.Entry(janela)
    input_kernel.insert(0, "3")  
    input_kernel.pack()
    
    botao = tk.Button(janela, text="Aplicar", command=lambda: aplicar_filtro_laplaciano(image_manager, input_kernel.get()))
    botao.pack(pady=10)

def aplicar_filtro_laplaciano(image_manager, kernel_size):
    try:
        kernel_size = int(kernel_size)
        if kernel_size not in [3, 5]:
            kernel_size = 3
    except ValueError:
        kernel_size = 3
    
    image_manager.load_image()
    edi_matrix = image_manager.get_edited_matrix()
    matrix = filtro_laplaciano(edi_matrix, ksize=kernel_size)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def filtro_sobel_janela(image_manager):
    janela = janela_base("Filtro Sobel")
    
    label_direcao = tk.Label(janela, text="Direção:")
    label_direcao.pack()
    
    direcao_var = tk.StringVar(value="ambos")
    tk.Radiobutton(janela, text="Horizontal (X)", variable=direcao_var, value="x").pack()
    tk.Radiobutton(janela, text="Vertical (Y)", variable=direcao_var, value="y").pack()
    tk.Radiobutton(janela, text="Ambas direções", variable=direcao_var, value="ambos").pack()
    
    label_kernel = tk.Label(janela, text="Tamanho do kernel (3, 5 ou 7):")
    label_kernel.pack()
    input_kernel = tk.Entry(janela)
    input_kernel.insert(0, "3")  
    input_kernel.pack()
    
    botao = tk.Button(janela, text="Aplicar", 
                     command=lambda: aplicar_filtro_sobel(image_manager, 
                                                        direcao_var.get(), 
                                                        input_kernel.get()))
    botao.pack(pady=10)

def aplicar_filtro_sobel(image_manager, direcao, kernel_size):
    try:
        kernel_size = int(kernel_size)
        if kernel_size not in [3, 5, 7]:
            kernel_size = 3
    except ValueError:
        kernel_size = 3
    
    image_manager.load_image()
    edi_matrix = image_manager.get_edited_matrix()
    matrix = filtro_sobel(edi_matrix, direcao=direcao, ksize=kernel_size)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def limiarizacao_global_janela(image_manager):
    janela = janela_base("Limiarização Global")
    
    label_limiar = tk.Label(janela, text="Valor do limiar (0-255):")
    label_limiar.pack()
    input_limiar = tk.Entry(janela)
    input_limiar.insert(0, "127")  # valor padrão
    input_limiar.pack()
    
    label_max = tk.Label(janela, text="Valor máximo (0-255):")
    label_max.pack()
    input_max = tk.Entry(janela)
    input_max.insert(0, "255")  # valor padrão
    input_max.pack()
    
    botao = tk.Button(janela, text="Aplicar", 
                     command=lambda: aplicar_limiarizacao_global(image_manager, 
                                                               input_limiar.get(),
                                                               input_max.get()))
    botao.pack(pady=10)

def aplicar_limiarizacao_global(image_manager, limiar, valor_max):
    try:
        limiar = int(limiar)
        if not 0 <= limiar <= 255:
            limiar = 127
    except ValueError:
        limiar = 127
        
    try:
        valor_max = int(valor_max)
        if not 0 <= valor_max <= 255:
            valor_max = 255
    except ValueError:
        valor_max = 255
    
    image_manager.load_image()
    edi_matrix = image_manager.get_edited_matrix()
    matrix = limiarizacao_global(edi_matrix, limiar=limiar, valor_max=valor_max)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()
    image_manager.root.mostrar_modificacoes()