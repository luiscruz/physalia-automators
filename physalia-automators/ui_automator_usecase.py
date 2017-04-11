"""Interaction using UiAutomator"""

# adb shell am instrument -w  com.example.android.testing.uiautomator.BasicSample.test/android.support.test.runner.AndroidJUnitRunner

from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries
import subprocess

class AppiumUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `Appium`."""

    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, name, app_apk, app_pkg, app_version,
                 run, prepare=None, cleanup=None):  # noqa: D102
        super(AppiumUseCase, self).__init__(
            name, app_apk, app_pkg, app_tests_pkg, app_version,
            run, prepare, cleanup
        )
        self.app_tests_pkg = app_tests_pkg
    
    def prepare(self):
        """Prepare environment for running.
        """
        self._prepare()
        click.secho("Starting use case {}.".format(self.name), fg='green')
    
    def _run(self):
        subprocess.check_output(
            "adb shell am instrument -w "
            "com.example.android.testing.uiautomator.BasicSample.test/"
            "android.support.test.runner.AndroidJUnitRunner",
            shell=True
        )

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()

# -------------------------------------------------------------------------- #

