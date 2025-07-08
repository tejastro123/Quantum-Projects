def convert_bitstrings_to_integers(input_file, output_file):
    integers = []
    
    with open(input_file, 'r') as f:
        for line in f:
            bitstring = line.strip()
            if bitstring:  # Skip empty lines
                integer = int(bitstring, 2)
                integers.append(integer)
    
    with open(output_file, 'w') as f:
        for i in integers:
            f.write(str(i) + '\n')

    print(f"Converted {len(integers)} bitstrings to integers.")
    print(f"Output saved to: {output_file}")
    print("Sample:")
    for i in integers[:5]:
        print(i)

if __name__ == "__main__":
    input_path = "output/random_bits.txt"
    output_path = "output/random_integers.txt"
    convert_bitstrings_to_integers(input_path, output_path)
