# Test registration
Write-Host "Testing user registration..." -ForegroundColor Green
$registerBody = @{
    email = "test@example.com"
    password = "password123"
    first_name = "John"
    last_name = "Doe"
    phone = "123-456-7890"
} | ConvertTo-Json

$registerResult = Invoke-RestMethod -Uri "http://localhost:8000/auth/register" `
    -Method Post `
    -Body $registerBody `
    -ContentType "application/json" `
    -ErrorVariable registerError

Write-Host "Registration Response:" -ForegroundColor Yellow
$registerResult | ConvertTo-Json

# Test login
Write-Host "`nTesting user login..." -ForegroundColor Green
$loginBody = "username=test@example.com&password=password123"

$loginResult = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
    -Method Post `
    -Body $loginBody `
    -ContentType "application/x-www-form-urlencoded" `
    -ErrorVariable loginError

Write-Host "Login Response:" -ForegroundColor Yellow
$loginResult | ConvertTo-Json 