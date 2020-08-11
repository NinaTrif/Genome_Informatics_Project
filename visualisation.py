import matplotlib.pyplot as plt
import numpy as np
import global_variables as g_var


def plot_scores_scatter(scores, seed, margin, n_mapped):
    data = {"x": [], "y": []}
    for k, v in scores.items():
        data["x"].append(k)
        data["y"].append(v / n_mapped)

    plt.title('Scores_' + str(seed) + '_' + str(margin))
    plt.xlabel('n')
    plt.ylabel('percentage')
    plt.scatter(data["x"], data["y"], marker='o')
    plt.savefig('Scores_' + str(seed) + '_' + str(margin), bbox_inches='tight')
    plt.close()
    pass


def plot_avg_scores(avg_scores):
    # res = sorted([(k, v) for k, v in exec_times.items()], key=lambda x: x[1][0], reverse=True)
    n = len(g_var.seed_length)
    x = np.arange(n)
    width = 0.8 / n
    fix, ax = plt.subplots()
    for i, m in enumerate(g_var.margin):
        # mapping_scores = res[m][1]
        mapping_scores = [s[1] for s in avg_scores[m]]
        bars = ax.bar(x + i * width, mapping_scores, width, label='margin=' + str(m))
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 1, str(yval), ha='center', va='bottom')
    ax.set_xticks(x, g_var.seed_length)
    plt.xticks(x, g_var.seed_length)
    ax.legend()

    plt.title('Average scores')
    plt.xlabel('seed length')
    plt.ylabel('average score')
    plt.savefig('avg_scores.png', bbox_inches='tight')
    plt.close()


def plot_exec_times(exec_times):
    # res = sorted([(k, v) for k, v in exec_times.items()], key=lambda x: x[1][0], reverse=True)
    n = len(g_var.seed_length)
    x = np.arange(n)
    width = 0.8 / n
    fix, ax = plt.subplots()
    for i, m in enumerate(g_var.margin):
        # durations = res[m][1]
        durations = [s[1] for s in exec_times[m]]
        bars = ax.bar(x + i * width, durations, width, label='margin=' + str(m))
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 1, str(yval), ha='center', va='bottom')
    ax.set_xticks(x, g_var.seed_length)
    plt.xticks(x, g_var.seed_length)
    ax.legend()

    plt.title('Execution times')
    plt.xlabel('seed length')
    plt.ylabel('duration')
    plt.savefig('exec_times.png', bbox_inches='tight')
    plt.close()


def plot_mapped(num_mapped_seed):
    res = sorted([(k, v) for k, v in num_mapped_seed.items()], key=lambda x: x[1], reverse=True)
    values = [i[1] for i in res]
    seeds = [str(i[0]) for i in res]
    bars = plt.bar(range(1, len(num_mapped_seed.keys()) + 1), values, align='center')
    plt.xticks(range(1, len(num_mapped_seed.keys()) + 1), seeds)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 1, str(yval), ha='center', va='bottom')

    plt.title('# mapped reads for different seed lengths')
    plt.xlabel('seed length')
    plt.ylabel('number of reads')
    plt.savefig('num_mapped.png', bbox_inches='tight')
    plt.close()
