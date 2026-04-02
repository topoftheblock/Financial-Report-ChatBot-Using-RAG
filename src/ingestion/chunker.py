import chromadb
from langchain_text_splitters import MarkdownHeaderTextSplitter

def chunk_markdown_file(file_path: str, base_metadata: dict) -> list:
    """
    Reads a markdown file, splits it by headers, and appends base metadata.
    
    Args:
        file_path (str): The path to the markdown file.
        base_metadata (dict): Metadata to append to every chunk (e.g., company info).
        
    Returns:
        list: A list of LangChain Document objects containing the text and metadata.
    """
    # Read the markdown file
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_document = file.read()

    # Define the markdown headers to split on
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    # Initialize the splitter and chunk the document
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(markdown_document)

    # Append the base metadata to the auto-generated header metadata
    for split in md_header_splits:
        split.metadata.update(base_metadata)
        
    return md_header_splits

def store_vectors_in_chroma(chunks: list, db_path: str, collection_name: str, id_prefix: str) -> None:
    """
    Takes document chunks and stores them in a local ChromaDB vector database.
    
    Args:
        chunks (list): List of LangChain Document objects to store.
        db_path (str): The local directory path to persist the database.
        collection_name (str): The name of the ChromaDB collection.
        id_prefix (str): A string prefix used to generate unique IDs for the chunks.
    """
    # Initialize a persistent ChromaDB client
    chroma_client = chromadb.PersistentClient(path=db_path)

    # Create or retrieve the collection
    collection = chroma_client.get_or_create_collection(name=collection_name)

    # Prepare the data arrays required by ChromaDB
    documents = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    ids = [f"{id_prefix}_{i}" for i in range(len(documents))]

    # Insert the data into the database
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Successfully stored {len(documents)} chunks into the '{collection_name}' collection at '{db_path}'.")

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    # Define configuration
    target_file = "AAPL_10Q_MDnA.md"
    
    # Define the core metadata for this specific document
    company_metadata = {
        "company": "Apple Inc.",
        "ticker": "AAPL",
        "document_type": "10-Q MD&A",
        "period": "Q1 2026"
    }
    
    # 1. Chunk the document
    document_chunks = chunk_markdown_file(
        file_path=target_file, 
        base_metadata=company_metadata
    )
    
    # 2. Store the chunks in the vector database
    store_vectors_in_chroma(
        chunks=document_chunks, 
        db_path="./chroma_financial_db", 
        collection_name="financial_statements",
        id_prefix="AAPL_10Q_Q1_2026"
    )