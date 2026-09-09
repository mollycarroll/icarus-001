from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from supabase import create_client

load_dotenv()
from .config import SUPABASE_URL, SUPABASE_KEY, HF_MODEL, HF_TOKEN

app = FastAPI(title="Icarus backend")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

embeddings = HuggingFaceEndpointEmbeddings(
    model="BAAI/bge-m3",
    provider="hf-inference",
    huggingfacehub_api_token=HF_TOKEN,
)

vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)

llm_endpoint = HuggingFaceEndpoint(
    repo_id=HF_MODEL,
    provider="auto",
    temperature=0.3,
    max_new_tokens=1024,
    huggingfacehub_api_token=HF_TOKEN,
)
llm = ChatHuggingFace(llm=llm_endpoint)

system_prompt = """
You are Icarus, an AI chatbot created by Molly Carroll to represent her.

YOU ARE NOT MOLLY. You must ALWAYS speak ABOUT Molly in the THIRD PERSON only.
Never use "I" when referring to Molly's experience.

Your purpose is to answer job candidate questions about Molly using ONLY the provided context.

Key Facts:
- Molly invented and built you (Icarus) as a key portfolio project.
- This demonstrates a largely self-taught achievement that takes a veteran engineer to accomplish successfully.

Rules:
- Always use third person: "Molly has...", "Molly worked at...", "Molly built...".
- If the context does not contain the answer, reply: "I don't have enough information about that."
- Be friendly, confident, and professional.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ]
)

retriever = vector_store.as_retriever(search_kwargs={"k": 6})


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


class Query(BaseModel):
    question: str


@app.post("/chat")
async def chat(query: Query):
    answer = rag_chain.invoke(query.question)
    return {"answer": answer}


@app.get("/health")
async def health():
    return {"status": "healthy"}
