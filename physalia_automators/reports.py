"""Reports generator for Physalia Automators experiment.

Example:
        ``$ python physalia_automators/reports.py``
"""

# pylint: disable=no-value-for-parameter
# pylint: disable=missing-docstring

import sys
import os
import time
import csv
import click
import bisect
from collections import defaultdict
from tabulate import tabulate
from operator import itemgetter
from collections import OrderedDict

import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
import matplotlib.pyplot as plt
from physalia.models import Measurement
from physalia.analytics import pairwise_welchs_ttest
from statsmodels.graphics.boxplots import violinplot as stats_violinplot
import tabulate as T

from physalia_automators.constants import loop_count

DARK_GREEN = "#009933"
DARK_DARK_GREEN = "#004d00"
LIGHT_GREEN = "#80ff80"

@click.command()
@click.option('-i','--results_input', default="results.csv", type=click.Path(dir_okay=False))
@click.option('-o','--results_output', default="results", type=click.Path())
def tool(results_input, results_output):

    with open(results_input, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = []
        for row in csv_reader:
            # row[6] = float(row[6])*1000 # convert to mJ
            data.append(Measurement(*row[:7]))
    if not os.path.isdir(results_output):
        os.makedirs(results_output)

    # calculate idle cost
    IDLE_COST_CSV = "./experiments_part_2/results_idle_time.csv"
    with open(IDLE_COST_CSV, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file)
        idle_cost_data = []
        idle_cost_total_data = []
        for row in list(csv_reader)[1:]:
            idle_cost_total_data.append(float(row[6]))
            idle_cost_data.append(float(row[6])/float(row[5])) #energy/delta_time
    global IDLE_COST
    IDLE_COST = np.mean(idle_cost_data)
    click.secho('Idle cost: {}'.format(IDLE_COST))
    click.secho('Idle coconsumption for 120 seconds: {}'.format(np.mean(idle_cost_total_data)))

    use_case_categories = [
        "tap",
        "long_tap",
        "dragndrop",
        "swipe",
        "pinch_and_spread",
        "back_button",
        "input_text",
        "find_by_id",
        "find_by_description",
        "find_by_content",
    ]
    
    # # collect human experiments data
    #
    # with open(results_input, 'rt') as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #     human_data = []
    #     for row in csv_reader:
    #         # row[6] = float(row[6])*1000 # convert to mJ
    #         data.append(Measurement(*row))
    
    
    
    summary_overheads = {}
    scores = defaultdict(lambda: 0)
    for use_case_category in use_case_categories:
        click.secho("----------------------------------------", fg="blue")
        click.secho("         {}".format(use_case_category), fg="blue")
        click.secho("----------------------------------------", fg="blue")
        use_case_data = list(Measurement.get_entries_with_name_like("-"+use_case_category, data))
        unique_use_cases = list(Measurement.get_unique_use_cases(use_case_data))
        number_of_frameworks = len(unique_use_cases)
        names_dict = {
            name: name.replace("-"+use_case_category, "") for name in unique_use_cases
        }
        groups = [
            list(Measurement.get_entries_with_name(use_case, use_case_data))
            for use_case in unique_use_cases
        ]
        names = [
            name.replace("-"+use_case_category, "") for name in unique_use_cases
        ]
        def custom_sort_key(a):
            name,_ = a
            if name == "Human":
                return 0
            return name
        names, groups = zip(*sorted(zip(names, groups), key=custom_sort_key))
        title = use_case_category.title().replace('_'," ")
        violinplot(
            *groups,
            save_fig=results_output+"/"+use_case_category+".pdf",
            names_dict=names_dict,
            millijoules=False
        )
        n_loop_iterations = _get_interactions_count(use_case_category)
        # Descriptive statistics
        with open(results_output+"/table_description_"+use_case_category+".tex", "w") as file:
            table = describe(*groups, names=names,
                             loop_count=n_loop_iterations,
                             ranking=True, out=file,
                             table_fmt="latex", float_fmt='.2f', mili_joules=False)
        # summary table
        if use_case_category not in ["find_by_id",
                                     "find_by_description",
                                     "find_by_content"]:

            summary_overheads[use_case_category] = dict(zip(names, map(lambda row: row['Overhead'], table)))
        # Update Ranking
        for name, row in zip(names, table):
            scores[name] += (number_of_frameworks - row["Rank"])/float(number_of_frameworks)
        # Welchs ttest
        with open(results_output+"/table_welchsttest_"+use_case_category+".tex", "w") as file:
            pairwise_welchs_ttest(*groups, names=names, out=file, table_fmt='latex')

    frameworks=[
        "AndroidViewClient",
        "Appium",
        "Calabash",
        "Espresso",
        "Monkeyrunner",
        "PythonUiAutomator",
        "Robotium",
        "UiAutomator",
    ]

    with open(results_output+"/overheads_summary.tex", "w") as file:
        old_escape_rules = T.LATEX_ESCAPE_RULES
        T.LATEX_ESCAPE_RULES = {}
        file.write((T.tabulate(
            {
                use_case.title().replace('_'," "): [row.get(framework, 'n.a.') for framework in frameworks]
                for use_case, row in summary_overheads.items()
            },
            headers="keys", showindex=frameworks,
            tablefmt="latex",
        )))
        T.LATEX_ESCAPE_RULES = old_escape_rules


    # Ranking
    click.secho("\nRanking".format(use_case_category), fg="blue")
    sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
    with open(results_output+"/table_ranking.tex", "w") as file:
        file.write(
            tabulate(sorted_scores, headers=["Framework", "Score"], tablefmt="latex",
            floatfmt=".4f")
        )


    framework_results_dir = results_output+"/frameworks/"
    if not os.path.isdir(framework_results_dir):
        os.makedirs(framework_results_dir)

    for framework in frameworks:
        means = []
        for interaction in use_case_categories:
            use_case = "{}-{}".format(framework, interaction)
            use_case_data = np.array(list(Measurement.get_entries_with_name(use_case, data)), dtype='float')
            if len(use_case_data):
                n_loop_iterations = _get_interactions_count(interaction)
                mean = np.mean(use_case_data)/n_loop_iterations*1000
            else:
                mean = 0
            bisect.insort(
                means,
                (interaction, mean)
            )
        # means = means[::-1]
        figure = plt.figure()
        figure.suptitle(framework)
        X = range(len(means))
        names, Y = zip(*means)
        plt.bar(X, Y)
        axes = figure.gca()
        axes.set_xticks(X)
        axes.set_xticklabels([name.replace("_", " ").title() for name in names], rotation = 'vertical')
        axes.set_ylabel("Energy Consumption (J)")

        figure.subplots_adjust(bottom=0.31)

        bar_labels = [y==0 and "n.a." or format(y, ".2f") for y in Y]
        for x,y,label in zip(X, Y, bar_labels):
            plt.text(x, y, label, ha='center', va= 'bottom')
        figure.tight_layout()
        figure.savefig(results_output+"/frameworks/"+framework)
        plt.close()

    # overall plot
    fig, ax = plt.subplots(figsize=(6.4, 11))
    for index, framework in enumerate(frameworks):
        means = []
        for interaction in use_case_categories[::-1]:
            use_case = "{}-{}".format(framework, interaction)
            use_case_data = np.array(list(Measurement.get_entries_with_name(use_case, data)), dtype='float')
            if len(use_case_data):
                n_loop_iterations = _get_interactions_count(interaction)
                mean = np.mean(use_case_data)/n_loop_iterations
            else:
                mean = 0
            means.append(mean)
        means
        width=0.105
        plt.barh(
            np.arange(len(use_case_categories))-(index+0.5-(len(frameworks))/2)*width,
            means,
            label=framework, height=width
        )
        # plt.scatter(range(len(frameworks)), means, marker='o', linewidth='1')
    ax.set_yticklabels([name.replace('_', ' ').title() for name in use_case_categories[::-1]])
    ax.set_yticks(range(len(use_case_categories)))
    ax.set_ylim(-0.5, 9.5)
    ax.set_xlim(0, 2)
    ax.set_xticks(np.arange(0, 2.1, 0.5))
    ax.set_xticklabels(np.append(np.arange(0, 2.0, 0.5), '>2.0'))
    ax.legend(loc='lower right', shadow=False)
    ax.xaxis.grid(linestyle='dotted', color='gray')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_xlabel("Energy Consumption (J)")
    fig.tight_layout()
    fig.savefig(results_output + "/overall_results.pdf")
    plt.close()



def _get_interactions_count(interaction_name):
    interaction_name = interaction_name.upper()
    return getattr(loop_count, interaction_name) * getattr(loop_count, interaction_name+"_UNIT")


def describe(*samples, **options):
    """Create table with statistic summary of samples."""
    loop_count = options.get("loop_count")
    names = list(options["names"])
    names_formatted = list(names)
    out = options.get('out', sys.stdout)
    table_fmt = options.get("table_fmt", "grid")
    float_fmt = options.get("float_fmt", "")
    mili_joules = options.get("mili_joules")

    consumption_samples = [np.array(sample, dtype='float') for sample in samples]
    if mili_joules:
        for sample in consumption_samples:
            sample *= 1000
        unit= 'mJ'
    else:
        unit = 'J'
    samples_means = np.array([np.mean(sample) for sample in consumption_samples])

    order = samples_means.argsort()
    ranking = order.argsort()

    durations = [
        np.mean([measurement.duration for measurement in sample])
        for sample in samples
    ]

    # best_framework_index = np.where(ranking == 0)[0][0]
    # baseline = np.mean(consumption_samples[best_framework_index])
    
    #human
    baseline_without_idle_cost = samples_means[0] - durations[0]*IDLE_COST
    #
    
    table = list()
    for index, sample in enumerate(consumption_samples):
        mean = np.mean(sample)
        row = OrderedDict((
            # ("N",    len(sample)),
            ("$\\bar{{x}}$ ({})".format(unit),  mean),
            ("$s$",  np.std(sample)),
        ))
        #duration
        row["$\\Delta t$ (s)"] = durations[index]
        mean_without_idle_cost = mean - durations[index]*IDLE_COST
        row["$\\bar{{x}}'$ (J)"] = mean_without_idle_cost
        if mean_without_idle_cost <= 0 :
            click.secho("WARNING: negative consumption for {}.".format(names[index]), fg='yellow')
            # import pdb; pdb.set_trace()
        # row["Idle (J)"] = IDLE_COST * durations[index]
        if loop_count:
            #row["Iter."] = loop_count
            row["Sg ({})".format(unit)] = mean_without_idle_cost/loop_count

        #duration
        row["$\\Delta t$ (s)"] = durations[index]
        row["Rank"] = int(ranking[index]+1)
        if row["Rank"] == 1 and table_fmt=='latex':
            names_formatted[index] = "\\textbf{"+names[index]+"}"
        if names[0] == "Human":
            row["Overhead"] = "{:.1f}\\%".format((mean_without_idle_cost / baseline_without_idle_cost - 1)*100)
            if row["Overhead"] == "0.0\\%":
                row["Overhead"] = "---"
        table.append(row)
    old_escape_rules = T.LATEX_ESCAPE_RULES
    T.LATEX_ESCAPE_RULES = {}
    out.write(T.tabulate(table, headers='keys', tablefmt=table_fmt, floatfmt=float_fmt, showindex=names_formatted).replace('rl}', 'rr}'))
    T.LATEX_ESCAPE_RULES = old_escape_rules
    out.write("\n")
    return table

def violinplot(*samples, **options):
    """Create violin plot for a set of measurement samples."""
    names_dict = options.get("names_dict")
    title = options.get("title")

    consumptions = [np.array(sample, dtype='float') for sample in samples]
    durations = np.array([np.mean([measurement.duration for measurement in sample]) for sample in samples])
    unit = 'J'

    if names_dict:
        labels = [
            sample and names_dict[sample[0].use_case]
            for sample in samples
        ]
    else:
        labels = [
            sample and sample[0].use_case.title().replace('_', ' ')
            for sample in samples
        ]
    plot = stats_violinplot(consumptions, labels=labels, plot_opts={'label_rotation': 70})
    axes = plt.gca()
    axes.set_ylabel("Energy ({})".format(unit))
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.yaxis.grid(linestyle='dashed')
    axes.yaxis.set_ticks_position('none')

    if title:
        plt.title(title)
    if options.get('save_fig'):
        plt.gcf().tight_layout()
        plt.savefig(options.get('save_fig'))
        plt.close()
    if options.get('show_fig'):
        plt.show()


    index = range(len(consumptions))
    means = [np.mean(sample) for sample in consumptions]
    stds = [np.std(sample) for sample in consumptions]
    means_without_idle_cost = means - IDLE_COST*durations
    fig, ax = plt.subplots(figsize=(6,3.5))
    from cycler import cycler
    ax.set_prop_cycle(cycler(color=[DARK_DARK_GREEN, 'r']))

    bars = ax.bar(index, means, width=0.7, #yerr=stds,
           capsize=5, color='white', edgecolor='gray', linewidth=0.6,
           zorder=0)
    bars = ax.bar(index, means_without_idle_cost, width=0.7, #yerr=stds,
           capsize=5, alpha=0.5, color=DARK_GREEN, edgecolor='gray', linewidth=0.6,
           zorder=1)
    # Highlight human results
    if labels[0] == "Human":
        bars[0].set_facecolor('yellow')
        plt.axhline(y=means_without_idle_cost[0], color='gray', linestyle='--', linewidth=0.6)
    
    plt.errorbar(index, means, yerr=stds, zorder=5, capsize=3, linewidth=0.7, capthick=0.7, fmt='none')
    parts = ax.violinplot(consumptions, index,
                  showmeans=False, showextrema=False, showmedians=False)

    for pc in parts['bodies']:
        pc.set_facecolor(DARK_GREEN)
        pc.set_edgecolor('black')
        pc.set_linewidth(0.6)

        pc.set_alpha(0.4)

    ax.set_xticklabels(labels, rotation=70)
    ax.set_xticks(range(len(labels)))
    ax.tick_params(direction='out', top='off')
    # ax.set_title("Number of projects by test framework")
    ax.set_ylabel("Energy ({})".format(unit))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.grid(linestyle='dotted')

    fig.tight_layout()
    fig.savefig(options.get('save_fig'))
    plt.close()


def exit_gracefully(start_time):
    exit_time = time.time()
    duration = exit_time - start_time
    click.secho(
        "Physalia Automators reports exited in {:.4f} seconds.".format(duration),
        fg='blue'
    )

if __name__ == '__main__':
    start_time = time.time()
    try:
        tool()
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully(start_time)
