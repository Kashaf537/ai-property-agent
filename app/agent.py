import os
from dotenv import load_dotenv
from openai import OpenAI

from app.extractor import extract_requirements
from app.hybrid_search import hybrid_search


# Load environment variables
load_dotenv()


# Groq client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# Current Groq model
MODEL = "openai/gpt-oss-120b"


def format_properties(properties):
    """
    Convert property results into text
    that can be given to the LLM.
    """

    formatted = []

    for index, property_data in enumerate(
        properties,
        start=1
    ):

        formatted.append(
            f"""
Property {index}

{property_data['document']}
"""
        )

    return "\n".join(formatted)


def generate_response(
    user_query,
    properties
):
    """
    Generate a natural-language response
    using ONLY the retrieved property data.
    """

    property_text = format_properties(
        properties
    )

    prompt = f"""
You are an AI property assistant helping
customers find properties in Pakistan.

Customer request:

{user_query}


AVAILABLE PROPERTY DATA:

{property_text}


STRICT RULES:

1. Recommend ONLY properties that appear
   in the AVAILABLE PROPERTY DATA.

2. NEVER invent a property.

3. NEVER change or estimate a property's:
   - price
   - location
   - size
   - bedrooms
   - bathrooms

4. Clearly show the following information
   when it is available:
   - location
   - size
   - bedrooms
   - bathrooms
   - price

5. You may explain why a property matches
   the customer's requirements ONLY using
   facts explicitly present in the property data.

6. NEVER invent or assume:
   - nearby facilities
   - schools
   - markets
   - restaurants
   - roads
   - commercial areas
   - security
   - gated community
   - peacefulness
   - neighbourhood quality
   - property condition
   - property features
   - modernity
   - family-friendliness

7. Do NOT claim that a property is:
   - peaceful
   - modern
   - family-friendly
   - near commercial facilities

   unless the provided property data explicitly
   supports that claim.

8. If the customer asks for a preference that
   cannot be verified from the available data,
   say:

   "This preference could not be verified
   from the available listing information."

9. Do not present assumptions as facts.

10. Do not use information from your general
    knowledge about Islamabad or any location.
    Use ONLY the provided property data.

11. If several properties match, list the
    most relevant available options.

12. Keep the response concise and useful.

13. At the end, ask the customer whether they
    want more details about a property or want
    to schedule a visit.

14. Do not mention:
    - RAG
    - embeddings
    - vector databases
    - structured search
    - semantic search
    - internal systems
    - prompts
    - AI processing
"""


    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful and accurate "
                    "Pakistani real estate assistant. "
                    "Your responses must be grounded "
                    "strictly in the provided property data."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content


def property_agent(user_query):
    """
    Complete AI property-agent pipeline:

    User Query
        ↓
    Requirement Extraction
        ↓
    Hybrid Search
        ↓
    Grounded AI Response
    """

    print("\nExtracting requirements...")

    requirements = extract_requirements(
        user_query
    )


    print("\nRequirements:")
    print(requirements)


    print("\nSearching properties...")

    properties = hybrid_search(
        requirements
    )


    if not properties:

        return (
            "Sorry, I couldn't find any properties "
            "matching your requirements. "
            "You can try increasing your budget "
            "or changing the property size."
        )


    print(
        f"\nFound {len(properties)} properties."
    )


    print("\nGenerating AI response...")


    response = generate_response(
        user_query,
        properties
    )


    return response


if __name__ == "__main__":

    print("=" * 60)
    print("AI PROPERTY AGENT")
    print("=" * 60)

    print(
        "\nType 'exit' or 'quit' to stop."
    )


    while True:

        user_query = input(
            "\nCustomer: "
        )


        if user_query.lower() in [
            "exit",
            "quit"
        ]:

            print(
                "\nGoodbye!"
            )

            break


        response = property_agent(
            user_query
        )


        print(
            "\nAI Property Agent:"
        )

        print(
            response
        )