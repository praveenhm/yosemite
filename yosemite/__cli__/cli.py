import argparse
import time
import random
from rich import print as rprint
from yosemite.util.richtext import RichText

def hello(args):
    text = RichText()

    colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    choice1 = random.choice(colors)
    choice2 = random.choice(colors)
    rprint(f"[bold {choice1}]Hello Yosemite![/bold {choice1}]")
    time.sleep(0.35)
    text.splash(f"Yosemite", art="random")
    
def help(args):
    rprint("Usage: yosemite [command]")
    rprint("Available commands:")
    rprint("  hello   ")
    rprint("  help    Show this help message")
    rprint("  make    'make' is coming soon!")

def make(args):
    rprint("Placeholder for the 'make' command")

def cli():
    parser = argparse.ArgumentParser(description="Yosemite CLI")
    subparsers = parser.add_subparsers(dest="command")

    hello_parser = subparsers.add_parser("hello", help="Print 'Hello Yosemite!'")
    hello_parser.set_defaults(func=hello)

    help_parser = subparsers.add_parser("help", help="Show help message")
    help_parser.set_defaults(func=help)

    make_parser = subparsers.add_parser("make", help="Placeholder for the 'make' command")
    make_parser.set_defaults(func=make)

    args = parser.parse_args()

    if args.command is None:
        help(args)
    else:
        args.func(args)

if __name__ == "__main__":
    cli()