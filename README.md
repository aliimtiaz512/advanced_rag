Description:
This is a Advanced Rag. In this I implemented a Great Gatsby Story. Now this answere all the questions about this document. The frontend of this app is implemented in Streamlit.

In example.env: 
There is a format in which we add our credentials.

In extraction.py:
PyPDF use for data extraction from document.

In ingestion.py:
In langchain_texttoken_splitter used for making tokens of the document. Then used chromadb to store vector embeddings we make chunks for the data which is inside the document for making their embeddings and then we store it into vector database.

In generation.py:
Implemented groq api for the better response related to document.Implemented pre retrieval and post retrival concept. In this if user send its query and gives the confidence score that how much it match with desire document and if the query didnot like that it gives 5 options then user select on it and then work on it.


Prerequisties:

For running this app you need to install:
pip install pypdf
pip install langchain
pip install groq
pip install chromadb
pip install streamlit

