import tkinter as tk

from backend.desafio import detectar_domino

def criar_menu_extracao(root, callback, image_manager):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Desafio", command=lambda: desafio_janela(image_manager))
    return menu

def desafio_janela(image_manager):
    janela = tk.Toplevel()
    janela.title("Desafio")
    janela.geometry("300x250")
    
    label = tk.Label(janela, wraplength=280, text="Descobrir quantos pontos tem na parte superior e na parte inferior da peça de dominó.")
    label.pack(pady=20)
    
    resultado_label = tk.Label(janela, text="")
    resultado_label.pack(pady=10)
    
    def executar_desafio():
        superior_valor, inferior_valor = detectar_domino(image_manager)
        
        if superior_valor == -1 and inferior_valor == -1:
            resultado_label.config(
                text="Não foi detectado um dominó na imagem",
                fg="red",
                font=("Arial", 10, "bold")
            )
        else:
            resultado_label.config(
                text=f"Superior: {superior_valor}, Inferior: {inferior_valor}",
                font=("Arial", 10, "bold")
            )
    
    botao = tk.Button(janela, text="Iniciar Desafio", command=executar_desafio)
    botao.pack(pady=10)