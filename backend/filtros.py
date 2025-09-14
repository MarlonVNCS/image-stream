from PIL import Image
import numpy as np


# Step 2: Edit the matrix (example: invert colors)
def invert_colors(matrix):
    # Example: Invert the colors (assuming an RGB image)
    # print("Matriz: ", matrix)
    edited_matrix = 255 - matrix
    return edited_matrix

def grayscale(matrix):
    # (Cor R + Cor G + Cor B)/3
    if len(matrix.shape) == 3 and matrix.shape[2] == 3:  # Check if it's an RGB image
        gray_matrix = np.mean(matrix, axis=2).astype(np.uint8)  # Convert to grayscale
        edited_matrix = np.stack((gray_matrix,)*3, axis=-1)  # Convert back to 3 channels
    else:
        edited_matrix = matrix  # If not RGB, return the original matrix
    return edited_matrix

def brilho_contraste(matrix, brilho=0.0, contraste=1.0):
    # Adjust brightness and contrast
    edited_matrix = np.clip(contraste * matrix + brilho, 0, 255).astype(np.uint8)
    return edited_matrix
