import os
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleWalletConfig:
    def __init__(self):
        # You'll need to download your service account key from Google Cloud Console
        # and save it as 'service-account-key.json' in this directory
        self.SCOPES = ['https://www.googleapis.com/auth/wallet_object.issuer']
        self.SERVICE_ACCOUNT_FILE = 'service-account-key.json'
        
        # Your Google Wallet issuer ID (you'll get this from Google Wallet API setup)
        self.ISSUER_ID = os.environ.get('GOOGLE_WALLET_ISSUER_ID', '3388000000022969042')
        
        # Your Google Wallet class ID (you'll create this)
        self.CLASS_ID = os.environ.get('GOOGLE_WALLET_CLASS_ID', '3388000000022969042-raseed')
        
    def get_credentials(self):
        """Get service account credentials for Google Wallet API"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES
            )
            return credentials
        except FileNotFoundError:
            print("Service account key file not found. Please download it from Google Cloud Console.")
            return None
    
    def get_wallet_service(self):
        """Get Google Wallet API service"""
        credentials = self.get_credentials()
        if credentials:
            return build('walletobjects', 'v1', credentials=credentials)
        return None 