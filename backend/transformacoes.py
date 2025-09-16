import numpy as np
from PIL import Image

def invert_colors(matrix):
    edited_matrix = 255 - matrix
    return edited_matrix

def transladar(matrix, x_shift, y_shift):
    translated_matrix = np.roll(matrix, shift=(y_shift, x_shift), axis=(0, 1))
    return translated_matrix

def escala(matrix, sx, sy):
    altura, largura = matrix.shape[:2]
    nova_altura = int(altura * sy)
    nova_largura = int(largura * sx)

    y_coords, x_coords = np.meshgrid(
        np.linspace(0, altura - 1, nova_altura),
        np.linspace(0, largura - 1, nova_largura),
        indexing="ij"
    )

    y_coords = y_coords.astype(int)
    x_coords = x_coords.astype(int)

    scaled_matrix = matrix[y_coords, x_coords]

    return scaled_matrix


def espelhar(matrix, mode="horizontal"):
    altura, largura = matrix.shape[:2]

    y, x = np.meshgrid(np.arange(altura), np.arange(largura), indexing="ij")
    ones = np.ones_like(x)
    coords = np.stack([x.ravel(), y.ravel(), ones.ravel()]).astype(float)

    if mode == "horizontal":
        M = np.array([
            [-1, 0, 0],
            [0,  1, 0],
            [0,  0, 1]
        ])
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

    new_x = np.round(coords[0]).astype(int)
    new_y = np.round(coords[1]).astype(int)

    mirrored = np.zeros_like(matrix)
    mask = (0 <= new_x) & (new_x < largura) & (0 <= new_y) & (new_y < altura)
    mirrored[new_y[mask], new_x[mask]] = matrix[y.ravel()[mask], x.ravel()[mask]]

    return mirrored

def rotacionar(matrix, angle_degrees):
    angle = np.radians(angle_degrees)
    cos_t, sin_t = np.cos(angle), np.sin(angle)

    altura, largura = matrix.shape[:2]

    y, x = np.meshgrid(np.arange(altura), np.arange(largura), indexing="ij")
    ones = np.ones_like(x)
    coords = np.stack([x.ravel(), y.ravel(), ones.ravel()]).astype(float)

    cx, cy = largura / 2, altura / 2
    coords[0] -= cx
    coords[1] -= cy

    M = np.array([
        [cos_t, -sin_t, 0],
        [sin_t,  cos_t, 0],
        [0,      0,     1]
    ])

    new_coords = M @ coords

    new_coords[0] += cx
    new_coords[1] += cy

    new_x = np.round(new_coords[0]).astype(int)
    new_y = np.round(new_coords[1]).astype(int)

    rotated = np.zeros_like(matrix)

    mask = (0 <= new_x) & (new_x < largura) & (0 <= new_y) & (new_y < altura)
    rotated[new_y[mask], new_x[mask]] = matrix[y.ravel()[mask], x.ravel()[mask]]

    return rotated


