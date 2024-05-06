import numpy as np
import ctypes
import tkinter as tk
# the standard parameters: message, key, and ciphertext bit lengths
model_name = 'ANC'
from keras.models import load_model

# the standard parameters: message, key, and ciphertext bit lengths
m_bits = 8
k_bits = 8
c_bits = 8
pad = 'same'
# Compute the size of the message space
m_train = 2 ** (m_bits + k_bits)

alice_file = 'models/crypto/' + model_name + '-alice'
bob_file = 'models/crypto/' + model_name + '-bob'
eve_file = 'models/crypto/' + model_name + '-eve'
alice = load_model(alice_file + '.h5')
bob = load_model(bob_file + '.h5')
eve = load_model(eve_file + '.h5')
block_size_unpadded = 5
block_padding = 3
block_size = block_size_unpadded + block_padding
# Dictonary and corresponding binary
chrlist = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', '.', ',', '!', '?',
    ':', ' '
]
binlist = [
    '00000', '00001', '00010', '00011', '00100',
    '00101', '00110', '00111', '01000', '01001',
    '01010', '01011', '01100', '01101', '01110',
    '01111', '10000', '10001', '10010', '10011',
    '10100', '10101', '10110', '10111', '11000',
    '11001', '11010', '11011', '11100', '11101',
    '11110', '11111'
]


def randombits(n):
    if n == 0:
        return ''
    decvalue = np.random.randint(0, 2 ** n)
    formatstring = '0' + str(n) + 'b'
    return format(decvalue, formatstring)


def encstr(message, block_padding=0):
    cipher = ""
    for c in message:
        binstr = binlist[chrlist.index(c)]
        binstrpadded = randombits(block_padding) + str(binstr)
        cipher = cipher + binstrpadded
    return cipher, len(message)


def decstr(cipher, n, block_padding=0):
    message = ""
    cipherlength = len(cipher)
    block_size = cipherlength // n
    for i in range(n):
        blockpadded = cipher[block_size * i: block_size * i + block_size]
        blockunpadded = blockpadded[block_padding:]
        character = chrlist[binlist.index(blockunpadded)]
        message = message + character
    return message


# Function for converting float to 32-bit binary string
def float_to_binary(value):
    binNum = bin(ctypes.c_uint.from_buffer(ctypes.c_float(value)).value)[2:]
    binstr = binNum.rjust(32, "0")
    return binstr


def binary_to_float(binstr):
    intvalue = int(binstr, 2)
    floatvalue = ctypes.c_float.from_buffer(ctypes.c_uint(intvalue))
    return floatvalue.value


# Convert a positive integer num into a bit vector of 'bits' size
def bitarray(num, bits):
    return np.array(list(np.binary_repr(num).zfill(bits))).astype(np.int8)


def encrypt_message(message, key):
    # Convert message to binary
    m_bin, _ = encstr(message, block_padding=3)
    m_bin_len = len(m_bin)

    ciphertext = ""
    for i in range(m_bin_len // m_bits):
        # Read blocks of size m_bits
        binblockstr = m_bin[m_bits * i: m_bits * i + m_bits]
        binblock = np.array(list(binblockstr)).astype(np.int8).reshape(1, m_bits)

        # print("binblock shape:", binblock.shape)
        # print("key shape:", key.shape)

        floatVector = alice.predict([binblock, key])

        # print("floatVector shape:", floatVector.shape)

        for j in range(c_bits):
            ciphertext += float_to_binary(floatVector[0][j])

    return ciphertext


def decrypt_message(ciphertext, key):
    plaintextbin = ""
    ciphertext_len = len(ciphertext)

    for i in range(ciphertext_len // (c_bits * 32)):
        # Read the ciphertext in chunks of 32 * c_bits bits, i.e., one encoding at a time
        floatVectorbin = ciphertext[c_bits * 32 * i: c_bits * 32 * i + c_bits * 32]

        # Convert the binary chunk to an 8-dim float vector (input for AI Bob)
        floatVector = np.zeros(c_bits, dtype=np.float32).reshape(1, c_bits)
        for j in range(len(floatVectorbin) // 32):
            floatValuebin = floatVectorbin[32 * j: 32 * j + 32]
            floatValue = binary_to_float(floatValuebin)
            floatVector[0][j] = floatValue

        # print("floatVector shape:", floatVector.shape)
        # print("key shape:", key.shape)

        charbinvector = list((bob.predict([floatVector, key]) > 0.5)[0].astype(int))
        for j in range(len(charbinvector)):
            plaintextbin += str(charbinvector[j])

    m_dec = ""
    for i in range(len(plaintextbin) // m_bits):
        strbin = plaintextbin[m_bits * i: m_bits * i + m_bits]
        m_dec += decstr(strbin, len(strbin) // m_bits, block_padding=3)

    return m_dec



# Define a function to handle encryption and decryption
def handle_message(message, key):

    # Convert key to numpy array
    key = np.array(eval(key))  # Assuming the key input is in the format [0, 1, 0, 1, ...]
    key = key.reshape(1, -1)  # Reshape key to (1, 8)

    # Encryption
    ciphertext = encrypt_message(message, key)

    # Decryption
    decrypted_message = decrypt_message(ciphertext, key)

#     # Update the UI with the results
#     encrypted_text_var.set(ciphertext)
#     decrypted_text_var.set(decrypted_message)
#
# # Create a Tkinter window
# window = tk.Tk()
# window.title("Secure Chat")
#
# # Labels
# tk.Label(window, text="Message:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
# tk.Label(window, text="Key:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
# tk.Label(window, text="Encrypted Text:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
# tk.Label(window, text="Decrypted Text:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
#
# # Entry fields
# message_entry = tk.Entry(window, width=50)
# message_entry.grid(row=0, column=1, padx=5, pady=5)
#
# key_entry = tk.Entry(window, width=50)
# key_entry.grid(row=1, column=1, padx=5, pady=5)
#
# # Text areas to display results
# encrypted_text_var = tk.StringVar()
# encrypted_text_var.set("")
# tk.Label(window, textvariable=encrypted_text_var, wraplength=500, justify="left").grid(row=2, column=1, padx=5, pady=5)
#
# decrypted_text_var = tk.StringVar()
# decrypted_text_var.set("")
# tk.Label(window, textvariable=decrypted_text_var, wraplength=500, justify="left").grid(row=3, column=1, padx=5, pady=5)
#
# # Button to trigger encryption and decryption
# encrypt_button = tk.Button(window, text="Encrypt/Decrypt", command=handle_message)
# encrypt_button.grid(row=4, column=1, padx=5, pady=5)
#
# # Start the Tkinter event loop
# window.mainloop()