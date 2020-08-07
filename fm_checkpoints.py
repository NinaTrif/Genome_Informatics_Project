class Checkpoints(object):
    """ Class for managing checkpoints and querying ranks"""

    def __init__(self, bw, cp_distance=256):
        """ Creates checkpoints with a given distance for given BW(T) """
        tally = dict()
        self.checkpoints = dict()
        self.cp_distance = cp_distance

        for c in bw:
            if c not in tally and c != '$':
                tally[c] = 0
                self.checkpoints[c] = list()

        for i, c in enumerate(bw):
            if c != '$':
                tally[c] += 1
            if i % self.cp_distance == 0:
                for ch in tally.keys():
                    self.checkpoints[ch].append(tally[ch])

    def calculate_rank(self, bw, c, row):
        """ Return rank of the given character, where rank is number of occurrences up to and including given row """
        if row < 0:
            return 0

        res = None
        # already at checkpoint
        if row % self.cp_distance == 0:
            # already at checkpoint
            res = self.checkpoints[c][row // self.cp_distance] - 1

        # find nearest checkpoint first (can be either "up" or "down")
        cp_row = row // self.cp_distance
        num_c = 0
        tmp_row = row
        if (row % self.cp_distance > self.cp_distance // 2) and (cp_row + 1 < len(self.checkpoints[c])):
            # seek number of occurrences of character "up"
            cp_row += 1
            tmp_row += 1
            while tmp_row % self.cp_distance != 0:
                if bw[tmp_row] == c:
                    num_c += 1
                tmp_row += 1
            res = self.checkpoints[c][cp_row] - num_c
            if bw[cp_row * self.cp_distance] == c:
                res -= 1

        else:
            # seek number of occurrences of character "down"
            while tmp_row % self.cp_distance != 0:
                if bw[tmp_row] == c:
                    num_c += 1
                tmp_row -= 1
            res = self.checkpoints[c][cp_row] + num_c

        if res < 0:
            return 0
        return res
