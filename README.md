[![GitHub release (latest by date)](https://img.shields.io/github/v/release/rpetit3/assembly-scan))](https://github.com/bactopia/rpetit3/assembly-scan)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/assembly-scan/badges/downloads.svg)](https://anaconda.org/bioconda/assembly-scan)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/rpetit3/assembly-scan)

_`assembly-scan` reads an assembly in FASTA format and outputs summary statistics
in TSV or JSON format_

# `assembly-scan`

I wanted a quick method to output simple summary statistics of an input assembly
in TSV or JSON format. There are alternatives including
[assemblathon-stats.pl](https://github.com/ucdavis-bioinformatics/assemblathon2-analysis)
and [assembly-stats](https://github.com/sanger-pathogens/assembly-stats), but
they didn't output what I wanted. Thus `assembly-scan` was born.

## Installation

### Bioconda

*assembly-scan* is availble on [BioConda](https://bioconda.github.io/recipes/assembly-scan/README.html).

```{bash}
conda create -n assembly-scan -c conda-forge -c bioconda assembly-scan
```

### From Source

While I will always recommend using the Bioconda installation, the only dependency
`assembly-scan` has is Python >=3.7. So, if you have that already you can use the
script directly.

```{bash}
git@github.com:rpetit3/assembly-scan.git
cd assembly-scan
python3 bin/assembly-scan YOUR_ASSEMBLY.fasta
```

From there you can decide to add it to your PATH or not. But, again, I recommend
just going the Bioconda route.

## Usage

`assembly-scan` requires an assembly, gzip compressed or uncompressed, as input.

### Usage

```{bash}
usage: assembly-scan [-h] [--json] [--transpose] [--prefix PREFIX] [--version] ASSEMBLY

Generate statistics for a given assembly.

positional arguments:
  ASSEMBLY         FASTA file to read (gzip or uncompressed)

options:
  -h, --help       show this help message and exit
  --json           Print output in a JSON format
  --transpose      Print output in a transposed tab-delimited format
  --prefix PREFIX  ID to use for output (Default: basename of assembly)
  --version        show program's version number and exit
```

## Example Usage

Many FASTA files are available in the _test_ directory. These include an uncompressed
complete phiX174 genome and a compressed _Staphylococcus aureus_ assembly. This script
reads the input and outputs summary statistics in JSON format to STDOUT.

### Uncompressed

By default `assembly-scan` outputs the results in tab-delimited format. But for example
purposes the `--transpose` option has been used. It is just easier to look at in the
README.

```{bash}
assembly-scan test/phiX174.fna --transpose
test/phiX174.fna        sample  phiX174.fna
test/phiX174.fna        total_contig    1
test/phiX174.fna        total_contig_length     5386
test/phiX174.fna        max_contig_length       5386
test/phiX174.fna        mean_contig_length      5386
test/phiX174.fna        median_contig_length    5386
test/phiX174.fna        min_contig_length       5386
test/phiX174.fna        n50_contig_length       5386
test/phiX174.fna        l50_contig_count        1
test/phiX174.fna        num_contig_non_acgtn    0
test/phiX174.fna        contig_percent_a        23.97
test/phiX174.fna        contig_percent_c        21.48
test/phiX174.fna        contig_percent_g        23.28
test/phiX174.fna        contig_percent_t        31.27
test/phiX174.fna        contig_percent_n        0.00
test/phiX174.fna        contig_non_acgtn        0.00
test/phiX174.fna        contigs_greater_1m      0
test/phiX174.fna        contigs_greater_100k    0
test/phiX174.fna        contigs_greater_10k     0
test/phiX174.fna        contigs_greater_1k      1
test/phiX174.fna        percent_contigs_greater_1m      0.00
test/phiX174.fna        percent_contigs_greater_100k    0.00
test/phiX174.fna        percent_contigs_greater_10k     0.00
test/phiX174.fna        percent_contigs_greater_1k      100.00
```

### gzip Compressed

`assembly-scan` includes a simple check (_.gz_ extension) for gzip compressed
assemblies. This example also demonstrates the `--json` option output.

```{bash}
assembly-scan test/saureus.fasta.gz --json
{
    "sample": "saureus.fasta.gz",
    "fasta": "test/saureus.fasta.gz",
    "total_contig": 139,
    "total_contig_length": 2761520,
    "max_contig_length": 269921,
    "mean_contig_length": 19867,
    "median_contig_length": 163,
    "min_contig_length": 56,
    "n50_contig_length": 86756,
    "l50_contig_count": 9,
    "num_contig_non_acgtn": 0,
    "contig_percent_a": "33.74",
    "contig_percent_c": "16.50",
    "contig_percent_g": "16.21",
    "contig_percent_t": "33.54",
    "contig_percent_n": "0.00",
    "contig_non_acgtn": "0.00",
    "contigs_greater_1m": 0,
    "contigs_greater_100k": 7,
    "contigs_greater_10k": 37,
    "contigs_greater_1k": 49,
    "percent_contigs_greater_1m": "0.00",
    "percent_contigs_greater_100k": "5.04",
    "percent_contigs_greater_10k": "26.62",
    "percent_contigs_greater_1k": "35.25"
}
```

## Output Columns

| Column                       | Description |
|------------------------------|--|
| sample                       | Either assembly file basename, or value of `--prefix` |
| fasta                        | Input assembly processed                              |
| total_contig                 | Total number of contigs in the assembly               |
| total_contig_length          | Sum of all contig lengths                             |
| max_contig_length            | Length of the longest contig                          |
| mean_contig_length           | Average length of all contigs                         |
| median_contig_length         | Median value of all contigs                           |
| min_contig_length            | Length of the smallest contig                         |
| n50_contig_length            | [N50](https://en.wikipedia.org/wiki/N50,_L50,_and_related_statistics) length of the contigs                    |
| l50_contig_count             | [L50](https://en.wikipedia.org/wiki/N50,_L50,_and_related_statistics) number of contigs make up half the total |
| num_contig_non_acgtn         | Number of contigs with non-A,T,G,C, or N characters   |
| contig_percent_a             | Percent of A nucleotides in contigs                   |
| contig_percent_c             | Percent of C nucleotides in contigs                   |
| contig_percent_g             | Percent of G nucleotides in contigs                   |
| contig_percent_t             | Percent of T nucleotides in contigs                   |
| contig_percent_n             | Percent of N nucleotides in contigs                   |
| contig_non_acgtn             | Percent of non-A,T,G,C, or N nucleotides in contigs   |
| contigs_greater_1m           | Number of contigs greater than 1,000,000 bp           |
| contigs_greater_100k         | Number of contigs greater than 100,000 bp             |
| contigs_greater_10k          | Number of contigs greater than 10,000 bp              |
| contigs_greater_1k           | Number of contigs greater than 1,000 bp               |
| percent_contigs_greater_1m   | Percent of contigs greater than 1,000,000 bp          |
| percent_contigs_greater_100k | Percent of contigs greater than 1,000,000 bp          |
| percent_contigs_greater_10k  | Percent of contigs greater than 1,000,000 bp          |
| percent_contigs_greater_1k   | Percent of contigs greater than 1,000,000 bp          |

# Naming

Originally this was named _assembly-stats_, but after a quick Google search (which I
didn't do, [again](https://github.com/rpetit3/fastq-scan#naming), I really should do
better!) I found another [_assembly-stats_](https://github.com/sanger-pathogens/assembly-stats)
from Sanger Pathogens. So I decided to rename it to `assembly-scan`, similar to my
[fastq-scan](https://github.com/rpetit3/fastq-scan) tool, since this process is similar
to the [_Scan_](https://tvtropes.org/pmwiki/pmwiki.php/Main/EnemyScan) ability found in
some video games/movies/tv etc... In otherwords, it 'scans' an assembly and provides the
user with otherwise hidden information about the assembly.
