import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


# Step 1: Load the image and convert to matrix
def load_image_as_matrix(image_path):
    image = Image.open(image_path)
    matrix = np.array(image)
    return matrix, image.mode

# Step 2: Edit the matrix (example: invert colors)
def invert_colors(matrix):
    # Example: Invert the colors (assuming an RGB image)
    edited_matrix = 255 - matrix
    return edited_matrix

def translate_image(matrix, x_shift, y_shift):
    # Translate the matrix by x_shift and y_shift
    translated_matrix = np.roll(matrix, shift=(y_shift, x_shift), axis=(0, 1))
    return translated_matrix

def scale_image(matrix, sx, sy):
    """
    Escala uma imagem representada por uma matriz numpy.
    sx = fator de escala no eixo X (largura)
    sy = fator de escala no eixo Y (altura)
    """
    altura, largura = matrix.shape[:2]

    # Novas dimensões
    nova_altura = int(altura * sy)
    nova_largura = int(largura * sx)

    # Criar coordenadas de destino
    y_coords, x_coords = np.meshgrid(
        np.linspace(0, altura - 1, nova_altura),
        np.linspace(0, largura - 1, nova_largura),
        indexing="ij"
    )

    # Arredondar para inteiros (nearest neighbor)
    y_coords = y_coords.astype(int)
    x_coords = x_coords.astype(int)

    # Mapear para a nova imagem
    scaled_matrix = matrix[y_coords, x_coords]

    return scaled_matrix


def mirror_image(matrix, mode="horizontal"):
    """
    Espelha a imagem.
    mode = "horizontal" -> inverte esquerda/direita
    mode = "vertical"   -> inverte cima/baixo
    """
    altura, largura = matrix.shape[:2]

    # Coordenadas originais
    y, x = np.meshgrid(np.arange(altura), np.arange(largura), indexing="ij")
    ones = np.ones_like(x)
    coords = np.stack([x.ravel(), y.ravel(), ones.ravel()]).astype(float)

    if mode == "horizontal":
        M = np.array([
            [-1, 0, 0],
            [0,  1, 0],
            [0,  0, 1]
        ])
        # Centralizar para espelhar em torno do meio
        coords[0] -= largura/2
        coords = M @ coords
        coords[0] += largura/2

    elif mode == "vertical":
        M = np.array([
            [1,  0, 0],
            [0, -1, 0],
            [0,  0, 1]
        ])
        coords[1] -= altura/2
        coords = M @ coords
        coords[1] += altura/2

    # Coordenadas finais
    new_x = np.round(coords[0]).astype(int)
    new_y = np.round(coords[1]).astype(int)

    mirrored = np.zeros_like(matrix)
    mask = (0 <= new_x) & (new_x < largura) & (0 <= new_y) & (new_y < altura)
    mirrored[new_y[mask], new_x[mask]] = matrix[y.ravel()[mask], x.ravel()[mask]]

    return mirrored

def rotate_image(matrix, angle_degrees):
    """
    Rotaciona uma imagem em torno do centro pelo ângulo dado (em graus).
    Usa rotação geométrica sem interpolação (nearest neighbor).
    """
    angle = np.radians(angle_degrees)
    cos_t, sin_t = np.cos(angle), np.sin(angle)

    altura, largura = matrix.shape[:2]

    # Coordenadas originais
    y, x = np.meshgrid(np.arange(altura), np.arange(largura), indexing="ij")
    ones = np.ones_like(x)
    coords = np.stack([x.ravel(), y.ravel(), ones.ravel()]).astype(float)  # ✅ conversão para float

    # Centralizar a imagem antes de rotacionar
    cx, cy = largura / 2, altura / 2
    coords[0] -= cx
    coords[1] -= cy

    # Matriz de rotação
    M = np.array([
        [cos_t, -sin_t, 0],
        [sin_t,  cos_t, 0],
        [0,      0,     1]
    ])

    # Aplicar rotação
    new_coords = M @ coords

    # Transladar de volta
    new_coords[0] += cx
    new_coords[1] += cy

    # Pegar coordenadas finais
    new_x = np.round(new_coords[0]).astype(int)
    new_y = np.round(new_coords[1]).astype(int)

    # Criar imagem de saída
    rotated = np.zeros_like(matrix)

    # Filtrar pontos dentro dos limites
    mask = (0 <= new_x) & (new_x < largura) & (0 <= new_y) & (new_y < altura)
    rotated[new_y[mask], new_x[mask]] = matrix[y.ravel()[mask], x.ravel()[mask]]

    return rotated


# Step 3: Save the matrix back as an image
def save_matrix_as_image(matrix, mode, output_path):
    edited_image = Image.fromarray(matrix, mode)  # Convert matrix back to image
    edited_image.save(output_path)                # Save the image

# Example usage
if __name__ == "__main__":
    input_file = "input_image.jpg"  # Replace with your input image file path
    output_file = "output_image.jpg"  # Replace with your desired output file path

    # Load the image and convert to matrix
    matrix, mode = load_image_as_matrix(input_file)

    # Edit the matrix: invert colors
    # edited_matrix = invert_colors(matrix)

    # Edit the matrix: translate position
    x_shift, y_shift = 50, 30  # Example: shift 50 pixels right and 30 pixels down
    # edited_matrix = translate_image(matrix, x_shift, y_shift)
    
    # edited_matrix = scale_image(matrix, sx=2, sy=2) #aumentar imagem
    # edited_matrix = rotate_image(matrix, 45) #rotacionar imagem
    
    # edited_matrix = mirror_image(matrix, "horizontal") # espelhar horizontalmente
    edited_matrix = mirror_image(matrix, "vertical") # espelhar verticalmente

    # Save the edited matrix as an image
    save_matrix_as_image(edited_matrix, mode, output_file)

    print(f"Edited image saved as {output_file}")
    
    
    mirrored_h = mirror_image(matrix, "horizontal")
    mirrored_v = mirror_image(matrix, "vertical")
    