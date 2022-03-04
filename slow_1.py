# Relevant file paths
GENOME_PATH = "path/to/human.fsa"
DESTINATION_PATH = "path/to/human_complement.fsa"

# Open files
infile = open(GENOME_PATH, "r")
outfile = open(DESTINATION_PATH, "w")

for line in infile:
    if line[0] == ">":
        outfile.write(line)  # Just write the line if it's a header
    else:
        comp_line = ""
        # Compute complementary sequence
        for char in line:
            new_char = char
            new_char = "a" if char == "t" else new_char
            new_char = "t" if char == "a" else new_char
            new_char = "c" if char == "g" else new_char
            new_char = "g" if char == "c" else new_char
            comp_line += new_char
        outfile.write(comp_line)  # Write to file

infile.close()
outfile.close()
