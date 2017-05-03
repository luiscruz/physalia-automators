"""Interaction using Calabash

Requires ruby >=2, calabash-android, and cucumber
Installation details:
https://github.com/calabash/calabash-android
"""

from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries
import subprocess
import click



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
            subprocess.check_output(
                "calabash-android run ../{apk} "
                "features/{feature}"
                " --name \"{scenario}\"".format(
                    apk=self.app_apk,
                    feature=self.feature,
                    scenario=self.scenario
                ),
                cwd="./calabash-ruby/",
                shell=True
            )
        launch_calabash()
        
APK = "../apks/app-debug.apk"
APP_PKG = "com.tqrg.physalia.testapp"
APP_VERSION = "0.01"
FEATURE = "physalia_test_app.feature"

# -------------------------------------------------------------------------- #

tap_use_case = CalabashUseCase(
    "Monkeyrunner-tap",
    APK,
    APP_PKG,
    APP_VERSION,
    FEATURE,
    "Tap\ on\ views",
    time_boundaries.TAP
)

print tap_use_case.run().duration

# -------------------------------------------------------------------------- #
