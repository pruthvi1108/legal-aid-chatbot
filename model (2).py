import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Legal Aid Chatbot API")

# 1. Initialize Embeddings and Vector Store ONCE upon starting the app to save memory
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vectorstore = Chroma(persist_directory="./legal_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 2. Define the Request Model
class QueryRequest(BaseModel):
    question: str

# 3. Define the POST endpoint BEFORE mounting the static files
@app.post("/ask")
async def ask_chatbot(request: QueryRequest):
    try:
        # Fetch the key from environment variables or use a default
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set in the environment.")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.3,
            api_key=api_key
        )

        template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer clear and in plain language, suitable for a legal aid chatbot.
Always cite the source document when providing a right or law.

{context}

Question: {question}
Helpful Answer:"""
        
        QA_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_PROMPT},
        )
        
        response = qa_chain.invoke({"query": request.question})
        return {
            "answer": response["result"],
            "sources": [
                doc.metadata for doc in response["source_documents"]
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Mount the Static website AFTER API endpoints have been declared
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("model:app", host="127.0.0.1", port=8000, reload=True)