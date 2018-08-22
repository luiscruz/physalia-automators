"""Experiments to measure idle time consumption of Android."""

import os
import time
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
@click.option('--output', default="results_idle_time.csv", type=click.Path(dir_okay=False))
def experiment(count, output):
    """Run idle time experiment."""

    power_meter = MonsoonPowerMeter(voltage=3.8, serial=12886)
    
    def prepare(use_case):
        use_case.install_app()
        use_case.open_app()
    
    def cleanup(use_case):
        """Clean environment after running."""
        use_case.uninstall_app()
    
    def run(_):
        time.sleep(120)

    use_case = AndroidUseCase(
        "idle_time",
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
