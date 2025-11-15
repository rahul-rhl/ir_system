import os
import re

from llama_index.core import (Document, VectorStoreIndex, SimpleDirectoryReader, PromptTemplate, 
                              StorageContext, Settings, load_index_from_storage)
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.embeddings.openai import OpenAIEmbedding
#from llama_index.vector_stores.qdrant import QdrantVectorStore
#from qdrant_client import QdrantClient
#from qdrant_client.http.models import VectorParams, Distance
from llama_index.core.node_parser import (SentenceSplitter, MarkdownNodeParser)
from config import Config_is
from constants import (SYSTEM_PROMPT, CUSTOM_PROMPT_AGENT)

    
# def initialize_index_markdown() -> object:
#     llm = OpenAI(model="gpt-4o", api_key=Config_is.OPENAI_API_KEY, temperature=0.2, max_tokens=4096)
#     Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large",
#                                            api_key=Config_is.OPENAI_API_KEY,
#                                            dimensions=1536, embed_batch_size=8,)
#     node_parser = MarkdownNodeParser(h1=True, include_metadata=True)
#     try:
#         if not os.path.exists(Config_is.MARKDOWN_EMBEDDING_NEW):
#             if not os.path.exists(Config_is.MARKDOWN_FILE_NEW):
#                 raise FileNotFoundError(f"Markdown file not found at: {Config_is.MARKDOWN_FILE_NEW}")
#             with open(Config_is.MARKDOWN_FILE_NEW, 'r', encoding='utf-8') as file:
#                 markdown_text = file.read()
            
#             document = Document(text=markdown_text, metadata={"source": Config_is.MARKDOWN_FILE_NEW, "file_type": "markdown"})
#             nodes = node_parser.get_nodes_from_documents([document])
#             for node in nodes:
#                 first_line = node.text.strip().split('\n')[0] if node.text else ""
#                 heading_match = re.match(r'^(#{1,6})\s+(.+)$', first_line)
#                 if heading_match:
#                     heading_level = len(heading_match.group(1))
#                     heading_title = heading_match.group(2).strip()
                   
#                     node.metadata.update({
#                         "heading_level": heading_level,
#                         "heading_title": heading_title,
#                         "section_type": f"h{heading_level}",
#                     })
#             index = VectorStoreIndex(nodes, llm=llm, embed_model=Settings.embed_model, show_progress=True)
#             index.storage_context.persist(persist_dir=Config_is.MARKDOWN_EMBEDDING_NEW)
#         else:
#             storage_context = StorageContext.from_defaults(persist_dir=Config_is.MARKDOWN_EMBEDDING_NEW)
#             index = load_index_from_storage(storage_context)
#         return index
#     except Exception as e:
#         raise Exception(f"Error initializing index from markdown file: {str(e)}")


def initialize_index_markdown() -> object:
    """
    Initializing the vectorized data and store the vector store in the specified folder.
    Creating nodes based for seperate sections and corresponding metadata for each sections
    """
    llm = OpenAI(model="gpt-4o", api_key=Config_is.OPENAI_API_KEY, temperature=0.2, max_tokens=4096)
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large",
                                           api_key=Config_is.OPENAI_API_KEY,
                                           dimensions=1536, embed_batch_size=8,)
    node_parser = MarkdownNodeParser(h1=True, include_metadata=True)
    try:
        if not os.path.exists(Config_is.CURRENT_MARKDOWN_VECTOR_STORE):
            if not os.path.exists(Config_is.CURRENT_MARKDOWN_FILE):
                raise FileNotFoundError(f"Markdown file not found at: {Config_is.CURRENT_MARKDOWN_FILE}")
            with open(Config_is.CURRENT_MARKDOWN_FILE, 'r', encoding='utf-8') as file:
                markdown_text = file.read()
            
            document = Document(text=markdown_text, metadata={"source": Config_is.CURRENT_MARKDOWN_FILE, "file_type": "markdown"})
            nodes = node_parser.get_nodes_from_documents([document])
            for node in nodes:
                first_line = node.text.strip().split('\n')[0] if node.text else ""
                heading_match = re.match(r'^(#{1,6})\s+(.+)$', first_line)
                if heading_match:
                    heading_level = len(heading_match.group(1))
                    heading_title = heading_match.group(2).strip()
                   
                    node.metadata.update({
                        "heading_level": heading_level,
                        "heading_title": heading_title,
                        "section_type": f"h{heading_level}",
                    })
            index = VectorStoreIndex(nodes, llm=llm, embed_model=Settings.embed_model, show_progress=True)
            index.storage_context.persist(persist_dir=Config_is.CURRENT_MARKDOWN_VECTOR_STORE)
        else:
            storage_context = StorageContext.from_defaults(persist_dir=Config_is.CURRENT_MARKDOWN_VECTOR_STORE)
            index = load_index_from_storage(storage_context)
        return index
    except Exception as e:
        raise Exception(f"Error initializing index from markdown file: {str(e)}")


def initialize_agent() -> object:
    """function to create agent, query engine and tool"""
    llm = OpenAI(model="gpt-4o", api_key=Config_is.OPENAI_API_KEY, temperature=0.3, max_tokens=4096)
    try:
        #index = initialize_index()
        index = initialize_index_markdown()
        query_engine = index.as_query_engine(similarity_top_k=5, context_window=16384,
                                             text_qa_template=PromptTemplate(f"""{CUSTOM_PROMPT_AGENT}
                                                                             **Context:**
                                                                             {{context_str}}

                                                                             **User Query:**
                                                                             {{query_str}}
                                                                             """))
        query_tool = QueryEngineTool.from_defaults(
            query_engine=query_engine,
            description="Retrieve EXACT and COMPLETE text from documents based on each combination given."
        ) 
        agent = OpenAIAgent.from_tools(
            [query_tool],
            llm=llm,
            verbose=True,
            system_prompt=SYSTEM_PROMPT
        )
        return query_engine, query_tool, agent
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        raise




