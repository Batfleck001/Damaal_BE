from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from utils import Utils
from datetime import date
u = Utils()

current_date = date.today()

class ExpenseState(TypedDict):
    expense: list[dict]
    balance: int
    bal_bef_expense: int
    response: str

def Expense_node(state: ExpenseState):
    expense_log = state["expense"]
    balance = state["balance"]
    bal_bef_expense = state['bal_bef_expense']

    prompt = f"""
    
    You are a practical financial advisor AI.

        every single day's expense record = {expense_log}
        balance before expense = {bal_bef_expense}
        balance after expense = {balance}
        current date = {current_date}

        Analyze a single day’s expense record and return only one compact paragraph.

        Rules you MUST follow:

            Output must be 3–5 sentences in a single line
            Do NOT use line breaks, newlines, or paragraph spacing
            Do NOT use bullet points, numbering, or headings
            Do NOT include emojis
            Do NOT repeat the expense data
            Do not ask questions


        Focus on:

        Comment on whether spending was reasonable or excessive
        Identify at least one unnecessary or optimizable expense if present
        Mention one saving or income improvement opportunity
        Give one clear actionable suggestion for the next day

        Maintain a supportive, non-judgmental tone

        Do not repeat the expense data.
        Do not ask questions.
        Do not give generic advice.

        Tone: clear, professional, practical, and supportive.
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
