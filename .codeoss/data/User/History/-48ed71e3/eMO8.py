from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)adk

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    req_data = request.get_json()
    # Extract user query from Dialogflow CX request
    user_query = ""
    try:
        user_query = req_data['text'] if 'text' in req_data else req_data['queryInput']['text']['text']
    except Exception:
        user_query = "No query found"

    # Call Gemini API
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_query}
                ]
            }
        ]
    }
    gemini_resp = requests.post(gemini_url, json=payload)
    if gemini_resp.status_code == 200:
        data = gemini_resp.json()
        answer = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "Sorry, I couldn't get an answer.")
        )
    else:
        answer = "Sorry, I couldn't get an answer from Gemini."

    # Respond in Dialogflow CX webhook format
    return jsonify({
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [answer]}}
            ]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)