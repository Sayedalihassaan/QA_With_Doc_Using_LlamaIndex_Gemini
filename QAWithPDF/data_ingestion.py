# data_ingestion.py
import sys
import os
from logger import logging
from llama_index.core import SimpleDirectoryReader
from exception import CustomException

def load_data(file_obj):
    try:
        logging.info("Data loading started...")
        temp_dir = "temp_data"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file_obj.name)
        with open(file_path, "wb") as f:
            f.write(file_obj.getvalue())
        loader = SimpleDirectoryReader(temp_dir)
        documents = loader.load_data()
        logging.info("Data loading completed...")
        os.remove(file_path)
        return documents
    except Exception as e:
        logging.error("Exception in loading data...")
        raise CustomException(e, sys)