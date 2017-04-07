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
        # self.uninstall_app()
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
    """Run script to test long tap descriptor."""

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

# print long_tap_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_multi_finger_tap(use_case):
    use_case.elements = [
        use_case.driver.find_element_by_accessibility_id('Button One'),
        use_case.driver.find_element_by_accessibility_id('Button Two'),
        use_case.driver.find_element_by_accessibility_id('Button Three'),
        use_case.driver.find_element_by_accessibility_id('Button Fab'),
        use_case.driver.find_element_by_accessibility_id('Text Area'),
    ]

def run_multi_finger_tap(use_case):
    """Run script to test multi finger tap."""

    @minimum_execution_time(seconds=time_boundaries.MULTI_FINGER_TAP)
    def simple_routine():
        for idx, el in enumerate(use_case.elements):
            prev_el = use_case.elements[idx-1]
            use_case.driver.tap([
                (el.location['x'],el.location['y']),
                (prev_el.location['x'],prev_el.location['y'])
            ])

    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

multi_finger_tap_use_case = AppiumUseCase(
    "Appium-multi_finger_tap",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_multi_finger_tap,
    prepare=prepare_multi_finger_tap,
)

# print multi_finger_tap_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_dragndrop(use_case):
    button1 = use_case.driver.find_element_by_accessibility_id('Button One')
    button2 = use_case.driver.find_element_by_accessibility_id('Button Two')
    button3 = use_case.driver.find_element_by_accessibility_id('Button Three')
    button_fab = use_case.driver.find_element_by_accessibility_id('Button Fab')
    text_area = use_case.driver.find_element_by_accessibility_id('Text Area')
    use_case.moves = [
        (button1, button2),
        (button2, button3),
        (button_fab, button3),
        (button_fab, text_area),
    ]

def run_dragndrop(use_case):
    """Run script to test multi finger tap."""

    @minimum_execution_time(seconds=time_boundaries.DRAGNDROP)
    def simple_routine():
        for first, second in use_case.moves:
            use_case.driver.drag_and_drop(first, second)

    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

dragndrop_use_case = AppiumUseCase(
    "Appium-dragndrop",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_dragndrop,
    prepare=prepare_dragndrop,
)

# print dragndrop_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_swipe(use_case):
    paint = use_case.driver.find_element_by_accessibility_id('Paint')
    use_case.x_i, use_case.y_i = (paint.location['x'], paint.location['y'])

def run_swipe(use_case):
    """Run script to test multi finger tap."""

    @minimum_execution_time(seconds=time_boundaries.SWIPE)
    def simple_routine(offset_y):
        # Swipe left
        x_f, y_f = (use_case.x_i+70, use_case.y_i+offset_y+1)
        paint = use_case.driver.find_element_by_accessibility_id('Paint')
        button_fab = use_case.driver.find_element_by_accessibility_id('Button Fab')
        use_case.driver.swipe(use_case.x_i, use_case.y_i+offset_y+1, x_f, y_f)
        # Swipe Right
        x_f, y_f = (use_case.x_i+1000, use_case.y_i+offset_y)
        use_case.driver.swipe(use_case.x_i, use_case.y_i+offset_y, x_f, y_f)

    try:
        for i in range(40):
            simple_routine(i*8)
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

swipe_use_case = AppiumUseCase(
    "Appium-swipe",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_swipe,
    prepare=prepare_swipe,
)

# print swipe_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_pinch_and_spread(use_case):
    use_case.paint = use_case.driver.find_element_by_accessibility_id('Paint')

def run_pinch_and_spread(use_case):
    """Run script to test multi finger tap."""

    @minimum_execution_time(seconds=time_boundaries.PINCH_AND_SPREAD)
    def simple_routine():
        for _ in range(40):
            use_case.driver.pinch(use_case.paint, percent=200, steps=50)
            use_case.driver.zoom(use_case.paint, percent=200, steps=50)

    simple_routine()
    try:
        simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

