from flask import jsonify,Flask, request
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
from utils import Utils
from Agents.MentorAgent import build_mentorgraph
from Agents.ExpenseAgent import build_Expensegraph
import json,os

mentorgraph = build_mentorgraph()
expensegraph = build_Expensegraph()

app = Flask(__name__)
CORS(app)
#include Utils

u = Utils()

@app.route("/")
def home():
    return "Supabase connected"

@app.route("/postlog", methods=["POST"])
def add_user():
    data = request.json

    log = data.get("log")
    expense = data.get("expense")

    #total expense of the day
    total = u.calculate_total(expense)
    expense["total_spending"] = total.get("total_spending")
    expense["total_income"] = total.get("total_income")
    resp = u.last_updated_get("Daily_logs", "balance")
    current_balance  = resp.data[0]["balance"]
    updated_balance = current_balance - total.get("total_spending")
    updated_balance += total.get("total_income")

    Advice = mentorgraph.invoke({"log":log})
    print(Advice)

    ExpenseAdvice = expensegraph.invoke({"expense" : expense,"bal_bef_expense":current_balance , "balance" : updated_balance})
#included necessary info
    result = u.insert("Daily_logs",{
        "log" : log,
        "advice" : Advice.get("response"),
        "expense" : expense,
        "expense_advice" : ExpenseAdvice.get("response"),
        "balance" : updated_balance
    })

    return jsonify(result.data)

@app.route("/gb", methods=["GET"])
def get_balance():
    result = u.last_updated_get("Daily_logs","balance")
    return jsonify(result.data)



@app.route("/balance", methods=["POST"])
def new_balance():
    data = request.json
    balance = data.get("balance")

    result = u.insert("Daily_logs",{
        "balance" : balance
    })

    return jsonify(result.data)


@app.route("/list", methods=["GET"])
def list_users():
    result = u.getall("Daily_logs")
    return jsonify(result.data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))