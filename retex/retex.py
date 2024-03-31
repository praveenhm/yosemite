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


@app.cell
def __():
    # The Entire Pipeline is Accesible Using Two Modules
    from yosemite.llms import RAG, MixtureOfExperts
    return MixtureOfExperts, RAG


if __name__ == "__main__":
    app.run()
