"""Interaction using Appium"""

from appium import webdriver
from physalia.energy_profiler import AndroidUseCase

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
            name, app_apk, app_pkg, app_version,
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
        desired_caps['app'] = PATH(self.app_apk)
        
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities=desired_caps)
        self._prepare()

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
        self.driver.quit()

    def install_app(self):
        self.driver.install_app('/Users/isaac/code/python-client/test/apps/selendroid-test-app.apk')

    def uninstall_app(self):
        """Uninstall app of the Android device."""
        click.secho("Uninstalling {}".format(self.app_pkg), fg='blue')
        self.driver.remove_app('self.app_pkg')


# View a listed app
def prepare(use_case):
    """Open app and wait until it loads."""
    use_case.open_app()


def run_view_listed_app(use_case):
    """Interaction of getting info about an application."""
    el = use_case.driver.find_element_by_accessibility_id('action_search')
    el.click()
    app_icon.touch()
    sleep(10)

view_listed_app_use_case = AppiumUseCase(
    "ViewListedApp",
    "./fdroid.apk",
    "org.fdroid.fdroid",
    "",
    "0.01",
    run_view_listed_app,
    prepare=prepare
)

view_listed_app_use_case.run()
