import sys
import global_variables as g_var
import argparse


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments: fasta file path, fastq file path, '
                                                 'seed length and margin.')

    # positional arguments
    # parser.add_argument('fastq', action='store', help='Fastq file path')
    # parser.add_argument('fasta', action='store', help='Fasta file path')
    # parser.add_argument('seed', action='store', type=int, help='Seed length')
    # parser.add_argument('margin', action='store', type=int, default=0, help='Margin value')

    if len(sys.argv) < 3:
        raise Exception('Not enough arguments supplied.')

    parser.add_argument('-q', '--fastq', action='store', dest='fastq', help='Fastq file path')
    parser.add_argument('-a', '--fasta', action='store', dest='fasta', help='Fasta file path')
    parser.add_argument('-s', '--seed', nargs='+', action='store', type=int, dest='seed', help='Seed length',
                        default=[10])
    parser.add_argument('-m', '--margin', nargs='+', action='store', type=int, dest='margin', help='Margin value',
                        default=[0])
    args = parser.parse_args(sys.argv[1:])

    g_var.fastq_file_path = args.fastq
    g_var.fasta_file_path = args.fasta
    g_var.seed_length = args.seed
    g_var.margin = args.margin

    for s in g_var.seed_length:
        if s <= 0:
            raise Exception('Seed length <= 0.')
    g_var.seed_length.sort()
    for m in g_var.margin:
        if m < 0 or m > 10:
            raise Exception('Margin not in range 0-10.')
    g_var.margin.sort()
