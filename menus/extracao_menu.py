import tkinter as tk

def criar_menu_extracao(root, callback):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Desafio", command=lambda: callback("Desafio"))
    return menu