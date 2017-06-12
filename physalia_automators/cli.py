"""Command Line Interface for Physalia.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python cli.py "python ui_interaction.py"
"""

# pylint: disable=no-value-for-parameter
# pylint: disable=missing-docstring

import signal
import sys
import time
import csv
import click
from physalia.power_meters import MonsoonPowerMeter, EmulatedPowerMeter
# from physalia_automators import android_view_client_use_case
# from physalia_automators import appium_usecase
# from physalia_automators import calabash_usecase
# from physalia_automators import espresso_usecase
# from physalia_automators import monkeyrunner_usecase
from physalia_automators import python_ui_automator_usecase
# from physalia_automators import robotium_usecase
# from physalia_automators import ui_automator_usecase

COLUMN_USE_CASE = 1

@click.command()
@click.argument('count', default=30, type=click.IntRange(min=1))
@click.argument('output', default="results.csv", type=click.Path(dir_okay=False))
def tool(count, output):
    """Run tool."""
    
    click.secho("=====================================", fg="blue")
    click.secho("         Physalia Automators         ", fg="blue")
    click.secho("=====================================", fg="blue")
    click.secho("By Luis Cruz and Rui Abreu.   ", fg="blue")
    click.secho("http://tqrg.github.io/physalia.", fg="blue")
    # click.launch('http://tqrg.github.io/physalia/')

    power_meter = MonsoonPowerMeter(voltage=3.8, serial=12886)
    for use_case_name,use_case in python_ui_automator_usecase.use_cases.items():
        if use_case:
            executions_done = get_number_of_rows_for_key(use_case.name, output)
            executions_left = count - executions_done
            
            if executions_left > 0:
                click.secho("\n\nRunning {}...".format(use_case_name),
                            fg='blue', bold=True)
                results = use_case.profile(power_meter=power_meter,
                                           count=executions_left,
                                           retry_limit=3,
                                           save_to_csv=output)
            else:
                click.secho(
                    "\nSkipping {}: already done...".format(use_case_name),
                    fg='yellow'
                )
        else:
            click.secho(
                "\nSkipping {}: not defined...".format(use_case_name),
                fg='yellow'
            )

def get_number_of_rows_for_key(key, filename):
    """Get number of elements for a given usecase name."""
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)
        return len([None for row in csv_reader if row[COLUMN_USE_CASE] == key])
        
def exit_gracefully(start_time):
    exit_time = time.time()
    duration = exit_time - start_time
    click.secho(
        "Physalia automators exited in {:.2f} minutes.".format(duration/60),
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
