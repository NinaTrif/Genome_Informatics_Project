import numpy


def scoring_matrix(a, b):
    """ Scoring Matrix: 1 - match, -3 - mismatch, -7 - gap """
    if a == b:
        return 1
    if a == '_' or b == '_':
        return -7
    return -3


def global_alignment(x, y, margin):
    D = numpy.zeros((len(x) + 1, len(y) + 1), dtype=int)

    for i in range(1, len(x) + 1):
        D[i, 0] = D[i - 1, 0] + scoring_matrix(x[i - 1], '_')
    for j in range(1, len(y) + 1):
        D[0, j] = D[0, j - 1] + scoring_matrix('_', y[j - 1])

    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            D[i, j] = max(D[i - 1, j] + scoring_matrix(x[i - 1], '_'),
                          D[i, j - 1] + scoring_matrix('_', y[j - 1]),
                          D[i - 1, j - 1] + scoring_matrix(x[i - 1], y[j - 1]))

    # function returns table and global alignment score
    # alignment score is in cell (n,m) of the matrix

    max_v = D[len(x), len(y)]
    m_ind = len(y)
    for k in range(len(y) - margin, len(y)):
        if D[len(x), k] >= max_v:
            max_v = D[len(x), k]
            m_ind = k

    return max_v, traceback(x, y, D, m_ind)[1]


def traceback(x, y, V, j):
    # initializing starting position cell(n,m)
    i = len(x)
    # j = len(y)

    # initializing strings we use to represent alignments in x, y, edit transcript and global alignment
    ax, ay, am, tr = '', '', '', ''

    # exit condition is when we reach cell (0,0)
    while i > 0 or j > 0:
        # calculating diagonal, horizontal and vertical scores for current cell
        d, v, h = -100, -100, -100

        if i > 0 and j > 0:
            delta = 1 if x[i - 1] == y[j - 1] else 0
            d = V[i - 1, j - 1] + scoring_matrix(x[i - 1], y[j - 1])  # diagonal movement
        if i > 0:
            v = V[i - 1, j] + scoring_matrix(x[i - 1], '_')  # vertical movement
        if j > 0:
            h = V[i, j - 1] + scoring_matrix('_', y[j - 1])  # horizontal movement

        # backtracing to next (previous) cell
        if d >= v and d >= h:
            ax += x[i - 1]
            ay += y[j - 1]
            if delta == 1:
                tr += 'M'
                am += '|'
            else:
                tr += 'R'
                am += ' '
            i -= 1
            j -= 1
        elif v >= h:
            ax += x[i - 1]
            ay += '_'
            tr += 'D'
            am += ' '
            i -= 1
        else:
            ay += y[j - 1]
            ax += '_'
            tr += 'I'
            am += ' '
            j -= 1

    alignment = '\n'.join([ax[::-1], am[::-1], ay[::-1]])
    return alignment, tr[::-1]
