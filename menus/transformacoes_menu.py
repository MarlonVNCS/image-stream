import tkinter as tk
import backend.transformacoes as t
from .utils import janela_base

def criar_menu_transformacoes(root, callback, image_manager):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Transladar", command=lambda: transladar_janela(image_manager))
    menu.add_command(label="Rotacionar", command=lambda: rotacionar_janela(image_manager))
    menu.add_command(label="Espelhar", command=lambda: espelhar_janela(image_manager))
    menu.add_command(label="Aumentar", command=lambda: aumentar_janela(image_manager))
    menu.add_command(label="Diminuir", command=lambda: diminuir_janela(image_manager))
    return menu

def transladar_janela(image_manager):
    janela = janela_base("Transladar")
    x = tk.Label(janela, text="Deslocamento X:")
    x.pack()
    input_x = tk.Entry(janela)
    input_x.pack()
    y = tk.Label(janela, text="Deslocamento Y:")
    y.pack()
    input_y = tk.Entry(janela)
    input_y.pack()
    
    botao = tk.Button(janela, text="Aplicar", command=lambda: transladar(image_manager,input_x.get(), input_y.get()))
    botao.pack(pady=10)
def transladar(image_manager, x_shift=0, y_shift=0):
    try:
        x_shift = int(x_shift)
    except ValueError:
        x_shift = 0
    try:
        y_shift = int(y_shift)
    except ValueError:
        y_shift = 0
    edi_matrix = image_manager.get_edited_matrix()
    matrix = t.transladar(edi_matrix, x_shift, y_shift)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()
    
def rotacionar_janela(image_manager):
    janela = janela_base("Rotacionar")
    label = tk.Label(janela, text="Ângulo (em graus):")
    label.pack()
    slider_angulo = tk.Scale(janela, from_=0, to=360, orient=tk.HORIZONTAL)
    slider_angulo.pack()
    botao = tk.Button(janela, text="Aplicar", command=lambda: rotacionar(image_manager, slider_angulo.get()))
    botao.pack(pady=10)
    
def rotacionar(image_manager, angle):
    edi_matrix = image_manager.get_edited_matrix()
    matrix = t.rotacionar(edi_matrix, angle)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def espelhar_janela(image_manager):
    janela = janela_base("Espelhar")
    label = tk.Label(janela, text="Direção:")
    label.pack()
    var = tk.StringVar(value="horizontal")
    radio_h = tk.Radiobutton(janela, text="Horizontal", variable=var, value="horizontal")
    radio_h.pack()
    radio_v = tk.Radiobutton(janela, text="Vertical", variable=var, value="vertical")
    radio_v.pack()
    botao = tk.Button(janela, text="Aplicar", command=lambda: espelhar(image_manager, var.get()))
    botao.pack(pady=10)
def espelhar(image_manager, mode):
    edi_matrix = image_manager.get_edited_matrix()
    matrix = t.espelhar(edi_matrix, mode)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()
    
def aumentar_janela(image_manager):
    janela = janela_base("Aumentar")
    label = tk.Label(janela, text="Fator de aumento (ex: 2 para dobrar):")
    label.pack()
    input_fator = tk.Entry(janela)
    input_fator.pack()
    botao = tk.Button(janela, text="Aplicar", command=lambda: aumentar(image_manager, input_fator.get()))
    botao.pack(pady=10)
    aviso = tk.Label(janela, text="(Só é possível ver o resultado no arquivo salvo)")
    aviso.pack()
    
def aumentar(image_manager, factor):
    try:
        factor = int(factor)
    except ValueError:
        factor = 1
    edi_matrix = image_manager.get_edited_matrix()
    matrix = t.escala(edi_matrix, factor, factor)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()

def diminuir_janela(image_manager):
    janela = janela_base("Diminuir")
    label = tk.Label(janela, text="Fator de diminuição (ex: 2 para metade):")
    label.pack()
    input_fator = tk.Entry(janela)
    input_fator.pack()
    botao = tk.Button(janela, text="Aplicar", command=lambda: diminuir(image_manager, input_fator.get()))
    botao.pack(pady=10)

def diminuir(image_manager, factor):
    try:
        factor = int(factor)
    except ValueError:
        factor = 1
    edi_matrix = image_manager.get_edited_matrix()
    matrix = t.escala(edi_matrix, 1/factor, 1/factor)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()
    