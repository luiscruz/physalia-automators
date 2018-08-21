"""Command Line Interface for Physalia.

Example:
        ``$ python physalia_automators/cli.py "python ui_interaction.py"``
"""

# pylint: disable=no-value-for-parameter
# pylint: disable=missing-docstring

import time
import csv
import click
from retrying import retry
from physalia.power_meters import MonsoonPowerMeter, EmulatedPowerMeter
from physalia_automators import android_view_client_use_case
from physalia_automators import monkeyrunner_usecase
from physalia_automators import robotium_usecase
from physalia_automators import espresso_usecase
from physalia_automators import ui_automator_usecase
from physalia_automators import calabash_usecase
from physalia_automators import python_ui_automator_usecase
from physalia_automators import appium_usecase

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
    click.secho("http://tqrg.github.io/physalia", fg="blue")
    # click.launch('http://tqrg.github.io/physalia/')

    power_meter = MonsoonPowerMeter(voltage=3.8, serial=12886)


    # -------- AndroidViewClient -------- #
    evaluate_platform(android_view_client_use_case.use_cases, power_meter, count, output)

    # -------- Monkeyrunner -------- #
    evaluate_platform(monkeyrunner_usecase.use_cases, power_meter, count, output)

    # -------- Robotium -------- #
    evaluate_platform(robotium_usecase.use_cases, power_meter, count, output)

    # -------- Espresso -------- #
    evaluate_platform(espresso_usecase.use_cases, power_meter, count, output)

    # -------- Ui Automator -------- #
    evaluate_platform(ui_automator_usecase.use_cases, power_meter, count, output)

    # -------- Calabash -------- #
    if(calabash_usecase.CalabashUseCase.calabash_is_installed()):
        evaluate_platform(calabash_usecase.use_cases, power_meter, count, output)
    else:
        click.secho("Skipping Calabash experiments.", fg="red")
        click.secho("Be sure to install it and run the experiments again.", fg="red")
        click.secho('Launching https://github.com/calabash/calabash-android', fg="red")
        click.launch('https://github.com/calabash/calabash-android')

    # ----- Python Ui Automator ----- #
    evaluate_platform(python_ui_automator_usecase.use_cases, power_meter, count, output)


    # ---------- Appium ---------- #
    @retry(wait_fixed=2000, stop_max_attempt_number=40)
    def run_appium_measurements():
        if appium_usecase.AppiumUseCase.appium_is_installed():
            appium_usecase.AppiumUseCase.start_appium_server()
            time.sleep(30)
            try:
                evaluate_platform(appium_usecase.use_cases, power_meter, count, output)
            finally:
                appium_usecase.AppiumUseCase.stop_appium_server()
        else:
            click.secho("Skipping Appium experiments.", fg="red")
            click.secho("Be sure to install it and run the experiments again.", fg="red")
            click.secho('Launching http://appium.io', fg="red")
            click.launch('http://appium.io')

    run_appium_measurements()

    

def evaluate_platform(use_cases, power_meter, count, output):
    for use_case_name,use_case in use_cases.items():
        if use_case:
            executions_done = get_number_of_rows_for_key(use_case.name, output)
            executions_left = count - executions_done
            
            if executions_left > 0:
                click.secho("\n\nRunning {}...".format(use_case.name),
                            fg='blue', bold=True)
                use_case.profile(power_meter=power_meter,
                                 count=executions_left,
                                 retry_limit=3,
                                 save_to_csv=output)
            else:
                click.secho(
                    "\nSkipping {}: already done...".format(use_case.name),
                    fg='yellow'
                )
        else:
            click.secho(
                "\nSkipping {}: not defined...".format(use_case_name),
                fg='yellow'
            )
    

def get_number_of_rows_for_key(key, filename):
    """Get number of elements for a given usecase name."""
    with open(filename, 'r') as csvfile:
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
