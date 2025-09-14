import tkinter as tk

def janela_base(nome):
    janela = tk.Toplevel()
    janela.title(nome)
    janela.geometry("300x200")
    tk.Label(janela, text=nome).pack(pady=20)
    return janela