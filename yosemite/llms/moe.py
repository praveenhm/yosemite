from yosemite.llms import RAG
from typing import Optional, List, Union

class MixtureOfExperts:
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key
        self.base_url = base_url
        self.RAGs = []

    def create(self, rags: Union[RAG, List[RAG]]):
        if isinstance(rags, RAG):
            self.RAGs = [rags]
        elif isinstance(rags, list):
            self.RAGs = rags
        else:
            raise ValueError("Invalid input. Expected a RAG instance or a list of RAG instances.")

    def invoke(self, query: str, k: int = 10, max_chunks: int = 10, max_chunk_length: int = 250, model: str = Optional[str]):
        expert_responses = []
        for RAG in self.RAGs:
            response = RAG.invoke(query, k, max_chunks, max_chunk_length, model)
            expert_responses.append(response)

        system_prompt = f"""
You are presented with the following expert responses to the query: {query}

Expert Responses:
{expert_responses}

Using the knowledge provided by the experts, as well as your own understanding and the relevant information from your vector-searched chunks, please provide a comprehensive and insightful response to the query. Synthesize the information from all sources to generate a well-informed and helpful answer.
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