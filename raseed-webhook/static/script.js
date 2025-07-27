// API Base URL - Use the same origin as the current page
const API_BASE_URL = window.location.origin;

// DOM Elements
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');
const loadingOverlay = document.getElementById('loadingOverlay');
const notification = document.getElementById('notification');

// Tab Navigation
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');
        
        // Update active tab button
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update active tab pane
        tabPanes.forEach(pane => pane.classList.remove('active'));
        document.getElementById(targetTab).classList.add('active');
    });
});

// Utility Functions
function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    loadingOverlay.classList.add('hidden');
}

function showNotification(message, type = 'info') {
    const notificationEl = document.getElementById('notification');
    const messageEl = notificationEl.querySelector('.notification-message');
    const iconEl = notificationEl.querySelector('.notification-icon');
    
    messageEl.textContent = message;
    notificationEl.className = `notification ${type}`;
    
    // Set icon based on type
    if (type === 'success') {
        iconEl.className = 'notification-icon fas fa-check-circle';
    } else if (type === 'error') {
        iconEl.className = 'notification-icon fas fa-exclamation-circle';
    } else {
        iconEl.className = 'notification-icon fas fa-info-circle';
    }
    
    notificationEl.classList.remove('hidden');
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        notificationEl.classList.add('hidden');
    }, 5000);
}

// Close notification
document.querySelector('.notification-close').addEventListener('click', () => {
    notification.classList.add('hidden');
});

