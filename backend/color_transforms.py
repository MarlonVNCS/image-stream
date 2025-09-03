from PIL import Image
import numpy as np

# Step 1: Load the image file
def load_image_as_matrix(file_path):
    image = Image.open(file_path)  # Open the image
    matrix = np.array(image)       # Convert to numpy array (matrix)
    return matrix, image.mode

# Step 2: Edit the matrix (example: invert colors)
def invert_colors(matrix):
    # Example: Invert the colors (assuming an RGB image)
    # print("Matriz: ", matrix)
    edited_matrix = 255 - matrix
    return edited_matrix

def gray_scale(matrix):
    # (Cor R + Cor G + Cor B)/3
    if len(matrix.shape) == 3 and matrix.shape[2] == 3:  # Check if it's an RGB image
        gray_matrix = np.mean(matrix, axis=2).astype(np.uint8)  # Convert to grayscale
        edited_matrix = np.stack((gray_matrix,)*3, axis=-1)  # Convert back to 3 channels
    else:
        edited_matrix = matrix  # If not RGB, return the original matrix
    return edited_matrix

def brightness_contrast(matrix, brightness=0, contrast=1):
    # Adjust brightness and contrast
    edited_matrix = np.clip(contrast * matrix + brightness, 0, 255).astype(np.uint8)
    return edited_matrix

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

    # Edit the matrix
    # edited_matrix = invert_colors(matrix) # Invert colors
    # edited_matrix = gray_scale(matrix) # Convert to grayscale
    
    edited_matrix = brightness_contrast(matrix, brightness=30, contrast=1.2) # Adjust brightness and contrast

    # Save the edited matrix as an image
    save_matrix_as_image(edited_matrix, mode, output_file)
    
    print(f"Edited image saved as {output_file}")