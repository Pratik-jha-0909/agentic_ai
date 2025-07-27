#!/usr/bin/env python3
"""
Debug script to test Google Wallet configuration
"""

import os
import json
from google_wallet_config import GoogleWalletConfig
from google_wallet_service import GoogleWalletService

def test_config():
    print("=== Testing Google Wallet Configuration ===")
    
    # Test 1: Check environment variables
    print("\n1. Environment Variables:")
    issuer_id = os.environ.get('GOOGLE_WALLET_ISSUER_ID', '3388000000022969042')
    class_id = os.environ.get('GOOGLE_WALLET_CLASS_ID', '3388000000022969042-raseed')
    print(f"   ISSUER_ID: {issuer_id}")
    print(f"   CLASS_ID: {class_id}")
    
    # Test 2: Check service account file
    print("\n2. Service Account File:")
    config = GoogleWalletConfig()
    print(f"   Service Account File Path: {config.SERVICE_ACCOUNT_FILE}")
    
    if os.path.exists(config.SERVICE_ACCOUNT_FILE):
        print("   ✓ Service account file exists")
        try:
            with open(config.SERVICE_ACCOUNT_FILE, 'r') as f:
                data = json.load(f)
                print(f"   ✓ Service account file is valid JSON")
                print(f"   Project ID: {data.get('project_id', 'N/A')}")
                print(f"   Client Email: {data.get('client_email', 'N/A')}")
        except Exception as e:
            print(f"   ✗ Error reading service account file: {e}")
    else:
        print("   ✗ Service account file not found")
    
    # Test 3: Test credentials
    print("\n3. Testing Credentials:")
    try:
        credentials = config.get_credentials()
        if credentials:
            print("   ✓ Credentials created successfully")
            print(f"   Scopes: {credentials.scopes}")
        else:
            print("   ✗ Failed to create credentials")
    except Exception as e:
        print(f"   ✗ Error creating credentials: {e}")
    
    # Test 4: Test wallet service
    print("\n4. Testing Wallet Service:")
    try:
        service = config.get_wallet_service()
        if service:
            print("   ✓ Wallet service created successfully")
            # Try to list loyalty classes to test API access
            try:
                result = service.loyaltyclass().list().execute()
                print("   ✓ API access confirmed - can list loyalty classes")
            except Exception as api_error:
                print(f"   ⚠ API access issue: {api_error}")
        else:
            print("   ✗ Failed to create wallet service")
    except Exception as e:
        print(f"   ✗ Error creating wallet service: {e}")

if __name__ == "__main__":
    test_config() 