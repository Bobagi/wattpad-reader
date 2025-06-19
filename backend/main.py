from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/summaries")
def get_summaries():
    with open("/app/shared/summaries.json", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/")
def index():
    return "Wattpad Summarizer API. Use /summaries para ver os resumos."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
