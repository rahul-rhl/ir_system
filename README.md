# WHO Guidelines for Malaria - Information Retrieval System

A Retrieval-Augmented Generation (RAG) based intelligent assistant system specifically designed for querying WHO Malaria Guidelines. This system uses advanced AI technologies to provide accurate, evidence-based answers from official WHO malaria documentation.

## Features

- **Intelligent Document Retrieval**: Semantic search through WHO malaria guidelines using vector embeddings
- **AI-Powered Responses**: Leverages Google Gemini LLM for generating accurate, context-aware answers
- **Source Citation**: Every answer includes source references with confidence scores
- **Markdown Document Processing**: Automatically parses and indexes markdown documents with heading-based chunking
- **Professional Healthcare Interface**: Designed for healthcare professionals and researchers
- **RESTful API**: Easy-to-integrate API endpoints for querying the system

## Tech Stack

### Backend Framework
- **Flask 3.0.0**: Lightweight WSGI web application framework

### AI/ML Components
- **LlamaIndex 0.11.0+**: RAG orchestration framework
  - `llama-index-llms-gemini 0.5.0`: Google Gemini LLM integration
  - `llama-index-agent-openai 0.4.12`: AI agent capabilities
  - `llama-index-embeddings-huggingface 0.5.5`: HuggingFace embeddings
  - `llama-index-vector-stores-qdrant 0.6.1`: Qdrant vector store integration
- **Google Generative AI 0.8.5**: Gemini API client
- **Sentence Transformers**: all-MiniLM-L6-v2 model for embeddings

### Vector Database
- **Qdrant 1.15.1**: High-performance vector similarity search engine

### Utilities
- **python-dotenv 1.0.0**: Environment variable management

## Prerequisites

- Python 3.12.7
- Docker (for running Qdrant)
- Google Gemini API key
- Qdrant instance (local or cloud)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd inerg_ir_system
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Qdrant Vector Database

#### Using Docker (Recommended)

```bash
# Pull and run Qdrant container
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```
QuickStart: https://qdrant.tech/documentation/quickstart/

### 5. Configure Environment Variables

Copy the sample environment file and configure it:

```bash
cp env.sample .env
```

Edit the `.env` file with your configuration:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
MARKDOWN_FILE_PATH=./malaria.md
QDRANT_URL=http://localhost:6333
QDRANT_API=
```

### 6. Prepare Your Document

Place your WHO malaria guidelines markdown file in the project root or specify its path in the `MARKDOWN_FILE_PATH` environment variable.

## Running the Application

### Development Mode

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run with Flask development server
export FLASK_DEBUG=1 
flask run
```

The application will be available at `http://127.0.0.1:5000/v1/ask`

## API Documentation

### Ask Endpoint

**Endpoint**: `/v1/ask`

**Methods**: `GET`, `POST`

**Description**: Submit a question and receive an AI-generated answer based on WHO malaria guidelines.

**See the Qdrant vector**: http://localhost:6333/dashboard#/collections/inerg_ir_syetm_collection

#### POST Request

```bash
curl -X POST http://localhost:5000/v1/ask \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "question=What are the WHO recommended treatments for malaria?"
```

#### Response Format

```json
{
  "answer": "According to WHO guidelines...",
  "confidence": 0.89,
  "sources": [
    {
      "source": "./malaria.md",
      "heading": "Treatment Guidelines",
      "section": "h2",
      "text": "WHO recommends artemisinin-based combination therapies...",
      "score": 0.89
    }
  ]
}
```

## Configuration

### Vector Store Configuration

The system automatically creates a Qdrant collection named `inerg_ir_syetm_collection` with:
- **Vector Size**: 384 dimensions (for all-MiniLM-L6-v2 embeddings)
- **Distance Metric**: Cosine similarity
- **Node Parser**: Markdown-based chunking with heading hierarchy

### LLM Configuration

- **Model**: gemini-2.5-flash
- **Temperature**: 0.3 (for consistent, factual responses)

## Use Cases

1. **Healthcare Professionals**: Quick access to WHO malaria treatment guidelines
2. **Researchers**: Evidence-based information retrieval with source citations
3. **Medical Students**: Learning and reference tool for malaria-related topics
4. **Public Health Organizations**: Policy and guideline implementation support

## How It Works

1. **Document Ingestion**: Markdown documents are parsed into semantic chunks based on heading structure
2. **Embedding Generation**: Each chunk is converted to a 384-dimensional vector using HuggingFace embeddings
3. **Vector Storage**: Embeddings are stored in Qdrant for efficient similarity search
4. **Query Processing**: User questions are embedded and matched against stored vectors
5. **Context Retrieval**: Top 5 most relevant chunks are retrieved
6. **Response Generation**: Gemini LLM generates accurate answers using retrieved context
7. **Source Attribution**: Sources are provided with confidence scores


## Contact
#### **name**: Rahul Sreenivasan P
#### **email**: rahulpudumana@gmail.com
#### **phone**: 7025899640

## Acknowledgments

- WHO for comprehensive malaria guidelines
- LlamaIndex team for the RAG framework
- Google for Gemini API access
- Qdrant team for the vector database
- HuggingFace for embedding models

---