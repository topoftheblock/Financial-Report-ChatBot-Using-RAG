# Financial Report ChatBot Using RAG

A sophisticated **Retrieval-Augmented Generation (RAG)** system for financial analysis of SEC 10-K reports. By combining Large Language Models, LangChain, and ChromaDB, the system lets users query dense financial filings to extract both qualitative insights (risk factors, business summaries) and quantitative data (revenue tables, operating margins) with high accuracy.

---

## System Architecture

The pipeline is divided into modular components that take data from raw source to interactive agent.

### 1. Data Ingestion
`src/sec_10k_scraper.py` interfaces with the **SEC EDGAR** database to download raw HTML 10-K filings for specified company tickers and years, storing them in `data/raw/`.

### 2. Parsing & Preprocessing
`src/ingestion/parser.py` converts messy HTML into clean Markdown:
- **Header detection** — identifies SEC-specific section headers (e.g., `PART I`, `Item 1. Business`) and maps them to Markdown headings.
- **Table extraction** — uses BeautifulSoup and Pandas to isolate financial tables, strip formatting artifacts, merge spanning multi-row headers, drop redundant columns, and output clean Markdown tables.

### 3. Chunking & Vectorization
`src/ingestion/chunker.py` processes the parsed Markdown files:
- **Context-aware splitting** — uses LangChain's `MarkdownHeaderTextSplitter` to keep tables and paragraphs tethered to their section headers, never split arbitrarily.
- **Metadata tagging** — each chunk is tagged with `Ticker`, `Year`, and `Document Type` before being embedded and stored in a local ChromaDB instance (`chroma_financial_db/`).

### 4. Agent & Tooling
The reasoning engine is a **ReAct agent** (`src/agent/generator.py` and `tools.py`) that selects from specialized tools to answer each query:

| Tool | Purpose |
|---|---|
| `search_financial_tables` | Strict retrieval with hard metadata filtering (Ticker, Year) to prevent mixing numbers across filings |
| `search_unstructured_text` | Semantic search for qualitative questions (e.g., "What are the macroeconomic risks?") |
| `python_calculator` | Python AST REPL for computing percentages, YoY growth, or differences from retrieved data |

---

## Directory Structure

```
Financial-Report-ChatBot-Using-RAG/
│
├── app/                            # Frontend interface
│   ├── main.py                     # Application entry point
│   └── components.py               # UI components
│
├── chroma_financial_db/            # Local ChromaDB vector store
│
├── data/
│   ├── raw/                        # Raw downloaded SEC HTML filings
│   └── processed/                  # Cleaned and parsed Markdown (.txt) files
│
├── src/
│   ├── agent/
│   │   ├── generator.py            # Agent initialization and execution loop
│   │   ├── tools.py                # Retrieval and calculation tools
│   │   ├── prompt.py               # System prompts
│   │   ├── state.py                # Graph state definitions
│   │   ├── config.py               # Agent configuration and token limits
│   │   ├── main_graph_nodes_and_edges.py
│   │   └── build_the_langgraph_graphs.py
│   │
│   ├── ingestion/
│   │   ├── parser.py               # HTML → Markdown parsing
│   │   └── chunker.py              # Text splitting and ChromaDB embedding
│   │
│   ├── tests/                      # Unit and integration tests
│   └── sec_10k_scraper.py          # SEC EDGAR downloader
│
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites
- Python 3.10+
- An active OpenAI API key

### Steps

**1. Clone the repository**
```bash
git clone <repository-url>
cd Financial-Report-ChatBot-Using-RAG
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the root directory:
```
OPENAI_API_KEY="your_openai_api_key_here"
```

---

## Usage

Run the following steps in sequence to operate the full pipeline from scratch.

**Step 1 — Scrape financial data**
```bash
python src/sec_10k_scraper.py
```

**Step 2 — Parse HTML to Markdown**
```bash
python src/ingestion/parser.py
```

**Step 3 — Chunk and populate the database**
```bash
python src/ingestion/chunker.py
```

**Step 4 — Launch the application**
```bash
python -m streamlit run app/main.py
```

---

## Testing

Run individual component tests as modules from the root directory to avoid path resolution issues.

```bash
# Test the HTML parser
python -m src.tests.test_parser

# Test the Markdown chunker
python -m src.tests.test_chunker

# Test database retrieval performance
python -m src.tests.test_retrieval_performance
```