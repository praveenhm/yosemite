import argparse
from yosemite.tools.text import Text

def display_greeting():
    text = Text()
    text.say("Yosemite | 0.1.xx Half Dome", bg="rgb(135, 192, 207)", bold=True)
    text.say("https://github.com/yosemiteml/yosemite", color="rgb(128, 128, 128)", italic=True)
    text.say("")

def help_command(args):
    text = Text()
    text.say("CLI functionality Coming Soon...", color="rgb(135, 192, 207)", bold=True)

def invoke_command(args):
    text = Text()
    text.say("CLI functionality Coming Soon...", color="rgb(135, 192, 207)", bold=True)

def list_command(args):
    text = Text()
    text.say("CLI functionality Coming Soon...", color="rgb(135, 192, 207)", bold=True)

def main():
    text = Text()
    parser = argparse.ArgumentParser(description="Yosemite CLI")
    subparsers = parser.add_subparsers(dest="command")

    help_parser = subparsers.add_parser("help", help="Display help information")
    invoke_parser = subparsers.add_parser("invoke", help="Invoke a specific functionality")
    list_parser = subparsers.add_parser("list", help="List available options", aliases=["ls"])

    args = parser.parse_args()

    if args.command:
        if args.command == "help":
            help_command(args)
        elif args.command == "invoke":
            invoke_command(args)
        elif args.command == "list":
            list_command(args)
    else:
        display_greeting()
        text.say("Available Commands:", color="rgb(135, 192, 207)", bold=True)
        text.say("yosemite help", color="rgb(123, 133, 152)", italic=True)
        text.say("yosemite invoke", color="rgb(123, 133, 152)", italic=True)
        text.say("yosemite list", color="rgb(123, 133, 152)", italic=True)

if __name__ == "__main__":
    main()