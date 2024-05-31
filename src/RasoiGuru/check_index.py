from pinecone import Pinecone, ServerlessSpec
import os
import time
from langchain_pinecone import PineconeVectorStore
from langchain_cohere import CohereEmbeddings
from src.exception import CustomException
from src.logger import logging
import sys
from src.RasoiGuru.data_ingestion import load_docs, make_chunks
from src.utils import get_paths

# Function to create or retrieve an index
def index_create(index_name, pc, spec):
    try:  
        if index_name not in pc.list_indexes().names():
            # Create a new index if it doesn't exist
            pc.create_index(
                    index_name,
                    dimension=4096,  
                    metric='cosine',
                    spec=spec
                )
        
        # Retrieve the index
        index = pc.Index(index_name)
        # Wait a moment for connection
        time.sleep(1)
        # Describe the index statistics
        index.describe_index_stats() 
        logging.info("Index created successfully") 

        return index
        
    except Exception as e:
        logging.info("Error creating index")
        # Raise a custom exception
        raise CustomException(e, sys)


# Function to insert documents into the index
def insert_docs(index, pdf_files, contents, index_name):
        ns = ["ns" + path.stem for path in pdf_files]  # Generate namespaces for documents
        try:
            embedding_model = CohereEmbeddings()  # Load the embedding model
            logging.info("Embedding model loaded")
        except Exception as e:
            logging.info("Error loading embedding model")
            # Raise a custom exception
            raise CustomException(e, sys)

        vectorstores = []
        # If no vectors are present in the index
        if index.describe_index_stats()['total_vector_count'] == 0:
            try:
                for namespace, content in zip(ns, contents):
                    # Create vector stores for each document
                    vectorstore = PineconeVectorStore.from_texts(
                        texts=content,
                        index_name=index_name,
                        embedding=embedding_model,
                        namespace=namespace
                    )
                    vectorstores.append(vectorstore)
                logging.info("Inserted the vectors")

            except Exception as e:
                logging.error("Error inserting vectors")
                # Raise a custom exception
                raise CustomException(e, sys)
        else:
            try:
                for namespace in ns:
                    # Retrieve vector stores from an existing index
                    vectorstore = PineconeVectorStore.from_existing_index(index_name, embedding_model, namespace=namespace)
                    vectorstores.append(vectorstore)
                logging.info("Received the vector stores from an existing index")
            
            except Exception as e:
                logging.error("Error retrieving vector stores from an existing index")
                # Raise a custom exception
                raise CustomException(e, sys)
        
        return vectorstores

        

# Main function
if __name__== "__main__":
    # Get paths of PDF files
    pdf_files = get_paths()
    # Load documents from PDF files
    docs = load_docs()
    # Make chunks of documents
    chunks = make_chunks(docs)
    # Initialize Pinecone client
    pc = Pinecone()
    # Specify index name
    index_name = "rasoiguru"
    # Specify cloud provider and region
    cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
    region = os.environ.get('PINECONE_REGION') or 'us-east-1'
    # Specify serverless specification
    spec = ServerlessSpec(cloud=cloud, region=region)
    # Create or retrieve the index
    index = index_create(index_name, pc, spec)
    # Insert documents into the index
    vectorstores = insert_docs(index, pdf_files, chunks, index_name)

