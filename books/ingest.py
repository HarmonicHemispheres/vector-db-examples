# Notes - https://www.kaggle.com/datasets/dhruvildave/wikibooks-dataset

import chromadb
import sqlite3

import sqlite3
from chromadb import Client, PersistentClient

# Connect to the Chroma database
chroma_client = PersistentClient(path="./embedding")
chroma_client.get_settings().allow_reset = True
chroma_client.reset()
abstracts_collection = chroma_client.get_or_create_collection("abstracts")

# Connect to the SQLite database
print("Connecting to Source DB")
sqlite_connection = sqlite3.connect('wikibooks.sqlite')
cursor = sqlite_connection.cursor()

# Define the chunk size
chunk_size = 1000
offset = 0

while True:
    # Fetch data from the 'en' table in chunks
    cursor.execute("SELECT abstract FROM en LIMIT ? OFFSET ?", (chunk_size, offset))
    rows = cursor.fetchall()
    if not rows:
        break

    row_count = len(rows)
    # Prepare data for upsert
    ids = []
    documents = []
    for idx, row in enumerate(rows):
        abstract = row[0]
        if abstract:  # Check if the abstract is not empty
            ids.append(f"doc_{offset + idx}")
            documents.append(abstract)

    # Upsert data into Chroma DB
    abstracts_collection.upsert(ids=ids, documents=documents)

    print(f"Ingested {row_count:,}")

    # Update the offset
    offset += chunk_size

# Commit and close the SQLite connection
sqlite_connection.commit()
sqlite_connection.close()

print("Data insertion completed successfully.")