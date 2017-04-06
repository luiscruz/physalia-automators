"""Interaction using Appium"""

from time import sleep
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import click
from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries

import os
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class AppiumUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `Appium`."""

    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, name, app_apk, app_pkg, activity, app_version,
                 run, prepare=None, cleanup=None):  # noqa: D102
        super(AppiumUseCase, self).__init__(
            name, PATH(app_apk), app_pkg, app_version,
            run, prepare, cleanup
        )
        self.activity = activity
        self.driver=None
    
    def prepare(self):
        """Prepare environment for running.

        Setup Appium driver in order to run experiments.
        """
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = '00e388b9e4931384'
        desired_caps['app'] = self.app_apk
        
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities=desired_caps)
        self._prepare()
        click.secho("Starting use case {}.".format(self.name), fg='green')

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
        self.uninstall_app()
        self.driver.quit()

    def install_app(self):
        """Install App"""
        click.secho("Installing {}".format(self.app_apk), fg='blue')
        self.driver.install_app(self.app_apk)

    def uninstall_app(self):
        """Uninstall app of the Android device."""
        click.secho("Uninstalling {}".format(self.app_pkg), fg='blue')
        self.driver.remove_app(self.app_pkg)

# -------------------------------------------------------------------------- #

def run_find_by_content_description(use_case):
    """Run script to test find by content descriptor."""

    @minimum_execution_time(seconds=time_boundaries.FIND_BY_CONTENT_DESCRIPTION)
    def simple_routine():
        use_case.driver.find_element_by_accessibility_id('Button One').click()
        use_case.driver.find_element_by_accessibility_id('Button Two')
        use_case.driver.find_element_by_accessibility_id('Button Three')
        use_case.driver.find_element_by_accessibility_id('Button Fab')
        use_case.driver.find_element_by_accessibility_id('Text Area')

    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

find_by_content_description_use_case = AppiumUseCase(
    "Appium-find_by_content_decription",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_find_by_content_description
)

# print find_by_content_description_use_case.run().duration

# -------------------------------------------------------------------------- #
def prepare_tap(use_case):
    use_case.button1 = use_case.driver.find_element_by_accessibility_id('Button One')
    use_case.button2 = use_case.driver.find_element_by_accessibility_id('Button Two')
    use_case.button3 = use_case.driver.find_element_by_accessibility_id('Button Three')
    use_case.button_fab = use_case.driver.find_element_by_accessibility_id('Button Fab')
    use_case.text_area = use_case.driver.find_element_by_accessibility_id('Text Area')

def run_tap(use_case):
    """Run script to test find by content descriptor."""

    @minimum_execution_time(seconds=time_boundaries.TAP)
    def simple_routine():
        use_case.button1.click()
        use_case.button2.click()
        use_case.button3.click()
        use_case.button_fab.click()
        use_case.text_area.click()
    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

tap_use_case = AppiumUseCase(
    "Appium-tap",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_tap,
    prepare=prepare_tap,
)

# print tap_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_long_tap(use_case):
    use_case.elements = [
        use_case.driver.find_element_by_accessibility_id('Button One'),
        use_case.driver.find_element_by_accessibility_id('Button Two'),
        use_case.driver.find_element_by_accessibility_id('Button Three'),
        use_case.driver.find_element_by_accessibility_id('Button Fab'),
        use_case.driver.find_element_by_accessibility_id('Text Area'),
    ]
    use_case.action = TouchAction(use_case.driver)

def run_long_tap(use_case):
    """Run script to test find by content descriptor."""

    @minimum_execution_time(seconds=time_boundaries.LONG_TAP)
    def simple_routine():
        for el in use_case.elements:
            use_case.action.long_press(el).perform()

    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

long_tap_use_case = AppiumUseCase(
    "Appium-long_tap",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_long_tap,
    prepare=prepare_long_tap,
)

print long_tap_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_long_tap(use_case):
    use_case.elements = [
        use_case.driver.find_element_by_accessibility_id('Button One'),
        use_case.driver.find_element_by_accessibility_id('Button Two'),
        use_case.driver.find_element_by_accessibility_id('Button Three'),
        use_case.driver.find_element_by_accessibility_id('Button Fab'),
        use_case.driver.find_element_by_accessibility_id('Text Area'),
    ]
    use_case.action = TouchAction(self.driver)

def run_long_tap(use_case):
    """Run script to test find by content descriptor."""

    @minimum_execution_time(seconds=time_boundaries.LONG_TAP)
    def simple_routine():
        for idx, el in enumerate(use_case.elements):
            prev_el = use_case.elements[idx-1]
            use_case.action.long_press(el).release().perform()

    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

long_tap_use_case = AppiumUseCase(
    "Appium-long_tap",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_long_tap,
    prepare=prepare_long_tap,
)

# print long_tap_use_case.run().duration

