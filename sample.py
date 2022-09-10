from app_abc import Application, autorun, HaltLoop, ExitApplication
import os

#@autorun(name="MyApp1", traceback=True)
class MyApp1(Application):

    def on_start(self):
        print("Level", self.run_params.level)
        self.greetings = "Hello World from MyApp1"

    def on_finish(self):
        print(self.greetings)

    def loop(self):
        print("Hello 1")
        q = input("Exit? [y/n]: ").strip()
        print()
        if q.lower() in ["y", "yes"]:
            raise ExitApplication
        else:
            print("Waiting 2 seconds")
            raise HaltLoop(sleep=1)


# this part of code cannot be reached when decorator autorun is used
my_app1 = MyApp1("MyApp1", traceback=True)
my_app1.run(level=1)
