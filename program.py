import two_step_alignment as tsa
from Bio import SeqIO
import util_multiple as util
import global_variables as g_var
import fm_index as fmi
from timeit import default_timer as timer
import visualisation as visual

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

exec_times = dict()  # key = margin, value = list of tuples(seed_length, exec_time)
avg_scores = dict()
num_mapped = dict()
num_mapped_seed = dict()

for i in g_var.seed_length:
    for j in g_var.margin:
        if j not in exec_times:
            exec_times[j] = list()
            avg_scores[j] = list()
        reads_to_alignments = dict()
        scores = dict()
        # initialize time, calculating just the alignment time, as everything else is the same for all pairs
        start_time = timer()

        # process reads
        for read_id in reads.keys():
            read = reads[read_id]
            reads_to_alignments[read_id] = tsa.seed_and_extend(reference_seq, read, i, j)
            reversed_read = read[::-1]
            reads_to_alignments[read_id] += tsa.seed_and_extend(reference_seq, reversed_read, i, j, is_reversed=True)

        # calculate average mapping score
        avg_mapping = 0
        n_mapped = 0
        for rd in reads_to_alignments.keys():
            if len(reads_to_alignments[rd]) > 0:
                n_mapped += 1
                s = reads_to_alignments[rd][0].alignment_score
                if reads_to_alignments[rd][0].is_valid is True:
                    avg_mapping += s
                    if s not in scores:
                        scores[s] = 1
                    else:
                        scores[s] += 1
        # avg_scores[(i, j)] = avg_mapping / n_mapped
        avg_scores[j] += [(i, avg_mapping / n_mapped)]
        num_mapped[(i, j)] = n_mapped
        num_mapped_seed[i] = n_mapped

        # end time
        end_time = timer()
        exec_times[j] += [(i, int(end_time - start_time))]

        # plot independent plots
        visual.plot_scores_scatter(scores, i, j, n_mapped)

# plot dependent plots
visual.plot_avg_scores(avg_scores)
visual.plot_exec_times(exec_times)
visual.plot_mapped(num_mapped_seed)
