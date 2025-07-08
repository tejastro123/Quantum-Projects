from qrng_utils import generate_random_numbers
import os

def save_to_file(bits_list, filepath):
    with open(filepath, 'w') as f:
        for bits in bits_list:
            f.write(bits + '\n')
    print(f"Saved {len(bits_list)} random bitstrings to: {filepath}")

def main():
    n_bits = 5       # Number of bits per sample
    n_samples = 5   # Number of random numbers

    print(f"Generating {n_samples} true quantum random numbers with {n_bits} bits each...")

    random_bits = generate_random_numbers(n_bits, n_samples)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    save_to_file(random_bits, os.path.join(output_dir, "random_bits.txt"))

    print("Sample Output:")
    for i in range(min(5, len(random_bits))):
        print(f"{i+1}: {random_bits[i]}")

if __name__ == "__main__":
    main()
