import tkinter as tk

def criar_menu_filtros(root, callback):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Brilho e contraste", command=lambda: callback("Brilho e contraste"))
    menu.add_command(label="Grayscale", command=lambda: callback("Grayscale"))
    menu.add_command(label="Passa-baixa", command=lambda: callback("Passa-baixa"))
    menu.add_command(label="Passa-alta", command=lambda: callback("Passa-alta"))
    menu.add_command(label="Threshold e afinamento", command=lambda: callback("Threshold e afinamento"))
    return menu