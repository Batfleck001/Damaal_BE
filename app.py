from flask import jsonify,Flask, request
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from utils import insert, getall

load_dotenv()

app = Flask(__name__)



@app.route("/")
def home():
    return "Supabase connected"

@app.route("/add", methods=["POST"])
def add_user():
    data = request.json
    log = data.get("log")

    result = insert("Daily_logs",{
        "log" : log
    })

    return jsonify(result.data)

@app.route("/list", methods=["GET"])
def list_users():
    result = getall("Daily_logs")
    return jsonify(result.data)


if __name__ == "__main__":
    app.run(port=5000, debug=True)