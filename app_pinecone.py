from pinecone import Pinecone, ServerlessSpec,PodSpec
from dotenv import load_dotenv
import os
import uuid

# Configuración inicial
load_dotenv(".env")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=pinecone_api_key)

def create_index(index_name="innovacion"):

    if index_name in pc.list_indexes().names():
        pc.delete_index(index_name)

    if index_name not in pc.list_indexes():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=PodSpec(
                environment='gcp-starter'
            )
        )
        print("Se crea el indice")



def insert_records(text_fomateo,embedding, index_name="innovacion"):
    index = pc.Index(index_name)
    index.upsert(
        vectors=
        [
            {"id": str(uuid.uuid1()), "values": embedding, "metadata": {"contenido": text_fomateo}}
        ]
    )


