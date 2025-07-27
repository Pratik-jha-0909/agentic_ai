#!/usr/bin/env python3

import json
from google_wallet_config import GoogleWalletConfig
from google_wallet_service import GoogleWalletService

def test_wallet_config():
    print("Testing Google Wallet Configuration...")
    
    # Test config
    config = GoogleWalletConfig()
    print(f"Issuer ID: {config.ISSUER_ID}")
    print(f"Class ID: {config.CLASS_ID}")
    print(f"Service Account File: {config.SERVICE_ACCOUNT_FILE}")
    
    # Test credentials
    credentials = config.get_credentials()
    if credentials:
        print("✓ Credentials loaded successfully")
    else:
        print("✗ Failed to load credentials")
        return False
    
    # Test service
    service = config.get_wallet_service()
    if service:
        print("✓ Wallet service created successfully")
    else:
        print("✗ Failed to create wallet service")
        return False
    
    return True

def test_wallet_service():
    print("\nTesting Google Wallet Service...")
    
    wallet_service = GoogleWalletService()
    
    # Test create loyalty class
    print("Testing create_loyalty_class...")
    result = wallet_service.create_loyalty_class(
        class_name="Test Class",
        program_name="Test Program", 
        issuer_name="Test Issuer"
    )
    
    print(f"Result: {json.dumps(result, indent=2)}")
    
    return result.get("success", False)

if __name__ == "__main__":
    print("=== Google Wallet Debug Test ===\n")
    
    if test_wallet_config():
        test_wallet_service()
    else:
        print("Configuration test failed, skipping service test") 