// API Functions
async function makeRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Google Wallet Functions
async function createLoyaltyClass(formData) {
    const data = {
        class_name: formData.get('class_name'),
        program_name: formData.get('program_name'),
        issuer_name: formData.get('issuer_name')
    };
    
    const response = await makeRequest(`${API_BASE_URL}/wallet/create-class`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    
    return response;
}

async function createDigitalCard(formData) {
    const data = {
        email: formData.get('email'),
        name: formData.get('name'),
        points: parseInt(formData.get('points'))
    };
    
    const response = await makeRequest(`${API_BASE_URL}/wallet/create-card`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    
    return response;
}

// Receipt Processing Functions
async function processReceiptFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/receipt/process`, {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

async function processReceiptUrl(url) {
    const data = { image_url: url };
    
    const response = await makeRequest(`${API_BASE_URL}/receipt/process-url`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    
    return response;
}

// Chat Functions
async function sendChatMessage(message) {
    const data = { text: message };
    
    const response = await makeRequest(`${API_BASE_URL}/webhook`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    
    return response;
}

// Form Event Listeners
document.getElementById('createClassForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading();
    
    try {
        const formData = new FormData(e.target);
        const response = await createLoyaltyClass(formData);
        
        if (response.success) {
            showNotification('Loyalty class created successfully!', 'success');
            addWalletActivity('Loyalty class created', 'success', response.class_id);
        } else {
            showNotification(response.error || 'Failed to create loyalty class', 'error');
            addWalletActivity('Failed to create loyalty class', 'error', response.error);
        }
    } catch (error) {
        showNotification('Error creating loyalty class: ' + error.message, 'error');
        addWalletActivity('Error creating loyalty class', 'error', error.message);
    } finally {
        hideLoading();
    }
});

document.getElementById('createCardForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading();
    
    try {
        const formData = new FormData(e.target);
        const response = await createDigitalCard(formData);
        
        if (response.success) {
            showNotification('Digital card created successfully!', 'success');
            addWalletActivity('Digital card created', 'success', `Card ID: ${response.card_id}`);
            
            // Show save URL if available
            if (response.save_url) {
                addWalletActivity('Save URL generated', 'success', 
                    `<a href="${response.save_url}" target="_blank">Click to add to Google Wallet</a>`);
            }
        } else {
            showNotification(response.error || 'Failed to create digital card', 'error');
            addWalletActivity('Failed to create digital card', 'error', response.error);
        }
    } catch (error) {
        showNotification('Error creating digital card: ' + error.message, 'error');
        addWalletActivity('Error creating digital card', 'error', error.message);
    } finally {
        hideLoading();
    }
});

document.getElementById('uploadReceiptForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('receiptFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showNotification('Please select a file', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await processReceiptFile(file);
        
        if (response.success) {
            showNotification('Receipt processed successfully!', 'success');
            addReceiptResult('Receipt processed', 'success', response.data);
        } else {
            showNotification(response.error || 'Failed to process receipt', 'error');
            addReceiptResult('Failed to process receipt', 'error', response.error);
        }
    } catch (error) {
        showNotification('Error processing receipt: ' + error.message, 'error');
        addReceiptResult('Error processing receipt', 'error', error.message);
    } finally {
        hideLoading();
        fileInput.value = ''; // Clear file input
    }
});

document.getElementById('urlReceiptForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const urlInput = document.getElementById('receiptUrl');
    const url = urlInput.value.trim();
    
    if (!url) {
        showNotification('Please enter a valid URL', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await processReceiptUrl(url);
        
        if (response.success) {
            showNotification('Receipt processed successfully!', 'success');
            addReceiptResult('Receipt processed from URL', 'success', response.data);
        } else {
            showNotification(response.error || 'Failed to process receipt', 'error');
            addReceiptResult('Failed to process receipt from URL', 'error', response.error);
        }
    } catch (error) {
        showNotification('Error processing receipt: ' + error.message, 'error');
        addReceiptResult('Error processing receipt from URL', 'error', error.message);
    } finally {
        hideLoading();
        urlInput.value = ''; // Clear URL input
    }
});

document.getElementById('chatForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addChatMessage(message, 'user');
    input.value = '';
    
    showLoading();
    
    try {
        const response = await sendChatMessage(message);
        
        if (response.fulfillment_response && response.fulfillment_response.messages) {
            const botMessage = response.fulfillment_response.messages[0].text.text[0];
            addChatMessage(botMessage, 'bot');
        } else {
            addChatMessage('Sorry, I couldn\'t process your request.', 'bot');
        }
    } catch (error) {
        addChatMessage('Error: ' + error.message, 'bot');
        showNotification('Error sending message: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
});

// UI Update Functions
function addWalletActivity(title, type, details) {
    const activityList = document.getElementById('walletActivity');
    const activityItem = document.createElement('div');
    activityItem.className = `activity-item ${type}`;
    
    const icon = type === 'success' ? 'fas fa-check-circle' : 
                 type === 'error' ? 'fas fa-exclamation-circle' : 
                 'fas fa-info-circle';
    
    activityItem.innerHTML = `
        <i class="${icon}"></i>
        <div>
            <strong>${title}</strong>
            <div style="font-size: 0.9rem; color: #6c757d; margin-top: 5px;">
                ${typeof details === 'string' ? details : JSON.stringify(details, null, 2)}
            </div>
        </div>
    `;
    
    activityList.insertBefore(activityItem, activityList.firstChild);
    
    // Keep only last 10 activities
    const activities = activityList.querySelectorAll('.activity-item');
    if (activities.length > 10) {
        activities[activities.length - 1].remove();
    }
}

function addReceiptResult(title, type, details) {
    const resultsContainer = document.getElementById('receiptResults');
    const resultItem = document.createElement('div');
    resultItem.className = `result-item ${type}`;
    
    const icon = type === 'success' ? 'fas fa-check-circle' : 
                 type === 'error' ? 'fas fa-exclamation-circle' : 
                 'fas fa-info-circle';
    
    let detailsContent = details;
    if (typeof details === 'object') {
        detailsContent = `<pre style="font-size: 0.8rem; margin-top: 10px; white-space: pre-wrap;">${JSON.stringify(details, null, 2)}</pre>`;
    }
    
    resultItem.innerHTML = `
        <i class="${icon}"></i>
        <div>
            <strong>${title}</strong>
            ${detailsContent}
        </div>
    `;
    
    resultsContainer.insertBefore(resultItem, resultsContainer.firstChild);
    
    // Keep only last 5 results
    const results = resultsContainer.querySelectorAll('.result-item');
    if (results.length > 5) {
        results[results.length - 1].remove();
    }
}

function addChatMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const icon = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
    
    messageDiv.innerHTML = `
        <i class="${icon}"></i>
        <div class="message-content">${message}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// File input preview
document.getElementById('receiptFile').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const fileInfo = document.querySelector('.file-info');
        fileInfo.innerHTML = `
            <small>Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</small>
        `;
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Raseed Frontend initialized');
    console.log('API Base URL:', API_BASE_URL);
    
    // Test API connection
    fetch(`${API_BASE_URL}/`)
        .then(response => response.text())
        .then(data => {
            console.log('API Status:', data);
        })
        .catch(error => {
            console.error('API Connection Error:', error);
            showNotification('Warning: Cannot connect to API server', 'error');
        });
}); 