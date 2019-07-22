#! /usr/bin/env python3
"""Produce basic assembly stats for a given assembly."""
VERSION = "0.3.0"

def open_fasta(filename):
    """Return filehandle depending on file extension."""
    import gzip
    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')
    return open(filename, 'r')


def default_stats():
    """Return an default dict for assembly stats."""
    keys = [
        "contig_percent_a", "contig_percent_c", "contig_percent_g",
        "contig_percent_t", "contig_percent_n", "contig_non_acgtn",
        "contigs_greater_100k", "contigs_greater_10k", "contigs_greater_1k",
        "contigs_greater_1m", "l50_contig_count", "max_contig_length",
        "mean_contig_length", "median_contig_length", "min_contig_length",
        "n50_contig_length", "num_contig_non_acgtn", "percent_contigs_greater_100k",
        "percent_contigs_greater_10k", "percent_contigs_greater_1k",
        "percent_contigs_greater_1m", "total_contig", "total_contig_length"
    ]
    return dict(zip(keys, [0] * len(keys)))


def read_fasta(input_fasta):
    """Return a list of seqeunces from a given FASTA file."""
    try:
        seq = []
        records = []
        is_fasta = False
        with open_fasta(input_fasta) as fasta_fh:
            for line in fasta_fh:
                line = line.rstrip()
                if line.startswith('>'):
                    is_fasta = True
                    if seq:
                        records.append(''.join(seq))
                        seq = []
                elif is_fasta:
                    seq.append(line)
            if is_fasta:
                records.append(''.join(seq))
        return records
    except IOError as error:
        raise RuntimeError("Error opening assembly.") from error


def contig_lengths(contigs):
    """Return number of contigs greater than 'X'."""
    return {
        '1k': sum(i > 1000 for i in contigs),
        '10k': sum(i > 10000 for i in contigs),
        '100k': sum(i > 100000 for i in contigs),
        '1m': sum(i > 1000000 for i in contigs)
    }


def nucleotide_usage(contigs, total_basepairs):
    """Calculate the overall nucleotide usage."""
    from collections import defaultdict
    counts = defaultdict(int)
    for contig in contigs:
        non_acgtn = False
        for nucleotide in contig:
            nucleotide = nucleotide.lower()
            if nucleotide not in ['a', 'c', 'g', 't', 'n']:
                nucleotide = 'non_acgtn'
                non_acgtn = True
            counts[nucleotide] += 1
        if non_acgtn:
            counts['total_non_acgtn'] += 1

    if 'non_acgtn' in counts:
        counts['non_acgtn'] = counts['non_acgtn'] / total_basepairs
    else:
        counts['non_acgtn'] = 0.00
    counts['a'] = counts['a'] / total_basepairs
    counts['c'] = counts['c'] / total_basepairs
    counts['g'] = counts['g'] / total_basepairs
    counts['n'] = counts['n'] / total_basepairs if 'n' in counts else 0.00
    counts['t'] = counts['t'] / total_basepairs
    return counts


def calculate_n50(contigs, assembly_size):
    """Calculate the n50 of the assembly."""
    n50_stats = {'n50': 0, 'l50': 0}
    total_length = 0
    total_contigs = 0
    for length in contigs:
        total_length += length
        total_contigs += 1
        if total_length >= assembly_size//2:
            n50_stats['n50'] = length
            n50_stats['l50'] = total_contigs
            break

    return n50_stats


def print_percent(val):
    """Return a fraction as a percent value."""
    return '{0:.2f}'.format(val * 100)


if __name__ == '__main__':
    import argparse as ap
    import json
    import sys
    from statistics import mean, median

    parser = ap.ArgumentParser(
        prog='assembly-summary.py',
        conflict_handler='resolve',
        description=("Generate statistics for a given assembly.")
    )
    parser.add_argument('assembly', metavar="ASSEMBLY", type=str,
                        help='FASTA file to read (gzip or uncompressed)')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(VERSION))
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    args = parser.parse_args()

    # Read FASTA
    fasta = list(filter(None, read_fasta(args.assembly)))
    stats = default_stats()

    if fasta:
        # Generate Stats
        lengths = sorted([len(seq) for seq in fasta], key=int, reverse=True)
        length_totals = contig_lengths(lengths)
        total_contig = len(fasta)
        total_bp = sum(lengths)
        usage = nucleotide_usage(fasta, total_bp)
        n50 = calculate_n50(lengths, total_bp)

        stats = {
            "contig_percent_a": print_percent(usage['a']),
            "contig_percent_c": print_percent(usage['c']),
            "contig_percent_g": print_percent(usage['g']),
            "contig_percent_t": print_percent(usage['t']),
            "contig_percent_n": print_percent(usage['n']),
            "contig_non_acgtn": print_percent(usage['non_acgtn']),
            "contigs_greater_100k": length_totals['100k'],
            "contigs_greater_10k": length_totals['10k'],
            "contigs_greater_1k": length_totals['1k'],
            "contigs_greater_1m": length_totals['1m'],
            "l50_contig_count": n50['l50'],
            "max_contig_length": max(lengths),
            "mean_contig_length": int(mean(lengths)),
            "median_contig_length": int(median(lengths)),
            "min_contig_length": min(lengths),
            "n50_contig_length": n50['n50'],
            "num_contig_non_acgtn": usage['total_non_acgtn'],
            "percent_contigs_greater_100k": print_percent(
                length_totals['100k'] / total_contig
            ),
            "percent_contigs_greater_10k": print_percent(
                length_totals['10k'] / total_contig
            ),
            "percent_contigs_greater_1k": print_percent(
                length_totals['1k'] / total_contig
            ),
            "percent_contigs_greater_1m": print_percent(
                length_totals['1m'] / total_contig
            ),
            "total_contig": total_contig,
            "total_contig_length": total_bp
        }
    else:
        stats["comment"] = "Invalid format, or empty FASTA. Please verify."
    print(json.dumps(stats, indent=4, sort_keys=True))
