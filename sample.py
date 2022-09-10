from app_abc import Application, autorun
import os
import sys

@autorun(name="MyApp1", traceback=False)
class MyApp1(Application):

    def onstart(self):
        self.greetings = "Leaving app..."

    def onfinish(self):
        print(self.greetings)

    def main(self):
        print(">>>")

        cmd = input("To exit enter 'exit': ").strip()
        if cmd.lower() in ["exit"]:
            return 0

    def exit(self, retval):
        sys.exit(retval)


# this part of code cannot be reached when decorator autorun is used
# my_app1 = MyApp1("MyApp1")
# my_app1.run()
