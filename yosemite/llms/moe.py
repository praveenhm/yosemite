from yosemite.llms import RAG, LLM
from typing import Optional, List, Union

class MixtureOfExperts:
    def __init__(self, provider: Optional[str] = "openai", api_key: Optional[str] = None, model: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key
        self.model_name_or_path = model
        self.llm = None
        if not model and api_key:
            self.llm = LLM(provider=provider)
        elif model and api_key:
            self.llm = LLM(provider=provider, api_key=api_key, model=model)
        elif model and not api_key:
            self.llm = LLM(provider=provider, model=model)
        elif not model and not api_key:
            self.llm = LLM()
        else:
            self.llm = LLM()
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
            if model:
                response = RAG.invoke(query=query, model=model)
                response = str(response)
            else:
                response = RAG.invoke(query=query)
            expert_responses.append(response)

        system_prompt = f"""
# CONTEXT
Responses:
{expert_responses}

Using the knowledge provided by a few sources, as well as your own understanding and the relevant information to provide a comprehensive and insightful response to the query. 
Synthesize the information from all sources to generate a well-informed and helpful answer. Please make sure your response is clear, concise, and accurate. Your response should use natural, organic language any human
can understand.

# OBJECTIVE
Do not explcitly mention your knowledge of the above information; simple use it as context for your response.

# QUERY
{query}
"""

        if self.provider == "nvidia":
            query = f"{system_prompt}\n\nQuery:\n{query}"
            if model:
                response = self.llm.invoke(
                    query=query,
                    model=self.model_name_or_path
                )
            else:
                response = self.llm.invoke(
                    query=query,
                    model="mistral"
                )
        else:
            response = self.llm.invoke(
                system=system_prompt,
                query=query
            )

        return response