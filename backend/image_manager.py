import numpy as np
from PIL import Image


class ImageManager:
    def __init__(self):
        self.original_matrix = None
        self.edited_matrix = None
        self.image_mode = None
        self.image_path = None
        self.root = None 

    def load_image(self):
        self.image_path = self.image_path
        image = Image.open(self.image_path)
        self.original_matrix = np.array(image)
        self.edited_matrix = np.copy(self.original_matrix)  
        self.image_mode = image.mode
        return self.original_matrix

    def save_image(self, output_path, use_original=False):
        matrix_to_save = self.original_matrix if use_original else self.edited_matrix
        if matrix_to_save is None:
            raise ValueError("Nenhuma imagem foi carregada ainda")
            
        image = Image.fromarray(matrix_to_save, self.image_mode)
        image.save(output_path)

    def reset_to_original(self):
        if self.original_matrix is not None:
            self.edited_matrix = np.copy(self.original_matrix)

    def get_original_matrix(self):
        return self.original_matrix

    def get_edited_matrix(self):
        return self.edited_matrix

    def set_edited_matrix(self, new_matrix):
        self.edited_matrix = new_matrix
    
    def set_image_path(self, path):
        self.image_path = path
    
    def get_image_path(self):
        return self.image_path
        
    def set_root(self, root):
        self.root = root