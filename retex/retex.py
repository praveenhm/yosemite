import marimo

__generated_with = "0.3.8"
app = marimo.App()


@app.cell(hide_code=True)
def __():
    from assets.yosemitecommon import YosemiteNotebookCommon
    note = YosemiteNotebookCommon()
    note.init()
    note.display_title(title="RETEX", header="Retrieval-Enhanced Text Generation with Experts")
    return YosemiteNotebookCommon, note


@app.cell(hide_code=True)
def __(note):
    note.display_header("Retrieval Augmented Generation")
    note.box_text_code(title="Goal I - Simple Modular RAG", content="At the very least, you need to build a pipeline with a few stages to properly setup RAG. Below is sample outline of libraries that would be necessary and still not the full list needed to properly achieve this goal. As a developer at home, it is a huge hassle building such a long pipeline for a simple concept.",language="python", code=str(f"""
    # Parsing Libraries \n
    from parser_x import PDF
    from parser_y import Text
    from ... import Image, GraphParser, etc...

    # NLP
    from cleaner import TextCleaner, ..Tokenizer, Chunker
    from transformer import SentenceTransformer, CrossEncoder, ..SimilaritySearch

    # Most Cases would Require a PreExisting Database Service
    # Database Service & Libraries
    from database.service import DatabaseClient, Search Client

    # Vector Index & Search
    from vector_library import IndexCreator, IndexSearcher
    ....
    """))
    return


@app.cell(hide_code=True)
def __(note):
    note.display_subtitle("Lets Build the RAG Database!")
    return


@app.cell
def __():
    from yosemite.llms import RAG
    return RAG,


@app.cell
def __(RAG):
    # Initialize RAG Pipeline & LLM Provider
    rag = RAG()
    return rag,


@app.cell
def __(rag):
    # Create & Build a Database for the RAG to Use
    # Use Provided Documents
    rag.build("documents")
    return


@app.cell(hide_code=True)
def __(note):
    note.display_subtitle("Did it work? Lets Search the Database and Find Out.")
    return


@app.cell
def __(rag):
    # Keyword Search
    rag.search("Lightning Mcqueen", k=3)
    return


@app.cell
def __(rag):
    rag.db.search_and_rank("lightning mcqueen")
    return


@app.cell(hide_code=True)
def __(note):
    note.display_subtitle("Lets Query our LLM Now!")
    return


@app.cell
def __(rag):
    rag.invoke("What did lightning mcqueen say about Mater?")
    return


if __name__ == "__main__":
    app.run()
