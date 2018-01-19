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

@click.command()
@click.option('-i','--results_input', default="results.csv", type=click.Path(dir_okay=False))
@click.option('-o','--results_output', default="results", type=click.Path())
def tool(results_input, results_output):
    
    with open(results_input, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = []
        for row in csv_reader:
            # row[6] = float(row[6])*1000 # convert to mJ
            data.append(Measurement(*row))
    if not os.path.isdir(results_output):
        os.makedirs(results_output)

    use_case_categories = [
        "find_by_id",
        "find_by_description",
        "find_by_content",
        "tap",
        "long_tap",
        "multi_finger_tap",
        "dragndrop",
        "swipe",
        "pinch_and_spread",
        "back_button",
        "input_text",
    ]
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
        names, groups = zip(*sorted(zip(names, groups)))
        title = use_case_category.title().replace('_'," ")
        violinplot(
            *groups,
            save_fig=results_output+"/"+use_case_category+".pdf",
            names_dict=names_dict, sort=True,
            millijoules=True
        )
        n_loop_iterations = _get_interactions_count(use_case_category)
        # Descriptive statistics
        with open(results_output+"/table_description_"+use_case_category+".tex", "w") as file: 
            table = describe(*groups, names=names,
                             loop_count=n_loop_iterations,
                             ranking=True, out=file,
                             table_fmt="latex", float_fmt='.3f', mili_joules=True)
        # Update Ranking
        for name, row in zip(names, table):
            scores[name] += (number_of_frameworks - row["Rank"])/float(number_of_frameworks)
        # Welchs ttest
        with open(results_output+"/table_welchsttest_"+use_case_category+".tex", "w") as file:
            pairwise_welchs_ttest(*groups, names=names, out=file, table_fmt='latex')

    # Ranking
    click.secho("\nRanking".format(use_case_category), fg="blue")
    sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
    with open(results_output+"/table_ranking.tex", "w") as file: 
        file.write(
            tabulate(sorted_scores, headers=["Framework", "Score"], tablefmt="latex",
            floatfmt=".4f")
        )
    
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
        axes.set_ylabel("Energy Consumption (mJ)")
                
        figure.subplots_adjust(bottom=0.31)

        bar_labels = [y==0 and "n.a." or format(y, ".2f") for y in Y]
        for x,y,label in zip(X, Y, bar_labels):
            plt.text(x, y, label, ha='center', va= 'bottom')
        figure.tight_layout()
        figure.savefig(results_output+"/frameworks/"+framework)

def _get_interactions_count(interaction_name):
    interaction_name = interaction_name.upper()
    return getattr(loop_count, interaction_name) * getattr(loop_count, interaction_name+"_UNIT")


def describe(*samples, **options):
    """Create table with statistic summary of samples."""
    loop_count = options.get("loop_count")
    names = list(options.get("names"))
    out = options.get('out', sys.stdout)
    table_fmt = options.get("table_fmt", "grid")
    float_fmt = options.get("float_fmt", "")
    show_ranking = options.get("ranking")
    mili_joules = options.get("mili_joules")

    consumption_samples = [np.array(sample, dtype='float') for sample in samples]
    if mili_joules:
        for sample in consumption_samples:
            sample *= 1000
        unit= 'mJ'
    else:    
        unit = 'J'
    samples_means = np.array([np.mean(sample) for sample in consumption_samples])
    if show_ranking:
        order = samples_means.argsort()
        ranking = order.argsort()
    
    durations = [
        np.mean([measurement.duration for measurement in sample])
        for sample in samples
    ]
    table = list()
    for index, sample in enumerate(consumption_samples):
        mean = np.mean(sample)
        row = OrderedDict((
            # ("N",    len(sample)),
            ("$\\bar{{x}}$ ({})".format(unit),  mean),
            ("$s$",  np.std(sample)),
        ))
        if loop_count:
            #row["Iter."] = loop_count
            row["Single ({})".format(unit)] = mean/loop_count
        #duration    
        row["$\\Delta t$ (s)"] = durations[index]
        cost_idle_power = 0.0933
        # row["$\\bar{{x'}}$ (mJ)"] = mean - durations[index]*cost_idle_power
        if show_ranking:
            row["Rank"] = int(ranking[index]+1)
            if row["Rank"] == 1 and table_fmt=='latex':
                names[index] = "\\textbf{"+names[index]+"}"
        table.append(row)
    old_escape_rules = T.LATEX_ESCAPE_RULES
    T.LATEX_ESCAPE_RULES = {}
    out.write(T.tabulate(table, headers='keys', tablefmt=table_fmt, floatfmt=float_fmt, showindex=names))
    T.LATEX_ESCAPE_RULES = old_escape_rules
    out.write("\n")
    return table

def violinplot(*samples, **options):
    """Create violin plot for a set of measurement samples."""
    names_dict = options.get("names_dict")
    title = options.get("title")
    sort = options.get("sort")
    millijoules = options.get("millijoules")

    consumptions = [np.array(sample, dtype='float') for sample in samples]
    if millijoules:
        for sample in consumptions:
            sample *= 1000
        unit= 'mJ'
    else:    
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
    
    if sort:
        labels, samples = zip(*sorted(zip(labels, samples)))

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
    if options.get('show_fig'):
        plt.show()


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
