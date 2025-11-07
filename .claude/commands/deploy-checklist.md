---
description: Run through production deployment security checklist
allowed-tools: [Read, Grep, Bash]
---

# Production Deployment Checklist

Verify PhiGEN is ready for production deployment.

## Security Checklist:

### 1. Secrets Management
- [ ] No hardcoded tokens (scan with grep)
- [ ] `.env` file exists and not in git
- [ ] `.env` in `.gitignore`
- [ ] Environment variables loaded in code

### 2. Encryption
- [ ] Encryption persistence test passes
- [ ] Cross-instance decryption works
- [ ] No unused key variables

### 3. Input Validation
- [ ] Command whitelisting implemented
- [ ] Path validation for file operations
- [ ] No `shell=True` with user input

### 4. Testing
- [ ] All unit tests pass
- [ ] Security scan clean (no CRITICAL/HIGH)
- [ ] Git hooks installed
- [ ] Multi-tool scan completed

### 5. Documentation
- [ ] Security docs created (3 levels)
- [ ] README updated
- [ ] Deployment guide ready

### 6. Monitoring
- [ ] Audit logging configured
- [ ] Error tracking set up
- [ ] Health checks ready

Run through checklist now and report status of each item.
