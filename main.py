import random
import csv

def generate_binary_field(length):
    binary_field = ""
    for _ in range(length):
        bit = random.randint(0, 1)
        binary_field += str(bit)
    return binary_field

def write_to_csv(filename, num_records):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Field 1', 'Field 2'])
        for _ in range(num_records):
            field1 = generate_binary_field(16)
            field2 = generate_binary_field(16)
            writer.writerow([field1, field2])

def main():
    num_records = 50000
    write_to_csv('notebooks/models/binary_fields_1M.csv', num_records)
    print(f"Data for {num_records} records written to binary_fields_50k.csv")

if __name__ == "__main__":
    main()
