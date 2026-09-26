from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import property_agent
from app.lead import analyze_lead


app = FastAPI(
    title="AI Property Agent",
    description=(
        "AI-powered property search and "
        "lead automation system"
    ),
    version="1.0"
)


class PropertyQuery(BaseModel):
    message: str


class LeadMessage(BaseModel):
    message: str


@app.get("/")
def home():

    return {
        "message": "AI Property Agent is running"
    }


@app.post("/property-search")
def property_search(
    query: PropertyQuery
):

    response = property_agent(
        query.message
    )

    return {
        "user_query": query.message,
        "response": response
    }


@app.post("/lead-analysis")
def lead_analysis(
    data: LeadMessage
):

    result = analyze_lead(
        data.message
    )

    return {
        "message": data.message,
        "lead": result
    }