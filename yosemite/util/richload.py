from rich.console import Console
from rich.status import Status
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.live import Live
from rich.table import Table
import time
import random

class RichLoader:
    """Displays an animated loading status using the Rich library.

    Attributes:
        message (str): The message to be displayed while loading.
        spinner (str): The spinner style to be used for the loading animation.
    """

    def __init__(self, message: str = "Loading...", spinner: str = "dots"):
        """
        Initializes the RichLoader with a message and spinner style.

        Example:
            ```python
            from yosemite.tools.load import RichLoader

            loader = RichLoader(message="Processing data", spinner="dots")
            with loader:
                time.sleep(2)
                loader.update("Processing step 1")
                time.sleep(2)
                loader.update("Processing step 2")
                time.sleep(2)
            ```

        Args:
            message (str, optional): The message to be displayed while loading. Defaults to "Loading...".
            spinner (str, optional): The spinner style to be used for the loading animation. Defaults to "dots".
        """
        self.console = Console()
        self.message = message
        self.spinner = spinner

    def __enter__(self):
        self.status = Status(self.message, spinner=self.spinner)
        self.status.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.status.stop()

    def update(self, message: str):
        """Updates the loading message while the loader is running.

        Example:
            ```python
            loader = RichLoader()
            with loader:
                time.sleep(2)
                loader.update("Processing step 1")
                time.sleep(2)
                loader.update("Processing step 2")
                time.sleep(2)
            ```

        Args:
            message (str): The updated message to be displayed.
        """
        self.status.update(message)

class RichProgress:
    """Displays a progress bar using the Rich library.

    Attributes:
        total (int): The total number of steps in the progress.
    """

    def __init__(self, total: int):
        """
        Initializes the RichProgress with the total number of steps.

        Example:
            ```python
            from yosemite.tools.load import RichProgress

            progress = RichProgress(total=100)
            with progress:
                for i in range(100):
                    progress.update(i)
                    time.sleep(0.1)
            ```

        Args:
            total (int): The total number of steps in the progress.
        """
        self.console = Console()
        self.total = total

    def __enter__(self):
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console,
        )
        self.task = self.progress.add_task("[cyan]Processing...", total=self.total)
        self.progress.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.progress.stop()

    def update(self, completed: int):
        """Updates the progress bar with the number of completed steps.

        Args:
            completed (int): The number of completed steps.
        """
        self.progress.update(self.task, completed=completed)

class RichLiveTable:
    """Displays a live updating table using the Rich library."""

    def __init__(self):
        """
        Initializes the RichLiveTable.

        Example:
            ```python
            from yosemite.tools.load import RichLiveTable

            table = RichLiveTable()
            with table:
                for i in range(10):
                    table.add_row(f"Row {i}", str(random.randint(0, 100)))
                    time.sleep(1)
            ```
        """
        self.console = Console()
        self.table = Table(show_header=True, header_style="bold magenta")
        self.table.add_column("Item", style="dim")
        self.table.add_column("Value")

    def __enter__(self):
        self.live = Live(self.table, console=self.console)
        self.live.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.live.stop()

    def add_row(self, item: str, value: str):
        """Adds a row to the live updating table.

        Args:
            item (str): The item name.
            value (str): The item value.
        """
        self.table.add_row(item, value)


if __name__ == "__main__":
    loader = RichLoader(message="Processing data", spinner="dots")

    with loader:
        time.sleep(2)
        loader.update("Processing step 1")
        time.sleep(2)
        loader.update("Processing step 2")
        time.sleep(2)

    print()

    progress = RichProgress(total=100)
    with progress:
        for i in range(100):
            progress.update(i)
            time.sleep(0.05)

    print()

    table = RichLiveTable()
    with table:
        for i in range(10):
            table.add_row(f"Row {i}", str(random.randint(0, 100)))
            time.sleep(1)