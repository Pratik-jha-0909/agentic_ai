# Simple PowerShell Test Script
$baseUrl = "http://localhost:8080"

Write-Host "Testing Raseed Webhook Service..." -ForegroundColor Green

# Test 1: Check if server is running
Write-Host "`n1. Testing server status..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/" -Method GET
    Write-Host "✓ Server is running: $response" -ForegroundColor Green
} catch {
    Write-Host "✗ Server is not running" -ForegroundColor Red
    exit 1
}

# Test 2: Test webhook endpoint
Write-Host "`n2. Testing webhook endpoint..." -ForegroundColor Yellow
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

Write-Host "`nTesting completed!" -ForegroundColor Green 