import numpy as np
from PIL import Image

def logistic_map(x, r):
    return r * x * (1 - x)

def generate_chaotic_sequence(length, seed, r=3.99):
    sequence = [seed]
    for _ in range(1, length):
        sequence.append(logistic_map(sequence[-1], r))
    return sequence

def embed_message(image_path, message, seed):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    message_length = len(binary_message)

    img = Image.open(image_path)
    img_array = np.array(img)
    if img.mode != 'RGB':
        raise ValueError("Image mode needs to be RGB")

    chaotic_sequence = generate_chaotic_sequence(message_length, seed)

    flat_indices = (np.array(chaotic_sequence) * img_array.size // 3).astype(np.int64)

    for idx, bit in zip(flat_indices, binary_message):
        row = (idx // 3) // img_array.shape[1]
        col = (idx // 3) % img_array.shape[1]
        channel = idx % 3

        if bit == '1':
            img_array[row, col, channel] |= 1;
        else:
            img_array[row, col, channel] &= ~1

    stego_image = Image.fromarray(img_array)
    stego_image.save('stego_image.png')

embed_message('download.png', 'porukamojajeova', 0.5)