from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
import uuid
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from src.RasoiGuru.data_ingestion import load_docs, make_chunks
from src.RasoiGuru.check_index import index_create, insert_docs
from src.RasoiGuru.create_tools import create_retriever, create_wiki, make_tools
from src.RasoiGuru.generation import create_prompt, create_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from src.utils import vector_exist, extract_answer, get_paths

# Load environment variables from a .env file
load_dotenv()

# Set the GROQ_API_KEY environment variable to the value retrieved from .env file
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Set the COHERE_API_KEY environment variable to the value retrieved from .env file
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")

# Set the PINECONE_API_KEY environment variable to the value retrieved from .env file
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

# Enable Langsmith tracking by setting the LANGCHAIN_TRACING_V2 environment variable to "true"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Set the LANGCHAIN_API_KEY environment variable to the value retrieved from .env file
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


# Initialize FastAPI app
app = FastAPI(
    title="RasoiGuru",
    description="RasoiGuru is your ultimate cooking assistant chatbot, offering detailed cooking instructions, ingredient substitutions, and personalized culinary tips to elevate your kitchen skills."
)

# Define input model
class Input(BaseModel):
    query: str

# Initialize Pinecone
pc = Pinecone()
index_name = "rasoiguru"
cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'
spec = ServerlessSpec(cloud=cloud, region=region)

# Memory store for session management
memory_store = {}

# Route to welcome page
@app.get("/", summary="Welcome", tags=["Welcome"])
def welcome():
    return "Welcome to RasoiGuru"

# Function to get memory for session management
def get_memory(session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = ConversationBufferWindowMemory(k=3, return_messages=True, memory_key="chat_history")
    return memory_store[session_id]

# Route for chat functionality
@app.post("/chat", summary="Chat with RasoiGuru", tags=["Chat"], response_model=Input)
def chat(input: Input, request: Request):
    # Generate a unique session ID for each user session
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    
    memory = get_memory(session_id)

    # Check if vector index exists, if not, create index and insert documents
    if not vector_exist(index_name, pc):
        pdf_files = get_paths()
        docs = load_docs()
        chunks = make_chunks(docs)
    else:
        pdf_files = get_paths()
        chunks = []

    index = index_create(index_name, pc, spec)
    vectorstores = insert_docs(index, pdf_files, chunks, index_name)

    # Create retrievers, wiki tool, and other tools
    retrievers = create_retriever(vectorstores)
    wiki_tool = create_wiki()
    tools = make_tools(wiki_tool, retrievers)

    # Create prompt, executor, and get response
    prompt = create_prompt(tools)
    executor = create_agent(prompt, memory, tools)
    response = executor.invoke({"input": input.query})
    result = extract_answer(response)
    response_data = {'input': input.query, 'output': result}

    # Set session ID cookie and return response
    response = JSONResponse(content=response_data)
    response.set_cookie(key="session_id", value=session_id)
    return response
