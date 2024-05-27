
from chromadb import PersistentClient
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from pathlib import Path

# open ai api key
oa_api_key = Path('./apikey').read_text().strip()

# Load PDF
file_path = "Geneva11.pdf"
loader = PyPDFLoader(file_path)
pages = loader.load_and_split()

# See chunk structure
# page = 20
# print(f"FILE: {pages[page].metadata.get('source')}  [{pages[page].metadata.get('page')}]")
# print(pages[page].page_content)


# Search for Pages with similar content
chroma_index = Chroma.from_documents(pages, OpenAIEmbeddings(api_key=oa_api_key))
docs = chroma_index.similarity_search("funding and the domino model", k=5)
for doc in docs:
    print(f"\n\n{doc.metadata['page']}: {doc.page_content}")