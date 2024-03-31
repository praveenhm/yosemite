from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.syntax import Syntax
from rich.markdown import Markdown
from art import text2art
import random

class RichText:
    """
    Dynamic, interchangeable text styling for the terminal using the Rich library.
    
    Attributes:
        console: A Rich Console instance for styled output.
    """
    def __init__(self):
        self.console = Console()

    def say(self, message, style="bold white"):
        """
        Style and print a single line of text using Rich.

        Example:
            ```python
            from yosemite.tools.text import Text

            text = Text()
            text.say("Hello, World!", style="bold red")
            ```

        Args:
            message (str): The message to be styled and printed.
            style (str, optional): The style of the text. Defaults to "bold white".
        """
        self.console.print(message, style=style)

    def list(self, items, style="white"):
        """
        Style and print a list of items using Rich Columns.

        Example:
            ```python
            from yosemite.tools.text import Text

            text = Text()
            text.list(["apple", "banana", "cherry"], style="green")
            ```

        Args:
            items (list): The items to be styled and printed.
            style (str, optional): The style of the text. Defaults to "white".
        """
        columns = Columns([Panel(item, expand=False) for item in items])
        self.console.print(columns, style=style)

    def splash(self, message="hammadpy", art="random"):
        """
        Creates an ASCII art styled splash 'logo' in the terminal using Rich Panel.

        Example:
            ```python
            from yosemite.tools.text import Text
            
            text = Text()
            text.splash("hammadpy", art="random")
            ```

        Args:
            message (str): The message to display in the splash. Defaults to "hammadpy".
            art (str): The ASCII art style to use. Defaults to "random".
        """
        if art == "random":
            fonts = ["block", "caligraphy", "doh", "dohc", "doom", "epic", "fender", "graffiti", "isometric1", "isometric2", "isometric3", "isometric4", "letters", "alligator", "dotmatrix", "bubble", "bulbhead", "digital", "ivrit", "lean", "mini", "script", "shadow", "slant", "speed", "starwars", "stop", "thin", "3-d", "3x5", "5lineoblique", "acrobatic", "alligator2", "alligator3", "alphabet", "banner", "banner3-D", "banner3", "banner4", "barbwire", "basic", "bell", "big", "bigchief", "binary", "block", "broadway", "bubble", "caligraphy", "doh", "dohc", "doom", "dotmatrix", "drpepper", "epic", "fender", "graffiti", "isometric1", "isometric2", "isometric3", "isometric4", "letters", "alligator", "dotmatrix", "bubble", "bulbhead", "digital", "ivrit", "lean", "mini", "script", "shadow", "slant", "speed", "starwars", "stop", "thin"]
            art = random.choice(fonts)

        art_message = text2art(message, font=art)
        panel = Panel(art_message, expand=False, border_style="bold dark_orange")
        self.console.print(panel)

def main():
    text = RichText()
    text.say("Hello Rich!", style="bold orange1")
    
    code = '''
def main():
    text = Text()
    text.say("Hello, Rich!")
    '''
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    text.console.print(syntax)

if __name__ == "__main__":
    main()