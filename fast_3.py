import os

# Relevant file paths
GENOME_PATH = "path/to/human.fsa"
DESTINATION_PATH = "path/to/human_complement_4.fsa"

# Clean outfile before each run, as I am working with append mode.
outfile = open(DESTINATION_PATH, "wb")
outfile.write(b"")
outfile.close()


infile = open(GENOME_PATH, "rb")  # Open file in read bytes mode.
# Open file in read bytes mode, then split into a list of all lines in the file. Also remove last blank line.
genome = tuple(infile.read(os.path.getsize(GENOME_PATH)).split(b"\n")[:-1])
infile.close()

comp = []  # List to store complementary sequence and headers.
seq_count, count_a, count_t, count_c, count_g, count_n = 0, 0, 0, 0, 0, 0  # Init useful counts
for genome_line in genome:
    if genome_line[0].to_bytes(1, "little") == b">":
        # Set previous header and reset counts when finding a new sequence
        if seq_count != 0:
            comp[prev_fasta_header] = f">seq{seq_count} A:{count_a} T:{count_t} C:{count_c} G:{count_g} " \
                                      f"N:{count_n}".encode("utf-8")
            count_a, count_t, count_c, count_g, count_n = 0, 0, 0, 0, 0
            # Run if RAM is limited. Writes file by sequence and cleans comp[] instead of storing the entire genome
            # twice in memory (lists take a lot of space!).
            # with open(DESTINATION_PATH, "ab") as outfile:
            #     outfile.write(b"\n".join(comp))
            # comp = []
        seq_count += 1  # Set count to next sequence
        comp.append(genome_line)  # Put header in comp list
        prev_fasta_header = len(comp) - 1  # Store index of this sequence's header for setting new header later on.
    # Compute complementary sequence for this line and count the bases.
    else:
        new_line = genome_line
        new_line.replace(b"a", b"t")
        new_line.replace(b"t", b"a")
        new_line.replace(b"c", b"g")
        new_line.replace(b"g", b"c")
        count_a += new_line.count(b"a")
        count_t += new_line.count(b"t")
        count_c += new_line.count(b"c")
        count_g += new_line.count(b"g")
        count_n += new_line.count(b"n")
        comp.append(new_line)  # Append complementary line to comp list.

# Set header to last sequence, as I have used the ">"s as triggers.
comp[prev_fasta_header] = f">seq{seq_count} A:{count_a} T:{count_t} C:{count_c} G:{count_g} " \
                          f"N:{count_n}".encode("utf-8")

# Write entire output to file.
outfile = open(DESTINATION_PATH, "ab")
outfile.write(b"\n".join(comp))
outfile.close()
