# Feature #6: Git Integration

**Status:** TBI (To Be Implemented)
**Priority:** High
**Complexity:** Medium
**Estimated Time:** 2 days

---

## Overview

Git operations directly from Discord. Check status, review commits, generate commit messages, review diffs.

**Commands:**
```
!git status                          # Show repo status
!git diff                            # Show uncommitted changes
!git commits 5                       # Last 5 commits
!git branches                        # List branches
!git review <commit-hash>            # AI review of commit
!git suggest-message                 # Generate commit message from diff
!git blame <file> <line>             # Show who changed line
!git log <file>                      # File history
!git compare <branch1> <branch2>     # Compare branches
!git stash list                      # Show stashed changes
```

---

## Architecture

```
Discord Command
        ↓
GitPython (local repo access)
        ↓
Git Operations
        ↓
AI Analysis (commit review, message generation)
        ↓
Formatted Response to Discord
```

---

## Tech Stack

- `GitPython` - Git operations
- `diff-match-patch` - Diff analysis
- AI models for code review
- Syntax highlighting for diffs

---

## Usage Examples

### Check Status

```
User: !git status
Bot: 📊 **Repo Status: PhiGEN**

     Branch: main
     Behind origin: 0 commits
     Ahead: 2 commits

     Modified: 3 files
     - src/encryption.py
     - tests/test_vault.py
     - README.md

     Untracked: 1 file
     - temp_debug.log

     Ready to commit
```

### View Diff

```
User: !git diff
Bot: 📝 **Changes in working directory:**

     **src/encryption.py** (+15, -8)
     ```diff
     - cipher = Fernet(Fernet.generate_key())
     + key_b64 = base64.urlsafe_b64encode(derived_key)
     + cipher = Fernet(key_b64)
     ```

     **tests/test_vault.py** (+25, -0)
     ```python
     + def test_encryption_persistence():
     +     # Test encryption survives restart
     +     ...
     ```

     Total: +40 insertions, -8 deletions
```

### Commit History

```
User: !git commits 5
Bot: 📜 **Recent Commits:**

     1. `abc123f` - Fix critical encryption bug (2 hours ago)
        Author: STRYK
        Files: src/encryption.py

     2. `def456a` - Add security tests (1 day ago)
        Author: JC
        Files: tests/test_security.py

     3. `789bcd` - Update documentation (2 days ago)
        Author: STRYK
        Files: README.md, docs/

     4. `012efg` - Refactor vault class (3 days ago)
        Author: JC

     5. `345hij` - Initial Discord bot (4 days ago)
        Author: STRYK
```

### AI Commit Review

```
User: !git review abc123f
Bot: 🔍 **Commit Review: abc123f**

     **Summary:** Fixes critical bug where random key was used instead of derived key

     **Analysis:**
     ✅ Good: Fixes CRITICAL security vulnerability
     ✅ Good: Adds base64 encoding for Fernet compatibility
     ✅ Good: Includes persistence test
     ⚠️  Note: Consider adding error handling for key derivation
     ⚠️  Note: Update documentation about key storage

     **Code Quality:** 8/10
     **Security Impact:** CRITICAL FIX
     **Test Coverage:** Good (added test)

     **Recommendation:** APPROVE with minor documentation updates
```

### Generate Commit Message

```
User: !git suggest-message
Bot: 💬 **Suggested Commit Message:**

     ```
     fix(encryption): use derived key instead of random key

     - Replace Fernet.generate_key() with base64-encoded derived key
     - Add test_encryption_persistence() to verify fix
     - Resolves critical bug where passwords unrecoverable after restart

     BREAKING: Existing encrypted data must be re-encrypted
     Fixes: #45
     ```

     Use this? (react ✅ to copy)
```

### Blame

```
User: !git blame src/encryption.py 125
Bot: 👤 **Line 125 in src/encryption.py:**

     ```python
     cipher = Fernet(Fernet.generate_key())  # ❌ Bug here
     ```

     **Author:** STRYK
     **Date:** 2025-11-01
     **Commit:** 789bcd - Initial encryption implementation
     **Message:** Add encryption module

     This line was changed in commit abc123f (2 hours ago) to fix bug
```

### Branch Comparison

```
User: !git compare main feature-oauth
Bot: 🔀 **Branch Comparison: main...feature-oauth**

     Commits ahead: 8
     Commits behind: 2

     **New commits in feature-oauth:**
     - abc123 - Add OAuth2 provider support
     - def456 - Implement token refresh
     - 789abc - Add OAuth tests
     ...

     **Files changed:** 12
     **Insertions:** +450
     **Deletions:** -120

     **Merge conflicts:** None detected
     ✅ Safe to merge
```

