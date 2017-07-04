"""Interaction using Calabash

Requires ruby >=2, calabash-android, and cucumber
Installation details:
https://github.com/calabash/calabash-android
"""

import subprocess
import click
from whichcraft import which
from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries


class CalabashUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `Calabash`."""

    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.
    def __init__(self, name, app_apk, app_pkg, app_version,
                 feature, scenario, minimum_execution_time):  # noqa: D102
        super(CalabashUseCase, self).__init__(
            name, app_apk, app_pkg, app_version,
        )
        self.feature = feature
        self.scenario = scenario
        self.minimum_execution_time = minimum_execution_time

    def prepare(self):
        """Prepare environment for running."""
        self.install_app()
        self._prepare()
        click.secho("Starting use case {}.".format(self.name), fg='green')

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
        self.uninstall_app()
    
    def _run(self):
        @minimum_execution_time(seconds=self.minimum_execution_time)
        def launch_calabash():
            try:
                print subprocess.check_output(
                    "calabash-android run ../../{apk} "
                    "features/{feature}"
                    " --name \"{scenario}\"".format(
                        apk=self.app_apk,
                        feature=self.feature,
                        scenario=self.scenario
                    ),
                    cwd="./physalia_automators/calabash-ruby/",
                    shell=True
                )
            except subprocess.CalledProcessError as e:
                click.secho(str(e), fg='red')
                print e.output
        launch_calabash()
    
    @staticmethod
    def calabash_is_installed():
        """Check if calabash is installed."""
        return bool(which("calabash-android"))
        
APK = "./apks/testapp-calabash-resigned.apk"
APP_PKG = "com.tqrg.physalia.testapp"
APP_VERSION = "0.01"
FEATURE = "physalia_test_app.feature"

# -------------------------------------------------------------------------- #

find_by_id_use_case = CalabashUseCase(
    "Calabash-find_by_id",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Find\ By\ Id",
    time_boundaries.FIND_BY_ID
)

# print find_by_id_use_case.run().duration

# -------------------------------------------------------------------------- #

find_by_description_use_case = CalabashUseCase(
    "Calabash-find_by_description",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Find\ By\ Description",
    time_boundaries.FIND_BY_DESCRIPTION
)

# print find_by_description_use_case.run().duration

# -------------------------------------------------------------------------- #

find_by_content_use_case = CalabashUseCase(
    "Calabash-find_by_content",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Find\ By\ Content",
    time_boundaries.FIND_BY_CONTENT
)

# print find_by_content_use_case.run().duration

# -------------------------------------------------------------------------- #

tap_use_case = CalabashUseCase(
    "Calabash-tap",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Tap\ on\ views",
    time_boundaries.TAP
)

# print tap_use_case.run().duration

# -------------------------------------------------------------------------- #

long_tap_use_case = CalabashUseCase(
    "Calabash-long_tap",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Long\ tap\ on\ views",
    time_boundaries.LONG_TAP
)

# print long_tap_use_case.run().duration

# -------------------------------------------------------------------------- #

dragndrop_use_case = CalabashUseCase(
    "Calabash-dragndrop",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Dragndrop",
    time_boundaries.DRAGNDROP
)

# print dragndrop_use_case.run().duration

# -------------------------------------------------------------------------- #

swipe_use_case = CalabashUseCase(
    "Calabash-swipe",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Swipe",
    time_boundaries.SWIPE
)

# print swipe_use_case.run().duration

# -------------------------------------------------------------------------- #

pinch_and_spread_use_case = CalabashUseCase(
    "Calabash-pinch_and_spread",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Pinch\ and\ spread",
    time_boundaries.PINCH_AND_SPREAD
)

# print pinch_and_spread_use_case.run().duration

# -------------------------------------------------------------------------- #

back_button_use_case = CalabashUseCase(
    "Calabash-back_button",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Back\ button",
    time_boundaries.BACK_BUTTON
)

# print back_button_use_case.run().duration

# -------------------------------------------------------------------------- #

input_text_use_case = CalabashUseCase(
    "Calabash-input_text",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Type\ with\ keyboard",
    time_boundaries.INPUT_TEXT
)

# print input_text_use_case.run().duration

# -------------------------------------------------------------------------- #

use_cases = {
    "find_by_id": find_by_id_use_case,
    "find_by_description": find_by_description_use_case,
    "find_by_content": find_by_content_use_case,
    "tap": tap_use_case,
    "long_tap": long_tap_use_case,
    "multi_finger_tap": None,
    "dragndrop": dragndrop_use_case,
    "swipe": swipe_use_case,
    "pinch_and_spread": pinch_and_spread_use_case,
    "back_button": back_button_use_case,
    "input_text": input_text_use_case,
}
