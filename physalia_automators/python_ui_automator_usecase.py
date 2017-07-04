"""Interaction using Python Ui Automator"""

import uiautomator
import click
from physalia.energy_profiler import AndroidUseCase
from utils import minimum_execution_time
import time_boundaries
from constants import loop_count

from uiautomator import device

APK = "./apks/testapp.apk"

def prepare(use_case):
    use_case.install_app()
    use_case.open_app()

def cleanup(use_case):
    """Clean environment after running."""
    use_case.uninstall_app()


# -------------------------------------------------------------------------- #

@minimum_execution_time(time_boundaries.FIND_BY_ID)
def run_find_by_id(_):
    for _ in range(loop_count.FIND_BY_ID):
        device(resourceId="com.tqrg.physalia.testapp:id/button_1").exists
        device(resourceId="com.tqrg.physalia.testapp:id/button_2").exists
        device(resourceId="com.tqrg.physalia.testapp:id/button_3").exists
        device(resourceId="com.tqrg.physalia.testapp:id/text_field").exists
        device(resourceId="com.tqrg.physalia.testapp:id/fab").exists
        device(resourceId="com.tqrg.physalia.testapp:id/paint").exists
        device(resourceId="com.tqrg.physalia.testapp:id/text_area").exists
    
find_by_id_use_case = AndroidUseCase(
    "PythonUiAutomator-find_by_id",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_find_by_id,
    prepare=prepare,
    cleanup=cleanup
)

# print find_by_id_use_case.run().duration

# -------------------------------------------------------------------------- #

@minimum_execution_time(time_boundaries.FIND_BY_DESCRIPTION)
def run_find_by_description(_):
    for _ in range(loop_count.FIND_BY_DESCRIPTION):
        device(description="Button One").exists
        device(description="Button Two").exists
        device(description="Button Three").exists
        device(description="Button Fab").exists
        device(description="Text Field").exists
        device(description="Paint").exists
        device(description="Text Area").exists
    
find_by_description_use_case = AndroidUseCase(
    "PythonUiAutomator-find_by_description",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_find_by_description,
    prepare=prepare,
    cleanup=cleanup
)

# print find_by_description_use_case.run().duration

# -------------------------------------------------------------------------- #

@minimum_execution_time(time_boundaries.FIND_BY_CONTENT)
def run_find_by_content(_):
    for _ in range(loop_count.FIND_BY_CONTENT):
        device(text="Button 1").exists
        device(text="Button 2").exists
        device(text="Button 3").exists
    
find_by_content_use_case = AndroidUseCase(
    "PythonUiAutomator-find_by_content",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_find_by_content,
    prepare=prepare,
    cleanup=cleanup
)

# print find_by_content_use_case.run().duration

# -------------------------------------------------------------------------- #
def prepare_tap(use_case):
    use_case.install_app()
    use_case.open_app()
    use_case.elements = [
        device(description="Button One"),
        device(description="Button Two"),
        device(description="Button Three"),
        device(description="Button Fab"),
    ]
    
@minimum_execution_time(time_boundaries.TAP)
def run_tap(use_case):
    for _ in range(loop_count.TAP):
        for el in use_case.elements:
            el.click()
    
tap_use_case = AndroidUseCase(
    "PythonUiAutomator-tap",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_tap,
    prepare=prepare_tap,
    cleanup=cleanup
)

# print tap_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_long_tap(use_case):
    use_case.install_app()
    use_case.open_app()
    use_case.elements = [
        device(description="Button One"),
        device(description="Button Two"),
        device(description="Button Three"),
        device(description="Button Fab"),
    ]
    
@minimum_execution_time(time_boundaries.LONG_TAP)
def run_long_tap(use_case):
    for _ in range(loop_count.LONG_TAP):
        for el in use_case.elements:
            el.long_click()
    
long_tap_use_case = AndroidUseCase(
    "PythonUiAutomator-long_tap",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_long_tap,
    prepare=prepare_long_tap,
    cleanup=cleanup
)

# print long_tap_use_case.run().duration

# -------------------------------------------------------------------------- #
def set_center(button):
    """Calculate the center of a uiobject."""
    button.centerY = (button.info['visibleBounds']["top"]+button.info['visibleBounds']["bottom"])/2
    button.centerX = (button.info['visibleBounds']["left"]+button.info['visibleBounds']["right"])/2


