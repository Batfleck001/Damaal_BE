from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from utils import Utils

u = Utils()

class ExpenseState(TypedDict):
    expense: list[dict]
    balance: int
    response: str

def Expense_node(state: ExpenseState):
    expense_log = state["expense"]
    balance = state["balance"]

    prompt = f"""
        
    You are an expert personal finance advisor who analyzes a user's day-to-day expense record and their remaining balance.

        User's Record:
        Expense of the day : {expense_log}, Balance we have after these expense : {balance}

        Based on this log, give a clear and practical 3-5 lines response including:
        - Key spending insights
        - Where unnecessary money leaked
        - What to change tomorrow for better financial discipline
        - How to stay on track with the remaining balance

        Tone: direct, practical, and supportive. Do NOT use bullet points or subheadings. Just write 3-5 impactful lines.
"""

    response = u.groq_chat_lite(prompt)
    state["response"] = response
    return state

def build_Expensegraph():
    graph = StateGraph(ExpenseState)
    graph.add_node("expense", Expense_node)
    graph.set_entry_point("expense")
    graph.add_edge("expense", END)
    return graph.compile()
