import numpy as np
from PIL import Image

def logistic_map(x, r):
    return r * x * (1 - x)

def generate_chaotic_sequence(length, seed, r=3.99):
    sequence = [seed]
    for _ in range(1, length):
        sequence.append(logistic_map(sequence[-1], r))
    return sequence

def extract_message(image_path, seed, message_length_bits):
    img = Image.open(image_path)
    img_array = np.array(img)
    if img.mode != 'RGB':
        raise ValueError("Image mode needs to be RGB")

    chaotic_sequence = generate_chaotic_sequence(message_length_bits, seed)
    flat_indices = (np.array(chaotic_sequence) * img_array.size // 3).astype(np.int64)

    binary_message = ''

    for idx in flat_indices:
        row = (idx // 3) // img_array.shape[1]
        col = (idx // 3) % img_array.shape[1]
        channel = idx % 3
        binary_message += str(img_array[row, col, channel] & 1)

    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    return message
# Example usage

extracted_message = extract_message('stego_image.png', 0.5, 8 * len('porukamojajeova'))
print("Extracted Message:", extracted_message)