def prepare_dragndrop(use_case):    
    use_case.install_app()
    use_case.open_app()
    button1 = device(description="Button One")
    button2 = device(description="Button Two")
    button3 = device(description="Button Three")
    button_fab = device(description="Button Fab")
    text_area = device(description="Text Area")
    
    set_center(button1)
    set_center(button2)
    set_center(button3)
    set_center(button_fab)
    set_center(text_area)
    
    use_case.moves = [
        (button1, button2),
        (button2, button3),
        (button_fab, button3),
        (button_fab, text_area),
    ]
    
@minimum_execution_time(time_boundaries.DRAGNDROP)
def run_dragndrop(use_case):
    @minimum_execution_time(seconds=time_boundaries.DRAGNDROP_UNIT)
    def simple_routine():
        for first, second in use_case.moves:
            first.drag.to(second.centerX, second.centerY, steps=100)

    for _ in range(loop_count.DRAGNDROP):
        simple_routine()
    
dragndrop_use_case = AndroidUseCase(
    "PythonUiAutomator-dragndrop",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_dragndrop,
    prepare=prepare_dragndrop,
    cleanup=cleanup
)

# print dragndrop_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_swipe(use_case):
    use_case.install_app()
    use_case.open_app()
    paint = device(description="Paint")
    set_center(paint)
    use_case.x_i, use_case.y_i = (paint.centerX, paint.info['visibleBounds']["top"])

    
@minimum_execution_time(time_boundaries.SWIPE)
def run_swipe(use_case):
    @minimum_execution_time(seconds=time_boundaries.SWIPE_UNIT)
    def simple_routine(offset_y):
        # Swipe left
        swipe_distance=420
        steps=40
        x_f, y_f = (use_case.x_i-swipe_distance, use_case.y_i+offset_y+1)
        device.swipe(use_case.x_i, use_case.y_i+offset_y+1, x_f, y_f, steps=steps)
        # Swipe Right
        x_f, y_f = (use_case.x_i+swipe_distance, use_case.y_i+offset_y)
        device.swipe(use_case.x_i, use_case.y_i+offset_y, x_f, y_f, steps=steps)
    
    
    for i in range(loop_count.SWIPE):
        simple_routine(i*8)

    
swipe_use_case = AndroidUseCase(
    "PythonUiAutomator-swipe",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_swipe,
    prepare=prepare_swipe,
    cleanup=cleanup
)

# print swipe_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_pinch_and_spread(use_case):
    use_case.install_app()
    use_case.open_app()
    use_case.paint = device(description="Paint")

    
@minimum_execution_time(time_boundaries.PINCH_AND_SPREAD)
def run_pinch_and_spread(use_case):
    def simple_routine():
        # Pinch in
        use_case.paint.pinch.In(percent=50, steps=40)
        # Spread
        use_case.paint.pinch.Out(percent=50, steps=40)    
    
    for i in range(loop_count.PINCH_AND_SPREAD):
        simple_routine()

    
pinch_and_spread_use_case = AndroidUseCase(
    "PythonUiAutomator-pinch_and_spread",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_pinch_and_spread,
    prepare=prepare_pinch_and_spread,
    cleanup=cleanup
)

# print pinch_and_spread_use_case.run().duration

# -------------------------------------------------------------------------- #
    
@minimum_execution_time(time_boundaries.BACK_BUTTON)
def run_back_button(use_case):

    @minimum_execution_time(seconds=time_boundaries.BACK_BUTTON_UNIT, warning=False)
    def simple_routine():
            device.press.back()

    for _ in range(loop_count.BACK_BUTTON):
        simple_routine()
    
back_button_use_case = AndroidUseCase(
    "PythonUiAutomator-back_button",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_back_button,
    prepare=prepare,
    cleanup=cleanup
)

# print back_button_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_input_text(use_case):
    use_case.install_app()
    use_case.open_app()
    use_case.text_field = device(resourceId="com.tqrg.physalia.testapp:id/text_field")

@minimum_execution_time(seconds=time_boundaries.INPUT_TEXT)
def run_input_text(use_case):
    """Run script for input text interaction."""
    message = "Physalia says hi!"
    for _ in range(loop_count.INPUT_TEXT):
        use_case.text_field.set_text(message)
        use_case.text_field.clear_text()

input_text_use_case = AndroidUseCase(
    "PythonUiAutomator-input_text",
    APK,
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_input_text,
    prepare=prepare_input_text,
    cleanup=cleanup
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
