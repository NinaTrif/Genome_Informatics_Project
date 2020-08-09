import two_step_alignment as tsa
from Bio import SeqIO
import util
import global_variables as g_var
import fm_index as fmi


def main():
    util.parse_command_line_arguments()

    # process fasta file
    try:
        fasta_file = open(g_var.fasta_file_path)
        fasta_sequences = SeqIO.parse(fasta_file, 'fasta')
    except Exception as ex:
        raise Exception('Error processing fasta file.' + '\n' + str(ex))

    reference_id = None
    reference_seq = None
    i = 0
    for ref in fasta_sequences:
        if i == 0:
            reference_id = ref.id
            reference_seq = str(ref.seq)
            g_var.reference = fmi.FM_Index(reference_seq, cp_distance=128, sa_distance=16)
            break

    # process fastq file
    try:
        fastq_file = open(g_var.fastq_file_path)
        fastq_sequences = SeqIO.parse(fastq_file, 'fastq')
    except Exception as ex:
        raise Exception('Error processing fastq file.' + '\n' + str(ex))
    reads = dict()
    for read in fastq_sequences:
        reads[read.id] = str(read.seq)
    reads_to_alignments = dict()

    # process reads
    for read_id in reads.keys():
        read = reads[read_id]
        reads_to_alignments[read_id] = tsa.seed_and_extend(reference_seq, read, g_var.seed_length, g_var.margin)
        reversed_read = read[::-1]
        reads_to_alignments[read_id] += tsa.seed_and_extend(reference_seq, reversed_read, g_var.seed_length,
                                                            g_var.margin, is_reversed=True)

    n_mapped = 0
    n_reads = len(reads_to_alignments.keys())
    print(n_reads)
    for r in reads_to_alignments.keys():
        if len(reads_to_alignments[r]) > 0:
            print(len(reads_to_alignments[r]))
            n_mapped += 1
    print(n_mapped)


if __name__ == "__main__":
    main()
