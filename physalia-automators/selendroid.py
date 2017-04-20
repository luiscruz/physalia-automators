"""Interaction using Python Ui Automator"""

from selenium import webdriver
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.action_chains import ActionChains
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

    def double_finger_tap(self, x1, y1, x2, y2):
        self.driver.tap([
            (x1, y1),
            (x2, y2),
        ])
    def drag_and_drop(self, element1, element2):
        click.secho("Drag And Drop", fg='yellow')
        touch_actions = TouchActions(self.driver)
        # touch_actions.tap_and_hold(element1.location['x'],
        #                    element1.location['y'])
        # touch_actions.move(element2.location['x'],
        #                    element2.location['y'])
        # touch_actions.release(element2.location['x'],
        #                  element2.location['y'])
        offset_x = element2.location['x'] - element1.location['x']
        offset_y = element2.location['y'] - element1.location['y']
        touch_actions.flick_element(element1, offset_x, offset_y, 2)
        touch_actions.perform()

    def swipe(self, element, offset_x, translate_y=0):
        touch_actions = TouchActions(self.driver)
        element.location['y'] -= 500
        touch_actions.flick_element(element, offset_x, 0, 0)
        touch_actions.perform()

    def cleanup(self):
        """Clean environment after running."""
        self._cleanup()
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
    "ScrollingActivity",
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
    "ScrollingActivity",
    "0.01",
    run_long_tap,
    prepare=prepare_long_tap,
)

print long_tap_use_case.run().duration


# -------------------------------------------------------------------------- #

def prepare_multi_finger_tap(use_case):
    use_case.elements = [
        use_case.driver.find_element_by_id('button_1'),
        use_case.driver.find_element_by_id('button_2'),
        use_case.driver.find_element_by_id('button_3'),
        use_case.driver.find_element_by_id('fab'),
    ]
    use_case.action = TouchActions(use_case.driver)

@minimum_execution_time(seconds=time_boundaries.DOUBLE_TAP)
def run_multi_finger_tap(use_case):
    """Run script to test long tap."""

    def simple_routine():
        for idx, el in enumerate(use_case.elements):
            prev_el = use_case.elements[idx-1]
            use_case.double_finger_tap(
                el.location['x'], el.location['y'],
                prev_el.location['x'], prev_el.location['y']
            )
    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

multi_finger_tap_use_case = SelendroidUseCase(
    "Selendroid-multi_finger_tap",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "ScrollingActivity",
    "0.01",
    run_multi_finger_tap,
    prepare=prepare_multi_finger_tap,
)

# print multi_finger_tap_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_dragndrop(use_case):
    button1 = use_case.driver.find_element_by_id('button_1')
    button2 = use_case.driver.find_element_by_id('button_2')
    button3 = use_case.driver.find_element_by_id('button_3')
    button_fab = use_case.driver.find_element_by_id('fab')
    text_area = use_case.driver.find_element_by_id('text_area')
    use_case.moves = [
        (button1, button2),
        (button2, button3),
        (button_fab, button3),
        (button_fab, text_area),
    ]

@minimum_execution_time(seconds=time_boundaries.DRAGNDROP)
def run_dragndrop(use_case):
    """Run script to test drag and drop."""

    # @minimum_execution_time(seconds=time_boundaries.DRAGNDROP_UNIT)
    def simple_routine():
        for first, second in use_case.moves:
            use_case.drag_and_drop(first, second)

    try:
        for i in range(10):
            simple_routine()
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

dragndrop_use_case = SelendroidUseCase(
    "Selendroid-dragndrop",
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
    use_case.paint = use_case.driver.find_element_by_id('button_3')
    use_case.x_i = use_case.paint.location['x']
    use_case.y_i = use_case.paint.location['y']

# @minimum_execution_time(seconds=time_boundaries.SWIPE)
def run_swipe(use_case):
    """Run script to test multi finger tap."""

    @minimum_execution_time(seconds=time_boundaries.SWIPE_UNIT)
    def simple_routine(offset_y):
        # Swipe left
        use_case.swipe(use_case.paint, -400)
        # Swipe Right
        use_case.swipe(use_case.paint, 400)
    try:
        for i in range(10):
            simple_routine(i*8)
    except Exception as e:
        click.secho("Error: {}.".format(e), fg='red')

swipe_use_case = SelendroidUseCase(
    "Selendroid-swipe",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "",
    "0.01",
    run_swipe,
    prepare=prepare_swipe,
)

print swipe_use_case.run().duration
