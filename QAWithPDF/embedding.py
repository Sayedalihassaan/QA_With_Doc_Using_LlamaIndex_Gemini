# QAWithPDF/embedding.py
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core import Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from QAWithPDF.data_ingestion import load_data
import sys
from exception import CustomException
from logger import logging
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def load_model():
    """
    Load the Gemini language model.
    
    Returns:
    - Initialized Gemini LLM.
    """
    try:
        logging.info("Loading Gemini LLM...")
        model = Gemini(model_name="gemini-1.5-flash", api_key=GOOGLE_API_KEY)
        logging.info("Gemini LLM loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Exception in loading Gemini LLM: {str(e)}")
        raise CustomException(e, sys)

def gemini_embedding(model, documents):
    """
    Create a query engine using Gemini embeddings and the provided model.

    Parameters:
    - model: Initialized LLM model.
    - documents: List of documents from load_data.

    Returns:
    - Query engine for answering questions.
    """
    try:
        logging.info("Initializing Gemini embedding model...")
        gemini_embed_model = GeminiEmbedding(model_name="models/embedding-001", api_key=GOOGLE_API_KEY)
        
        logging.info("Configuring global settings...")
        Settings.llm = model
        Settings.embed_model = gemini_embed_model
        Settings.chunk_size = 800
        Settings.chunk_overlap = 20
        
        logging.info("Building vector index...")
        index = VectorStoreIndex.from_documents(documents)
        
        # Persist the index for potential reuse
        index.storage_context.persist(persist_dir="./storage")
        
        logging.info("Creating query engine...")
        query_engine = index.as_query_engine()
        
        return query_engine

    except Exception as e:
        logging.error(f"Exception in creating query engine: {str(e)}")
        raise CustomException(e, sys)