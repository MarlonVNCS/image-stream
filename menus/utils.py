import tkinter as tk

def janela_base(nome, altura=200):
    janela = tk.Toplevel()
    janela.title(nome)
    janela.geometry(f"300x{altura}")
    tk.Label(janela, text=nome).pack(pady=20)
    return janela