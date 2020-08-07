import fm_checkpoints as cp
import burrows_wheeler_suffix_array as bw_sa
import burrows_wheeler_transform as bwt


class FM_Index():
    """ Class that represents an FM Index """

    def __init__(self, t, cp_distance=256, sa_distance=32):
        if t[-1] != '$':
            t += '$'

        sa = bw_sa.suffix_array(t)
        self.bwt = bw_sa.bwt_via_sa(t)
        self.sample_sa = self.downsample_suffix_array(sa, sa_distance)
        self.cp_distance = cp_distance
        self.checkpoints = cp.Checkpoints(self.bwt, self.cp_distance)
        self.first = bwt.first_col(bwt.rank_bwt(self.bwt)[1])

    @staticmethod
    def downsample_suffix_array(sa, sa_distance):
        """ Take every sa_distance'th entry of Suffix Array sa """
        sample_sa = dict()

        for i, ind in enumerate(sa):
            if ind % sa_distance == 0:
                sample_sa[i] = ind
        return sample_sa

    def query(self, p):
        """ Return positions where P is found in T """
        rng = self.range(p)
        if rng is None or rng[1] < rng[0]:
            return -1
        lower, upper = rng[0], rng[1]
        indices = list()

        for i in range(lower, upper):
            row = i
            step_cnt = 0
            while row not in self.sample_sa:
                step_cnt += 1
                row = self.first[self.bwt[row]][0] + self.checkpoints.calculate_rank(self.bwt, self.bwt[row], row - 1)
            indices.append(self.sample_sa[row] + step_cnt)
        return indices

    def range(self, p):
        """ Return range of rows of BWM(T) with P as prefix, None if P doesn't exist as prefix """
        lower = 0
        upper = len(self.bwt) - 1

        for i in range(len(p) - 1, -1, -1):
            if p[i] not in self.first:
                return None
            else:
                lower = self.first[p[i]][0] + self.checkpoints.calculate_rank(self.bwt, p[i], lower - 1)
                upper = self.first[p[i]][0] + self.checkpoints.calculate_rank(self.bwt, p[i], upper) - 1
                if upper < lower:
                    break
        return lower, upper + 1

    # def is_present(self, p):
    #     rng = self.range(p)
    #     if rng is None or rng[1] <= rng[0]:
    #         return False
    #     else:
    #         return True
