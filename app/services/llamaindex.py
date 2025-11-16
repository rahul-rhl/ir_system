import os
import re

from llama_index.core import (
    Document, VectorStoreIndex, PromptTemplate,
    StorageContext, Settings
)
from llama_index.llms.gemini import Gemini
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent import ReActAgent
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from llama_index.core.node_parser import MarkdownNodeParser

from config import Config_is
from constants import SYSTEM_PROMPT, CUSTOM_PROMPT



def initialize_index_markdown() -> object:
    file_path = Config_is.MARKDOWN_FILE_PATH
    collection_name = "inerg_ir_syetm_collection"

    llm = Gemini(
        model="gemini-2.5-flash",
        api_key=Config_is.GEMINI_API_KEY,
        temperature=0.3
    )
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    Settings.llm = llm
    Settings.embed_model = embed_model
    node_parser = MarkdownNodeParser(h1=True, include_metadata=True)

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Markdown file not found at: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_text = file.read()

        document = Document(
            text=markdown_text,
            metadata={"source": file_path, "file_type": "markdown"}
        )

        qdrant_client = QdrantClient(
            url=Config_is.QDRANT_URL,
            api_key=Config_is.QDRANT_API
        )

        vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name=collection_name
        )

        if qdrant_client.collection_exists(collection_name):
            print("Qdrant collection found — loading existing index.")
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
                storage_context=storage_context,
                llm=llm,
                embed_model=embed_model
            )

            return index
        print("Qdrant collection missing — creating and embedding documents.")

        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

        nodes = node_parser.get_nodes_from_documents([document])
        for node in nodes:
            first_line = node.text.strip().split('\n')[0] if node.text else ""
            match = re.match(r'^(#{1,6})\s+(.+)$', first_line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                node.metadata.update({
                    "heading_level": level,
                    "heading_title": title,
                    "section_type": f"h{level}",
                })

        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            llm=llm,
            embed_model=embed_model,
            show_progress=True
        )
        return index

    except Exception as e:
        raise Exception(f"Error initializing index from markdown file: {str(e)}")

def initialize_agent():
    index = initialize_index_markdown()

    llm = Gemini(
        model="gemini-2.5-flash",
        api_key=Config_is.GEMINI_API_KEY,
        temperature=0.3
    )
    Settings.llm = llm

    query_engine = index.as_query_engine(
        similarity_top_k=5,
        response_mode="compact",
        include_metadata=True,
        node_postprocessors=[]
    )

    tool = QueryEngineTool.from_defaults(
        query_engine,
        name="rag_tool",
        description="Answer questions from documentation",
    )

    agent = ReActAgent.from_tools(
        tools=[tool],
        llm=llm,
        verbose=True
    )

    return agent
