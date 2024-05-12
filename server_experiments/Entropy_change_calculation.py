import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy
import encryption_decryption_functions
# Function to calculate entropy of a string
def decstr(cipher, n, block_padding=0):
    message = ""
    cipher_length = len(cipher)
    block_size = cipher_length // n
    for i in range(n):
        block_padded = cipher[block_size * i: block_size * (i + 1)]
        block_unpadded = block_padded[block_padding:]  # Exclude padding
        for j in range(len(block_unpadded) // 5):  # Each character is represented by 5 bits
            char_bin = block_unpadded[j * 5: (j + 1) * 5]
            character = encryption_decryption_functions.chrlist[encryption_decryption_functions.binlist.index(char_bin)]
            message += character
    return message
def calculate_entropy(text):
    # Calculate probability distribution
    prob_dist = [text.count(c) / len(text) for c in set(text)]
    # Calculate entropy
    return entropy(prob_dist, base=2)

# Function to plot entropy comparison
def plot_entropy_comparison(original_text, encrypted_text):
    original_words = original_text.split()
    encrypted_words = encrypted_text.split()

    num_words = min(len(original_words), len(encrypted_words))

    original_entropies = [calculate_entropy(word) for word in original_words[:num_words]]
    encrypted_entropies = [calculate_entropy(word) for word in encrypted_words[:num_words]]

    plt.figure(figsize=(10, 6))
    plt.plot(original_entropies, label='Original Text', marker='o')
    plt.plot(encrypted_entropies, label='Encrypted Text', marker='x')
    plt.xlabel('Word Index')
    plt.ylabel('Entropy')
    plt.title('Entropy Comparison of Original and Encrypted Text')
    plt.legend()
    plt.grid(True)
    plt.xticks(range(num_words))
    plt.show()

original_text = "lorem ipsum dolor sit amet consectetur adipiscing elit vestibulum commodo justo vel erat bibendum eget venenatis felis commodo sed nec metus a nisi luctus lacinia integer nec felis id velit consequat lacinia nullam efficitur metus eu augue consectetur quis vestibulum orci efficitur in hac habitasse platea dictumst duis at turpis eu justo efficitur scelerisque fusce euismod nisi sit amet dictum consectetur odio diam varius odio id lobortis arcu libero ut leo integer ut finibus mauris vitae luctus nunc sed elementum sodales nisi quis dignissim velit rhoncus eu vivamus mattis odio sit amet laoreet viverra ut gravida justo ut justo vestibulum nec placerat dui tempor etiam ultrices tortor a justo vestibulum at convallis nunc feugiat phasellus tincidunt ipsum nec ante posuere at auctor metus ullamcorper sed ut met"
encrypted_text = decstr(encryption_decryption_functions.encrypt_message(original_text, np.array([[0, 0, 0, 0, 0, 0, 0, 0]])))
plot_entropy_comparison(original_text, encrypted_text)
