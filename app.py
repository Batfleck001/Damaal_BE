from flask import jsonify,Flask, request
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from utils import insert, getall
from Agents.MentorAgent import build_mentorgraph

graph = build_mentorgraph()


load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return "Supabase connected"

@app.route("/postlog", methods=["POST"])
def add_user():
    data = request.json

    log = data.get("log")
    expense = data.get("expense")

    Advice = graph.invoke({"log":log})

    print(Advice)

    result = insert("Daily_logs",{
        "log" : log,
        "advice" : Advice.get("response"),
        "expense" : expense
    })

    return jsonify(result.data)

@app.route("/list", methods=["GET"])
def list_users():
    result = getall("Daily_logs")
    return jsonify(result.data)


if __name__ == "__main__":
    app.run(port=5000, debug=True)