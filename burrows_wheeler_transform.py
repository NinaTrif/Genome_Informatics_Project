def rotations(s):
    """ Return list of all rotations of input string s """
    # Assumes $ has already been appended to the input string t
    tmp = s * 2
    return [tmp[i:i + len(s)] for i in range(0, len(s))]


def bwm(t):
    """ Return lexicographically sorted list of t’s rotations """
    return sorted(rotations(t))


def bwt_via_bwm(t):
    """ Given T, returns BWT(T) by way of the BWM """
    return ''.join(map(lambda x: x[-1], bwm(t)))


def rank_bwt(bw):
    """ Given BWT string bw, return parallel list of B-ranks.  Also
        returns freq: map from character to # times it appears. """
    freq = dict()
    ranks = []
    for c in bw:
        if c not in freq:
            freq[c] = 0
        ranks.append(freq[c])
        freq[c] += 1
    return ranks, freq


def first_col(freq):
    """ Return map from character to the range of rows prefixed by
        the character. """
    first = {}
    start_row = 0
    for c, count in sorted(freq.items()):
        first[c] = (start_row, start_row + count)
        start_row += count
    return first


def reverse_bwt(bw):
    """ Make T from BWT(T) """
    ranks, freq = rank_bwt(bw)
    first = first_col(freq)
    rowi = 0 # start in first row
    t = '$' # start with rightmost character
    while bw[rowi] != '$':
        c = bw[rowi]
        t = c + t # prepend to answer
        # jump to row that starts with c of same rank
        rowi = first[c][0] + ranks[rowi]
    return t
