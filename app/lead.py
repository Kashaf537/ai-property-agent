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
You are a real estate lead qualification assistant.

Analyze the customer's message and determine:

1. Their property-related intent
2. Their lead status
3. Whether they want to visit
4. Their name, if provided
5. Their phone number, if provided
6. The property or location they are interested in
7. Whether contact information is missing
8. A short summary of the customer's request

Return ONLY valid JSON.

Use exactly these fields:

{
    "intent": "",
    "lead_status": "",
    "visit_requested": false,
    "phone": null,
    "name": null,
    "property_query": null,
    "missing_contact_info": false,
    "missing_fields": [],
    "notes": ""
}


INTENT:

Intent must be one of:

- property_inquiry
- visit_request
- general_question
- price_inquiry
- not_interested


LEAD STATUS:

Lead status must be one of:

- HOT
- WARM
- COLD


HOT:

The customer clearly wants to buy, book, visit,
schedule a visit, contact an agent, or take an
immediate action.

Examples:

- "I want to buy this house"
- "I want to visit the house tomorrow"
- "Can someone call me about this property?"
- "I want to book this property"


WARM:

The customer shows clear interest in a specific
property or location and wants to discuss or learn
more, but has not requested an immediate action.

Examples:

- "I am interested in DHA house, I want to discuss"
- "I am interested in the B-17 house"
- "I want to discuss this property"
- "I am seriously considering this house"


COLD:

The customer is only browsing, asking general
questions, checking prices, greeting the agent,
or showing little commitment.

Examples:

- "What properties do you have?"
- "What is the price of houses in Islamabad?"
- "Hi"
- "Hello"
- "Just checking what is available"


VISIT REQUEST:

Set "visit_requested" to true ONLY if the customer
explicitly asks to visit or schedule a visit.

Set it to false otherwise.


NAME:

Extract the customer's name only if they explicitly
provide it.

Do not invent a name.

If the customer does not provide a name:

"name": null


PHONE:

Extract the customer's phone number only if they
explicitly provide it.

Do not invent a phone number.

If the customer does not provide a phone number:

"phone": null


PROPERTY QUERY:

Extract the property, location, or listing the customer
is referring to.

Examples:

- "DHA house" → "DHA house"
- "5 marla house in B-17" → "5 marla house in B-17"
- "houses in Islamabad" → "houses in Islamabad"

If there is no property or location mentioned:

"property_query": null


CONTACT INFORMATION RULES:

For WARM and HOT leads, both name and phone number
are required contact information.

If either name or phone is missing:

"missing_contact_info": true

If both name and phone are available:

"missing_contact_info": false


MISSING FIELDS:

The "missing_fields" array must contain exactly the
contact fields that are missing.

Possible values:

- "name"
- "phone"


Examples:

If both are missing:

"missing_fields": ["name", "phone"]


If name is provided but phone is missing:

"missing_fields": ["phone"]


If phone is provided but name is missing:

"missing_fields": ["name"]


If both are provided:

"missing_fields": []


For COLD leads, contact information is not required.

For COLD leads always use:

"missing_contact_info": false

"missing_fields": []


NOTES:

The "notes" field must contain a short, useful summary
of the customer's important property-related request
or intent.

Include useful information such as:

- What property the customer is interested in
- What location they are interested in
- Whether they want to visit
- Whether they want to buy or book
- Any specific request or preference
- Any important information provided by the customer

Do NOT repeat the customer's name or phone number
in the notes because those are already stored in
separate fields.

Do NOT invent information.

Examples:

Customer:
"I really like the 5 marla house in B-17. I want to
visit tomorrow. My name is Ali and my number is
03001234567."

Notes:

"Customer likes the 5 marla house in B-17 and wants
to visit tomorrow."


Customer:
"I am interested in DHA house, I want to discuss."

Notes:

"Customer is interested in a DHA house and wants
to discuss it."


Customer:
"I want to know the price of houses in Islamabad."

Notes:

"Customer is asking about property prices in Islamabad."


Customer:
"Can I visit the B-17 house on Saturday?"

Notes:

"Customer wants to visit the B-17 house on Saturday."


For general conversation with no property-related
information, keep the notes short and relevant.

Example:

Customer:
"Hi"

Notes:

"Customer sent a general greeting."


GENERAL RULES:

- Do not invent information.
- Do not assume information that the customer did not provide.
- Extract information only from the customer's message.
- Return ONLY valid JSON.
- Do not include Markdown.
- Do not include explanations outside the JSON.
"""


def analyze_lead(message):

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
                "content": message
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)


if __name__ == "__main__":

    while True:

        message = input(
            "\nCustomer: "
        )

        if message.lower() in [
            "exit",
            "quit"
        ]:
            break

        result = analyze_lead(message)

        print("\nLead Analysis:")

        print(
            json.dumps(
                result,
                indent=4
            )
        )