"""Utils used for the creation of tests."""

from functools import partial
import time
import os
import click

def minimum_execution_time(seconds, warning=True):
    def ret_fun(fun):
        def repl(*args, **kwargs):    
            start = time.time()
            finish = start + seconds
            return_value = fun(*args, **kwargs)
            if time.time() < finish:
                time.sleep(finish-time.time())
            else:
                if warning and seconds != -1:
                    click.secho(
                        "Warning: execution time boundary exceed by {:.1f}s."
                        .format(time.time()-finish),
                        fg='yellow'
                    )
            return return_value
        return repl
    return ret_fun
# minimum_execution_time = partial(_partial_minimum_execution_time, argument='seconds')

def get_path(relative_path):
    """Get path relative to the source file."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), relative_path)
    )