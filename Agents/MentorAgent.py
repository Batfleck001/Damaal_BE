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
    You are a concise self-improvement advisor.

        Analyze the user's daily log: {dlog}

        Based on the log, give a short 3-5 line response that:
        • Points out what went well (only if relevant)
        • Identifies mistakes, inefficiencies, or weak decisions
        • Suggests 1-2 practical improvements or experiments to try next
        • Gently pushes accountability and growth

        Rules:
        - Do NOT use line breaks, newlines, or paragraph spacing
        - Do not use bullet points, numbering, headings, or emojis
        - Do not repeat the log
        - Keep it direct, honest, and actionable
        - Write each sentence as a single line
        - Avoid unnecessary praise or motivational fluff

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



