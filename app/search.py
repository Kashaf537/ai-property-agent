import pandas as pd


DATA_FILE = "data/properties_clean.csv"


def load_properties():
    return pd.read_csv(DATA_FILE)


def search_properties(
    city=None,
    max_price=None,
    min_price=None,
    size_marla=None,
    beds=None,
    baths=None,
    property_type=None,
    limit=5
):

    df = load_properties()

    # City filter
    if city:
        df = df[
            df["city"].str.contains(
                city.lower(),
                na=False
            )
        ]

    # Maximum price
    if max_price:
        df = df[
            df["price_pkr"] <= max_price
        ]

    # Minimum price
    if min_price:
        df = df[
            df["price_pkr"] >= min_price
        ]

    # Property size
    if size_marla:
        df = df[
            df["size_marla"].between(
                size_marla - 1,
                size_marla + 1
            )
        ]

    # Bedrooms
    if beds:
        df = df[
            df["beds"] >= beds
        ]

    # Bathrooms
    if baths:
        df = df[
            df["baths"] >= baths
        ]

    # Property type
    if property_type:
        df = df[
            df["title"].str.contains(
                property_type.lower(),
                na=False
            )
        ]

    return df.head(limit)