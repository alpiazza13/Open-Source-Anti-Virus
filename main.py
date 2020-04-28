from loop_and_onefile import main_loop, one_file
from loop_and_onefile_v2 import main_loop_v2, one_file_v2
import multiprocessing as mp
import rumps
import dialogs
from os_functions import open_github

# This is the class defining the Mac MenuBar item which is the main user
# interface and center of the app
class MenuBar(rumps.App):

    started = 0       # will be 1 or 0, 1 when the app is running, 0 when it is paused

    @rumps.clicked("Help/About")
    def help_about(self, _):
        dialogs.help_dialog()

    @rumps.clicked("Start")
    def start(self, _):
        if self.started == 0:
            dialogs.start_dialog()
            self.p1 = mp.Process(target=main_loop)
            # self.p1 = mp.Process(target=main_loop_v2) #to initialize the second method of detecting viruses
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

    @rumps.clicked("Single File Check")
    def set_time(self, _):
        result = dialogs.file_dialog()
        self.p2 = mp.Process(target=one_file, args = (result,))
        # self.p2 = mp.Process(target=one_file_v2, args = (result,)) #to initialize the second method of detecting viruses
        self.p2.start()

    @rumps.clicked("Help us! Share a Virus")
    def share(self, _):
        open_github()

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
    app.menu = [
    "Help/About",
    None,
    "Start",
    "Pause",
    None,
    "Single File Check",
    None,
    "Help us! Share a Virus",
    None,
    "Quit App",
    ]
    app.run()
