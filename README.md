# sanger-reverse-complement

Reverse-complements the reverse reads in a combined Sanger FASTA file, so every read runs in the same direction as the forward reads.

You name the input file when you run the script. It reads only that file, so other FASTA files in the same folder are ignored, and your file can have any name. Forward reads are copied unchanged, headers are not changed, and the original file is not modified.

## Install

```
python -m pip install -r requirements.txt
```

## Run

Open PowerShell in the folder that holds your file and give the file name after the script name:

```
python rc_reads.py my_reads.fasta
```

This writes `my_reads_rc.fasta` in the same folder. The output name is the input name plus `_rc`.

To choose the output name yourself, add it as a second name:

```
python rc_reads.py my_reads.fasta flipped_reads.fasta
```

If the file is in another folder, give the path:

```
python rc_reads.py C:\data\sanger\my_reads.fasta
```

If the name or path has spaces, put it in quotes:

```
python rc_reads.py "my reads.fasta"
```

If you run the script without a file name, it stops and prints how to use it. It also stops if the file is not found, or if the output name is the same as the input.

The terminal prints how many sequences were written and how many were reverse-complemented. The second number should equal your count of reverse reads. To check it in PowerShell:

```
(Select-String -Path my_reads.fasta -Pattern "^>.*R$").Count
```

## How reverse reads are recognised

The script checks the **FASTA read name**, which is the header line after the `>`. It never looks at file names.

```
>34B_OTSU_Otr-56-1728R     name ends in R, so the read is flipped
ACGTTGCA...
>38B_OTSU_Otr-56-573F      name ends in F, so the read is left alone
ACGTTGCA...
```

Details that matter:

- Only the first word of the header is checked. In `>34B_OTSU_Otr-56-1728R sample 3`, the script sees `34B_OTSU_Otr-56-1728R` and ignores `sample 3`.
- The name must end exactly in `R`. A header such as `>34B_OTSU_Otr-56-1728R-` ends in `-`, so that read is not flipped. Headers from some assemblers and editors carry extra characters like this, so check yours.
- A forward read whose name happens to end in `R` would be flipped by mistake. Check your naming first.
- The input is one FASTA file holding all the reads you want to process.

## Try it

```
python rc_reads.py example_data/combined.fasta
```

In the example, the two `R` reads hold the same sequence as their `F` partners, so after the run they appear as the reverse complement in `example_data/combined_rc.fasta`.

## Settings

`REVERSE_SUFFIX` at the top of `rc_reads.py` is the letter that marks a reverse read. Change it if your reads use a different tag.

## Notes

- Do not run the output through the script a second time. That would flip the reverse reads back.

## Licence

MIT
