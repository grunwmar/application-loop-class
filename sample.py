from app_abc import Application, autorun
import os
import sys

@autorun(name="MyApp1", traceback=True)
class MyApp1(Application):

    def onstart(self):
        self.count = 0

    def main(self):
        cmd = input(f"[{self.count}] To leave enter 'x': ").strip()
        if cmd.lower() in ["x"]:
            return 0
        self.count += 1

    def exit(self, retval):
        sys.exit(retval)

    def onfinish(self):
        print("Leaving...")


# this part of code cannot be reached when decorator autorun is used
# my_app1 = MyApp1("MyApp1")
# my_app1.run()
