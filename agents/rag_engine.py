from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
import os

load_dotenv()

def get_rag_engine():
    try:
        documents = SimpleDirectoryReader("data/regulatory_docs").load_data()
        index = VectorStoreIndex.from_documents(documents)
        return index.as_query_engine()
    except:
        return None

query_engine = get_rag_engine()

def query_rag(query):
    if query_engine:
        response = query_engine.query(query)
        return str(response)
    else:
        # Fallback to Groq
        from groq import Groq
        client = Groq()
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"Industrial safety expert: {query}"}]
        )
        return resp.choices[0].message.content
