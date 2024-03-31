class Moe_Text:    
    INTRODUCTION_TEXT = """
    STaR (Self-Taught Reasoner) is a technique that allows language models to iteratively improve their reasoning abilities. It works by having the model generate step-by-step rationales to answer questions, and then fine-tuning the model on the rationales that led to correct answers. By repeating this process, the model bootstraps its own reasoning capabilities using a small number of initial examples. 
    The ROCK-STaR framework takes this architechture in the form of using many different 'experts' with shared or different knowledge bases, that come together collectively to answer a question.
    """