import tkinter as tk

def criar_menu_arquivo(root, callback):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Abrir imagem", command=lambda: callback("Abrir imagem"))
    menu.add_command(label="Salvar imagem", command=lambda: callback("Salvar imagem"))
    menu.add_command(label="Sobre", command=lambda: callback("Sobre"))
    menu.add_separator()
    menu.add_command(label="Sair", command=root.quit)
    return menu