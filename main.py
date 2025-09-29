import tkinter as tk

from menus import MenuManager
from backend.image_manager import ImageManager
from PIL import Image, ImageTk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Stream")
        self.root.geometry("1000x800")

        self.image_manager = ImageManager()
        self.image_manager.set_root(self)
        self.menu_manager = MenuManager(self.root, self.on_menu_click, self.image_manager)
        self.create_widgets()

    def create_widgets(self):
       
        self.root.grid_rowconfigure(3, weight=1)  
        self.root.grid_columnconfigure(0, weight=1)        
        self.name_frame = tk.Frame(self.root)
        self.name_frame.grid(row=0, column=0, pady=10, sticky='ew')
        
        label_texts = {
            "julia": "Júlia Nathalie Schmitz",
            "marlon": "Marlon Vinicius Gonçalves",
        }
        
        julia = tk.Label(self.name_frame, text=label_texts["julia"])
        marlon = tk.Label(self.name_frame, text=label_texts["marlon"])
        julia.pack(side=tk.LEFT, expand=True)
        marlon.pack(side=tk.LEFT, expand=True)
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=1, column=0, pady=10, sticky='ew')
        
        button_texts = {
            "arquivo": "Arquivo",
            "transf": "Transformações Geométricas",
            "filtros": "Filtros",
            "morfo": "Morfologia Matemática",
            "extracao": "Extração de Características",
        }

        for key, text in button_texts.items():
            button = tk.Button(
                self.button_frame,
                text=text,
                width=25
            )
            button.pack(side=tk.LEFT, padx=5, expand=True)
            button.bind('<Button-1>', lambda e, menu=key: self.menu_manager.show_menu(e, menu))

        self.text_frame = tk.Frame(self.root)
        self.text_frame.grid(row=2, column=0, pady=5, sticky='ew')
        
        self.original_image_text = tk.Label(self.text_frame, text="Imagem Original")
        self.original_image_text.pack(side=tk.LEFT, expand=True)
        
        self.modified_image_text = tk.Label(self.text_frame, text="Imagem Modificada")
        self.modified_image_text.pack(side=tk.RIGHT, expand=True)

        self.image_frame = tk.Frame(self.root)
        self.image_frame.grid(row=3, column=0, pady=10, sticky='nsew')
        
        self.image_frame.grid_columnconfigure(0, weight=1) 
        self.image_frame.grid_columnconfigure(1, weight=1)  
        
        self.original_image_label = None
        self.modified_image_label = None
        

    def on_menu_click(self, menu_item):
        print(f"Selecionou o item de menu: {menu_item}")
        if "imagem aberta" in menu_item.lower():
            path = self.image_manager.get_image_path()
            print(path)
            if path:
                self.mostrar_imagem(path)
        
            

    def run(self):
        self.root.mainloop()
        
    def mostrar_modificacoes(self):
        print("Mostrando modificações...")
        if self.modified_image_label is not None:
            self.modified_image_label.destroy()
            
        edited_matrix = self.image_manager.get_edited_matrix()
        if edited_matrix is not None:
            image = Image.fromarray(edited_matrix)
            w = 0
            h = 0
            if image.width > 500 or image.height > 500:
                if image.width > image.height:
                    w = 500
                    h = int((500 / image.width) * image.height)
                else:
                    h = 500
                    w = int((500 / image.height) * image.width)
                image = image.resize((w, h))
            photo = ImageTk.PhotoImage(image)
            self.modified_image_label = tk.Label(self.image_frame, image=photo)
            self.modified_image_label.image = photo
            self.modified_image_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        else:
            self.modified_image_label = tk.Label(self.image_frame, text="Nenhuma imagem editada disponível")
            self.modified_image_label.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
    def mostrar_imagem(self, image_path):
        if self.original_image_label is not None:
            self.original_image_label.destroy()
            
        image = Image.open(image_path)
        w = 0
        h = 0
        if image.width > 500 or image.height > 500:
            if image.width > image.height:
                w = 500
                h = int((500 / image.width) * image.height)
            else:
                h = 500
                w = int((500 / image.height) * image.width)
            image = image.resize((w, h))
        photo = ImageTk.PhotoImage(image)

        self.original_image_label = tk.Label(self.image_frame, image=photo)
        self.original_image_label.image = photo
        self.original_image_label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')


if __name__ == "__main__":
    app = MainWindow()
    app.run()
