from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.logger import logging
from src.exception import CustomException
import sys
from src.utils import get_paths


# Function to load documents from PDF files
def load_docs():
    
    # Get paths of PDF files
    pdf_files = get_paths()
    
    try:
        docs = []
        # Iterate through PDF files and load each document
        for filepath in pdf_files:
            print(filepath)
            loader = PyPDFLoader(filepath)
            docs.append(loader.load())
        
        logging.info("Loaded the PDF documents")

        return docs

    except Exception as e:
        logging.info("Error occurred while loading the PDF documents")
        # Raise a custom exception
        raise CustomException(e, sys)


# Function to split documents into chunks
def make_chunks(docs):
    try:
        documents = []
        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        # Iterate through documents and split each document into chunks
        for doc in docs:
            splitted_docs = text_splitter.split_documents(doc)
            documents.append(splitted_docs)
        
        logging.info("Chunks created")
        
    except Exception as e:
        logging.error("Error in chunking")
        # Raise a custom exception
        raise CustomException(e, sys)

    try:
        contents = []
        # Iterate through splitted documents and retrieve page content
        for document in documents:
            page_content = []
            for pages in range(len(document)):
                page_content.append(document[pages].page_content)
            contents.append(page_content)
        
        logging.info("Page content retrieved")
        
        return contents
        
    except Exception as e:
        logging.error("Error in page content retrieval")
        # Raise a custom exception
        raise CustomException(e, sys)

# Main function to load documents and create chunks
if __name__  == "__main__":
    # Load documents from PDF files
    docs = load_docs()
    # Create chunks from loaded documents
    chunks = make_chunks(docs)
