import numpy as np
from chromadb import PersistentClient

# Connect to the Chroma database
chroma_client = PersistentClient(path="./embedding")
abstracts_collection = chroma_client.get_or_create_collection(name="abstracts")

# Number of nearest neighbors to retrieve
k = 10

# Query the collection
results = abstracts_collection.query(
    query_texts=["accounts payable", "finance"],
    n_results=10,
    # where={"metadata_field": "is_equal_to_this"},
    # where_document={"$contains":"search_string"}
)

# Sort results by score in descending order
# sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)

# Display the results
for result in results:
    print(result)
    # print(f"ID: {result['id']}")
    # print(f"Document: {result['document']}")
    # print(f"Score: {result['score']}")
    # print("-" * 50)


for i in range(len(results['ids'][0])):
    _id = results['ids'][0][i]
    doc = results['documents'][0][i]
    score = results['distances'][0][i]
    print(f"[{_id}][{score}]  {doc}")