import os
import chromadb
from langchain.tools import tool
from langchain_experimental.tools.python.tool import PythonAstREPLTool

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "chroma_financial_db")
COLLECTION_NAME = "financial_statements"

@tool
def semantic_financial_search(query: str, company_ticker: str = None, year: int = None) -> str:
    """
    Performs a semantic similarity search across financial documents and markdown tables.
    Provide a descriptive semantic 'query' (e.g., 'What are the top risk factors?' or 'Revenue and net income table').
    Optionally filter by 'company_ticker' (e.g., 'AAPL') and 'year' (e.g., 2024).
    """
    try:
        chroma_client = chromadb.PersistentClient(path=DB_PATH)
        collection = chroma_client.get_collection(name=COLLECTION_NAME)
        
        # Build ChromaDB metadata filters dynamically based on LLM input
        where_clause = {}
        conditions = []
        
        if company_ticker:
            conditions.append({"ticker": company_ticker.upper()})
        if year:
            conditions.append({"year": year})
            
        if len(conditions) > 1:
            where_clause = {"$and": conditions}
        elif len(conditions) == 1:
            where_clause = conditions[0]
        else:
            where_clause = None

        # Execute semantic vector search
        results = collection.query(
            query_texts=[query], 
            n_results=5, 
            where=where_clause if where_clause else None
        )
        
        if not results['documents'] or not results['documents'][0]:
            return "No documents found."
            
        valid_chunks = []
        for i in range(len(results['documents'][0])):
            meta = results['metadatas'][0][i]
            chunk = results['documents'][0][i]
            
            # Keep the citation formatting so the Reviewer instruction still works
            # CHANGED: 'Item' was replaced with 'section' to pull the correct header metadata
            source_citation = f"[Source: {meta.get('Ticker', 'Unknown')} | Year: {meta.get('Year', 'Unknown')} | Section: {meta.get('Section', 'Unknown')}]"
            formatted_chunk = f"{source_citation}\nExact Passage: {chunk}"
            
            valid_chunks.append(formatted_chunk)
                    
        return "\n\n---\n\n".join(valid_chunks)
    except Exception as e:
        return f"Database error: {str(e)}"

python_calculator = PythonAstREPLTool(
    name="python_calculator",
    description="Python shell. Use this to execute math, percentages, or differences. Input valid python."
)