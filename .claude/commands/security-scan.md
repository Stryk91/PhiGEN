---
description: Run comprehensive security scan on PhiGEN project
allowed-tools: [Bash, Read, Grep]
argument-hint: "[quick|full]"
---

# Security Scan Command

Run security analysis on the PhiGEN project.

**Mode:** ${1:-full}

## Tasks:

1. **Secret Detection**
   - Check for hardcoded credentials
   - Scan git history for exposed secrets
   - Validate .env configuration

2. **Code Analysis**
   - Look for command injection (shell=True)
   - Check for path traversal vulnerabilities
   - Find dangerous functions (eval, exec)
   - Verify encryption implementation

3. **Dependency Check**
   - Scan for vulnerable packages
   - Check for outdated dependencies

4. **Report**
   - Summarize findings
   - Prioritize by severity
   - Provide fix recommendations

Start the security scan now.
