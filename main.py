from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.retrievers import AzureAISearchRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import hub
from dotenv import load_dotenv
import os

load_dotenv()

embeddings_model = AzureOpenAIEmbeddings(
    model = "text-embedding-ada-002"
)

llm = AzureChatOpenAI(
    deployment_name="nlp-llm"
)

retriever = AzureAISearchRetriever(
    service_name="cognitive-search-nlp",
    api_key=os.getenv('STORE_PASSWORD'),
    index_name="newindex",
    content_key = "content",
    top_k = 1
)

prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def llmworkflow(query):
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    result = chain.invoke(query)

    return result