from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from utils import groq_chat

class MentorState(TypedDict):
    log: str
    response: str

def Mentor_node(state: MentorState):
    dlog = state["log"]

    prompt = f"""
    You are a high-performance self-development mentor who specializes in building courage, exploring new ways to make money, and helping people break limitations.
    Your job is to analyze the user’s daily log {dlog} with clarity and honesty.
    For every daily log, deliver a 3–5 line response containing:
        1. Wins of the Day
        2. Limits & Fears Noticed
        3. Money & Growth Opportunities
        4. Corrections for Tomorrow
        5. Self-Development Push
    Tone must be direct, growth-focused, and empowering.
    """

    response = groq_chat(prompt)
    state["response"] = response
    return state

def build_mentorgraph():
    graph = StateGraph(MentorState)
    graph.add_node("mentor", Mentor_node)
    graph.set_entry_point("mentor")
    graph.add_edge("mentor", END)
    return graph.compile()
