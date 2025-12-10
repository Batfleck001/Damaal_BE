from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from utils import Utils

u = Utils()

class MentorState(TypedDict):
    log: str
    response: str

def Mentor_node(state: MentorState):
    dlog = state["log"]

    prompt_template = f"""
    You are a high-performance self-development mentor.

        Analyze the user’s daily log {dlog} and produce a sharp 1–2 line summary.
        Include only the most important insights about progress, limitations, growth or money opportunities, and the most critical correction or push for tomorrow, if relevant.

        Tone: direct, honest, growth-focused, and actionable.
        No labels, no bullets, no formatting.
        Keep the response extremely concise and under 220 tokens.
    """

    response = u.groq_chat(prompt_template)
    state["response"] = response
    print(state)
    return state

def build_mentorgraph():
    graph = StateGraph(MentorState)
    graph.add_node("mentor", Mentor_node)
    graph.set_entry_point("mentor")
    graph.add_edge("mentor", END)
    return graph.compile()



