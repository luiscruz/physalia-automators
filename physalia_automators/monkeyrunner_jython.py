"""Interaction using monkey runner.

Only works with Nexus 5X.
"""

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from constants import loop_count
import sys

PACKAGE = "com.tqrg.physalia.testapp"
ACTIVITY = "com.tqrg.physalia.testapp.ScrollingActivity"
APK = '../apks/testapp.apk'

BUTTON_1 = (560, 580)
BUTTON_2 = (560, 705)
BUTTON_3 = (560, 830)
BUTTON_FAB = (965, 474)
TEXT_FIELD = (560, 950)
PAINT_TOP = (560, 1012)
TEXT_AREA = (560, 1610)

# -------------------------------------------------------------------------- #

def run_find_by_id():
    elements = [
        "com.tqrg.physalia.testapp:id/button_1",
        "com.tqrg.physalia.testapp:id/button_2",
        "com.tqrg.physalia.testapp:id/button_3",
        "com.tqrg.physalia.testapp:id/text_field",
        "com.tqrg.physalia.testapp:id/fab",
        "com.tqrg.physalia.testapp:id/paint",
        "com.tqrg.physalia.testapp:id/text_area",
    ]
    device = MonkeyRunner.waitForConnection()
    for _ in range(loop_count.FIND_BY_ID):
        for element in elements:
            device.getViewById(element).getLocation()

# -------------------------------------------------------------------------- #

def run_tap():
    elements = [
        BUTTON_1,
        BUTTON_2,
        BUTTON_3,
        BUTTON_FAB,
    ]
    device = MonkeyRunner.waitForConnection()
    for _ in range(loop_count.TAP):
        for element in elements:
            device.touch(
                element[0],
                element[1],
                MonkeyDevice.DOWN_AND_UP
            )
            MonkeyRunner.sleep(1)

# -------------------------------------------------------------------------- #

def run_long_tap():
    elements = [
        BUTTON_1,
        BUTTON_2,
        BUTTON_3,
        BUTTON_FAB,
    ]
    device = MonkeyRunner.waitForConnection()
    for _ in range(loop_count.LONG_TAP):
        for element in elements:
            device.touch(
                element[0],
                element[1],
                MonkeyDevice.DOWN
            )
            MonkeyRunner.sleep(1)
            device.touch(
                element[0],
                element[1],
                MonkeyDevice.UP
            )

# -------------------------------------------------------------------------- #

def run_dragndrop():
    moves = [
        (BUTTON_1, BUTTON_2),
        (BUTTON_2, BUTTON_3),
        (BUTTON_FAB, BUTTON_3),
        (BUTTON_FAB, TEXT_AREA),
    ]
    device = MonkeyRunner.waitForConnection()
    for _ in range(loop_count.DRAGNDROP):
        for first, second in moves:
            device.drag(
                first,
                second,
                0.5,
                100
            )

# -------------------------------------------------------------------------- #

def run_swipe():
    x_i, y_i = PAINT_TOP
    device = MonkeyRunner.waitForConnection()

    def simple_routine(offset_y):
        # Swipe left
        swipe_distance=420
        steps=40
        x_f, y_f = (x_i-swipe_distance, y_i+offset_y+1)
        device.drag((x_i, y_i+offset_y+1), (x_f, y_f), 0.4, steps)
        # Swipe Right
        x_f, y_f = (x_i+swipe_distance, y_i+offset_y)
        device.drag((x_i, y_i+offset_y), (x_f, y_f), 0.4, steps)

    for i in range(loop_count.SWIPE):
        simple_routine(i*8)

# -------------------------------------------------------------------------- #

def run_back_button():
    device = MonkeyRunner.waitForConnection()
    for _ in range(loop_count.BACK_BUTTON):
        device.press("KEYCODE_BACK", MonkeyDevice.DOWN_AND_UP)

# run_back_button()

# -------------------------------------------------------------------------- #

def run_input_text():
    device = MonkeyRunner.waitForConnection()
    len_message = 17
    for _ in range(loop_count.INPUT_TEXT):
        device.type("Physalia")
        device.press("SPACE", MonkeyDevice.DOWN_AND_UP)
        device.type("says")
        device.press("SPACE", MonkeyDevice.DOWN_AND_UP)
        device.type("hi!")
        for _ in range(17):
            device.press("KEYCODE_DEL", MonkeyDevice.DOWN_AND_UP)    

# run_input_text()

if len(sys.argv) == 2:
    method_name = sys.argv[1]
    exec(method_name+"()")

# -------------------------------------------------------------------------- #
#
# def run_multi_finger_tap():
#     elements = [
#         BUTTON_1,
#         BUTTON_2,
#         BUTTON_3,
#         BUTTON_FAB,
#         TEXT_AREA,
#     ]
#     device = MonkeyRunner.waitForConnection()
#     for _ in range(10):
#         for idx, el in enumerate(elements):
#             prev_el = elements[idx-1]
#             device.touch(
#                 el[0],
#                 el[1],
#                 MonkeyDevice.DOWN
#             )
#             device.touch(
#                 prev_el[0],
#                 prev_el[1],
#                 MonkeyDevice.DOWN
#             )
#             device.touch(
#                 el[0],
#                 el[1],
#                 MonkeyDevice.UP
#             )
#             device.touch(
#                 prev_el[0],
#                 prev_el[1],
#                 MonkeyDevice.UP
#             )
#             MonkeyRunner.sleep(1)
#
# run_multi_finger_tap()
