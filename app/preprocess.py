import pandas as pd

INPUT_FILE = "data/properties.csv"
OUTPUT_FILE = "data/properties_clean.csv"


def load_data():
    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded {len(df)} properties")

    return df


def clean_data(df):

    # Normalize text columns
    text_columns = [
        "city",
        "location",
        "title",
        "neighbourhood",
        "area"
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # Make sure numeric columns are numeric
    numeric_columns = [
        "price_pkr",
        "size_marla",
        "beds",
        "baths",
        "price_per_marla"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove rows with missing critical information
    df = df.dropna(
        subset=[
            "city",
            "price_pkr",
            "size_marla"
        ]
    )

    # Remove duplicate properties
    df = df.drop_duplicates()

    return df


if __name__ == "__main__":

    df = load_data()

    df = clean_data(df)

    print(f"After cleaning: {len(df)} properties")

    print("\nCities:")
    print(df["city"].value_counts())

    print("\nSample:")
    print(df.head())

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nSaved cleaned data to {OUTPUT_FILE}")