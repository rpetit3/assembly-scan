[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square)](http://bioconda.github.io/recipes/assembly-scan/README.html) 
[![Docker Repository on Quay.io](https://quay.io/repository/biocontainers/assembly-scan/status "Docker Repository on Quay.io")](https://quay.io/repository/biocontainers/assembly-scan)


*assembly-scan* reads an assembly in FASTA format and outputs summary statistics in JSON format.

# assembly-scan
I wanted a quick method to output simple summary statistics of an input assembly in JSON format. There are alternatives including [assemblathon-stats.pl](https://github.com/ucdavis-bioinformatics/assemblathon2-analysis) and [assembly-stats](https://github.com/sanger-pathogens/assembly-stats), but they didn't ouput JSON which I wanted. There are examples below on which stats are output below.

# Installation
### Bioconda
*assembly-scan* is availble on [BioConda](https://bioconda.github.io/recipes/assembly-scan/README.html).
```
conda install assembly-scan
```

### From Source
```
git@github.com:rpetit3/assembly-scan.git
cd assembly-scan
python3 assembly-scan.py YOUR_ASSEMBLY.fasta
```
Nothing much to it, just a simple Python3 script to calculate all the stats. You can then move this to your local bin.

# Requirements
* Python >= 3.4 

I've used the [*statistics*](https://docs.python.org/3/library/statistics.html) package from the Python3 Standard Library to limit the number of dependencies. Due to this, this script requires at least Python 3.4 or newer.

# Usage
*assembly-scan* requires an assembly, gzip compressed or uncompressed, as input. 

### Usage
```
python3 assembly-scan.py
usage: assembly-scan.py [-h] [--version] ASSEMBLY

Generate statistics for a given assembly.

positional arguments:
  ASSEMBLY    FASTA file to read (gzip or uncompressed)

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

#### *--version* Version
```
assembly-scan.py --version
assembly-scan.py 0.2
```

### Example Usage
Two fasta files have been included in the *example-data* directory. These include an uncompressed complete phiX174 genome and a compressed *Staphylococcus aureus* assembly. This script reads the input and outputs summary statistics in JSON format to STDOUT.

### Example Execution and Output
#### Uncompressed
```
python3 assembly-scan.py example-data/phiX174.fna
{
    "contig_non_acgtn": "0.00",
    "contig_percent_a": "23.97",
    "contig_percent_c": "21.48",
    "contig_percent_g": "23.28",
    "contig_percent_n": "0.00",
    "contig_percent_t": "31.27",
    "contigs_greater_100k": 0,
    "contigs_greater_10k": 0,
    "contigs_greater_1k": 1,
    "contigs_greater_1m": 0,
    "l50_contig_count": 1,
    "max_contig_length": 5386,
    "mean_contig_length": 5386,
    "median_contig_length": 5386,
    "min_contig_length": 5386,
    "n50_contig_length": 5386,
    "num_contig_non_acgtn": 0,
    "percent_contigs_greater_100k": "0.00",
    "percent_contigs_greater_10k": "0.00",
    "percent_contigs_greater_1k": "100.00",
    "percent_contigs_greater_1m": "0.00",
    "total_contig": 1,
    "total_contig_length": 5386
}
```

#### gzip Compressed
This script includes a simple check (*.gz* extension) for gzip compressed assemblies.
```
python3 assembly-scan.py example-data/saureus.fasta.gz
{
    "contig_non_acgtn": "0.00",
    "contig_percent_a": "33.74",
    "contig_percent_c": "16.50",
    "contig_percent_g": "16.21",
    "contig_percent_n": "0.00",
    "contig_percent_t": "33.54",
    "contigs_greater_100k": 7,
    "contigs_greater_10k": 37,
    "contigs_greater_1k": 49,
    "contigs_greater_1m": 0,
    "l50_contig_count": 9,
    "max_contig_length": 269921,
    "mean_contig_length": 19867,
    "median_contig_length": 163,
    "min_contig_length": 56,
    "n50_contig_length": 86756,
    "num_contig_non_acgtn": 0,
    "percent_contigs_greater_100k": "5.04",
    "percent_contigs_greater_10k": "26.62",
    "percent_contigs_greater_1k": "35.25",
    "percent_contigs_greater_1m": "0.00",
    "total_contig": 139,
    "total_contig_length": 2761520
}
```

# Naming
Originally this was named *assembly-stats*, but after a quick Google search (which I didn't do, [again](https://github.com/rpetit3/fastq-scan#naming), I really should do better!) I found another [*assembly-stats*](https://github.com/sanger-pathogens/assembly-stats) from Sanger Pathogens. So I decided to rename it to *assembly-scan*, similar to my [fastq-scan](https://github.com/rpetit3/fastq-scan) tool, since this process is similar to the [*Scan*](
https://tvtropes.org/pmwiki/pmwiki.php/Main/EnemyScan) ability found in some video games/movies/tv etc... In otherwords, it 'scans' an assembly and provides the user with otherwise hidden information about the assembly.
