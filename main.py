import multiprocessing as mp
import rumps
import dialogs
from os_functions import open_github, show_code

# set detction method
detection_method = "v2"

# This is the class defining the Mac MenuBar item which is the main user
# interface and center of the app
class MenuBar(rumps.App):

    started = 0       # will be 1 or 0, 1 when the app is running, 0 when it is paused

    @rumps.clicked("More","Help/About")
    def help_about(self, _):
        dialogs.help_dialog()

    @rumps.clicked("Start")
    def start(self, sender):
        if self.started == 0:
            dialogs.start_dialog()
            if detection_method == "v1":
                self.p1 = mp.Process(target=main_loop)
            elif detection_method == "v2":
                self.p1 = mp.Process(target=main_loop_v2) #to initialize the second method of detecting viruses
            self.p1.start()
            self.started = 1
        else :
            dialogs.already_started()

    @rumps.clicked("Pause")
    def pause(self, _):
        if self.started == 1:
            dialogs.pause_dialog()
            self.started = 0
            self.p1.terminate()
            self.p1.join()
        else :
            dialogs.wrong_pause()

    @rumps.clicked("More","Single File Check")
    def single_file_check(self, _):
        result = dialogs.file_dialog()
        if detection_method == "v1":
            self.p2 = mp.Process(target=one_file, args = (result,))
        elif detection_method == "v2":
            self.p2 = mp.Process(target=one_file_v2, args = (result,)) #to initialize the second method of detecting viruses
        self.p2.start()

    @rumps.clicked("More", "Help us! Share a Virus")
    def share(self, _):
        open_github()

    @rumps.clicked("More", "Peek at the Code")
    def code(self,_):
        show_code()

    @rumps.clicked("Quit App")
    def quit_app(self, _):
        if self.started == 1:
            self.p1.terminate()
            self.p1.join()
        rumps.quit_application()

# Startup of Anti-virus File App
dialogs.intro()
if __name__ == "__main__":
    app = MenuBar("Anti-🦠", quit_button=None)
    dialogs.wait()

    # this will start  loading the viruses, can take some time
    if detection_method == "v1":
        from loop_and_onefile import main_loop, one_file
    elif detection_method == "v2":
        from loop_and_onefile_v2 import main_loop_v2, one_file_v2

    app.start(0)
    app.menu = [
    "Start",
    "Pause",
    None,
    ["More",["Help/About","Single File Check","Help us! Share a Virus", "Peek at the Code"]],
    None,
    "Quit App",
    ]
    app.run()
