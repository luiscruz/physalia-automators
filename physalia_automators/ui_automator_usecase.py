"""Interaction using UiAutomator"""

# adb shell am instrument -w  com.example.android.testing.uiautomator.BasicSample.test/android.support.test.runner.AndroidJUnitRunner

from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries
import subprocess
import click

APP_APK = "./apks/testapp-debug.apk"
TEST_APK = "./apks/test_routines.apk"
TEST_CLASS = "com.tqrg.physalia.testapp.ApplicationTest"

class UiAutomatorUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `UiAutomator`."""

    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, name, app_apk, app_pkg, app_version,
                 test_class, test_method,
                 test_apk, test_pkg, minimum_execution_time):  # noqa: D102
        super(UiAutomatorUseCase, self).__init__(
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
        self.open_app()
        self._prepare()
        click.secho("Starting use case {}.".format(self.name), fg='green')

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
        self.uninstall_app()
        self.uninstall_test()
    
    def _run(self):
        @minimum_execution_time(seconds=self.minimum_execution_time)
        def launch_ui_automator():
            print subprocess.check_output(
                "adb shell am instrument -w -r -e debug false -e class {test_class}#{test_method} "
                "{test_pkg}/android.support.test.runner.AndroidJUnitRunner".format(
                    test_class=self.test_class,
                    test_method=self.test_method,
                    test_pkg=self.test_pkg
                ),
                shell=True
            )
        launch_ui_automator()
        

# -------------------------------------------------------------------------- #

find_by_id_use_case = UiAutomatorUseCase(
    "UiAutomator-find_by_id",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "findById", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.FIND_BY_ID
)


# print find_by_id_use_case.run().duration
# -------------------------------------------------------------------------- #

find_by_description_use_case = UiAutomatorUseCase(
    "UiAutomator-find_by_description",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "findByDescription", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.FIND_BY_DESCRIPTION
)
# -------------------------------------------------------------------------- #

find_by_content_use_case = UiAutomatorUseCase(
    "UiAutomator-find_by_content",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "findByContent", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.FIND_BY_CONTENT
)

# -------------------------------------------------------------------------- #

tap_use_case = UiAutomatorUseCase(
    "UiAutomator-tap",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "tap", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.TAP
)

# -------------------------------------------------------------------------- #

long_tap_use_case = UiAutomatorUseCase(
    "UiAutomator-long_tap",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "longTap", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.LONG_TAP
)

# -------------------------------------------------------------------------- #

dragndrop_use_case = UiAutomatorUseCase(
    "UiAutomator-dragndrop",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "dragndrop", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.DRAGNDROP
)

# -------------------------------------------------------------------------- #

swipe_use_case = UiAutomatorUseCase(
    "UiAutomator-swipe",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "swipe", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.SWIPE
)

# -------------------------------------------------------------------------- #

pinch_and_spread_use_case = UiAutomatorUseCase(
    "UiAutomator-pinch_and_spread",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "pinchAndSpread", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.PINCH_AND_SPREAD
)
# -------------------------------------------------------------------------- #

back_button_use_case = UiAutomatorUseCase(
    "UiAutomator-back_button",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "backButton", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.BACK_BUTTON
)
# -------------------------------------------------------------------------- #

input_text_use_case = UiAutomatorUseCase(
    "UiAutomator-input_text",
    APP_APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    TEST_CLASS,
    "inputText", # test_method
    TEST_APK,
    "com.tqrg.physalia.testapp.test",
    time_boundaries.INPUT_TEXT
)



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
