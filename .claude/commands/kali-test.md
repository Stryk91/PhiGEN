---
description: Run Kali Linux security tests on PhiGEN
allowed-tools: [Bash]
argument-hint: "[secrets|static|crypto|all]"
---

# Kali Security Testing

Execute security tests using Kali Linux tools.

**Test Type:** ${1:-all}

Run the Kali security test suite:

```bash
wsl -d kali-linux bash /mnt/e/PythonProjects/PhiGEN/kali_security_tests.sh $ARGUMENTS
```

After tests complete:
1. Summarize findings
2. Highlight CRITICAL and HIGH issues
3. Show report file locations
4. Provide fix recommendations
