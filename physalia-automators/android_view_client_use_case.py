"""Interaction using Android View Client."""

import sys
import click
from physalia.energy_profiler import AndroidUseCase
from com.dtmilano.android.viewclient import ViewClient
from utils import minimum_execution_time
import time_boundaries


class AndroidViewClientUseCase(AndroidUseCase):
    """`AndroidUseCase` to use with `AndroidViewClient`."""

    # pylint: disable=too-many-arguments
    # Eight is reasonable in this case.

    def __init__(self, name, app_apk, app_pkg, app_version,
                 run, prepare=None, cleanup=None):  # noqa: D102
        super(AndroidViewClientUseCase, self).__init__(
            name, app_apk, app_pkg, app_version,
            run, prepare, cleanup
        )
        self.device = None
        self.serialno = None
        self.view_client = None

    def get_device_model(self, serialno=None):
        """Find out which is the current connected device model.

        Use serialno if a device is already connected
        using `AndroidViewClient`.
        """
        if serialno is None:
            serialno = self.serialno
        super(AndroidViewClientUseCase, self).get_device_model(serialno)

    def start_view_client(self, force=False):
        """Setup `AndroidViewClient`.

        Args:
            force (boolean): force start even if it was previously done (default False).
        """
        # pylint: disable=attribute-defined-outside-init

        if self.view_client is None or force is True:
            original_argv = sys.argv
            sys.argv = original_argv[:1]
            kwargs1 = {'ignoreversioncheck': False,
                       'verbose': False,
                       'ignoresecuredevice': False}
            device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
            kwargs2 = {'forceviewserveruse': False,
                       'useuiautomatorhelper': False,
                       'ignoreuiautomatorkilled': True,
                       'autodump': False,
                       'startviewserver': True,
                       'compresseddump': True}
            view_client = ViewClient(device, serialno, **kwargs2)
            sys.argv = original_argv
            self.device = device
            self.serialno = serialno
            self.view_client = view_client
        #always refresh
        self.refresh()

    def prepare(self):
        """Prepare environment for running.

        Setup Android View Client in order to run experiments.
        """
        self.start_view_client()
        self._prepare()

    def refresh(self):
        """Refresh `AndroidViewClient`."""
        while True:
            try:
                self.view_client.dump(window='-1')
            except RuntimeError:
                continue
            break

    def wait_for_id(self, view_id):
        """Refresh `AndroidViewClient` until view id is found."""
        view = self.view_client.findViewById(view_id)
        while view is None:
            self.refresh()
            view = self.view_client.findViewById(view_id)
        return view

    def wait_for_text(self, text):
        """Refresh `AndroidViewClient` until text is found."""
        view = self.view_client.findViewWithText(text)
        while view is None:
            self.refresh()
            view = self.view_client.findViewWithText(text)
        return view

    def wait_for_content_description(self, content_description):
        """Refresh `AndroidViewClient` until content description is found."""
        view = self.view_client.findViewWithContentDescription(
            content_description
        )
        while view is None:
            self.refresh()
            view = self.view_client.findViewWithContentDescription(
                content_description
            )
        return view


def prepare(use_case):
    use_case.install_app()
    use_case.open_app()
    use_case.wait_for_id("com.tqrg.physalia.testapp:id/button_1")
    

def cleanup(use_case):
    """Clean environment after running."""
    use_case.uninstall_app()


# -------------------------------------------------------------------------- #

@minimum_execution_time(time_boundaries.FIND_BY_ID)
def run_find_by_id(use_case):
    for _ in range(40):
        use_case.view_client.findViewById("com.tqrg.physalia.testapp:id/button_1")
        use_case.view_client.findViewById("com.tqrg.physalia.testapp:id/button_2")
        use_case.view_client.findViewById("com.tqrg.physalia.testapp:id/button_3")
        use_case.view_client.findViewById("com.tqrg.physalia.testapp:id/text_field")
        use_case.view_client.findViewById("com.tqrg.physalia.testapp:id/fab")
        use_case.view_client.findViewById("com.tqrg.physalia.testapp:id/paint")
        use_case.view_client.findViewById("com.tqrg.physalia.testapp:id/text_area")

find_by_id_use_case = AndroidViewClientUseCase(
    "AndroidViewClient-find_by_id",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_find_by_id,
    prepare=prepare,
    cleanup=cleanup
)

# print find_by_id_use_case.run().duration

# -------------------------------------------------------------------------- #

@minimum_execution_time(time_boundaries.FIND_BY_DESCRIPTION)
def run_find_by_description(use_case):
    for _ in range(40):
        use_case.view_client.findViewWithContentDescription("Button One")
        use_case.view_client.findViewWithContentDescription("Button Two")
        use_case.view_client.findViewWithContentDescription("Button Three")
        use_case.view_client.findViewWithContentDescription("Button Fab")
        use_case.view_client.findViewWithContentDescription("Text Field")
        use_case.view_client.findViewWithContentDescription("Paint")
        use_case.view_client.findViewWithContentDescription("Text Area")
    
