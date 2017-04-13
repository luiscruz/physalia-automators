"""Interaction using UiAutomator"""

# adb shell am instrument -w  com.example.android.testing.uiautomator.BasicSample.test/android.support.test.runner.AndroidJUnitRunner

from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries
import subprocess
import click

class UiAutomatorUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `UiAutomator`."""

    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, name, app_apk, app_pkg, app_version,
                 test_apk, test_pkg, minimum_execution_time):  # noqa: D102
        super(UiAutomatorUseCase, self).__init__(
            name, app_apk, app_pkg, app_version,
        )
        self.test_pkg = test_pkg
        self.test_apk = test_apk
        self.minimum_execution_time = minimum_execution_time

    def install_test(self):
        click.secho("Installing {}".format(self.test_apk), fg='blue')
        subprocess.check_output(["adb", "install", self.test_apk])

    def uninstall_test(self):
        """Uninstall test app of the Android device."""
        click.secho("Uninstalling {}".format(self.test_pkg), fg='blue')
        subprocess.check_output(["adb", "uninstall", self.test_pkg])

    def prepare(self):
        """Prepare environment for running."""
        self.install_app()
        self.install_test()
        self.open_app()
        self._prepare()
        click.secho("Starting use case {}.".format(self.name), fg='green')

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
        # self.uninstall_app()
        # self.uninstall_test()
    
    def _run(self):
        @minimum_execution_time(seconds=self.minimum_execution_time)
        def launch_ui_automator():
            print subprocess.check_output(
                "adb shell am instrument -w {test_pkg}/"
                "android.support.test.runner.AndroidJUnitRunner".format(
                    test_pkg= self.test_pkg
                ),
                shell=True
            )
        launch_ui_automator()
        

# -------------------------------------------------------------------------- #

use_case = UiAutomatorUseCase(
    "UiAutomator-test",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "0.01",
    "../apks/uiautomator_routines.apk",
    "com.tqrg.physalia.testapp.test",
    time_boundaries.FIND_BY_ID
)

print use_case.run().duration
