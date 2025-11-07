---
description: Quick reference for common PhiGEN security fixes
allowed-tools: [Read]
---

# Quick Fix Reference

Quick reference for implementing common security fixes.

Show code examples for:

## 1. Environment Variables
```python
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if not TOKEN:
    raise ValueError("Token not set!")
```

## 2. Command Whitelisting
```python
import shlex
ALLOWED = {'ls', 'git', 'python'}
parts = shlex.split(cmd)
if parts[0] not in ALLOWED:
    return False
subprocess.run(parts, shell=False)
```

## 3. Path Validation
```python
from pathlib import Path
ALLOWED_DIRS = [Path("/app/data").resolve()]
resolved = Path(user_path).resolve()
# Check if within allowed dirs
```

## 4. Encryption Fix
```python
import base64
key = kdf.derive(password.encode())
key_b64 = base64.urlsafe_b64encode(key)
self.cipher = Fernet(key_b64)  # Use derived key!
```

Display these patterns now for reference.
