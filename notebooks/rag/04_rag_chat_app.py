
from yosemite.llms import RAG, Chat

rag = RAG()
rag.create("databases/db")

chat = Chat(rag)
chat.serve()