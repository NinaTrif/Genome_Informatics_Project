import global_alignment as gl_align
import global_variables as gl_var
import alignment as al


def seed_and_extend(reference_sq, read, seed_length, margin, is_reversed=False):
    seed = read[:seed_length]
    positions = gl_var.reference.query(seed)
    alignments = list()
    for index in positions:
        alignment = align_read_at_position(reference_sq, read[seed_length:], index, seed_length, margin, is_reversed)
        if alignment is not None:
            alignments.append(alignment)
    # alignments.sort(key=lambda read: read.alignment_score, reverse=True)
    return alignments


def align_read_at_position(reference_sq, read, position, seed_length, margin, is_reversed):
    """ Return alignment of a read at given index (position), if exists """
    # assumes read has already been truncated
    alignment = None
    start = position + seed_length
    end = start + len(read) + margin
    if len(reference_sq) >= end:
        # score, transcript = gl_align.global_alignment(reference_sq[start:end], read)
        score, transcript, true_margin = gl_align.global_alignment(read, reference_sq[start:end], margin)
        alignment = al.Alignment(position, reference_sq[position:end-margin+true_margin], score, transcript, is_reversed)
    else:
        # alignment = al.Alignment(position, -sys.maxsize - 1, '', is_reversed, is_valid=False)
        pass
    return alignment
