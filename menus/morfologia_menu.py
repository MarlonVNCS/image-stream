import tkinter as tk
from menus.utils import janela_base
from backend.morfologia import erosao
import backend.morfologia as m

def criar_menu_morfologia(root, callback, image_manager):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Dilatação", command=lambda: callback("Dilatação"))
    menu.add_command(label="Erosão", command=lambda: erosao_janela(image_manager))
    menu.add_command(label="Abertura", command=lambda: callback("Abertura"))
    menu.add_command(label="Fechamento", command=lambda: callback("Fechamento"))
    return menu


def erosao_janela(image_manager):
    janela = janela_base("Erosão")
    x = tk.Label(janela, text="Valor:")
    x.pack()
    input_x = tk.Entry(janela)
    input_x.pack()
    
    botao = tk.Button(janela, text="Aplicar", command=lambda: erosao(image_manager,input_x.get()))
    botao.pack(pady=10)
def erosao(image_manager, x=0):
    try:
        x = int(x)
    except ValueError:
        x = 0

    edi_matrix = image_manager.get_edited_matrix()
    matrix = m.erosao(edi_matrix, x)
    image_manager.set_edited_matrix(matrix)
    image_manager.root.mostrar_modificacoes()