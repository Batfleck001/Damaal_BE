from flask import jsonify,Flask, request
from supabase import create_client, Client
from dotenv import load_dotenv
from utils import Utils
from Agents.MentorAgent import build_mentorgraph
from Agents.ExpenseAgent import build_Expensegraph
import json

mentorgraph = build_mentorgraph()
expensegraph = build_Expensegraph()

app = Flask(__name__)

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
    total = u.add_json_nums(expense)
    expense["total"] = total
    resp = u.last_updated_get("Daily_logs", "balance")
    current_balance  = resp.data[0]["balance"]
    updated_balance = current_balance - total

    Advice = mentorgraph.invoke({"log":log})
    print(Advice)

    ExpenseAdvice = expensegraph.invoke({"expense" : expense, "balance" : updated_balance})
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
    app.run(port=5000, debug=True)