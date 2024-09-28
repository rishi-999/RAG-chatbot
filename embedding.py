from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

embeddings_model = AzureOpenAIEmbeddings(
    model = "text-embedding-ada-002",
    openai_api_version = os.getenv('EMBEDDING_API_VERSION')
)

name = "newindex"

Vector_store = AzureSearch(
    azure_search_endpoint=os.getenv('STORE_ADDRESS'),
    azure_search_key=os.getenv('STORE_PASSWORD'),
    index_name=name,
    embedding_function=embeddings_model.embed_query
)


loader = TextLoader("./resume.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

Vector_store.add_documents(documents=docs)
