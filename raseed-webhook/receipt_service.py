import requests
import os
from werkzeug.utils import secure_filename
import mimetypes

class ReceiptService:
    def __init__(self):
        self.receipt_processing_url = "https://us-central1-raseed-467016.cloudfunctions.net/process_receipt"
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    def allowed_file(self, filename):
        """Check if the uploaded file has an allowed extension"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def process_receipt(self, file):
        """Process a receipt by sending it to the external API"""
        try:
            if not file or not self.allowed_file(file.filename):
                return {
                    "error": "Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF) or PDF file."
                }
            
            # Prepare the file for upload
            files = {
                'file': (secure_filename(file.filename), file.read(), file.content_type)
            }
            
            # Send the file to the receipt processing API
            response = requests.post(
                self.receipt_processing_url,
                files=files,
                timeout=30  # 30 second timeout
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
            else:
                return {
                    "error": f"Receipt processing failed with status code: {response.status_code}",
                    "details": response.text
                }
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def process_receipt_from_url(self, image_url):
        """Process a receipt from a URL instead of file upload"""
        try:
            # Download the image from URL
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Determine content type
            content_type = response.headers.get('content-type', 'image/jpeg')
            
            # Create a file-like object
            from io import BytesIO
            file_obj = BytesIO(response.content)
            
            # Prepare for upload
            files = {
                'file': ('receipt.jpg', file_obj, content_type)
            }
            
            # Send to receipt processing API
            upload_response = requests.post(
                self.receipt_processing_url,
                files=files,
                timeout=30
            )
            
            if upload_response.status_code == 200:
                return {
                    "success": True,
                    "data": upload_response.json() if upload_response.headers.get('content-type', '').startswith('application/json') else upload_response.text
                }
            else:
                return {
                    "error": f"Receipt processing failed with status code: {upload_response.status_code}",
                    "details": upload_response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"} 