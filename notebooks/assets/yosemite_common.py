from IPython.display import HTML, display

class Html:
    def __init__(self):
        pass

    def html_title(self) -> str:
        self.html = """
        <!-- TailwindCSS CDN --> <script src="https://cdn.tailwindcss.com"></script>

        <!-- Lexend Variable Font --> <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">

        <!-- JetBrains Mono Variable Font --> <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@100..800&display=swap" rel="stylesheet">

        <style>

        .lex { font-family: 'Lexend', sans-serif; }

        .jet { font-family: 'JetBrains Mono', monospace; }

        .sky { color: #D6EEF2; }

        .skybg { background-color: #D6EEF2; }

        .blue { color: #4D8DAC; }

        .bluebg { background-color: #4D8DAC; }

        .cream { color: #F2E2D6; }

        .creambg { background-color: #F2E2D6; }

        .peach { color: #F9E0C7; }

        .peachbg { background-color: #F9E0C7; }

        .orange { color: #D1AA8A; }

        .orangebg { background-color: #D1AA8A; }

        .olive { color: #9DBE9A; }

        .olivebg { background-color: #9DBE9A; }

        .darkolive { color: #6B8C6E; }

        .darkolivebg { background-color: #6B8C6E; }

        .green { color: #E0F0D6; }

        .greenbg { background-color: #E0F0D6; }

        .orchid { color: #AC4D8D; }

        .orchidbg { background-color: #AC4D8D; }

        </style>

        <div class="darkolivebg p-4 w-full flex flex-col rounded-md mb-2 space-y-4">

        <div class="w-full flex justify-center">

        <span class="lex peach font-medium text-3xl">

        Yosemite 🏞️

        </span>

        </div>

        </div>
        """
        return self.html

    def display_title(self):
        display(HTML(self.html_title()))

    def html_subtitle(header: str = None) -> str:
        return 

    def display_subtitle(self, header = None):
        self.subtitle = f"""
        <div class="creambg p-4 w-full flex flex-col rounded-md mb-2 space-y-4">

        <div class="w-full flex justify-center">

        <span class="lex olive font-medium text-2xl">

        {header}

        </span>

        </div>

        </div>
        """
        
        display(HTML(self.subtitle))