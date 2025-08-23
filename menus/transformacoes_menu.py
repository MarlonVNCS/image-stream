import tkinter as tk

def criar_menu_transformacoes(root, callback):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Transladar", command=lambda: callback("Transladar"))
    menu.add_command(label="Rotacionar", command=lambda: callback("Rotacionar"))
    menu.add_command(label="Espelhar", command=lambda: callback("Espelhar"))
    menu.add_command(label="Aumentar", command=lambda: callback("Aumentar"))
    menu.add_command(label="Diminuir", command=lambda: callback("Diminuir"))
    return menu