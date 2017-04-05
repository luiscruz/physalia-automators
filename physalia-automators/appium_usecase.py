"""Interaction using Appium"""

from time import sleep
from appium import webdriver
import click
from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time

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

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
        self.driver.quit()

    def install_app(self):
        """Install App"""
        click.secho("Installing {}".format(self.app_apk), fg='blue')
        self.driver.install_app(self.app_apk)

    def uninstall_app(self):
        """Uninstall app of the Android device."""
        click.secho("Uninstalling {}".format(self.app_pkg), fg='blue')
        self.driver.remove_app(self.app_pkg)


def prepare(use_case):
    """Install and open app."""
    use_case.install_app()
    use_case.open_app()
    sleep(1)


def cleanup(use_case):
    """Uninstall app."""
    use_case.uninstall_app()

def run_view_listed_app(use_case):
    """Interaction of getting info about an application."""

    @minimum_execution_time(seconds=5)
    def find_and_click_button():
        el = use_case.driver.find_element_by_accessibility_id('Search').click()
        use_case.driver.find_element_by_accessibility_id('Collapse').click()

    try:
        for i in range(10):
            print i
            find_and_click_button()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

view_listed_app_use_case = AppiumUseCase(
    "ViewListedApp",
    "./fdroid.apk",
    "org.fdroid.fdroid",
    "",
    "0.01",
    run_view_listed_app,
    prepare=prepare,
    cleanup=cleanup
)

print view_listed_app_use_case.run().duration
