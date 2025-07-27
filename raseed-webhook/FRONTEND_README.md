# Raseed Frontend - Digital Wallet & Receipt Processing

A beautiful, modern web interface for managing Google Wallet digital cards and processing receipts.

## 🚀 Features

### 📱 **Google Wallet Management**
- **Create Loyalty Classes**: Set up loyalty programs for your business
- **Create Digital Cards**: Issue digital loyalty cards to users
- **Activity Tracking**: Monitor all wallet operations in real-time
- **Save URLs**: Direct links to add cards to Google Wallet

### 📄 **Receipt Processing**
- **File Upload**: Upload receipt images or PDFs directly
- **URL Processing**: Process receipts from image URLs
- **Real-time Results**: View processing results instantly
- **Multiple Formats**: Support for PNG, JPG, JPEG, GIF, PDF

### 🤖 **AI Chat Assistant**
- **Interactive Chat**: Chat with the AI assistant
- **Gemini Integration**: Powered by Google's Gemini AI
- **Real-time Responses**: Get instant answers to your questions

## 🎨 **UI Features**

- **Modern Design**: Beautiful gradient background and clean interface
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Tab Navigation**: Easy switching between different features
- **Loading States**: Visual feedback during API calls
- **Notifications**: Success/error notifications with auto-dismiss
- **Activity Logs**: Track all operations with timestamps

## 🛠 **Technical Stack**

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with Flexbox and Grid
- **Icons**: Font Awesome 6.0
- **Fonts**: Inter (Google Fonts)
- **Backend**: Flask (Python)
- **API**: RESTful endpoints with JSON responses

## 📁 **File Structure**

```
static/
├── index.html          # Main HTML file
├── styles.css          # CSS styles
└── script.js           # JavaScript functionality
```

## 🚀 **Getting Started**

1. **Start the Flask Server**:
   ```bash
   python main.py
   ```

2. **Open Your Browser**:
   Navigate to `http://localhost:8080`

3. **Start Using the Features**:
   - Switch between tabs to access different features
   - Fill out forms and submit requests
   - View real-time results and activity logs

## 📋 **API Endpoints Used**

### Google Wallet
- `POST /wallet/create-class` - Create loyalty class
- `POST /wallet/create-card` - Create digital card

### Receipt Processing
- `POST /receipt/process` - Upload receipt file
- `POST /receipt/process-url` - Process receipt from URL

### AI Chat
- `POST /webhook` - Send chat messages to AI

## 🎯 **Usage Examples**

### Creating a Digital Card
1. Go to the "Google Wallet" tab
2. Fill in the user details (email, name, points)
3. Click "Create Card"
4. View the generated save URL to add to Google Wallet

### Processing a Receipt
1. Go to the "Receipt Processing" tab
2. Either upload a file or provide a URL
3. Click "Process Receipt"
4. View the processing results

### Chatting with AI
1. Go to the "AI Chat" tab
2. Type your message
3. Press Enter or click the send button
4. View the AI response

## 🔧 **Configuration**

The frontend automatically connects to the Flask backend at `http://localhost:8080`. To change the API URL, edit the `API_BASE_URL` constant in `script.js`.

## 📱 **Mobile Responsive**

The interface is fully responsive and works great on:
- Desktop computers
- Tablets
- Mobile phones

## 🎨 **Customization**

### Colors
The main color scheme uses:
- Primary: `#667eea` (Blue)
- Success: `#28a745` (Green)
- Error: `#dc3545` (Red)
- Info: `#17a2b8` (Cyan)

### Styling
All styles are in `styles.css` and can be easily customized:
- Change colors in the CSS variables
- Modify layouts using Flexbox/Grid
- Adjust spacing and typography

## 🔒 **Security Features**

- Input validation on all forms
- File type restrictions for uploads
- Size limits for file uploads (16MB max)
- CORS handling for API requests
- Error handling and user feedback

## 🚀 **Deployment**

To deploy the frontend with the backend:

1. **Build and deploy the Flask app** to your preferred hosting service
2. **Update the API_BASE_URL** in `script.js` to point to your deployed backend
3. **Serve the static files** from your web server

## 📞 **Support**

If you encounter any issues:
1. Check the browser console for JavaScript errors
2. Verify the Flask server is running
3. Ensure all API endpoints are accessible
4. Check the network tab for failed requests

## 🎉 **Enjoy!**

The frontend provides a complete, user-friendly interface for all your Raseed platform features. Happy coding! 🚀 