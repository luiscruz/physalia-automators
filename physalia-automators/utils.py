"""Utils used for the creation of tests."""

from functools import partial
import time

def minimum_execution_time(seconds):
    def ret_fun(fun):
        def repl(*args, **kwargs):    
            start = time.time()
            finish = start + seconds
            return_value = fun(*args, **kwargs)
            if time.time() < finish:
                time.sleep(finish-time.time())
            return return_value
        return repl
    return ret_fun
# minimum_execution_time = partial(_partial_minimum_execution_time, argument='seconds')