from email.mime import image
from os import name
from tkinter import *
import tkinter as tk
from menus import MenuManager


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Stream")
        self.root.geometry("1000x800")

        # Inicializa o gerenciador de menus
        self.menu_manager = MenuManager(self.root, self.on_menu_click)

        # Criando os elementos da interface
        self.create_widgets()

    def create_widgets(self):
        # Frame para conter os nomes
        self.name_frame = tk.Frame(self.root)
        self.name_frame.pack(pady=10)

        # Frame para conter os botões
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(pady=10)

        # Lista de textos para os botões
        button_texts = {
            "arquivo": "Arquivo",
            "transf": "Transformações Geométricas",
            "filtros": "Filtros",
            "morfo": "Morfologia Matemática",
            "extracao": "Extração de Características",
        }
        label_texts = {
            "julia": "Júlia Nathalie Schmitz",
            "marlon": "Marlon Vinicius Gonçalves",
        }

        # Criando os labels dentro do name_frame
        julia = tk.Label(self.name_frame, text=label_texts["julia"])
        marlon = tk.Label(self.name_frame, text=label_texts["marlon"])
        julia.pack(side=tk.LEFT, padx=5)
        marlon.pack(side=tk.LEFT, padx=5)

        # Criando os botões com menus popup
        for key, text in button_texts.items():
            button = tk.Button(
                self.button_frame,
                text=text,
                width=25
            )
            button.pack(side=tk.LEFT, padx=5)
            # Vincula o evento de clique do botão ao menu popup correspondente
            button.bind('<Button-1>', lambda e, menu=key: self.menu_manager.show_menu(e, menu))


    def on_menu_click(self, menu_item):
        print(f"Selecionou o item de menu: {menu_item}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
