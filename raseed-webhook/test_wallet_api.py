#!/usr/bin/env python3
"""
Simple test to call Google Wallet API directly
"""

from google_wallet_config import GoogleWalletConfig

def test_wallet_api():
    print("=== Testing Google Wallet API Directly ===")
    
    config = GoogleWalletConfig()
    service = config.get_wallet_service()
    
    if not service:
        print("❌ No wallet service available")
        return
    
    print(f"✅ Wallet service created")
    print(f"📋 Issuer ID: {config.ISSUER_ID}")
    print(f"📋 Class ID: {config.CLASS_ID}")
    
    # Test 1: Try to create a loyalty class
    print("\n🔍 Testing loyalty class creation...")
    
    loyalty_class = {
        'id': f"{config.ISSUER_ID}.{config.CLASS_ID}",
        'issuerName': 'Raseed Inc.',
        'programName': 'Raseed Rewards',
        'reviewStatus': 'UNDER_REVIEW',
        'allowMultipleUsersPerObject': True
    }
    
    try:
        result = service.loyaltyclass().insert(body=loyalty_class).execute()
        print(f"✅ Success! Class ID: {result['id']}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Try to get more details about the error
        if hasattr(e, 'resp') and hasattr(e.resp, 'status'):
            print(f"   Status: {e.resp.status}")
        if hasattr(e, 'content'):
            print(f"   Content: {e.content}")
        
        return None

if __name__ == "__main__":
    test_wallet_api() 