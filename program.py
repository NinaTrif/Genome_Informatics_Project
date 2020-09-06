import two_step_alignment as tsa
from Bio import SeqIO
import util_multiple as util
import global_variables as g_var
import fm_index as fmi
from timeit import default_timer as timer
import visualisation as visual
import os
import sys

util.parse_command_line_arguments()

try:
    path = os.path.dirname(sys.argv[0]) + '/results'
    if not os.path.exists(path):
        os.mkdir(path)
except OSError:
    raise Exception("Creation of directory %s failed" % path)

try:
    res_file = open('results/results.txt', 'w')
except Exception as ex:
    raise Exception('Error opening results file.' + '\n' + str(ex))
res_file.write('ALIGNMENT SCORES DISTRIBUTION:\n')

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
    # fastq_file = open(g_var.fastq_file_path)
    fastq_sequences = SeqIO.index(g_var.fastq_file_path, 'fastq')
except Exception as ex:
    raise Exception('Error processing fastq file.' + '\n' + str(ex))
# reads = dict()
# for read in fastq_sequences:
#     reads[read.id] = str(read.seq)

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
        # for read_id in reads.keys():
        #     read = reads[read_id]
        #     reads_to_alignments[read_id] = tsa.seed_and_extend(reference_seq, read, i, j)
        #     reversed_read = read[::-1]
        #     reads_to_alignments[read_id] += tsa.seed_and_extend(reference_seq, reversed_read, i, j, is_reversed=True)

        avg_mapping = 0
        n_mapped = 0
        n_forward = 0
        n_reverse = 0

        # create alignment file for this seed/margin pair
        try:
            alignment_file = open('results/alignments_best_' + str(i) + '_' + str(j) + '.txt', 'w')
        except Exception as ex:
            raise Exception('Error opening alignment file.' + '\n' + str(ex))
        alignment_file.write('READ_ID\tREAD_SEQ\tPOS\tREF_SEQ\tSCORE\tEDIT_TRANSCRIPT\tFORWARD\n')

        # iterate over all reads
        for r in list(fastq_sequences.keys()):
            read = str(fastq_sequences[r].seq)
            reads_to_alignments[r] = tsa.seed_and_extend(reference_seq, read, i, j)
            reversed_read = list(read[::-1])
            for chr in range(len(reversed_read)):
                if reversed_read[chr] == 'G':
                    reversed_read[chr] = 'C'
                elif reversed_read[chr] == 'T':
                    reversed_read[chr] = 'A'
                elif reversed_read[chr] == 'A':
                    reversed_read[chr] = 'T'
                elif reversed_read[chr] == 'C':
                    reversed_read[chr] = 'G'
            reversed_read = ''.join([str(elem) for elem in reversed_read])
            tmp = tsa.seed_and_extend(reference_seq, reversed_read, i, j, is_reversed=True)
            reads_to_alignments[r] += tmp
            reads_to_alignments[r].sort(key=lambda read: read.alignment_score, reverse=True)
            if len(reads_to_alignments[r]) > 0:
                n_mapped += 1
                if reads_to_alignments[r][0].is_reversed is True:
                    n_reverse += 1
                else:
                    n_forward += 1
                s = reads_to_alignments[r][0].alignment_score
                if reads_to_alignments[r][0].is_valid is True:
                    avg_mapping += s
                    if s not in scores:
                        scores[s] = 1
                    else:
                        scores[s] += 1

                    # write best alignment score for current alignment
                    alignment_file.write(r + '\t' + str(fastq_sequences[r].seq) + '\t' + str(
                        reads_to_alignments[r][0].position) + '\t' + reads_to_alignments[r][0].ref_seq + '\t' + str(
                        reads_to_alignments[r][0].alignment_score) + '\t' + reads_to_alignments[r][0].edit_transcript + '\t' + str(
                        not reads_to_alignments[r][0].is_reversed) + '\n')

            # write all alignments for current read to file, sorted by descending alignment score
            # for alignment in reads_to_alignments[r]:
            #     alignment_file.write(r + '\t' + str(fastq_sequences[r].seq) + '\t' + str(
            #         alignment.position) + '\t' + alignment.ref_seq + '\t' + str(
            #         alignment.alignment_score) + '\t' + alignment.edit_transcript + '\t' + str(
            #         not alignment.is_reversed) + '\n')

        alignment_file.close()

        # calculate average mapping score
        # avg_scores[(i, j)] = avg_mapping / n_mapped
        avg_scores[j] += [(i, avg_mapping / n_mapped)]
        num_mapped[(i, j)] = n_mapped
        num_mapped_seed[i] = n_mapped

        # end time
        end_time = timer()
        exec_times[j] += [(i, int((end_time - start_time) / 60))]

        # plot independent plots
        visual.plot_scores_scatter(scores, i, j, n_mapped)
        res_file.write('SEED=' + str(i) + '/MARGIN=' + str(j) + '\n')
        res_file.write('# mapped reads: ' + str(n_mapped) + '\n')
        res_file.write('# forward: ' + str(n_forward) + '\n')
        res_file.write('# reverse: ' + str(n_reverse) + '\n')
        scores = sorted([(k, v) for k, v in scores.items()], key=lambda x: x[0], reverse=True)
        for score in scores:
            res_file.write(str(score[0]) + ': ' + str(score[1]) + '\n')
        res_file.write('\n\n')

# plot dependent plots
visual.plot_avg_scores(avg_scores)
visual.plot_exec_times(exec_times)
visual.plot_mapped(num_mapped_seed)

res_file.close()
