import chromadb
from extraction import extract_from_pdf
from langchain_text_splitters import TokenTextSplitter

pdf_content=extract_from_pdf()

token_splitter=TokenTextSplitter(chunk_size=800, chunk_overlap=100)
chunks=token_splitter.split_text(pdf_content)

client=chromadb.Client()
collection=client.create_collection(name="feb24")
chunks_ids=[f"chunk_{i}" for i in range(len(chunks))] 
collection.add(
    ids=chunks_ids,
    documents=chunks
)
