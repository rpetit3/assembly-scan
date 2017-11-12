#! /usr/bin/env python3
"""Produce basic assembly stats for a given assembly."""


def gziplines(fname):
    """Use zcat to deliver lines from gzipped input."""
    from subprocess import Popen, PIPE
    f = Popen(['zcat', fname], stdout=PIPE)
    for line in f.stdout:
        yield line


def read_fasta(fasta):
    """Return a list of seqeunces from a given FASTA file."""
    seq = []
    records = []

    for line in fasta:
        line = line.rstrip()
        if line.startswith('>'):
            if len(seq):
                records.append(''.join(seq))
                seq = []
        else:
            seq.append(line)
    records.append(''.join(seq))

    return records


def contig_lengths(contigs):
    return {
        '100k': sum(i > 100000 for i in contigs),
        '10k': sum(i > 10000 for i in contigs),
        '1k': sum(i > 1000 for i in contigs),
        '1m': sum(i > 1000000 for i in contigs)
    }


def nucleotide_counts(contigs, total_bp):
    from collections import defaultdict
    c = defaultdict(int)
    for contig in contigs:
        non_acgtn = False
        for n in contig:
            n = n.lower()
            if n not in ['a', 'c', 'g', 't', 'n']:
                n = 'non_acgtn'
                non_acgtn = True
            c[n.lower()] += 1
        if non_acgtn:
            c['total_non_acgtn'] += 1

    c['non_acgtn'] = c['non_acgtn'] / total_bp if 'non_acgtn' in c else 0.00
    c['a'] = c['a'] / total_bp
    c['c'] = c['c'] / total_bp
    c['g'] = c['g'] / total_bp
    c['n'] = c['n'] / total_bp if 'n' in c else 0.00
    c['t'] = c['t'] / total_bp
    return c


def calculate_n50(contigs, genome_size, assembly_size):
    stats = {
        'n50': 0, 'ng50': 0, 'l50': 0, 'lg50': 0
    }
    total = 0
    total_contig = 0
    for contig in contigs:
        total += contig
        total_contig += 1
        if total >= genome_size:
            if not stats['ng50']:
                stats['ng50'] = contig
                stats['lg50'] = total_contig
        if total >= assembly_size:
            if not stats['n50']:
                stats['n50'] = contig
                stats['l50'] = total_contig

        if stats['n50'] and stats['ng50']:
            break

    return stats


def print_percent(val):
    return '{0:.2f}'.format(val * 100)


if __name__ == '__main__':
    import argparse as ap
    import json
    import numpy
    import os
    import sys

    parser = ap.ArgumentParser(
        prog='assembly-stats.py',
        conflict_handler='resolve',
        description=("Generate statistics for a given assembly.")
    )
    parser.add_argument('--assembly', metavar="ASSEMBLY", type=str,
                        help='FASTA file to read (Default STDIN)')
    parser.add_argument('--genome_size', metavar="INT", type=int,
                        help='Estimated genome size. (Default: 2814816)',
                        default=2814816)
    parser.add_argument('--output', metavar="STRING", type=str,
                        default='/dev/stdout',
                        help='File to write JSON output to (Default STDOUT).')

    args = parser.parse_args()

    fasta = None
    if args.assembly:
        if os.path.exists(args.assembly):
            assembly = args.assembly
            compressed = True if assembly.endswith('.gz') else False
            fh = gziplines(fasta) if compressed else open(fasta, 'r')
            fasta = read_fasta(fh)
    else:
        fasta = read_fasta(sys.stdin.readlines())

    # Generate Stats
    stats = {}

    lengths = sorted([len(seq) for seq in fasta], key=int, reverse=True)
    length_totals = contig_lengths(lengths)
    total_contig = len(fasta)
    total_bp = sum(lengths)
    counts = nucleotide_counts(fasta, total_bp)
    n50 = calculate_n50(lengths, args.genome_size//2, total_bp//2)
    np_array = numpy.array(lengths)

    stats = {
        "contig_non_acgtn": print_percent(counts['non_acgtn']),
        "contig_percent_a": print_percent(counts['a']),
        "contig_percent_c": print_percent(counts['c']),
        "contig_percent_g": print_percent(counts['g']),
        "contig_percent_n": print_percent(counts['n']),
        "contig_percent_t": print_percent(counts['t']),
        "contigs_greater_100k": length_totals['100k'],
        "contigs_greater_10k": length_totals['10k'],
        "contigs_greater_1k": length_totals['1k'],
        "contigs_greater_1m": length_totals['1m'],
        "l50_contig_count": n50['l50'],
        "lg50_contig_count": n50['lg50'],
        "max_contig_length": max(lengths),
        "mean_contig_length": int(numpy.mean(np_array)),
        "median_contig_length": int(numpy.median(np_array)),
        "min_contig_length": min(lengths),
        "n50_contig_length": n50['n50'],
        "ng50_contig_length": n50['ng50'],
        "num_contig_non_acgtn": counts['total_non_acgtn'],
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
    print(json.dumps(stats, indent=4, sort_keys=True))
