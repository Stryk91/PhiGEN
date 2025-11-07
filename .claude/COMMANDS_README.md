# PhiGEN Custom Claude Code Commands

Custom slash commands for PhiGEN project development and security testing.

## Available Commands

### Security Commands

#### `/security-scan [quick|full]`
**Purpose:** Comprehensive security analysis of the codebase

**Usage:**
```
/security-scan          # Full scan (default)
/security-scan quick    # Quick scan
/security-scan full     # Explicit full scan
```

**What it does:**
- Secret detection (hardcoded credentials)
- Code analysis (command injection, path traversal)
- Dangerous function detection (eval, exec)
- Encryption implementation verification
- Dependency vulnerability check
- Prioritized report with fix recommendations

---

#### `/kali-test [secrets|static|crypto|all]`
**Purpose:** Run Kali Linux security tests

**Usage:**
```
/kali-test              # Run all tests
/kali-test secrets      # Only secret detection
/kali-test static       # Only static analysis
/kali-test crypto       # Only cryptographic tests
```

**What it does:**
- Executes `kali_security_tests.sh` in Kali Linux
- Runs TruffleHog, Gitleaks, Bandit, Semgrep
- Tests encryption implementation
- Generates JSON reports
- Highlights CRITICAL/HIGH issues

---

#### `/fix-crypto`
**Purpose:** Fix the CRITICAL encryption bug in password_vault_backend.py

**Usage:**
```
/fix-crypto
```

**What it does:**
1. Identifies the broken encryption code (lines 420-421)
2. Applies the correct fix (use derived key, not random)
3. Runs encryption persistence test
4. Verifies fix works

**The Bug:** Uses `Fernet.generate_key()` instead of derived key
**The Fix:** Uses `base64.urlsafe_b64encode(derived_key)`

---

### Testing Commands

#### `/test-encryption`
**Purpose:** Verify encryption persistence works correctly

**Usage:**
```
/test-encryption
```

**What it does:**
- Runs critical encryption persistence test
- Tests: create → save → close → reopen → decrypt
- Shows PASS/FAIL with detailed results
- If test doesn't exist, creates it from template

**Critical:** This test MUST pass before production!

---

#### `/deploy-checklist`
**Purpose:** Production deployment readiness check

**Usage:**
```
/deploy-checklist
```

**What it does:**
Checks all items on security checklist:
- ✓ Secrets management
- ✓ Encryption verification
- ✓ Input validation
- ✓ Testing completion
- ✓ Documentation
- ✓ Monitoring setup

Reports status of each item with pass/fail.

---

### Agent Commands

#### `/agent-status`
**Purpose:** Check multi-agent coordination system status

**Usage:**
```
/agent-status
```

**What it does:**
- Reads agent feed (last 10 entries)
- Checks autonomous worker status
- Verifies Discord bot status
- Shows pending tasks
- Reports health status

---

### Reference Commands

#### `/quick-fix`
**Purpose:** Display quick reference for common security fixes

**Usage:**
```
/quick-fix
```

**What it shows:**
1. Environment variable configuration
2. Command whitelisting pattern
3. Path validation pattern
4. Encryption fix code

Copy-paste ready code examples for immediate use.

---

## Creating Your Own Commands

### Location
Commands go in: `.claude/commands/`

### File Format
```markdown
---
description: What your command does
allowed-tools: [Bash, Read, Edit]
argument-hint: "[arg1|arg2]"
---

# Command Title

Your prompt instructions here.

Use $ARGUMENTS or $1, $2 for parameters.
```

### Example
Create `.claude/commands/test.md`:
```markdown
---
description: Run project tests
allowed-tools: [Bash]
---

Run all PhiGEN tests:

```bash
cd E:\PythonProjects\PhiGEN
pytest tests/ -v
```

Show results and highlight failures.
```

Then use: `/test`

---

## Command Features

### Arguments
- `$ARGUMENTS` - All arguments as string
- `$1`, `$2`, etc. - Individual arguments
- `${1:-default}` - Argument with default value

### File References
- `@filename.py` - Include file contents
- `@src/**/*.py` - Include multiple files

### Bash Execution
```markdown
```bash
your command here
```
```

**Important:** Must include `allowed-tools: [Bash]`

---

## Tips

### For Security Commands
- Always scan before committing
- Run `/security-scan` regularly
- Use `/kali-test` before releases
- Check `/deploy-checklist` before production

### For Development
- Use `/agent-status` to monitor coordination
- Run `/test-encryption` after crypto changes
- Keep `/quick-fix` handy for reference

### For Team Collaboration
- Share commands in `.claude/commands/`
- Document in this README
- Use descriptive names
- Include usage examples

---

## Advanced: Namespaced Commands

Organize in subdirectories:

```
.claude/commands/
├── security/
│   ├── scan.md          → /scan (project:security)
│   └── audit.md         → /audit (project:security)
├── deploy/
│   ├── staging.md       → /staging (project:deploy)
│   └── production.md    → /production (project:deploy)
└── test/
    └── integration.md   → /integration (project:test)
```

---

## Personal Commands

Create global commands in: `~/.claude/commands/`

These are available across ALL projects.

Example use cases:
- Git workflow helpers
- Code review templates
- Documentation generators
- Security audit routines

---

## Command Best Practices

1. **Clear Descriptions:** Help autocomplete work better
2. **Allowed Tools:** Only include tools you need
3. **Argument Hints:** Guide users on what to pass
4. **Error Handling:** Handle missing arguments gracefully
5. **Output Format:** Consistent, readable results

---

## Troubleshooting

### Command Not Found
- Check file is in `.claude/commands/`
- Verify filename has `.md` extension
- Restart Claude Code if needed

### Command Doesn't Execute
- Check `allowed-tools` includes necessary tools
- Verify Bash commands have correct syntax
- Check file paths are absolute when needed

### Arguments Not Working
- Use `$ARGUMENTS` for all args
- Use `$1`, `$2` for individual args
- Use `${1:-default}` for defaults

---

## Examples in Action

### Quick Security Check Before Commit
```
/security-scan quick
```

### Full Security Audit Before Release
```
/kali-test all
/deploy-checklist
```

### Fix and Verify Encryption
```
/fix-crypto
/test-encryption
```

### Monitor Agent System
```
/agent-status
```

---

## Contributing

To add new commands:

1. Create `.md` file in `.claude/commands/`
2. Follow format above
3. Test the command
4. Document it in this README
5. Commit to project repo

---

## Resources

- [Claude Code Slash Commands Docs](https://code.claude.com/docs/en/slash-commands)
- [PhiGEN Security Reports](./SECURITY_ANALYSIS_REPORT.md)
- [Remediation Examples](./REMEDIATION_CODE_EXAMPLES.md)
- [AI Coder Encyclopedia](../AI_CODER_ENCYCLOPEDIA.md)

---

**Last Updated:** 2025-11-06
**Commands:** 7 security & development shortcuts
**Location:** `.claude/commands/`
