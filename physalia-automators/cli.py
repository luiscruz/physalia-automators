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
from physalia_automators import android_view_client_use_case
from physalia_automators import appium_usecase
from physalia_automators import calabash_use_case
from physalia_automators import espresso_use_case
from physalia_automators import monkeyrunner_use_case
from physalia_automators import python_ui_automator_use_case
from physalia_automators import robotium_use_case
from physalia_automators import ui_automator_use_case

@click.command()
def tool(runner):
    """Run tool."""
    print android_view_client_use_case.use_cases


if __name__ == '__main__':
    tool()