pinch_and_spread_use_case = AppiumUseCase(
    "Appium-pinch_and_spread",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_pinch_and_spread,
    prepare=prepare_pinch_and_spread,
)

# print pinch_and_spread_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_back_button(use_case):
    use_case.paint = use_case.driver.find_element_by_accessibility_id('Paint')

@minimum_execution_time(seconds=time_boundaries.BACK_BUTTON)
def run_back_button(use_case):
    """Run script to test multi finger tap."""

    @minimum_execution_time(seconds=time_boundaries.BACK_BUTTON_UNIT, warning=False)
    def simple_routine():
        for _ in range(200):
            keycode_back=4
            use_case.driver.press_keycode(keycode_back)

    try:
        simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

back_button_use_case = AppiumUseCase(
    "Appium-back_button",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_back_button,
    prepare=prepare_back_button,
)

# print back_button_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_input_text(use_case):
    use_case.text_field = use_case.driver.find_element_by_accessibility_id('Text Field')

@minimum_execution_time(seconds=time_boundaries.INPUT_TEXT)
def run_input_text(use_case):
    """Run script to test multi finger tap."""

    try:
        use_case.text_field.send_keys(
            "Physalia says hi!"
        )
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

input_text_use_case = AppiumUseCase(
    "Appium-input_text",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_input_text,
    prepare=prepare_input_text,
)

# print input_text_use_case.run().duration

# -------------------------------------------------------------------------- #

@minimum_execution_time(seconds=time_boundaries.FIND_BY_DESCRIPTION)
def run_find_by_description(use_case):
    """Run script to test multi finger tap."""

    try:
        for _ in range(40):
            use_case.driver.find_element_by_accessibility_id('Button One')
            use_case.driver.find_element_by_accessibility_id('Button Two')
            use_case.driver.find_element_by_accessibility_id('Button Three')
            use_case.driver.find_element_by_accessibility_id('Button Fab')
            use_case.driver.find_element_by_accessibility_id('Text Field')
            use_case.driver.find_element_by_accessibility_id('Paint')
            use_case.driver.find_element_by_accessibility_id('Text Area')
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

find_by_description_use_case = AppiumUseCase(
    "Appium-find_by_description",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_find_by_description,
)

# print find_by_description_use_case.run().duration

# -------------------------------------------------------------------------- #

@minimum_execution_time(seconds=time_boundaries.FIND_BY_ID)
def run_find_by_id(use_case):
    """Run script to test multi finger tap."""

    try:
        for _ in range(40):
            use_case.driver.find_elements(by="id", value="com.tqrg.physalia.testapp:id/button_1")[0]
            use_case.driver.find_elements(by="id", value="com.tqrg.physalia.testapp:id/button_2")[0]
            use_case.driver.find_elements(by="id", value="com.tqrg.physalia.testapp:id/button_3")[0]
            use_case.driver.find_elements(by="id", value="com.tqrg.physalia.testapp:id/text_field")[0]
            use_case.driver.find_elements(by="id", value="com.tqrg.physalia.testapp:id/fab")[0]
            use_case.driver.find_elements(by="id", value="com.tqrg.physalia.testapp:id/paint")[0]
            use_case.driver.find_elements(by="id", value="com.tqrg.physalia.testapp:id/text_area")[0]
            
        
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

find_by_id_use_case = AppiumUseCase(
    "Appium-find_by_id",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_find_by_id,
)

# print find_by_id_use_case.run().duration

# -------------------------------------------------------------------------- #

@minimum_execution_time(seconds=time_boundaries.FIND_BY_CONTENT)
def run_find_by_content(use_case):
    """Run script to test multi finger tap."""
    def find_by_content(content):
        return use_case.driver.find_element_by_android_uiautomator(
            "new UiSelector().textContains(\"{}\")".format(content)
        )
    try:
        for _ in range(40):
            find_by_content("Button 1")
            find_by_content("Button 2")
            find_by_content("Button 3")            
        
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

find_by_content_use_case = AppiumUseCase(
    "Appium-find_by_content",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_find_by_content,
)

print find_by_content_use_case.run().duration
