import tkinter as tk
from tkinter import filedialog, messagebox

def criar_menu_arquivo(root, callback, image_manager):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Abrir imagem", command=lambda: abrir_imagem(image_manager, callback))
    menu.add_command(label="Salvar imagem", command=lambda: salvar_imagem(image_manager, callback))
    menu.add_command(label="Sobre", command=lambda: mostrar_sobre())
    menu.add_separator()
    menu.add_command(label="Sair", command=root.quit)
    return menu

def abrir_imagem(image_manager, callback):
    file_path = filedialog.askopenfilename(
        title="Abrir Imagem",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            image_manager.set_image_path(file_path)
            image_manager.load_image()
            callback(f"Imagem aberta: {file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir a imagem: {str(e)}")

def salvar_imagem(image_manager, callback):
    if image_manager.get_edited_matrix() is None:
        messagebox.showwarning("Aviso", "Nenhuma imagem aberta para salvar")
        return

    file_path = filedialog.asksaveasfilename(
        title="Salvar Imagem",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), 
                  ("BMP files", "*.bmp"), ("TIFF files", "*.tiff"), ("All Files", "*.*")]
    )
    
    if file_path:
        try:
            image_manager.set_image_path(file_path)
            image_manager.save_image(file_path)
            callback(f"Imagem salva: {file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar a imagem: {str(e)}")

def mostrar_sobre():
    messagebox.showinfo("Sobre", 
        "Image Stream\n\n" +
        "Desenvolvido por:\n" +
        "Júlia Nathalie Schmitz\n" +
        "Marlon Vinicius Gonçalves\n\n" +
        "Processamento Digital de Imagens\n" +
        "Universidade Feevale - 2023/2")