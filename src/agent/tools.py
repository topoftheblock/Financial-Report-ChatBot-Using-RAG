from typing import Optional, Dict, Any
from langchain.tools import tool
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from pydantic import BaseModel, Field

# Assuming these exist in your retrieval pipeline
# from src.retrieval.search import perform_hybrid_search, perform_metadata_search

class TableSearchInput(BaseModel):
    query: str = Field(description="The specific financial metric or table sought (e.g., 'Total Revenue', 'Operating Margins').")
    company_ticker: str = Field(description="The stock ticker of the company (e.g., 'AAPL', 'MSFT').")
    year: int = Field(description="The 4-digit financial year (e.g., 2023).")
    document_type: str = Field(description="The type of SEC filing (e.g., '10-K', '10-Q'). Default is '10-K'.", default="10-K")

@tool("search_financial_tables", args_schema=TableSearchInput)
def search_financial_tables(query: str, company_ticker: str, year: int, document_type: str = "10-K") -> str:
    """
    Search strictly within financial tables and numerical data. 
    Requires strict metadata filtering to prevent retrieving the wrong year or company.
    """
    # Construct exact metadata filter for your Vector DB (e.g., Pinecone/Weaviate)
    metadata_filter = {
        "ticker": company_ticker.upper(),
        "year": year,
        "doc_type": document_type.upper(),
        "is_table": True # Assuming your chunker tags tables
    }
    
    # Mocking the actual DB call from src.retrieval.search
    # context = perform_metadata_search(query=query, filters=metadata_filter)
    
    # Mock response for illustration
    context = f"[Simulated Output] Retrieved table data for {company_ticker} {year} {document_type} related to '{query}'."
    return context

@tool("search_unstructured_text")
def search_unstructured_text(query: str, company_ticker: Optional[str] = None) -> str:
    """
    Perform a semantic hybrid search over unstructured text like MD&A, Risk Factors, and Business Summaries.
    Use this for qualitative questions.
    """
    filters = {}
    if company_ticker:
        filters["ticker"] = company_ticker.upper()
        
    # Mocking the actual DB call from src.retrieval.search
    # context = perform_hybrid_search(query=query, filters=filters)
    
    # Mock response
    context = f"[Simulated Output] Retrieved narrative context for '{query}'."
    return context

def get_financial_tools() -> list:
    """Returns the list of tools available to the agent."""
    
    # Langchain's built-in Python REPL tool is excellent for math calculations.
    # It safely evaluates python AST for math (e.g., calculating YoY growth).
    calculator_tool = PythonAstREPLTool(
        name="python_calculator",
        description="A Python shell. Use this to execute python commands to calculate math, percentages, or differences. Input should be a valid python command. Print the final answer."
    )
    
    return [
        search_financial_tables,
        search_unstructured_text,
        calculator_tool
    ]