"""Reports generator for Physalia Automators experiment.

Example:
        ``$ python physalia_automators/reports.py``
"""

# pylint: disable=no-value-for-parameter
# pylint: disable=missing-docstring

import time
import csv
import click
from physalia.models import Measurement
from physalia.analytics import violinplot

@click.command()
@click.option('-i','--results_input', default="results.csv", type=click.Path(dir_okay=False))
@click.option('-o','--results_output', default="results", type=click.Path())
def tool(results_input, results_output):
    
    with open(results_input, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = {Measurement(*row) for row in csv_reader}
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
        for use_case_category in use_case_categories:
            find_by_id_data = set(Measurement.get_entries_with_name_like(use_case_category, data))
            unique_use_cases = Measurement.get_unique_use_cases(find_by_id_data)
            names = {
                name: name.replace("-"+use_case_category, "") for name in unique_use_cases
            }
            groups = [
                list(Measurement.get_entries_with_name(use_case, data))
                for use_case in unique_use_cases
            ]
            title = use_case_category.title().replace('_'," ")
            violinplot(*groups, save_fig=results_output+"/"+use_case_category, names=names, title=title)
        
            

def exit_gracefully(start_time):
    exit_time = time.time()
    duration = exit_time - start_time
    click.secho(
        "Physalia automators exited in {:.4f} seconds.".format(duration),
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