# def initialize_qdrant_index() -> object:
#     file_path = "C:\\Projects\\git_clone\\Hair_Colour\\flask_boilerplate\\embedding_data_new.md"
#     collection_name = "The_shades_embedding_collection"

#     llm = OpenAI(model="gpt-4o", api_key=Config_is.OPENAI_API_KEY)
#     Settings.embed_model = OpenAIEmbedding(
#         model="text-embedding-3-large",
#         api_key=Config_is.OPENAI_API_KEY,
#         dimensions=1536,
#         embed_batch_size=8,
#     )
#     node_parser = MarkdownNodeParser(h1=True, include_metadata=True)
#     try:
#         if not os.path.exists(file_path):
#             raise FileNotFoundError(f"Markdown file not found at: {file_path}")
#         with open(file_path, 'r', encoding='utf-8') as file:
#             markdown_text = file.read()
#         document = Document(text=markdown_text, metadata={"source": file_path, "file_type": "markdown"})
#         nodes = node_parser.get_nodes_from_documents([document])
#         for node in nodes:
#             first_line = node.text.strip().split('\n')[0] if node.text else ""
#             heading_match = re.match(r'^(#{1,6})\s+(.+)$', first_line)
#             if heading_match:
#                 heading_level = len(heading_match.group(1))
#                 heading_title = heading_match.group(2).strip()
#                 node.metadata.update({
#                     "heading_level": heading_level,
#                     "heading_title": heading_title,
#                     "section_type": f"h{heading_level}",
#                 })

#         #qdrant_client = QdrantClient(host="localhost", port=6333)  # Adjust host and port as needed
#         qdrant_client = QdrantClient(url=Config_is.QDRANT_URL, api_key=Config_is.QDRANT_API)
#         if not qdrant_client.collection_exists(collection_name):
#             qdrant_client.create_collection(
#                 collection_name=collection_name,
#                 vectors_config=VectorParams(
#                     size=1536,
#                     distance=Distance.COSINE
#                 )
#             )

#         vector_store = QdrantVectorStore(client=qdrant_client, collection_name=collection_name)
#         storage_context = StorageContext.from_defaults(vector_store=vector_store)
#         index = VectorStoreIndex(nodes, storage_context=storage_context, llm=llm, embed_model=Settings.embed_model, show_progress=True)
#         return index
#     except Exception as e:
#         raise Exception(f"Error initializing index from markdown file: {str(e)}")



# def initialize_index() -> object:
#     """function to vectorize the uploaded pdf"""
#     sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
#     llm = OpenAI(model="gpt-4", api_key=Config_is.OPENAI_API_KEY, max_tokens=4096)
#     Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002", api_key=Config_is.OPENAI_API_KEY)
#     text_splitter = SentenceSplitter(
#         chunk_size=4096,
#         chunk_overlap=200
#     )
#     try:
#         if not os.path.exists(Config_is.PERSIST_DIR):
#             documents = SimpleDirectoryReader(Config_is.VECTORIZED_FOLDER).load_data()   
#             if not documents:
#                 raise ValueError("No documents were loaded from the directory")  
#             nodes = text_splitter.get_nodes_from_documents(documents)
#             index = VectorStoreIndex(nodes, llm=llm, embed_model=Settings.embed_model)
#             index.storage_context.persist(persist_dir=Config_is.PERSIST_DIR)
#         else:
#             storage_context = StorageContext.from_defaults(persist_dir=Config_is.PERSIST_DIR)
#             index = load_index_from_storage(storage_context)        
#         return index
#     except Exception as e:
#         raise Exception(f"Error initializing index: {str(e)}")

# def initialize_index() -> object:
#     """function to vectorize the uploaded .txt"""
#     llm = OpenAI(model="gpt-4o", api_key=Config_is.OPENAI_API_KEY, temperature=0.3, max_tokens=4096)
#     Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large", api_key=Config_is.OPENAI_API_KEY)
#     text_splitter = SentenceSplitter(chunk_size=4096, chunk_overlap=200)
#     try:
#         if not os.path.exists(Config_is.TEMP_TEXT_EMBEDDING):
#             if not os.path.exists(Config_is.TEMP_TEXT_FILE):
#                 raise FileNotFoundError(f"Text file not found at: {Config_is.TEMP_TEXT_FILE}")
#             with open(Config_is.TEMP_TEXT_FILE, 'r', encoding='utf-8') as file:
#                 raw_text = file.read()            
#             document = Document(text=raw_text)        
#             nodes = text_splitter.get_nodes_from_documents([document])        
#             index = VectorStoreIndex(nodes, llm=llm, embed_model=Settings.embed_model)
#             index.storage_context.persist(persist_dir=Config_is.TEMP_TEXT_EMBEDDING)
#         else:
#             storage_context = StorageContext.from_defaults(persist_dir=Config_is.TEMP_TEXT_EMBEDDING)
#             index = load_index_from_storage(storage_context)
#         return index
#     except Exception as e:
#         raise Exception(f"Error initializing index from text file: {str(e)}")