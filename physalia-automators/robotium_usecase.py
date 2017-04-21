"""Interaction using Espresso"""

from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries
import subprocess
import click

class RobotiumUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `UiAutomator`."""

    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, name, app_apk, app_pkg, app_version,
                 test_class, test_method,
                 test_apk, test_pkg, minimum_execution_time):  # noqa: D102
        super(RobotiumUseCase, self).__init__(
            name, app_apk, app_pkg, app_version,
        )
        self.test_class = test_class
        self.test_method = test_method
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
        # self.open_app()
        self._prepare()
        click.secho("Starting use case {}.".format(self.name), fg='green')

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
        self.uninstall_app()
        self.uninstall_test()
    
    def _run(self):
        @minimum_execution_time(seconds=self.minimum_execution_time)
        def launch_espresso():
            print subprocess.check_output(
                "adb shell am instrument -w -r -e debug false "
                "-e class {test_class}#{test_method} {test_pkg}/"
                "android.test.InstrumentationTestRunner".format(
                    test_class=self.test_class,
                    test_method=self.test_method,
                    test_pkg=self.test_pkg
                ),
                shell=True
            )
        launch_espresso()
        

APK = "../apks/RobotiumTest.apk"
APP_PKG = "com.tqrg.physalia.testapp"
APP_VERSION = "0.01"

# -------------------------------------------------------------------------- #

find_by_id_use_case = RobotiumUseCase(
    "Robotium-find_by_id",
    APK,
    APP_PKG,
    APP_VERSION,
    "com.tqrg.physalia.testapp.test.RobotiumTest",
    "testFindById",
    "../apks/RobotiumTest_routines.apk",
    "com.tqrg.physalia.testapp.test",
    time_boundaries.FIND_BY_ID
)

# print find_by_id_use_case.run().duration

# -------------------------------------------------------------------------- #

tap_use_case = RobotiumUseCase(
    "Robotium-tap",
    APK,
    APP_PKG,
    APP_VERSION,
    "com.tqrg.physalia.testapp.test.RobotiumTest",
    "testTap",
    "../apks/RobotiumTest_routines.apk",
    "com.tqrg.physalia.testapp.test",
    time_boundaries.TAP
)

print tap_use_case.run().duration

# -------------------------------------------------------------------------- #

long_tap_use_case = RobotiumUseCase(
    "Robotium-long_tap",
    APK,
    APP_PKG,
    APP_VERSION,
    "com.tqrg.physalia.testapp.test.RobotiumTest",
    "testLongTap",
    "../apks/RobotiumTest_routines.apk",
    "com.tqrg.physalia.testapp.test",
    time_boundaries.LONG_TAP
)

print long_tap_use_case.run().duration

# -------------------------------------------------------------------------- #

dragndrop_use_case = RobotiumUseCase(
    "Robotium-dragndrop",
    APK,
    APP_PKG,
    APP_VERSION,
    "com.tqrg.physalia.testapp.test.RobotiumTest",
    "testDragndrop",
    "../apks/RobotiumTest_routines.apk",
    "com.tqrg.physalia.testapp.test",
    time_boundaries.DRAGNDROP
)

print dragndrop_use_case.run().duration

# -------------------------------------------------------------------------- #

swipe_use_case = RobotiumUseCase(
    "Robotium-swipe",
    APK,
    APP_PKG,
    APP_VERSION,
    "com.tqrg.physalia.testapp.test.RobotiumTest",
    "testSwipe",
    "../apks/RobotiumTest_routines.apk",
    "com.tqrg.physalia.testapp.test",
    time_boundaries.SWIPE
)

print swipe_use_case.run().duration

# -------------------------------------------------------------------------- #

back_button_use_case = RobotiumUseCase(
    "Robotium-back_button",
    APK,
    APP_PKG,
    APP_VERSION,
    "com.tqrg.physalia.testapp.test.RobotiumTest",
    "testBackButton",
    "../apks/RobotiumTest_routines.apk",
    "com.tqrg.physalia.testapp.test",
    time_boundaries.BACK_BUTTON
)

print back_button_use_case.run().duration


# -------------------------------------------------------------------------- #

input_text_use_case = RobotiumUseCase(
    "Robotium-input_text",
    APK,
    APP_PKG,
    APP_VERSION,
    "com.tqrg.physalia.testapp.test.RobotiumTest",
    "testInputText",
    "../apks/RobotiumTest_routines.apk",
    "com.tqrg.physalia.testapp.test",
    time_boundaries.INPUT_TEXT
)

print input_text_use_case.run().duration
