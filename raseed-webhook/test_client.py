import requests
import json

# Base URL for your Flask app
BASE_URL = "http://localhost:8080"

def test_create_wallet_card():
    """Test creating a Google Wallet card"""
    url = f"{BASE_URL}/wallet/create-card"
    data = {
        "email": "test@example.com",
        "name": "John Doe",
        "points": 100
    }
    
    response = requests.post(url, json=data)
    print("Create Wallet Card Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_create_wallet_class():
    """Test creating a Google Wallet loyalty class"""
    url = f"{BASE_URL}/wallet/create-class"
    data = {
        "class_name": "Raseed Loyalty Program",
        "program_name": "Raseed Rewards",
        "issuer_name": "Raseed Inc."
    }
    
    response = requests.post(url, json=data)
    print("Create Wallet Class Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_process_receipt_from_url():
    """Test processing a receipt from a URL"""
    url = f"{BASE_URL}/receipt/process-url"
    data = {
        "image_url": "https://example.com/receipt.jpg"  # Replace with actual receipt image URL
    }
    
    response = requests.post(url, json=data)
    print("Process Receipt from URL Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

def test_webhook():
    """Test the original webhook endpoint"""
    url = f"{BASE_URL}/webhook"
    data = {
        "text": "Hello, how can you help me?"
    }
    
    response = requests.post(url, json=data)
    print("Webhook Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json()

if __name__ == "__main__":
    print("Testing Raseed Webhook Service...")
    print("=" * 50)
    
    # Test webhook
    test_webhook()
    print("\n" + "=" * 50)
    
    # Test Google Wallet class creation
    test_create_wallet_class()
    print("\n" + "=" * 50)
    
    # Test Google Wallet card creation
    test_create_wallet_card()
    print("\n" + "=" * 50)
    
    # Test receipt processing
    test_process_receipt_from_url() 