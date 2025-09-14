import tkinter as tk
from .arquivo_menu import criar_menu_arquivo
from .transformacoes_menu import criar_menu_transformacoes
from .filtros_menu import criar_menu_filtros
from .morfologia_menu import criar_menu_morfologia
from .extracao_menu import criar_menu_extracao

class MenuManager:
    def __init__(self, root, callback, image_manager):
        self.root = root
        self.callback = callback
        self.image_manager = image_manager
        self.popup_menus = {}
        self.create_popup_menus()

    def create_popup_menus(self):
        self.popup_menus["arquivo"] = criar_menu_arquivo(self.root, self.callback, self.image_manager)
        self.popup_menus["transf"] = criar_menu_transformacoes(self.root, self.callback, self.image_manager)
        self.popup_menus["filtros"] = criar_menu_filtros(self.root, self.callback, self.image_manager)
        self.popup_menus["morfo"] = criar_menu_morfologia(self.root, self.callback, self.image_manager)
        self.popup_menus["extracao"] = criar_menu_extracao(self.root, self.callback, self.image_manager)

    def show_menu(self, event, menu_key):
        if menu_key in self.popup_menus:
            button = event.widget
            x = button.winfo_rootx()
            y = button.winfo_rooty() + button.winfo_height()
            self.popup_menus[menu_key].post(x, y)