from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from utils import Utils

u = Utils()

class MentorState(TypedDict):
    log: str
    response: str

def Mentor_node(state: MentorState):
    dlog = state["log"]

    prompt = f"""
    You are a high-performance self-development mentor.

        Analyze the user’s daily log {dlog} and give a short 3–5 line response.  
        Each line must begin with the following labels:

        1. Wins of the Day:
        2. Limits & Fears Noticed:
        3. Money & Growth Opportunities:
        4. Corrections for Tomorrow:
        5. Self-Development Push:

        Tone: direct, honest, growth-focused, and actionable. Keep every line concise.

    """

    response = u.groq_chat(prompt)
    state["response"] = response
    print(state)
    return state

def build_mentorgraph():
    graph = StateGraph(MentorState)
    graph.add_node("mentor", Mentor_node)
    graph.set_entry_point("mentor")
    graph.add_edge("mentor", END)
    return graph.compile()



