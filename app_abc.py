import os
import datetime
import sys
import time
import traceback
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import NamedTuple


# custom exceptions
class ExitApplication(Exception):
    """When raised exits Application."""

    def __init__(self, return_code:int=0):
        self.return_code = return_code


class HaltLoop(Exception):
    """When raised waits defined sleep time then skips to new loop iteration.""" \
    """When raised waits to press enter then skips to new loop iteration."""

    def __init__(self, sleep:float=None, text:str=None):
        self.sleep = sleep
        self.text = text


# class definition
class Application(ABC):

    def __init__(self, name:str, traceback:bool=False):
        self._name = name
        self._do_print_traceback = traceback

    @property
    def name(self) -> str:
        """Returns name of application."""

        return self._name

    @property
    def run_params(self) -> NamedTuple:
        """Returns named parameters passed to run method."""

        return self._run_params

    def run(self, **kwargs:dict):
        """Runs application loop while handling exceptions occured in the loop."""

        parameters = namedtuple("Parameters", list(kwargs.keys()))
        self._run_params = parameters(**kwargs)
        try:
            self.on_start()
            while True:
                try:
                    self.loop()
                except HaltLoop as halt_app:
                    if halt_app.sleep is None:
                        t = halt_app.text
                        t = "" if t is None else t
                        input(t)
                    else:
                        time.sleep(halt_app.sleep)
        except ExitApplication as exit_app:
            self.on_finish()

            # Message printed when application exits
            print("\n" + 40 * "=")
            print(f" Application: {self._name}")
            print(" Exit with code", exit_app.return_code)
            print()
            sys.exit(exit_app.return_code)
        except KeyboardInterrupt as exc:
            self._print_traceback("Keyboard interrupt")
            self.on_kb_interrupt()
            sys.exit(1)
        except Exception as exc:
            self._print_traceback()
            self.on_error(exc)
            sys.exit(1)

    @property
    def timestamp(self) -> str:
        """Returns string time stamp"""

        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _print_traceback(self, custom_message:str=None):
        """Writes traceback content to log file with option to print that to console."""

        traceback_text = traceback.format_exc() if custom_message is None else custom_message
        with open(f"{self.name}_error.log", "a") as logfile:
            logfile.write(f"{self.timestamp} *** {self.name} *** \n" + traceback_text + "\n\n")
        if self._do_print_traceback:
            print(f"\n\033[0;31m{traceback_text}\033[0m")

    @abstractmethod
    def loop(self): ...

    def on_start(self): ...

    def on_finish(self): ...

    def on_error(self, exc): ...

    def on_kb_interrupt(self): ...


# decorator
def autorun(name:str, traceback:bool=False, run_params:dict=None):
    """Instantiates application class and calls its run function."""

    def decorator(f):
        def wrapper():
            app = f(name, traceback)
            if run_params is None:
                app.run()
            else:
                app.run(**run_params)
        return wrapper()
    return decorator
