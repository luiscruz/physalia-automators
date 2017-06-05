"""Command Line Interface for Physalia.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python cli.py "python ui_interaction.py"
"""

# pylint: disable=no-value-for-parameter
# pylint: disable=missing-docstring

import click
from physalia.power_meters import MonsoonPowerMeter
# from physalia_automators import android_view_client_use_case
# from physalia_automators import appium_usecase
# from physalia_automators import calabash_usecase
# from physalia_automators import espresso_usecase
# from physalia_automators import monkeyrunner_usecase
from physalia_automators import python_ui_automator_usecase
# from physalia_automators import robotium_usecase
# from physalia_automators import ui_automator_usecase

@click.command()
def tool():
    """Run tool."""
    power_meter = MonsoonPowerMeter(voltage=3.8, sample_hz=5000, serial=12886)
    print power_meter
    print python_ui_automator_usecase.use_cases
    for use_case_name,use_case in python_ui_automator_usecase.use_cases.items():
        if use_case:
            click.secho("Running {}...".format(use_case_name),
                        fg='blue')
            results = use_case.profile(power_meter=power_meter,
                                       count=30, retry_limit=10,
                                       save_to_csv="results.csv")
        else:
            click.secho("Skipping {}...".format(use_case_name),
                        fg='red')

if __name__ == '__main__':
    tool()
