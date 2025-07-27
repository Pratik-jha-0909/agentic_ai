from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from werkzeug.utils import secure_filename
from google_wallet_service import GoogleWalletService
from receipt_service import ReceiptService

app = Flask(__name__, static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# CORS headers function
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# CORS preflight handler
@app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = jsonify({'status': 'ok'})
    return add_cors_headers(response)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# Initialize services
wallet_service = GoogleWalletService()
receipt_service = ReceiptService()

@app.route('/')
def index():
    response = send_from_directory('static', 'index.html')
    return add_cors_headers(response)

@app.route('/<path:filename>')
def static_files(filename):
    response = send_from_directory('static', filename)
    return add_cors_headers(response)

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
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
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
    response = jsonify({
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [answer]}}
            ]
        }
    })
    return add_cors_headers(response)

# Google Wallet Endpoints
@app.route('/wallet/create-card', methods=['POST'])
def create_wallet_card():
    """Create a digital card for Google Wallet"""
    try:
        data = request.get_json()
        user_email = data.get('email')
        user_name = data.get('name', 'User')
        points_balance = data.get('points', 0)
        
        if not user_email:
            response = jsonify({"error": "Email is required"})
            return add_cors_headers(response), 400
        
        # Create the loyalty card
        result = wallet_service.create_loyalty_object(user_email, user_name, points_balance)
        
        if result.get("success"):
            # Get the save URL
            save_result = wallet_service.get_save_url(result["object_id"])
            if save_result.get("success"):
                response = jsonify({
                    "success": True,
                    "card_id": result["object_id"],
                    "save_url": save_result["save_url"],
                    "message": "Digital card created successfully. Use the save_url to add it to your Google Wallet."
                })
                return add_cors_headers(response)
        
        response = jsonify(result)
        return add_cors_headers(response), 400
        
    except Exception as e:
        response = jsonify({"error": str(e)})
        return add_cors_headers(response), 500

@app.route('/wallet/create-class', methods=['POST'])
def create_wallet_class():
    """Create a loyalty class for Google Wallet"""
    try:
        data = request.get_json()
        class_name = data.get('class_name', 'Loyalty Program')
        program_name = data.get('program_name', 'Raseed Loyalty')
        issuer_name = data.get('issuer_name', 'Raseed')
        
        result = wallet_service.create_loyalty_class(class_name, program_name, issuer_name)
        
        if result.get("success"):
            response = jsonify({
                "success": True,
                "class_id": result["class_id"],
                "message": "Loyalty class created successfully"
            })
            return add_cors_headers(response)
        
        response = jsonify(result)
        return add_cors_headers(response), 400
        
    except Exception as e:
        response = jsonify({"error": str(e)})
        return add_cors_headers(response), 500

# Receipt Processing Endpoints
@app.route('/receipt/process', methods=['POST'])
def process_receipt():
    """Process a receipt by uploading a file"""
    try:
        if 'file' not in request.files:
            response = jsonify({"error": "No file provided"})
            return add_cors_headers(response), 400
        
        file = request.files['file']
        if file.filename == '':
            response = jsonify({"error": "No file selected"})
            return add_cors_headers(response), 400
        
        result = receipt_service.process_receipt(file)
        
        if result.get("success"):
            response = jsonify({
                "success": True,
                "data": result["data"],
                "message": "Receipt processed successfully"
            })
            return add_cors_headers(response)
        
        response = jsonify(result)
        return add_cors_headers(response), 400
        
    except Exception as e:
        response = jsonify({"error": str(e)})
        return add_cors_headers(response), 500

@app.route('/receipt/process-url', methods=['POST'])
def process_receipt_from_url():
    """Process a receipt from a URL"""
    try:
        data = request.get_json()
        image_url = data.get('image_url')
        
        if not image_url:
            response = jsonify({"error": "Image URL is required"})
            return add_cors_headers(response), 400
        
        result = receipt_service.process_receipt_from_url(image_url)
        
        if result.get("success"):
            response = jsonify({
                "success": True,
                "data": result["data"],
                "message": "Receipt processed successfully"
            })
            return add_cors_headers(response)
        
        response = jsonify(result)
        return add_cors_headers(response), 400
        
    except Exception as e:
        response = jsonify({"error": str(e)})
        return add_cors_headers(response), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)