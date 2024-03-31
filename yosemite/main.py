from yosemite.tools.input import Input, Dialog
from yosemite.tools.richload import RichLoader, RichLiveTable, RichProgress
from yosemite.tools.richtext import RichText
from yosemite.tools.ui import InlineUI

class Yosemite:
    def __init__(self):
        self.text = RichText()
        self.input = Input()
        self.dialog = Dialog()
        self.progress = RichProgress()
        self.loader = RichLoader()
        self.table = RichLiveTable()
        self.ui = InlineUI()
    
    def say(self, message : str, style : str = "bold white"):
        self.text.say(message, style=style)

    def list(self, items : list, style : str = "white"):
        self.text.list(items, style=style)

    def art(self, message : str= "yosemite", art : str= "random"):
        self.text.splash(message, art=art)

if __name__ == "__main__":
    import time

    yosemite = Yosemite()
    yosemite.say("Hello, Yosemite!", style="bold red")
        
    name = yosemite.input.ask("What is your name?")

    name = yosemite.dialog.ask("What is your name?")

    with yosemite.loader:
        time.sleep(0.2)
        yosemite.loader.update("Processing step 1")
        time.sleep(0.3)
        yosemite.loader.update("Processing step 2")
        time.sleep(0.2)

    ui = InlineUI()
    ui.create()
    ui.add_button(text="Hello.")
    ui.run()