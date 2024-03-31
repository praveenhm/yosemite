import marimo

__generated_with = "0.3.8"
app = marimo.App()


@app.cell(hide_code=True)
def __():
    from lib.yosemitecommon import YosemiteNotebookCommon
    ynbc = YosemiteNotebookCommon()
    ynbc.html_init()
    ynbc.display_header("ROCK-STaR")
    return YosemiteNotebookCommon, ynbc


@app.cell(hide_code=True)
def __(ynbc):
    ynbc.display_header("Getting Started - Concept")
    ynbc.box_subtitle("I | Micro-Scaled Retrieval Augmented Generation")
    return


@app.cell
def __():
    # Building A Singular RAG Client
    # Super High Level

    # Import RAG From Yosemite
    from yosemite.llms import RAG

    # Initialize & Build RAG From Sample Documents
    rag = RAG()
    rag.build("documents/")

    # Perform a Simple Cross-Encoded & Ranked Search
    query = "Who is going to win the Piston Cup?"
    rag.search(query)
    return RAG, query, rag


if __name__ == "__main__":
    app.run()
