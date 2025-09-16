from PIL import Image
import numpy as np


def invert_colors(matrix):
    edited_matrix = 255 - matrix
    return edited_matrix

def grayscale(matrix):
    if len(matrix.shape) == 3 and matrix.shape[2] == 3:  
        gray_matrix = np.mean(matrix, axis=2).astype(np.uint8)  
        edited_matrix = np.stack((gray_matrix,)*3, axis=-1)  
    else:
        edited_matrix = matrix  
    return edited_matrix

def brilho_contraste(matrix, brilho=0.0, contraste=1.0):
    edited_matrix = np.clip(contraste * matrix + brilho, 0, 255).astype(np.uint8)
    return edited_matrix
