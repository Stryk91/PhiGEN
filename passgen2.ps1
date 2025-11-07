# ============================================================================
# STRONG PASSWORD GENERATOR WITH JSON STORAGE AND DPAPI ENCRYPTION
# ============================================================================

# Define the storage path for the JSON file
$storagePath = "C:\Users\Stryker\Desktop\Unnamed\passwords.json"
$storageDirectory = Split-Path -Path $storagePath -Parent

# ============================================================================
# INITIALIZATION FUNCTIONS
# ============================================================================

# Function to ensure the storage directory exists
function Initialize-StorageDirectory
{
    if (-not (Test-Path -Path $storageDirectory))
    {
        New-Item -ItemType Directory -Path $storageDirectory -Force | Out-Null
        Write-Host "Created storage directory at: $storageDirectory" -ForegroundColor Green
    }
}

# Function to initialize the JSON storage file if it doesn't exist
function Initialize-PasswordVault
{
    if (-not (Test-Path -Path $storagePath))
    {
        $emptyVault = @{ }
        $emptyVault | ConvertTo-Json | Set-Content -Path $storagePath
        Write-Host "Created new password vault at: $storagePath" -ForegroundColor Green
    }
}

# ============================================================================
# PASSWORD ENCRYPTION/DECRYPTION FUNCTIONS
# ============================================================================

# Function to encrypt a password using DPAPI
function Encrypt-PasswordDPAPI
{
    param (
        [string]$plainPassword
    )

    try
    {
        $passwordBytes = [System.Text.Encoding]::UTF8.GetBytes($plainPassword)
        $encryptedBytes = [System.Security.Cryptography.ProtectedData]::Protect(
                $passwordBytes,
                $null,
                [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        )
        $encryptedBase64 = [Convert]::ToBase64String($encryptedBytes)
        return $encryptedBase64
    }
    catch
    {
        Write-Host "Error encrypting password: $_" -ForegroundColor Red
        return $null
    }
}

# Function to decrypt a password using DPAPI
function Decrypt-PasswordDPAPI
{
    param (
        [string]$encryptedBase64
    )

    try
    {
        $encryptedBytes = [Convert]::FromBase64String($encryptedBase64)
        $decryptedBytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
                $encryptedBytes,
                $null,
                [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        )
        $plainPassword = [System.Text.Encoding]::UTF8.GetString($decryptedBytes)
        return $plainPassword
    }
    catch
    {
        Write-Host "Error decrypting password: $_" -ForegroundColor Red
        return $null
    }
}

# ============================================================================
# PASSWORD GENERATION FUNCTION
# ============================================================================

# Function to generate a strong, random password
function Generate-StrongPassword
{
    param (
        [int]$length = 16
    )

    $upperCase = 65..90 | ForEach-Object { [char]$_ }
    $lowerCase = 97..122 | ForEach-Object { [char]$_ }
    $numbers = 48..57 | ForEach-Object { [char]$_ }
    $specialChars = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"

    $allChars = $upperCase + $lowerCase + $numbers + $specialChars.ToCharArray()
    $password = -join ((1..$length) | ForEach-Object { $allChars | Get-Random })
    return $password
}

# ============================================================================
# JSON VAULT MANAGEMENT FUNCTIONS
# ============================================================================

# Function to load the password vault from the JSON file
function Load-PasswordVault
{
    try
    {
        $vaultContent = Get-Content -Path $storagePath -Raw | ConvertFrom-Json
        $vault = @{ }
        foreach ($property in $vaultContent.PSObject.Properties)
        {
            $vault[$property.Name] = $property.Value
        }
        return $vault
    }
    catch
    {
        Write-Host "Error loading password vault: $_" -ForegroundColor Red
        return $null
    }
}

# Function to save the password vault back to the JSON file
function Save-PasswordVault
{
    param (
        [hashtable]$vault
    )

    try
    {
        $vault | ConvertTo-Json | Set-Content -Path $storagePath
        return $true
    }
    catch
    {
        Write-Host "Error saving password vault: $_" -ForegroundColor Red
        return $false
    }
}

# Function to save a password to the vault
function Save-PasswordToVault
{
    param (
        [string]$association,
        [string]$password
    )

    $vault = Load-PasswordVault

    if ($null -eq $vault)
    {
        return $false
    }

    if ( $vault.ContainsKey($association))
    {
        Write-Host "An entry for '$association' already exists. Use a different name or delete it first." -ForegroundColor Yellow
        return $false
    }

    $encryptedPassword = Encrypt-PasswordDPAPI -plainPassword $password

    if ($null -eq $encryptedPassword)
    {
        return $false
    }

    $vault[$association] = $encryptedPassword

    if (Save-PasswordVault -vault $vault)
    {
        Write-Host "Password for '$association' saved successfully!" -ForegroundColor Green
        return $true
    }
    else
    {
        return $false
    }
}

# Function to retrieve a password from the vault
function Get-PasswordFromVault
{
    param (
        [string]$association
    )

    $vault = Load-PasswordVault

    if ($null -eq $vault)
    {
        return $null
    }

    if ( $vault.ContainsKey($association))
    {
        $encryptedPassword = $vault[$association]
        $decryptedPassword = Decrypt-PasswordDPAPI -encryptedBase64 $encryptedPassword
        return $decryptedPassword
    }
    else
    {
        Write-Host "No password found for association: '$association'" -ForegroundColor Yellow
        return $null
    }
}

# Function to list all password associations
function List-PasswordAssociations
{
    $vault = Load-PasswordVault

    if ($null -eq $vault)
    {
        return
    }

    if ($vault.Count -gt 0)
    {
        Write-Host "`nStored Password Associations:" -ForegroundColor Cyan
        Write-Host "==============================" -ForegroundColor Cyan
        $vault.Keys | Sort-Object | ForEach-Object {
            Write-Host "  • $_" -ForegroundColor White
        }
        Write-Host "==============================" -ForegroundColor Cyan
        Write-Host "Total stored: $( $vault.Count )" -ForegroundColor Cyan
    }
    else
    {
        Write-Host "No passwords stored yet." -ForegroundColor Yellow
    }
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

Initialize-StorageDirectory
Initialize-PasswordVault

$strongPassword = Generate-StrongPassword -length 22
Write-Host "`nGenerated Strong Password: " -ForegroundColor Cyan -NoNewline
Write-Host "$strongPassword" -ForegroundColor Yellow

$association = Read-Host "`nWhat is this password associated with? (e.g., Gmail, GitHub, MyApp)"

if ( [string]::IsNullOrWhiteSpace($association))
{
    Write-Host "Association cannot be empty. Password not saved." -ForegroundColor Red
}
else
{
    Save-PasswordToVault -association $association -password $strongPassword
}

List-PasswordAssociations

Write-Host "`nPassword generation and storage complete!" -ForegroundColor Green