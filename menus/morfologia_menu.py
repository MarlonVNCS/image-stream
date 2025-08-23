import tkinter as tk

def criar_menu_morfologia(root, callback):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Dilatação", command=lambda: callback("Dilatação"))
    menu.add_command(label="Erosão", command=lambda: callback("Erosão"))
    menu.add_command(label="Abertura", command=lambda: callback("Abertura"))
    menu.add_command(label="Fechamento", command=lambda: callback("Fechamento"))
    return menu