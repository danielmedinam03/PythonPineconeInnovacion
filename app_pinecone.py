from pinecone import Pinecone, PodSpec
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Configuración inicial
load_dotenv(".env")
os.environ['PINECONE_API_KEY'] = os.getenv("PINECONE_API_KEY")


embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-3-small")

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name='gpt-3.5-turbo',
    temperature=0.0)

chain = load_qa_chain(llm, chain_type="stuff")

INDEX_NAME = "innovacion"

vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings,
    text_key="text",
    pinecone_api_key=os.getenv("PINECONE_API_KEY"))


def create_index():
    if INDEX_NAME in pc.list_indexes().names():
        pc.delete_index(INDEX_NAME)

    if INDEX_NAME not in pc.list_indexes():
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=PodSpec(
                environment='gcp-starter'
            )
        )


def insert_records(items, metadata=None):
    vectorstore.from_texts(items, embeddings, index_name=INDEX_NAME, metadatas=metadata)


def results_similarity_search(query, n_results=4):
    result = vectorstore.similarity_search(query, k=n_results)
    print(result)
    return result


def retrieve_answer(query, n_results=4):
    doc_result = results_similarity_search(query, n_results=n_results)
    answer = chain.run(input_documents=doc_result, question=query)
    print(f"Pregunta: {query}")
    print(f"Repuesta: {answer}")
