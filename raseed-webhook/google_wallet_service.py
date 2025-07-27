import uuid
from google_wallet_config import GoogleWalletConfig

class GoogleWalletService:
    def __init__(self):
        self.config = GoogleWalletConfig()
        self.service = self.config.get_wallet_service()
    
    def create_loyalty_class(self, class_name, program_name, issuer_name):
        """Create a loyalty class for Google Wallet"""
        if not self.service:
            return {"error": "Wallet service not available"}
        
        loyalty_class = {
            'id': f"{self.config.ISSUER_ID}.{self.config.CLASS_ID}",
            'issuerName': issuer_name,
            'programName': program_name,
            'programLogo': {
                'sourceUri': {
                    'uri': 'https://www.shutterstock.com/image-vector/link-icon-hyperlink-chain-symbol-260nw-1186749931.jpg'  # Replace with your logo URL
                }
            },
            'reviewStatus': 'UNDER_REVIEW',
            'allowMultipleUsersPerObject': True,
            'locations': [
                {
                    'kind': 'walletobjects#latLongPoint',
                    'latitude': 37.424015499999996,
                    'longitude': -122.09259560000001
                }
            ],
            'textModulesData': [
                {
                    'header': 'POINTS BALANCE',
                    'body': '1234'
                }
            ]
        }
        
        try:
            result = self.service.loyaltyclass().insert(body=loyalty_class).execute()
            return {"success": True, "class_id": result['id']}
        except Exception as e:
            return {"error": str(e)}
    
    def create_loyalty_object(self, user_email, user_name, points_balance=0):
        """Create a loyalty card for a specific user"""
        if not self.service:
            return {"error": "Wallet service not available"}
        
        object_id = f"{self.config.ISSUER_ID}.{uuid.uuid4()}"
        
        loyalty_object = {
            'id': object_id,
            'classId': f"{self.config.ISSUER_ID}.{self.config.CLASS_ID}",
            'state': 'ACTIVE',
            'heroImage': {
                'sourceUri': {
                    'uri': 'https://www.shutterstock.com/image-vector/link-icon-hyperlink-chain-symbol-260nw-1186749931.jpg'  # Replace with your image
                }
            },
            'textModulesData': [
                {
                    'header': 'POINTS BALANCE',
                    'body': str(points_balance)
                },
                {
                    'header': 'MEMBER SINCE',
                    'body': '2024'
                }
            ],
            'linksModuleData': {
                'uris': [
                    {
                        'uri': 'https://your-domain.com/terms',
                        'description': 'Terms of Service'
                    }
                ]
            },
            'imageModulesData': [
                {
                    'mainImage': {
                        'sourceUri': {
                            'uri': 'https://your-domain.com/qr-code.png'  # QR code if needed
                        }
                    }
                }
            ],
            'barcode': {
                'type': 'QR_CODE',
                'value': object_id,
                'alternateText': object_id
            },
            'locations': [
                {
                    'kind': 'walletobjects#latLongPoint',
                    'latitude': 37.424015499999996,
                    'longitude': -122.09259560000001
                }
            ],
            'accountId': user_email,
            'accountName': user_name,
            'loyaltyPoints': {
                'balance': {
                    'kind': 'walletobjects#loyaltyPointsBalance',
                    'stringBalance': str(points_balance)
                }
            }
        }
        
        try:
            result = self.service.loyaltyobject().insert(body=loyalty_object).execute()
            return {"success": True, "object_id": result['id']}
        except Exception as e:
            return {"error": str(e)}
    
    def get_save_url(self, object_id):
        """Generate a save URL for the user to add the card to their wallet"""
        if not self.service:
            return {"error": "Wallet service not available"}
        
        try:
            result = self.service.loyaltyobject().get(
                resourceId=object_id
            ).execute()
            
            save_url = f"https://pay.google.com/gp/v/save/{object_id}"
            return {"success": True, "save_url": save_url, "object": result}
        except Exception as e:
            return {"error": str(e)} 