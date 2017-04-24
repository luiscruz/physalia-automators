"""Interaction using monkey runner.

Only works with Nexus 5X.
"""

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice


PACKAGE = "com.tqrg.physalia.testapp"
ACTIVITY = "com.tqrg.physalia.testapp.ScrollingActivity"
APK = '../apks/testapp.apk'

BUTTON_1 = (560, 580)
BUTTON_2 = (560, 705)
BUTTON_3 = (560, 830)
BUTTON_FAB = (965, 474)
TEXT_AREA = (560, 1610)

# -------------------------------------------------------------------------- #

def run_tap():
    elements = [
        BUTTON_1,
        BUTTON_2,
        BUTTON_3,
        BUTTON_FAB,
    ]
    device = MonkeyRunner.waitForConnection()
    for _ in range(10):
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
    for _ in range(10):
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
