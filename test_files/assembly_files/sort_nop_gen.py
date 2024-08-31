def insert_nop_between_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            outfile.write(line)
            outfile.write("nop\nnop\n")  # Inserting two 'nop' lines after each line in the input file

if __name__ == "__main__":
    input_filename = "sort.s"  # Input file name
    output_filename = "sort_test.s"  # Output file name
    insert_nop_between_lines(input_filename, output_filename)
    print("Inserted 'nop' lines between each line in the input file.")
