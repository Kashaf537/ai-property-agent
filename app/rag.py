import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer


DATA_FILE = "data/properties_clean.csv"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "properties"

# ChromaDB batch size limit
BATCH_SIZE = 5000


def create_property_text(row):

    return f"""
Property in {row['city']}.

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


def build_vector_database():

    print("Loading properties...")

    df = pd.read_csv(DATA_FILE)

    print(f"Properties loaded: {len(df)}")

    print("Loading embedding model...")

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Creating ChromaDB...")

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    documents = []
    ids = []
    metadatas = []

    print("Preparing property documents...")

    for index, row in df.iterrows():

        document = create_property_text(row)

        documents.append(document)

        ids.append(f"property_{index}")

        metadatas.append({
            "city": str(row["city"]),
            "location": str(row["location"]),
            "beds": float(row["beds"]),
            "baths": float(row["baths"]),
            "size_marla": float(row["size_marla"]),
            "price_pkr": float(row["price_pkr"])
        })

    print(f"Prepared {len(documents)} property documents.")

    print("\nCreating embeddings...")

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    print("\nAdding properties to ChromaDB...")

    # Add properties in batches because ChromaDB
    # has a maximum batch size.
    for start in range(0, len(documents), BATCH_SIZE):

        end = min(
            start + BATCH_SIZE,
            len(documents)
        )

        print(
            f"Adding properties "
            f"{start + 1} to {end}..."
        )

        collection.add(
            ids=ids[start:end],
            documents=documents[start:end],
            embeddings=embeddings[start:end],
            metadatas=metadatas[start:end]
        )

    print("\n" + "=" * 50)
    print("RAG database created successfully!")
    print("=" * 50)

    print(
        f"Total properties in ChromaDB: "
        f"{collection.count()}"
    )


if __name__ == "__main__":
    build_vector_database()