---

## Implementation Components

**Files Created:**
- `git_integration.py` - GitPython wrapper (500 lines)
- `diff_analyzer.py` - Diff parsing and formatting
- `commit_reviewer.py` - AI code review
- `message_generator.py` - AI commit message generation
- Bot integration (~250 lines)

**Key Classes:**
- `GitManager` - Repository operations
- `DiffAnalyzer` - Parse and format diffs
- `CommitReviewer` - AI-powered code review
- `MessageGenerator` - Generate commit messages

---

## Advanced Features

### Smart Commit Analysis

- Detects bug fixes vs features
- Identifies security changes
- Checks for breaking changes
- Suggests semantic versioning impact

### File History

```
User: !git log src/encryption.py
Bot: 📜 **History: src/encryption.py**

     1. abc123f (2h ago) - Fix critical encryption bug
     2. 789bcd (5 days ago) - Initial encryption implementation
     3. def456 (1 week ago) - Add file structure

     Total commits: 3
     Last modified: 2 hours ago
     Authors: STRYK (3)
```

### Stash Management

```
User: !git stash list
Bot: 💾 **Stashed Changes:**

     stash@{0}: WIP on main (2 hours ago)
        - Experimental feature attempt
        - 5 files changed

     stash@{1}: WIP on feature-oauth (1 day ago)
        - OAuth token storage
        - 3 files changed

User: !git stash show 0
Bot: 📦 **Stash 0 Contents:**
     [Shows diff of stashed changes]
```

### Commit Message Templates

```
User: !git templates
Bot: **Commit Message Templates:**

     1. **fix** - Bug fix
     2. **feat** - New feature
     3. **refactor** - Code restructure
     4. **docs** - Documentation
     5. **test** - Tests
     6. **chore** - Maintenance

User: !git suggest-message --template fix
Bot: Generated using 'fix' template:
     fix(module): brief description
     ...
```

---

## Security Considerations

- Read-only operations by default
- Configurable repo paths (whitelist)
- No push/force operations
- No branch deletion
- Requires repo owner authorization for writes
- Git credentials not exposed
- Sanitize file paths (prevent directory traversal)

---

## Configuration

**Per-channel repo setup:**
```
User: !git config set-repo E:/PythonProjects/PhiGEN
Bot: ✅ Repository set for this channel
     Repo: PhiGEN
     Branch: main
     Path: E:/PythonProjects/PhiGEN

User: !git config show
Bot: **Git Configuration:**
     Repository: PhiGEN
     Path: E:/PythonProjects/PhiGEN
     Default branch: main
     Auto-review: enabled
```

---

## Resource Usage

- Minimal: Git operations are fast
- Diff analysis: <1s for typical changes
- AI review: 2-5s depending on commit size
- No continuous polling (on-demand only)
- Memory: ~50MB for repo cache

**Performance:**
- Status check: 0.1-0.3s
- Diff generation: 0.2-0.5s
- Commit history: 0.1-0.2s
- AI review: 2-5s (depends on model)

---

## Limitations

1. **Local repos only** - Can't access remote-only repos
2. **Single repo** - One repo per channel (configurable)
3. **No write operations** - Read-only by default (safety)
4. **Large diffs** - Discord message limit may truncate
5. **Submodules** - Limited submodule support
6. **Binary files** - Can't diff non-text files

---

## Future Enhancements

- GitHub/GitLab API integration (PR creation, reviews)
- Automatic PR creation from Discord
- CI/CD status in commit view
- Branch protection warnings
- Merge conflict resolution help
- Interactive rebase guidance
- Webhook notifications for pushes
- Multi-repo support
- Write operations (with confirmation)
- Git flow automation

---

## Dependencies

```
GitPython>=3.1.0
diff-match-patch>=20200713
```

---

## Use Cases

1. **Quick Status Checks** - Check repo state without terminal
2. **Code Review** - Review commits before merging
3. **Commit Message Help** - AI-generated messages
4. **Blame Investigation** - Find who changed what
5. **Branch Comparison** - Check merge safety
6. **Team Coordination** - Shared visibility into repo state
7. **Documentation** - Understand file evolution

---

## Pros & Cons

### Pros
- Quick git checks without switching windows
- AI-powered commit reviews
- Automatic commit message generation
- Team visibility into repo status
- No need for terminal access
- Syntax-highlighted diffs
- Blame tracking

### Cons
- Read-only by default (safety)
- Single repo per channel
- Can't handle very large diffs (Discord limit)
- Local repos only (no remote-only)
- No interactive Git operations

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**Implementation Complexity:** Medium (GitPython + AI integration)
**ROI:** High (frequently used Git operations)
