import os
import datetime
import sys
import time
import traceback
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import NamedTuple


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
            self.onstart()
            while True:
                retval = self.main()
                if retval is not None:
                    if isinstance(retval, int):
                        self.onfinish()
                        self.exit(retval)
                        break
                    else:
                        raise ValueError("return value must be an integer")
        except KeyboardInterrupt as exc:
            self._print_traceback("Keyboard interrupt")
            self.onkeyboardinterrupt()
            print()
        except Exception as exc:
            self._print_traceback()
            self.onerror(exc)
        finally:
            self.exit(1)


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
    def main(self): ...

    @abstractmethod
    def exit(self): ...

    def onstart(self): ...

    def onfinish(self): ...

    def onerror(self, exc): ...

    def onkeyboardinterrupt(self): ...


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
