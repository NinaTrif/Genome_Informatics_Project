from collections import defaultdict, Counter


def suffix_array(s):
    """ Given T return suffix array SA(T).  We use Python's sorted
        function here for simplicity, but we can do better. """
    # Assumes $ has already been appended to the input string t
    satups = sorted([(s[i:], i) for i in range(len(s))])
    # Extract and return just the offsets
    return map(lambda x: x[1], satups)


def suffix_array_ManberMyers(s):
    result = []

    def sort_bucket(s, bucket, order=1):
        d = defaultdict(list)
        for i in bucket:
            key = s[i:i+order]
            d[key].append(i)
        for k, v in sorted(d.items()):
            if len(v) > 1:
                sort_bucket(s, v, order*2)
            else:
                result.append(v[0])
        return result

    return sort_bucket(s, (i for i in range(len(s))))


def bwt_via_sa(t):
    """ Given T, returns BWT(T) by way of the suffix array. """
    bw = []
    for si in suffix_array_ManberMyers(t):
        if si == 0:
            bw.append('$')
        else:
            bw.append(t[si-1])
    return ''.join(bw)  # return string-ized version of list bw
