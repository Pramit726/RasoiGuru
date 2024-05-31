from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool
from langchain.tools.retriever import create_retriever_tool
from src.logger import logging
from src.exception import CustomException
import sys
from src.RasoiGuru.check_index import insert_docs, index_create
from src.RasoiGuru.data_ingestion import load_docs, make_chunks
from pinecone import Pinecone, ServerlessSpec
import os
from src.utils import get_paths

index_name = "rasoiguru"  # Define the name of the Pinecone index

# Function to create retrievers from vectorstores
def create_retriever(vectorstores):
    try:
        retrievers = []
        # Adding retriever to all vectorstores
        for vectorstore in vectorstores:
            retriever = vectorstore.as_retriever()
            retrievers.append(retriever)
        logging.info("Retrievers created successfully")
        return retrievers
    except Exception as e:
        logging.error("Error creating retrievers")
        raise CustomException(e, sys)

# Function to create Wikipedia tool
def create_wiki():
    try:
        # Define the Wikipedia tool
        wiki_tool = WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper(
                top_k_results=1,
                load_all_available_meta=False,
                doc_content_chars_max=500
            )
        )
        wiki_tool = Tool(
            name='Wikipedia',
            description='look up things in wikipedia for knowing about food recipes, cooking instructions and their history',
            func=wiki_tool.invoke
        )
        logging.info("Wikipedia tool created successfully")
        return wiki_tool
    except Exception as e:
        logging.error("Error creating Wikipedia tool")
        raise CustomException(e, sys)
    
# Function to create all search tools
def make_tools(wiki_tool, retrievers):
    tools = []
    try:
        tools_name = [
            'BHM-401T_pdf_search',
            'Book1_pdf_search',
            'Professional_Cooking_pdf_search',
            'USU-Student-Cookbook-FINAL-1_pdf_search'
        ]
        tools_desc = [
            "Indian food cooking and heritage related information use this tool",
            "For information related to any ingredient use this tool",
            "For professional cooking techniques, sanitization and safety in kitchen and food presentation tips use this tool",
            "For specific information about quick recipes for students and seasonal grocery shopping use this tool"
        ]

        # Iterate through tool names, descriptions, and retrievers to create search tools
        for name, desc, retv in zip(tools_name, tools_desc, retrievers):
            pdf_tool = create_retriever_tool(retv, name, desc, document_prompt="Search the query")
            tools.append(pdf_tool)

        # Adding wikipedia tool
        tools.append(wiki_tool)

        logging.info("Tools created successfully")
        
        return tools
    
    except Exception as e:
        logging.error("Error creating tools")
        raise CustomException(e, sys)

if __name__ == "__main__":
    pdf_files = get_paths()  # Get paths of PDF files
    docs = load_docs()  # Load documents from PDF files
    chunks = make_chunks(docs)  # Make chunks from documents
    pc = Pinecone()  # Initialize Pinecone
    cloud = os.environ.get('PINECONE_CLOUD') or 'aws'  # Get cloud provider from environment variables or default to 'aws'
    region = os.environ.get('PINECONE_REGION') or 'us-east-1'  # Get region from environment variables or default to 'us-east-1'
    spec = ServerlessSpec(cloud=cloud, region=region)  # Create serverless specification
    index = index_create(index_name, pc, spec)  # Create or retrieve Pinecone index
    vectorstores = insert_docs(index, pdf_files, chunks, index_name)  # Insert documents into Pinecone index
    retrievers = create_retriever(vectorstores)  # Create retrievers from vectorstores
    wiki_tool = create_wiki()  # Create Wikipedia tool
    tools = make_tools(wiki_tool, retrievers)  # Create all search tools