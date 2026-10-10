import sys
from pathlib import Path
from Bio import SeqIO

# Reads whose FASTA read name (the header after ">") ends with this letter are
# reverse reads and get reverse-complemented. File names are never checked.
REVERSE_SUFFIX = "R"

# The input file must be named on the command line. There is no default file name,
# so the script only ever reads the file you give it, even if the folder holds other FASTA files.
if len(sys.argv) < 2:
    sys.exit("Usage: python rc_reads.py <input.fasta> [output.fasta]")

infile = Path(sys.argv[1])
if not infile.is_file():
    sys.exit(f"File not found: {infile}")

# Output file: the second argument if given, otherwise the input name plus "_rc"
# (my_reads.fasta -> my_reads_rc.fasta)
outfile = Path(sys.argv[2]) if len(sys.argv) > 2 else infile.with_name(infile.stem + "_rc.fasta")
if outfile.resolve() == infile.resolve():
    sys.exit("The output file must be different from the input file")

records = []
n_rc = 0
for rec in SeqIO.parse(infile, "fasta"):          # go through every sequence in the file
    # rec.id is the first word of the header: in ">34B_OTSU_Otr-56-1728R sample 3"
    # it is "34B_OTSU_Otr-56-1728R" and "sample 3" is ignored.
    # The name must END exactly in R: "...1728R-" would not match.
    if rec.id.endswith(REVERSE_SUFFIX):
        # flip the sequence; id=True and description=True keep the original header
        rec = rec.reverse_complement(id=True, description=True)
        n_rc += 1
    records.append(rec)                           # forward reads are kept unchanged

SeqIO.write(records, outfile, "fasta")            # write all reads to the new file
print(f"Wrote {len(records)} sequences to {outfile}, reverse-complemented {n_rc}")
