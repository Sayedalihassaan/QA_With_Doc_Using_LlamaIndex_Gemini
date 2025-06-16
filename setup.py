# setup.py
from setuptools import find_packages, setup

setup(
    name='QApplication',
    version='0.0.1',
    author='Sayed Ali',
    author_email='saiedhassaan2@gmail.com',
    packages=find_packages(),
    install_requires=[
        'llama-index',
        'llama-index-llms-gemini',
        'llama-index-embeddings-gemini',
        'streamlit',
        'python-dotenv',
        'google-generativeai',
    ]
)