find_by_description_use_case = AndroidViewClientUseCase(
    "AndroidViewClient-find_by_description",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_find_by_description,
    prepare=prepare,
    cleanup=cleanup
)

# print find_by_description_use_case.run().duration

# -------------------------------------------------------------------------- #

@minimum_execution_time(time_boundaries.FIND_BY_CONTENT)
def run_find_by_content(use_case):
    for _ in range(40):
        use_case.view_client.findViewWithText(text="Button 1")
        use_case.view_client.findViewWithText(text="Button 2")
        use_case.view_client.findViewWithText(text="Button 3")
    
find_by_content_use_case = AndroidViewClientUseCase(
    "AndroidViewClient-find_by_content",
    "../apks/testapp.apk",
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
        use_case.wait_for_content_description("Button One"),
        use_case.view_client.findViewWithContentDescription("Button Two"),
        use_case.view_client.findViewWithContentDescription("Button Three"),
        use_case.view_client.findViewWithContentDescription("Button Fab"),
        use_case.view_client.findViewWithContentDescription("Text Area"),
    ]
    
@minimum_execution_time(time_boundaries.TAP)
def run_tap(use_case):
    for _ in range(10):
        for el in use_case.elements:
            el.click()
    
tap_use_case = AndroidViewClientUseCase(
    "AndroidViewClient-tap",
    "../apks/testapp.apk",
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
        use_case.wait_for_content_description("Button One"),
        use_case.view_client.findViewWithContentDescription("Button Two"),
        use_case.view_client.findViewWithContentDescription("Button Three"),
        use_case.view_client.findViewWithContentDescription("Button Fab"),
        use_case.view_client.findViewWithContentDescription("Text Area"),
    ]
    
@minimum_execution_time(time_boundaries.LONG_TAP)
def run_long_tap(use_case):
    for _ in range(10):
        for el in use_case.elements:
            el.longTouch()
    
long_tap_use_case = AndroidViewClientUseCase(
    "AndroidViewClient-long_tap",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_long_tap,
    prepare=prepare_long_tap,
    cleanup=cleanup
)

# print long_tap_use_case.run().duration

# -------------------------------------------------------------------------- #

def prepare_dragndrop(use_case):    
    use_case.install_app()
    use_case.open_app()
    button1 = use_case.wait_for_content_description("Button One")
    button2 = use_case.view_client.findViewWithContentDescription("Button Two")
    button3 = use_case.view_client.findViewWithContentDescription("Button Three")
    button_fab = use_case.view_client.findViewWithContentDescription("Button Fab")
    text_area = use_case.view_client.findViewWithContentDescription("Text Area")

    print button1.getCenter()
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
            duration = 500
            use_case.device.drag(first.getCenter(), second.getCenter(), duration)

    for _ in range(10):
        simple_routine()
    
dragndrop_use_case = AndroidViewClientUseCase(
    "AndroidViewClient-dragndrop",
    "../apks/testapp.apk",
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
    paint = use_case.wait_for_content_description("Paint")
    use_case.x_i, use_case.y_i = (paint.getCenter()[0], paint.getY())

    
@minimum_execution_time(time_boundaries.SWIPE)
def run_swipe(use_case):
    @minimum_execution_time(seconds=time_boundaries.SWIPE_UNIT)
    def simple_routine(offset_y):
        # Swipe left
        swipe_distance=420
        steps=800
        x_f, y_f = (use_case.x_i-swipe_distance, use_case.y_i+offset_y+1)
        use_case.view_client.swipe(use_case.x_i, use_case.y_i+offset_y+1, x_f, y_f, steps=steps)
        # Swipe Right
        x_f, y_f = (use_case.x_i+swipe_distance, use_case.y_i+offset_y)
        use_case.view_client.swipe(use_case.x_i, use_case.y_i+offset_y, x_f, y_f, steps=steps)
    
    
    for i in range(40):
        simple_routine(i*8)

    
swipe_use_case = AndroidViewClientUseCase(
    "AndroidViewClient-swipe",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_swipe,
    prepare=prepare_swipe,
    cleanup=cleanup
)

# print swipe_use_case.run().duration

# -------------------------------------------------------------------------- #

# No pinch and spread

# -------------------------------------------------------------------------- #
    
@minimum_execution_time(time_boundaries.BACK_BUTTON)
def run_back_button(use_case):

    @minimum_execution_time(seconds=time_boundaries.BACK_BUTTON_UNIT, warning=False)
    def simple_routine():
            use_case.device.press('BACK')

    for _ in range(200):
        simple_routine()
    
back_button_use_case = AndroidViewClientUseCase(
    "AndroidViewClient-back_button",
    "../apks/testapp.apk",
    "com.tqrg.physalia.testapp",
    "0.01",
    run=run_back_button,
    prepare=prepare,
    cleanup=cleanup
)

print back_button_use_case.run().duration

