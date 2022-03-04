import os

# Relevant file paths
GENOME_PATH = "path/to/human.fsa"
DESTINATION_PATH = "path/to/human_complement.fsa"
TEMP_PATH = "path/to/temp.fsa"

# Clean outfile before each run, as I am working with append mode.
outfile = open(DESTINATION_PATH, "w")
outfile.write("")
outfile.close()

outfile = open(DESTINATION_PATH, "a")  # Open in append mode


# Function for writing to outfile with the proper FASTA sequence headers. Reads from the temp file.
def write_outfile():
    global outfile, tempfile, count_a, count_t, count_c, count_g, count_n
    # Close and reopen temp_file in read+write mode
    tempfile.close()
    tempfile_f = open(TEMP_PATH, "r+")
    # Append new lines to outfile
    for temp_line in tempfile_f:
        if temp_line[0] == ">":
            # Seq header
            outfile.write(f">seq{seq_count} A:{count_a} T:{count_t} C:{count_c} G:{count_g} N:{count_n}\n")
        else:
            # Normal sequence
            outfile.write(temp_line)

    tempfile_f.truncate(0)  # Clean temp file
    tempfile_f.close()
    tempfile = open(TEMP_PATH, "a")  # Reopen temp file in append mode
    count_a, count_t, count_c, count_g, count_n = 0, 0, 0, 0, 0  # reset base counts


# Open files
infile = open(GENOME_PATH, "r")
tempfile = open(TEMP_PATH, "a")

# Set useful counts to 0
seq_count = 0
count_a, count_t, count_c, count_g, count_n = 0, 0, 0, 0, 0
for line in infile:
    # Write sequence and header to out file if first char is ">" (unless it's the first one)
    if line[0] == ">":
        if seq_count != 0:
            write_outfile()
        # Write header to temp file and increase sequence count
        tempfile.write(line)
        seq_count += 1
    # Compute complementary sequence and add to corresponding count
    else:
        comp_line = ""
        for char in line:
            new_char = char
            if char == "a":
                new_char = "t"
                count_t += 1
            elif char == "t":
                new_char = "a"
                count_a += 1
            elif char == "c":
                new_char = "g"
                count_g += 1
            elif char == "g":
                new_char = "c"
                count_c += 1
            elif char == "n":
                count_n += 1
            comp_line += new_char
        tempfile.write(comp_line)  # Write line to temp file

write_outfile()  # Write last sequence to out file (needed here as I use the ">" as triggers)

# Close all files
tempfile.close()
infile.close()
outfile.close()

os.remove(TEMP_PATH)  # Delete temp file
