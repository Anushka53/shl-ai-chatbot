from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# JSON file read
with open("assessments.json", "r") as file:
    assessments = json.load(file)

class ChatRequest(BaseModel):
    messages: list

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):

    user_message = req.messages[-1]["content"].lower()
    if "difference" in user_message or "compare" in user_message:

        return {
            "reply": "OPQ32r measures personality and behavior, while General Ability Test measures reasoning and problem-solving skills.",
            "recommendations": [],
            "end_of_conversation": False
        }
    if "legal" in user_message or "salary" in user_message:

        return {
            "reply": "I can only help with SHL assessments.",
            "recommendations": [],
            "end_of_conversation": False
        }
    if "assessment" in user_message and "java" not in user_message and "personality" not in user_message:

        return {
            "reply": "Which role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    recommendations = []

    for assessment in assessments:

        for skill in assessment["skills"]:

            if skill in user_message:

                recommendations.append({
                    "name": assessment["name"],
                    "url": assessment["url"],
                    "test_type": assessment["test_type"]
                })

                break

    if recommendations:

        return {
            "reply": "Here are recommended assessments.",
            "recommendations": recommendations,
            "end_of_conversation": True
        }

    return {
        "reply": "Tell me more about the role.",
        "recommendations": [],
        "end_of_conversation": False
    }