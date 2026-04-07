# FINANCIAL REPORT CHATBOT  
## Application Handbook  
### Enterprise AI Analyst for SEC 10-K Filings — Version 1.0  

---

## Table of Contents
1. Application Overview  
2. Data Acquisition — SEC EDGAR Scraper  
3. HTML-to-Markdown Parser  
4. Context-Aware Vectorisation  
5. LangGraph Agent Architecture  
6. Specialised Tool Suite  
7. End-to-End Data Flow  
8. Configuration Reference  
9. Known Limitations and Design Decisions  

---

## 1. Application Overview

The Financial Report ChatBot is a Streamlit-based enterprise AI analyst that enables users to query dense SEC 10-K filings through a natural-language chat interface. It combines a sophisticated data ingestion pipeline, a specialised HTML parser, a context-aware vector database, and a multi-step LangGraph agent to deliver accurate, verifiable financial analysis.

### 1.1 Key Capabilities

| Capability | Description | Technical Basis |
|----------|------------|----------------|
| Natural-Language Querying | Ask questions in plain English about any ingested 10-K filing | LangGraph ReAct agent |
| Multi-Company Analysis | Compare financials across companies and fiscal years simultaneously | Map-Reduce subgraph pattern |
| Precise Arithmetic | Year-over-year growth, margins, and ratios computed exactly | Python sandbox calculator |
| Source Transparency | View every intermediate reasoning step the agent took | Streamlit expander UI |
| Token Safety | Automatic context compression prevents prompt overflow | Dynamic token estimation |
| Duplicate Prevention | Retrieval-key deduplication avoids redundant DB searches | AgentState tracking set |

---

### 1.2 User Interface

The Streamlit frontend maintains session state for both the chat history and the agent instance.

- **Chat History:** Stored in `st.session_state` and re-rendered each page load  
- **Thought-Process Expander:**  
  A collapsible panel showing:
  - Tool selections  
  - Query parameters  
  - Retrieved data previews  

**Transparency by Design**  
The thought-process expander is a core feature. Financial professionals are expected to audit the agent's reasoning.

---

## 2. Data Acquisition — SEC EDGAR Scraper

A structured ETL pipeline (Extract, Transform, Load).

### 2.1 CIK Mapping

- Converts ticker → SEC CIK  
- Uses `company_tickers.json`  
- Ensures zero-padded CIK format  

---

### 2.2 Filing Validation and Deduplication

Filters applied:

- **Form Type:** Only `"10-K"`  
- **Date Range:** User-defined  
- **Deduplication:** Accession number set prevents duplicates  

---

### 2.3 Metadata Catalogue

Stored in `metadata.csv`.

| Column | Description |
|--------|------------|
| ticker | Stock ticker |
| cik | SEC identifier |
| company_name | Official name |
| filing_date | Filing date |
| period_of_report | Fiscal year |
| accession_number | Unique ID |
| local_path | File path |

---

## 3. HTML-to-Markdown Parser

Transforms messy SEC HTML into clean Markdown.

### 3.1 Semantic Header Promotion

Detects patterns like:
- PART I / II  
- Item 1  
- Item 7  

Converts them into proper Markdown headers.

---

### 3.2 Financial Table Reconstruction

Fixes table issues:

- Multi-row header merging  
- Empty column removal  
- Cell-by-cell currency merging  

**Why This Matters**  
Ensures numbers like `$` and `4,521` become `$4,521`, improving model accuracy.

---

## 4. Context-Aware Vectorisation

### 4.1 Hierarchical Chunking

Uses Markdown structure to split by sections (not arbitrary text length).

---

### 4.2 Strict Metadata Tagging

Each chunk includes:

| Field | Purpose |
|------|--------|
| ticker | Company filter |
| year | Time filter |
| doc_type | Document type |

**Critical Safety Guarantee**  
Prevents mixing data from different years or companies.

---

## 5. LangGraph Agent Architecture

A two-tier state machine.

---

### 5.1 State Management

#### Main Graph State

| Field | Description |
|------|------------|
| conversation_summary | Condensed history |
| originalQuery | User input |
| rewrittenQuestions | Structured queries |
| agent_answers | Aggregated results |

#### Agent Subgraph State

| Field | Description |
|------|------------|
| tool_call_count | Tool usage limit |
| iteration_count | Loop limit |
| context_summary | Compressed context |
| retrieval_keys | Prevents duplicate searches |

---

### 5.2 Main Graph — Planning (Map-Reduce)

Nodes:

- **summarize_history** → compresses chat  
- **rewrite_query** → splits queries  
- **route_after_rewrite** → decision logic  
- **aggregate_answers** → combines results  

---

### 5.3 Agent Subgraph — Execution

ReAct loop:

- Orchestrator decides:
  - Call tool  
  - Return answer  

Safety mechanisms:

- Max 10 tool calls  
- Max 5 iterations  
- Token compression at ~4000 tokens  

---

## 6. Specialised Tool Suite

### 6.1 search_financial_tables

- Retrieves structured data  
- Uses two-pass filtering workaround  

---

### 6.2 search_unstructured_text

- Retrieves narrative sections  
- Same filtering strategy  

---

### 6.3 python_calculator

- Executes exact arithmetic  
- Prevents hallucinated calculations  

---

## 7. End-to-End Data Flow

1. User submits query  
2. summarize_history runs  
3. rewrite_query splits input  
4. route_after_rewrite decides path  
5. Subgraphs execute in parallel  
6. Results collected  
7. Final synthesis generated  
8. Output + reasoning shown  

---

## 8. Configuration Reference

| Constant | Default | Effect |
|----------|--------|--------|
| MAX_ITERATIONS | 5 | Max loops |
| MAX_TOOL_CALLS | 10 | Max tool calls |
| TOKEN_THRESHOLD | 4000 | Compression trigger |
| GROWTH_FACTOR | 1.3 | Token estimate buffer |
| HISTORY_THRESHOLD | 4 | Chat compression |
| PRE_FILTER_K | 20 | Retrieval pool size |

---

## 9. Known Limitations and Design Decisions

### 9.1 Legacy AgentExecutor

- Present but unused  
- Replaced by LangGraph  

---

### 9.2 Token Estimation

- Based on char/4 heuristic  
- May underestimate large tables  

---

### 9.3 ChromaDB Filter Bug

- Requires two-pass filtering  
- Tradeoff: higher memory usage  

---

### 9.4 Parallel Subgraph Concurrency

- Efficient for I/O-bound tasks  
- Risk of API rate limits with many queries  

---

**Financial Report ChatBot — Application Handbook | Version 1.0**