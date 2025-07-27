# Raseed Webhook Setup Instructions

This guide will help you set up Google Wallet integration and receipt processing for your Raseed webhook service.

## Prerequisites

1. Python 3.7 or higher
2. Google Cloud Platform account
3. Google Wallet API access

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Google Wallet API Setup

### 2.1 Enable Google Wallet API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Wallet API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Wallet API"
   - Click "Enable"

### 2.2 Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - Name: `raseed-wallet-service`
   - Description: `Service account for Google Wallet integration`
4. Click "Create and Continue"
5. Skip role assignment (we'll handle this manually)
6. Click "Done"

### 2.3 Download Service Account Key

1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create New Key"
4. Choose "JSON" format
5. Download the key file and save it as `service-account-key.json` in the project root

### 2.4 Set Up Google Wallet Issuer Account

1. Go to [Google Wallet API Console](https://developers.google.com/wallet)
2. Sign up for the Google Wallet API
3. Create an issuer account
4. Note down your **Issuer ID** (you'll need this)

### 2.5 Create a Loyalty Class

1. In the Google Wallet API Console, create a loyalty class
2. Note down the **Class ID** (you'll need this)

## Step 3: Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_WALLET_ISSUER_ID=your_issuer_id_here
GOOGLE_WALLET_CLASS_ID=your_class_id_here
```

## Step 4: Update Configuration

### 4.1 Update Google Wallet Configuration

Edit `google_wallet_config.py` and update:
- `ISSUER_ID`: Your Google Wallet issuer ID
- `CLASS_ID`: Your Google Wallet class ID
- `SERVICE_ACCOUNT_FILE`: Path to your service account key file

### 4.2 Update Image URLs

In `google_wallet_service.py`, update the image URLs:
- Replace `https://your-domain.com/logo.png` with your actual logo URL
- Replace `https://your-domain.com/hero-image.png` with your actual hero image URL
- Replace `https://your-domain.com/qr-code.png` with your QR code image URL (if needed)

## Step 5: Test the Integration

### 5.1 Start the Server

```bash
python main.py
```

### 5.2 Test Google Wallet Endpoints

#### Create a Loyalty Class
```bash
curl -X POST http://localhost:8080/wallet/create-class \
  -H "Content-Type: application/json" \
  -d '{
    "class_name": "Raseed Loyalty Program",
    "program_name": "Raseed Rewards",
    "issuer_name": "Raseed Inc."
  }'
```

#### Create a Digital Card
```bash
curl -X POST http://localhost:8080/wallet/create-card \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "points": 100
  }'
```

### 5.3 Test Receipt Processing

#### Process Receipt from URL
```bash
curl -X POST http://localhost:8080/receipt/process-url \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/receipt.jpg"
  }'
```

#### Process Receipt File Upload
```bash
curl -X POST http://localhost:8080/receipt/process \
  -F "file=@/path/to/your/receipt.jpg"
```

## Step 6: Deploy to Cloud Run

### 6.1 Update Dockerfile

The existing Dockerfile should work, but make sure it includes:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "main.py"]
```

### 6.2 Deploy

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/raseed-webhook

# Deploy to Cloud Run
gcloud run deploy raseed-webhook \
  --image gcr.io/YOUR_PROJECT_ID/raseed-webhook \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_gemini_api_key,GOOGLE_WALLET_ISSUER_ID=your_issuer_id,GOOGLE_WALLET_CLASS_ID=your_class_id
```

## API Endpoints

### Google Wallet Endpoints

1. **POST /wallet/create-class**
   - Creates a loyalty class for Google Wallet
   - Body: `{"class_name": "...", "program_name": "...", "issuer_name": "..."}`

2. **POST /wallet/create-card**
   - Creates a digital loyalty card for a user
   - Body: `{"email": "...", "name": "...", "points": 100}`

### Receipt Processing Endpoints

1. **POST /receipt/process**
   - Upload a receipt file (image or PDF)
   - Form data with `file` field

2. **POST /receipt/process-url**
   - Process a receipt from a URL
   - Body: `{"image_url": "..."}`

### Original Endpoint

1. **POST /webhook**
   - Original Dialogflow webhook endpoint
   - Body: `{"text": "..."}`

## Troubleshooting

### Common Issues

1. **Service Account Key Not Found**
   - Make sure `service-account-key.json` is in the project root
   - Check file permissions

2. **Google Wallet API Errors**
   - Verify your issuer ID and class ID are correct
   - Ensure your service account has the necessary permissions
   - Check that the Google Wallet API is enabled

3. **Receipt Processing Errors**
   - Verify the receipt processing URL is accessible
   - Check file format (only PNG, JPG, JPEG, GIF, PDF allowed)
   - Ensure file size is under 16MB

### Debug Mode

To enable debug mode, add this to your `.env` file:
```env
FLASK_DEBUG=1
```

## Security Notes

1. Never commit `service-account-key.json` to version control
2. Use environment variables for sensitive data
3. Implement proper authentication for production use
4. Validate all input data
5. Implement rate limiting for production use 