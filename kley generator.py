import numpy as np

# Generate a random key of length 8
key = np.random.randint(2, size=8)

# Convert the key to a list if needed
key_list = key.tolist()

print("Generated key:", key_list)

