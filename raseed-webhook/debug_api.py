import requests
import json

# Test API endpoints
base_url = "http://127.0.0.1:8080"

def test_endpoint(endpoint, data, description):
    print(f"\n=== Testing {description} ===")
    print(f"Endpoint: {endpoint}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(f"{base_url}{endpoint}", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
        else:
            print("❌ FAILED")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

# Test data
webhook_data = {
    "text": "Hello, how are you?"
}

create_class_data = {
    "class_name": "Test Class",
    "program_name": "Test Program", 
    "issuer_name": "Test Issuer"
}

create_card_data = {
    "email": "test@example.com",
    "name": "Test User",
    "points": 100
}

receipt_url_data = {
    "image_url": "https://example.com/test.jpg"
}

# Test all endpoints
test_endpoint("/webhook", webhook_data, "Webhook")
test_endpoint("/wallet/create-class", create_class_data, "Create Loyalty Class")
test_endpoint("/wallet/create-card", create_card_data, "Create Digital Card")
test_endpoint("/receipt/process-url", receipt_url_data, "Process Receipt URL")

print("\n=== Debug Complete ===") 