import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


MODEL = "openai/gpt-oss-120b"


SYSTEM_PROMPT = """
You are a property search requirement extractor.

Extract property requirements from the user's message.

Return ONLY a valid JSON object.

Use exactly these fields:

{
    "city": null,
    "max_price": null,
    "min_price": null,
    "size_marla": null,
    "beds": null,
    "baths": null,
    "property_type": null,
    "semantic_query": ""
}

Rules:

1. Convert Pakistani crore/lakh amounts into PKR.

Examples:
2 crore = 20000000
1.5 crore = 15000000
50 lakh = 5000000
75 lakh = 7500000

2. "under 2 crore" means:
   max_price = 20000000

3. "above 1 crore" means:
   min_price = 10000000

4. "5 marla" means:
   size_marla = 5

5. "4 bedrooms" means:
   beds = 4

6. "3 bathrooms" means:
   baths = 3

7. Normalize cities to lowercase.

8. If the user mentions preferences such as:
   modern
   peaceful
   family-friendly
   good location
   near commercial area
   spacious

   put those preferences into semantic_query.

9. Do not invent missing information.

10. Use null when information is not provided.

11. Return JSON only.
"""


def extract_requirements(user_query):

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )

    content = response.choices[0].message.content

    requirements = json.loads(content)

    return requirements


if __name__ == "__main__":

    query = input(
        "Enter property requirement:\n"
    )

    requirements = extract_requirements(query)

    print("\nExtracted requirements:")

    print(
        json.dumps(
            requirements,
            indent=4
        )
    )