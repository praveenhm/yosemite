
from IPython.display import HTML, display, IFrame, Image, Audio
from typing import Optional, List, Union

class YosemiteNotebookCommon:
    def __init__(self):
        self.style = """
<!-- TailwindCSS CDN --> <script src="https://cdn.tailwindcss.com"></script>
<!-- Lexend Variable Font --> <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">
<!-- JetBrains Mono Variable Font --> <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@100..800&display=swap" rel="stylesheet">

        <style>
        .primary_box { width: 100%;
                       padding: 1rem;
                       margin: 0.5rem 0;
                       border-radius: 0.5rem;
                       display: flex;
                       flex-direction: column;
                       space-between: 1rem;
                       background-color: #6B8C6E;
                    }
        .splash-box { width: 100%;
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 0.5rem;
                display: flex;
                flex-direction: column;
                space-between: 1rem;
                background-color: #4D8DAC;
            }
        .secondary_box { width: 100%;
                       padding: 1rem;
                       margin: 0.5rem 0;
                       border-radius: 0.5rem;
                       display: flex;
                       flex-direction: column;
                       space-between: 1rem;
                       background-color: #F2E2D6;
        code { font-family: 'JetBrains Mono', monospace; }
        .dark { color: #54565D; }
        .darkbg { background-color: #22262E; }
        .lex { font-family: 'Lexend Variable', sans-serif; }
        .jet { font-family: 'JetBrains Mono Variable', monospace; }
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
        display(HTML(self.style))

    def yosemite(self):
        yosemite = """
        <div class="splash_box darkbg">
        <span style="width: 100%; display: flex; flex-direction: column; space-between: 4px;">
        <span class="jet dark">hammad saeed</span>
        <span class="jet dark">hammad@supportvectors.com</span>
        </span>
        <span class="dark lex">Yosemite</span>
        </div>
        """
        display(HTML(yosemite))

    def splash(self, title: str):
        splash = f"""
        <div class="primary_box">
            <h1>{title}</h1>
        </div>
        """
        display(HTML(splash))

    def box_text(self, title: str, content: str):
        box = f"""
        <div class="primary_box">
            <h2>{title}</h2>
            <p>{content}</p>
        </div>
        """
        display(HTML(box))

    def box_code(self, code: str):
        box = f"""
        <div class="primary_box">
            <code>{code}</code>
        </div>
        """
        display(HTML(box))

    def box_text_code(self, title: str, content: str, code: str):
        box = f"""
        <div class="primary_box">
            <h2>{title}</h2>
            <p>{content}</p>
            <code>{code}</code>
        </div>
        """
        display(HTML(box))

    def box_image(self, title: str, image_path: str):
        box = f"""
        <div class="primary_box">
            <h2>{title}</h2>
            <img src="{image_path}" alt="{title}" />
        </div>
        """
        display(HTML(box))

    def box_audio(self, title: str, audio_path: str):
        box = f"""
        <div class="primary_box">
            <h2>{title}</h2>
            <audio controls>
                <source src="{audio_path}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </div>
        """
        display(HTML(box))

    def box_video(self, title: str, video_path: str):
        box = f"""
        <div class="primary_box">
            <h2>{title}</h2>
            <video width="320" height="240" controls>
                <source src="{video_path}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        """
        display(HTML(box))