from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from src.logger import logging
from src.exception import CustomException
import sys
from src.RasoiGuru.data_ingestion import load_docs, make_chunks
from src.RasoiGuru.check_index import index_create, insert_docs
from src.RasoiGuru.create_tools import create_retriever, create_wiki, make_tools
from pinecone import Pinecone, ServerlessSpec
import os
from src.utils import get_paths

llm = ChatGroq(model="mixtral-8x7b-32768")  # Initialize a large language model for chat interactions

# Function to create the prompt template
def create_prompt(tools):
    try:
        system_instruction = """
        You are a helpful cooking assistant named Rasoiguru.
        Greet the user.
        Answer the following questions as best you can in terms of a passionate and helpful professional cooking assistant.
        """

        format = """
        Use the following format:

        Use the chat history which will be provided to you for understanding the context of the most recent conversation in case user query is not clearly defined.
        Question: the input question you must answer.
        Thought: you should always think about what to do.
        Action: the action to take, should be one of the provided tools.
        Action Input: the input to the action.
        Observation: the result of the action.
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer.
        Final Answer: the final answer to the original input question.

        Remember to answer as a compassionate professional cooking assistant when giving your final answer.
        """

        prefix = f""" You have access to the following tools:
        Tools:
        {tools}
        Instruction:
        {system_instruction}.
        """

        suffix = """Begin! Now answer the question
        {intermediate_steps}
        Chat history:
        {chat_history}
        Question: {input}
        {agent_scratchpad}
        ## In case the user query is not about food cooking, grocery shopping, and history of food,
        then reply I do not know the answer to your question.
        ## You need to always provide the answer after writing Final Answer: \
        """

        prompt = PromptTemplate(
            input_variables=["input", "chat_history", "intermediate_steps", "agent_scratchpad"],
            template= prefix + format + suffix
        )

        logging.info("Prompt created successfully")

        return prompt

    except Exception as e:
        logging.info("Error occurred while creating the prompt")
        raise CustomException(e, sys)


# Function to create agent and agent executor
def create_agent(prompt, memory, tools):
    ## Agent creation
    try:
        agent = create_tool_calling_agent(llm, tools=tools, prompt=prompt)  # Create an agent calling the specified tools using the language model and prompt
        logging.info("Agent created successfully")
        
    except Exception as e:
        logging.info("Error occurred while creating the agent")
        raise CustomException(e, sys)

    ## Agent Executor
    try:
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)  # Create an agent executor with the created agent, tools, and memory
        logging.info("Agent executor created successfully")
        return agent_executor
    
    except Exception as e:
        logging.info("Error occurred while creating the agent executor")
        raise CustomException(e, sys)



if __name__ == "__main__":
    pdf_files = get_paths()  # Get paths of PDF files
    docs = load_docs()  # Load documents from PDF files
    chunks = make_chunks(docs)  # Make chunks from documents
    pc = Pinecone()  # Initialize Pinecone
    index_name = "rasoiguru"  # Define the name of the Pinecone index
    cloud = os.environ.get('PINECONE_CLOUD') or 'aws'  # Get cloud provider from environment variables or default to 'aws'
    region = os.environ.get('PINECONE_REGION') or 'us-east-1'  # Get region from environment variables or default to 'us-east-1'
    spec = ServerlessSpec(cloud=cloud, region=region)  # Create serverless specification
    index = index_create(index_name, pc, spec)  # Create or retrieve Pinecone index
    vectorstores = insert_docs(index, pdf_files, chunks, index_name)  # Insert documents into Pinecone index
    retrievers = create_retriever(vectorstores)  # Create retrievers from vectorstores
    wiki_tool = create_wiki()  # Create Wikipedia tool
    tools = make_tools(wiki_tool, retrievers)  # Create all search tools
    prompt = create_prompt(tools)  # Create prompt template
    memory = ConversationBufferWindowMemory(k=3, return_messages=True)  # Initialize conversation memory
    executor = create_agent(prompt, memory, tools)  # Create agent executor