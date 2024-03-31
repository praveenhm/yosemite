from IPython.display import HTML, display
from IPython.core.interactiveshell import InteractiveShell

class YosemiteNotebookCommon:
    def __init__(self):
        pass

    def init(self) -> str:
        self.html = """
        <!-- TailwindCSS CDN --> <script src="https://cdn.tailwindcss.com"></script>

        <!-- Lexend Variable Font --> <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">

        <!-- JetBrains Mono Variable Font --> <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@100..800&display=swap" rel="stylesheet">

        <script>Jupyter.notebook.hide_input_code = true;</script>
        <style>

        .dark { color: #54565D; }

        .darkbg { background-color: #22262E; }

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

        """

        self.title=f"""

        <div class="darkbg p-4 w-full flex flex-col rounded-md mb-2">

        <div class="w-full flex flex-col space-y-[8px] dark">

        <span class="font-medium text-sm jet">

        Hammad Saeed

        </span>

        <span class="font-medium text-sm jet">

        hammad@supportvectors.com

        </span>

        </div>

        </div>

        <div class="darkbg p-4 w-full flex flex-col rounded-md mb-2 space-y-2">

        <span class="font-medium text-lg lex">

        Yosemite

        </span>

        </div>
        """
        display(HTML(self.html))
        display(HTML(self.title))

    def display_title(self, title: str, header: str = None):
        self.header = f"""
        <div class="darkolivebg p-4 w-full flex flex-col rounded-md mb-2 space-y-2">

        <span class="lex peach font-medium text-3xl">

        {title}

        </span>

        <span class="lex peach font-light text-2xl">

        {header}

        </span>

        </div>
        """
        
        display(HTML(self.header))


    def display_header(self, header: str = None):
        self.header = f"""
        <div class="darkbg p-4 w-full flex flex-col rounded-md mb-2 space-y-2">

        <div class="w-full flex justify-center">

        <span class="lex peach font-medium text-3xl">

        {header}

        </span>

        </div>

        </div>
        """
        
        display(HTML(self.header))

    def display_image(self, image: str = None):
        self.image = f"""
        <div class="w-full flex justify-center">

        <img src="{image}" class="w-1/2 h-1/2 rounded-md" />

        </div>
        """
        
        display(HTML(self.image))

    def display_subtitle(self, header = None):
        self.subtitle = f"""
        <div class="darkbg p-4 w-full flex flex-col rounded-md mb-2 space-y-4">

        <div class="w-full flex">

        <span class="lex peach font-medium text-2xl">

        {header}

        </span>

        </div>

        </div>
        """
        
        display(HTML(self.subtitle))

    def display_code(self, code: str = None):
        self.code = f"""
        <div class="bluebg p-4 w-full flex flex-col rounded-md mb-2 space-y-4">

        <div class="w-full flex">

        <span class="jet font-medium text-sm">

        {code}

        </span>

        </div>

        </div>
        """
        
        display(HTML(self.code))

    def display_text(self, markdown: str = None):
        self.markdown = f"""
        <div class="creambg p-4 w-full flex flex-col rounded-md mb-2 space-y-4">

        <div class="w-full flex">

        <span class="font-medium dark text-sm">

        {markdown}

        </span>

        </div>

        </div>
        """
        
        display(HTML(self.markdown))

    def box_text(self, title: str, content: str):
        box = f"""
        <div class="darkolivebg p-4 w-full flex flex-col rounded-md mb-2 space-y-4">
        <h2 class="lex cream font-medium text-2xl">{title}</h2>
        <p class="font-medium peach text-sm">{content}</p>
        </div>
        """
        display(HTML(box))

    def box_subtitle(self, title: str):
        box = f"""
        <div class="creambg p-4 w-full flex flex-col rounded-md mb-2 space-y-4">
        <h2 class="lex darkolive font-medium text-2xl">{title}</h2>
        </div>
        """
        display(HTML(box))

    def box_code(self, code: str):
        box = f"""
        <div class="darkbg p-4 w-full flex flex-col rounded-md mb-2 space-y-4">
        <code class="jet font-medium text-sm">{code}</code>
        </div>
        """
        display(HTML(box))

    def box_text_code(self, title: str, content: str, code: str, language: str = "python"):
        box = f"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">
<script>hljs.highlightAll();</script>

        <div class="darkbg p-4 w-full flex flex-col rounded-md mb-2 space-y-4">
        <h2 class="lex cream font-medium text-2xl">{title}</h2>
        <p class="font-medium cream text-sm">{content}</p>
        <pre class="w-full language-python"><code class=" language-{language}">
        {code}
        </code></pre>
        </div>
        """
        display(HTML(box))
    