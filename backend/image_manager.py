import numpy as np
from PIL import Image


class ImageManager:
    def __init__(self):
        self.original_matrix = None
        self.edited_matrix = None
        self.image_mode = None
        self.image_path = None
        self.root = None  # Referência para a janela principal

    def load_image(self):
        """
        Carrega uma imagem e armazena sua matriz original
        """
        self.image_path = self.image_path
        image = Image.open(self.image_path)
        self.original_matrix = np.array(image)
        self.edited_matrix = np.copy(self.original_matrix)  # Cria uma cópia para edição
        self.image_mode = image.mode
        return self.original_matrix

    def save_image(self, output_path, use_original=False):
        """
        Salva a imagem em um arquivo
        Args:
            output_path: Caminho onde a imagem será salva
            use_original: Se True, salva a imagem original. Se False, salva a imagem editada
        """
        matrix_to_save = self.original_matrix if use_original else self.edited_matrix
        if matrix_to_save is None:
            raise ValueError("Nenhuma imagem foi carregada ainda")
            
        image = Image.fromarray(matrix_to_save, self.image_mode)
        image.save(output_path)

    def reset_to_original(self):
        """
        Restaura a imagem editada para o estado original
        """
        if self.original_matrix is not None:
            self.edited_matrix = np.copy(self.original_matrix)

    def get_original_matrix(self):
        """
        Retorna a matriz da imagem original
        """
        return self.original_matrix

    def get_edited_matrix(self):
        """
        Retorna a matriz da imagem editada
        """
        return self.edited_matrix

    def set_edited_matrix(self, new_matrix):
        """
        Atualiza a matriz da imagem editada
        """
        self.edited_matrix = new_matrix
    
    def set_image_path(self, path):
        """
        Define o caminho da imagem atual
        """
        self.image_path = path
    
    def get_image_path(self):
        """
        Retorna o caminho da imagem atual
        """
        return self.image_path
        
    def set_root(self, root):
        """
        Define a referência para a janela principal
        """
        self.root = root