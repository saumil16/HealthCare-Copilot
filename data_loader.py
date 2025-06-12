from pymongo import MongoClient
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain_community.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import gradio as gr   
from gradio.themes.base import Base
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('mongo_url'))
dbName = os.getenv('dbName')
collectionName = os.getenv('collectionName')
collection = client[dbName][collectionName]

doc = DirectoryLoader('./dataset',glob="./*.pdf",show_progress=True,loader_cls=PyPDFLoader)
loader = doc.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap = 50)
data=text_splitter.split_documents(loader)

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

vectorStore = MongoDBAtlasVectorSearch.from_documents(data, embeddings, collection=collection)