"""Experiments to measure idle time consumption of Android."""

import os
import time
import textwrap
import click
from physalia.energy_profiler import AndroidUseCase
from physalia.power_meters import MonsoonPowerMeter

def get_path(relative_path):
    """Get path relative to the source file."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), relative_path)
    )

APP_APK = get_path("../apks/testapp.apk")
APP_PKG = "com.tqrg.physalia.testapp"
APP_VERSION = "0.01"


@click.command()
@click.option('--count', default=30, type=click.IntRange(min=1))
@click.option('--output', default="results_human_consumption.csv", type=click.Path(dir_okay=False))
@click.option('--duration', default=60, type=click.IntRange(min=1))
@click.argument('interaction')
def experiment(count, output, duration, interaction):
    """Run human consumption experiment."""

    power_meter = MonsoonPowerMeter(voltage=3.8, serial=12886)
    
    def prepare(use_case):
        use_case.install_app()
        use_case.open_app()
        if interaction == "tap":
            click.secho(textwrap.fill(
                "Please, tap 40 times in the buttons 'Button One',"
                " 'Button Two', 'Button Three', and 'Button Fab', "
                "sequentially."
            ),fg='green',blink=True, bold=True)
        elif interaction == "long_tap":
            click.secho(textwrap.fill(
                "Please, long tap 40 times in the buttons 'Button One',"
                " 'Button Two', 'Button Three', and 'Button Fab', "
                "sequentially."
            ),fg='green',blink=True, bold=True)
        elif interaction == "dragndrop":
            click.secho((
                "Please, repeat the following set of drag and drop for 10 times:\n"
                " 1) 'Button One' -> 'Button Two',\n"
                " 2) 'Button Two' -> 'Button Three',\n"
                " 3) 'Button Fab' -> 'Button Three',\n"
                " 4) 'Button Fab' 'Text Area'."
            ),fg='green',blink=True, bold=True)
        elif interaction == "swipe":
            click.secho(textwrap.fill(
                "In the center of the drawing area, perform a swipe to the left"
                " of the screen and another to the right. Repeat this 40 times."
            ),fg='green',blink=True, bold=True)
        elif interaction == "back_button":
            click.secho(textwrap.fill(
                "Please, click on back button 200 times."
            ),fg='green',blink=True, bold=True)
        elif interaction == "pinch_and_spread":
            click.secho(textwrap.fill(
                "In paint area, perform a pinch in followed by a pinch out. "
                "Repeat this procedure for 40 times."
            ),fg='green',blink=True, bold=True)
        elif interaction == "input":
            click.secho(textwrap.fill(
                "Please, fill the text field with 'Physalia says hi!', "
                "then clear the field and repeat this for 10 times."
            ),fg='green',blink=True, bold=True)
        click.pause(info="Press any key to start ...",)
    
    def cleanup(use_case):
        """Clean environment after running."""
        use_case.uninstall_app()
    
    def run(_):
        click.pause(info="Press any key when you're done' ...",)
        # time.sleep(duration)

    use_case = AndroidUseCase(
        interaction,
        APP_APK,
        APP_PKG,
        APP_VERSION,
        run=run,
        prepare=prepare,
        cleanup=cleanup
    )
    use_case.profile(power_meter=power_meter,
                     count=count,
                     retry_limit=3,
                     save_to_csv=output)


def exit_gracefully(start_time):
    exit_time = time.time()
    duration = exit_time - start_time
    click.secho(
        "Physalia automators idle time exited in {:.2f} minutes.".format(duration/60),
        fg='blue'
    )

if __name__ == '__main__':
    start_time = time.time()
    try:
        experiment()
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully(start_time)
