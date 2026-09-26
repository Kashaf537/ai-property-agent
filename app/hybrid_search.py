import chromadb
from sentence_transformers import SentenceTransformer

from app.search import search_properties


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "properties"

# Load embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to ChromaDB
client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


def semantic_search(
    query,
    n_results=20
):
    """
    Search properties using semantic similarity.
    """

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    properties = []

    if not results["documents"]:
        return properties

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        properties.append({
            "document": document,
            "metadata": metadata,
            "distance": distance
        })

    return properties


def hybrid_search(requirements):
    """
    Combine structured filtering with semantic search.
    """

    # --------------------------------
    # 1. Get extracted requirements
    # --------------------------------

    city = requirements.get("city")
    max_price = requirements.get("max_price")
    min_price = requirements.get("min_price")
    size_marla = requirements.get("size_marla")
    beds = requirements.get("beds")
    baths = requirements.get("baths")
    property_type = requirements.get("property_type")

    semantic_query = requirements.get(
        "semantic_query",
        ""
    )


    # --------------------------------
    # 2. Structured filtering
    # --------------------------------

    structured_results = search_properties(
        city=city,
        max_price=max_price,
        min_price=min_price,
        size_marla=size_marla,
        beds=beds,
        baths=baths,
        property_type=property_type,
        limit=50
    )

    print(
        f"Structured search found "
        f"{len(structured_results)} properties."
    )


    # --------------------------------
    # 3. If no structured matches
    # --------------------------------

    if structured_results.empty:
        return []


    # --------------------------------
    # 4. Create candidate locations
    # --------------------------------

    candidate_locations = set(
        structured_results["location"]
        .astype(str)
        .str.lower()
        .str.strip()
    )


    # --------------------------------
    # 5. Semantic search
    # --------------------------------

    if semantic_query:

        semantic_results = semantic_search(
            semantic_query,
            n_results=50
        )

    else:

        semantic_results = []


    # --------------------------------
    # 6. Match semantic results
    #    against structured candidates
    # --------------------------------

    final_results = []

    for result in semantic_results:

        metadata = result["metadata"]

        location = str(
            metadata.get("location", "")
        ).lower().strip()

        if location in candidate_locations:

            final_results.append(result)


    # --------------------------------
    # 7. If semantic search doesn't
    #    find enough candidates,
    #    use structured results
    # --------------------------------

    if len(final_results) < 3:

        final_results = []

        for _, row in structured_results.iterrows():

            document = f"""
Property in {row['city']}

Location: {row['location']}

Neighbourhood: {row['neighbourhood']}

Area: {row['area']}

Property size: {row['size_marla']} Marla

Bedrooms: {row['beds']}

Bathrooms: {row['baths']}

Price: PKR {row['price_pkr']:,.0f}

Price per Marla: PKR {row['price_per_marla']:,.0f}

Property title: {row['title']}
""".strip()

            final_results.append({

                "document": document,

                "metadata": {
                    "city": row["city"],
                    "location": row["location"],
                    "beds": row["beds"],
                    "baths": row["baths"],
                    "size_marla": row["size_marla"],
                    "price_pkr": row["price_pkr"]
                },

                "distance": None
            })


    # --------------------------------
    # 8. Return top 5
    # --------------------------------

    return final_results[:5]