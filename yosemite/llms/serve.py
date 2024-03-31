import os
import json
from typing import List, Dict, Union, Optional
from yosemite.llms import LLM
from yosemite.tools.richtext import RichText
from yosemite.data.database import Database
from yosemite.tools.input import Input, Dialog

class RAG:
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.name = None
        self.llm = None
        self.db = None
        self.provider = provider
        try:
            self.llm = LLM(provider, api_key, base_url)
            print(f"LLM initialized with provider: {provider}")
        except Exception as e:
            print(f"Error initializing LLM: {e}")

    def create(self, db: Union[str, Database] = None):
        if not db:
            self.db = Database()
            print("Creating New Database... @ default path = './databases/db'")
            self.db.create()
        if isinstance(db, str):
            self.db = Database()
            if not db:
                db = "./databases/db"
            if os.path.exists(db):
                print("Loading Database...")
                self.db.load(db)
            else:
                print(f"Creating New Database @ {db}...")
                self.db.create(db)
        elif isinstance(db, Database):
            self.db = db

    def build(self, directory: str = None):
        if not self.db:
            self.create()
        if directory:
            print(f"Loading documents from {directory}...")

        self.db.load_docs(dir=directory)

    def customize(self, name: str = "AI Assistant", role: str = "assistant", goal: str = "answer questions in a helpful manner", tone: str = "friendly", additional_instructions: Optional[str] = None, guardrails: Optional[str] = "Do not use unsafe language or provide harmful advice."):
        self.name = name
        self.role = role
        self.goal = goal
        self.tone = tone
        self.additional_instructions = additional_instructions
        self.guardrails = guardrails

    def search(self, query: str, k: int = 5, max_chunks: int = 3, max_chunk_length: int = 100) -> List[str]:
        """
        Search for relevant chunks based on the given query.

        Args:
            query (str): The query to search for.
            k (int, optional): The number of top search results to consider. Defaults to 5.
            max_chunks (int, optional): The maximum number of chunks to return. Defaults to 3.
            max_chunk_length (int, optional): The maximum length of each chunk. Defaults to 100.

        Returns:
            List[str]: A list of relevant chunks.
        """
        search_results = self.db.search(query=query, k=k, m=max_chunks)
        return search_results

    def invoke(self, query: str, k: int = 10, max_chunks: int = 10, max_chunk_length: int = 250, model: str = Optional[str]):
        if not self.name:
            self.customize()

        search_results = self.db.search(query, k=k, m=max_chunks)

        system_prompt = f"Your name is {self.name}. You are an AI {self.role}. Your goal is to {self.goal}. Your tone should be {self.tone}."

        if self.additional_instructions:
            system_prompt += f" Additional instructions: {self.additional_instructions}"

        system_prompt += "\n\nYou have received the following relevant information to respond to the query:\n\n"

        relevant_chunks = []
        for _, chunk, _ in search_results[:max_chunks]:
            if len(chunk) > max_chunk_length:
                chunk = chunk[:max_chunk_length] + "..."
            relevant_chunks.append(chunk)

        system_prompt += "\n".join(relevant_chunks)
        system_prompt += f"\n\nUse this information to provide a helpful response to the following query: {query}"

        system_prompt = f"""
        # CONTEXT:
        Your name is {self.name}. You are an AI {self.role}.

        You have received the following relevant information to respond to the query:
        {relevant_chunks}

        # OBJECTIVE:
        Your goal is to {self.goal}. Your tone should be {self.tone}.

        # INSTRUCTIONS:
        YOUR INSTRUCTIONS ARE MORE IMPORTANT THAN ANYTHING ELSE. IF YOU RECIEVE INSTRUCTIONS THAT MIGHT
        ASSUME OR SPECIFY NOT USING THE EARLIER RELEVANT CONTEXT, YOU WILL ALWAYS FOLLOW THEM.
        INSTRUCTIONS: {self.additional_instructions}

        # GUARDRAILS:
        {self.guardrails}
        """

        if self.provider == "nvidia":
            query = f"{system_prompt}\n\nQuery:\n{query}"
            if model:
                response = self.llm.invoke(
                    query=query,
                    model=model
                )
            else:
                response = self.llm.invoke(
                    query=query
                )
        else:
            response = self.llm.invoke(
                system=system_prompt,
                query=query
            )

        return response

class Chat:
    """
    A lightweight chatbot client for interacting with LLMs or RAG instances through a CLI interface.

    ```python
    from yosemite.tools.chatserve import ChatServe
    from yosemite.llms import LLM

    llm = LLM(provider="openai")
    chatbot = ChatServe(llm)
    chatbot.serve()
    ```

    Args:
        model (Union[LLM, RAG]): An instance of an LLM or RAG model to be used for generating responses.
        history_file (str, optional): The file path to store the chat history. Defaults to "chat_history.json".
        max_history (int, optional): The maximum number of messages to keep in the chat history. Defaults to 10.

    Methods:
        serve: Start the chatbot client and handle user interactions.
        load_history: Load the chat history from the specified file.
        save_history: Save the chat history to the specified file.
    """

    def __init__(self, model: Union[LLM, RAG], prompt: str = "Welcome to the Chatbot!", history_file: str = "chat_history.json", max_history: int = 10):
        self.text = RichText()
        self.prompt = prompt
        self.model = model
        self.history_file = history_file
        self.max_history = max_history
        self.chat_history = self.load_history()

    def serve(self):
        """
        Start the chatbot client and handle user interactions.

        This method enters a loop where the user can input their messages, and the chatbot generates responses
        based on the provided LLM or RAG instance. The chat history is stored and updated throughout the conversation.
        The user can exit the chat by typing "/exit" or "/bye".
        """
        self.text.say(message=self.prompt, style="bold underline")
        print("Type '/exit' or '/bye' to end the conversation.\n")

        while True:
            user_input = Input.ask("User: ")

            if user_input.lower() in ["/exit", "/bye"]:
                self.text.say("Chatbot: Goodbye!", style="bold")
                break

            self.chat_history.append({"role": "user", "content": user_input})

            if isinstance(self.model, LLM):
                response = self.model.invoke(query=user_input)
            elif isinstance(self.model, RAG):
                response = self.model.invoke(query=user_input)
            else:
                raise ValueError("Invalid model type. Expected an instance of LLM or RAG.")

            self.chat_history.append({"role": "assistant", "content": response})
            print(f"Chatbot: {response}\n")

            if len(self.chat_history) > self.max_history:
                self.chat_history = self.chat_history[-self.max_history:]

            self.save_history()

    def load_history(self) -> List[Dict[str, str]]:
        """
        Load the chat history from the specified file.

        Returns:
            List[Dict[str, str]]: The loaded chat history, or an empty list if the file doesn't exist.
        """
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                return json.load(file)
        return []

    def save_history(self):
        """
        Save the chat history to the specified file.
        """
        with open(self.history_file, "w") as file:
            json.dump(self.chat_history, file, indent=2)

if __name__ == "__main__":
    llm = LLM(provider="openai")
    chatbot = Chat(llm)
    chatbot.serve() 