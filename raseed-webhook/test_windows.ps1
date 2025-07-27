# PowerShell Test Script for Raseed Webhook Service
$baseUrl = "http://localhost:8080"

Write-Host "Testing Raseed Webhook Service..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Test 1: Check if server is running
Write-Host "`n1. Testing server status..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/" -Method GET
    Write-Host "✓ Server is running: $response" -ForegroundColor Green
} catch {
    Write-Host "✗ Server is not running or not accessible" -ForegroundColor Red
    Write-Host "Make sure to run: python main.py" -ForegroundColor Red
    exit 1
}

# Test 2: Test original webhook endpoint
Write-Host "`n2. Testing original webhook endpoint..." -ForegroundColor Yellow
try {
    $body = @{
        text = "Hello, how can you help me?"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$baseUrl/webhook" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✓ Webhook response received" -ForegroundColor Green
    Write-Host "Response: $($response.fulfillment_response.messages[0].text.text[0])" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Webhook test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Test Google Wallet class creation
Write-Host "`n3. Testing Google Wallet class creation..." -ForegroundColor Yellow
try {
    $body = @{
        class_name = "Raseed Loyalty Program"
        program_name = "Raseed Rewards"
        issuer_name = "Raseed Inc."
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$baseUrl/wallet/create-class" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✓ Wallet class creation response received" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Wallet class creation failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Note: This will fail if Google Wallet API is not configured" -ForegroundColor Yellow
}

# Test 4: Test Google Wallet card creation
Write-Host "`n4. Testing Google Wallet card creation..." -ForegroundColor Yellow
try {
    $body = @{
        email = "test@example.com"
        name = "John Doe"
        points = 100
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$baseUrl/wallet/create-card" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✓ Wallet card creation response received" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Wallet card creation failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Note: This will fail if Google Wallet API is not configured" -ForegroundColor Yellow
}

# Test 5: Test receipt processing from URL
Write-Host "`n5. Testing receipt processing from URL..." -ForegroundColor Yellow
try {
    $body = @{
        image_url = "https://example.com/receipt.jpg"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$baseUrl/receipt/process-url" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✓ Receipt processing response received" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Depth 3)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Receipt processing failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Note: This will fail with the example URL" -ForegroundColor Yellow
}

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "Testing completed!" -ForegroundColor Green
Write-Host "`nTo test file upload, you can use a web browser or Postman:" -ForegroundColor Yellow
Write-Host "POST http://localhost:8080/receipt/process" -ForegroundColor Cyan
Write-Host "Content-Type: multipart/form-data" -ForegroundColor Cyan
Write-Host "Body: file=@your_receipt.jpg" -ForegroundColor Cyan 