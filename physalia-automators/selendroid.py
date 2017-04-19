"""Interaction using Python Ui Automator"""

from selenium import webdriver
from selenium.webdriver.common.touch_actions import TouchActions
import click
from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries

class SelendroidUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `Selendroid`."""

    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, name, app_apk, app_pkg, activity, app_version,
                 run, prepare=None, cleanup=None):  # noqa: D102
        super(SelendroidUseCase, self).__init__(
            name, app_apk, app_pkg, app_version,
            run, prepare, cleanup
        )
        self.activity = activity
        self.driver=None
    
    def prepare(self):
        """Prepare environment for running.

        Setup Appium driver in order to run experiments.
        """
        desired_capabilities = {
            'aut': self.app_pkg,
            'emulator': False
        }

        self.driver = webdriver.Remote(
            desired_capabilities=desired_capabilities
        )
        self.driver.implicitly_wait(30)
        self.driver.get('and-activity://com.tqrg.physalia.testapp.ScrollingActivity')
        self._prepare()
        click.secho("Starting use case {}.".format(self.name), fg='green')

    def find_by_id(self, element_id):
        self.driver.find_element_by_id(element_id)
    
    def find_by_description(self, description):
        self.driver.find_element_by_accessibility_id(description)
    
    def tap(self, element):
        element.click()
    
    def long_tap(self, element):
        self.action.long_press(element).perform()

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
        # self.uninstall_app()
        self.driver.quit()

# -------------------------------------------------------------------------- #

def prepare_tap(use_case):
    use_case.button1 = use_case.driver.find_element_by_id('button_1')
    use_case.button2 = use_case.driver.find_element_by_id('button_2')
    use_case.button3 = use_case.driver.find_element_by_id('button_3')
    use_case.button_fab = use_case.driver.find_element_by_id('fab')

def run_tap(use_case):
    """Run script to test tap."""

    @minimum_execution_time(seconds=time_boundaries.TAP)
    def simple_routine():
        use_case.tap(use_case.button1)
        use_case.tap(use_case.button2)
        use_case.tap(use_case.button3)
        use_case.tap(use_case.button_fab)
    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

tap_use_case = SelendroidUseCase(
    "Selendroid-tap",
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
        use_case.driver.find_element_by_id('button_1'),
        use_case.driver.find_element_by_id('button_2'),
        use_case.driver.find_element_by_id('button_3'),
        use_case.driver.find_element_by_id('fab'),
    ]
    use_case.action = TouchActions(use_case.driver)

def run_long_tap(use_case):
    """Run script to test long tap."""

    @minimum_execution_time(seconds=time_boundaries.LONG_TAP)
    def simple_routine():
        for el in use_case.elements:
            use_case.long_tap(el)

    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

long_tap_use_case = SelendroidUseCase(
    "Selendroid-long_tap",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_long_tap,
    prepare=prepare_long_tap,
)

print long_tap_use_case.run().duration

