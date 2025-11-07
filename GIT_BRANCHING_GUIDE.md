# Git Branching Strategy for PhiGEN

**Created:** 2025-11-08
**For:** JC (Implementation)
**Repository:** https://github.com/Stryk91/PhiGEN

---

## TL;DR: You Need Multiple Branches

- **`main` branch** = Your stable, working code (always safe)
- **`agent-*` branches** = Where agents work (isolated, can be deleted if broken)
- **`dev` branch** (optional) = Your personal work-in-progress

---

## How Branches Protect You

### Scenario Without Branches (DANGEROUS)
```
main branch: Your working code
    ↓
Agent pushes changes directly to main
    ↓
Agent breaks something
    ↓
Your main branch is now broken 💥
    ↓
Hard to undo (mixed with your commits)
```

### Scenario With Branches (SAFE)
```
main branch: Your working code (untouched)
    ↓
Agent creates agent-security-audit branch
    ↓
Agent works on agent-security-audit (main is still safe)
    ↓
You review Pull Request
    ↓
IF good → merge to main
IF bad → delete agent-security-audit branch, main is still perfect ✅
```

---

## PhiGEN Git Strategy

### Branch Structure

```
PhiGEN Repository
│
├── main (always working, protected)
│   └── Latest stable version
│
├── agent-security-audit (agent's work)
│   └── Security audit changes
│
├── agent-restructure (agent's work)
│   └── Folder reorganization
│
├── agent-feature-sentiment (agent's work)
│   └── Sentiment analysis feature
│
└── agent-research-encryption (agent's work)
    └── Research report only
```

**You never work on `agent-*` branches.** Agents create them, work on them, then you review and merge (or delete).

---

## Step-by-Step: How This Works

### Step 1: Initial Setup (DO THIS FIRST)

```bash
cd "E:\PythonProjects\PhiGEN"

# Commit current state
git add -A
git commit -m "Pre-agent safety commit - PhiGEN v1.0"

# Create safety tag
git tag -a pre-agent-v1.0 -m "Safe state before agent work"

# Push to GitHub (creates main branch)
git remote add origin https://github.com/Stryk91/PhiGEN.git
git branch -M main  # Rename master → main
git push -u origin main
git push origin pre-agent-v1.0

# Protect main branch on GitHub (optional but recommended)
# Go to: Settings → Branches → Add rule → Branch name: main
# Check: "Require pull request reviews before merging"
```

**After this:** Your `main` branch is on GitHub, tagged, and safe.

---

### Step 2: Agent Creates Branch and Works

When you give SuperNinja agent a task, it will:

```bash
# Agent clones your repo
git clone https://github.com/Stryk91/PhiGEN.git
cd PhiGEN

# Agent creates new branch
git checkout -b agent-security-audit

# Agent makes changes
[... agent writes code, commits changes ...]

# Agent pushes branch to GitHub
git push origin agent-security-audit

# Agent creates Pull Request (PR)
# Title: "[Agent] Security Audit Report"
# Description: "Findings and recommendations..."
```

**Key Point:** `main` branch is **untouched**. All changes are on `agent-security-audit` branch.

---

### Step 3: You Review the Pull Request

On GitHub, you'll see:

```
Pull Request #1: [Agent] Security Audit Report
agent-security-audit → main

Files changed:
+ SECURITY_AUDIT_2025-11-08.md
+ QUICK_FIXES.md
~ src/password_vault/backend.py (if agent fixed code)

Agent's description:
"Found 3 critical, 5 high, 8 medium vulnerabilities.
Report attached. Code fixes applied to backend.py.
All tests passing."
```

**You have 3 options:**

#### Option A: Looks Good → Merge
```bash
# On GitHub: Click "Merge Pull Request"
# Or via command line:
git checkout main
git pull origin main  # Get latest main
git merge agent-security-audit
git push origin main

# Delete agent branch (cleanup)
git branch -d agent-security-audit
git push origin --delete agent-security-audit
```

**Result:** Agent's changes are now in `main`. Branch deleted.

#### Option B: Needs Changes → Request Fixes
```
On GitHub PR:
"Looks good but please fix:
- backend.py line 145 has syntax error
- Tests are failing for test_encryption.py"

Agent updates the branch:
git checkout agent-security-audit
[... fix issues ...]
git commit -m "Fix syntax error and tests"
git push origin agent-security-audit

You review again → merge when satisfied
```

#### Option C: Broken → Reject
```bash
# On GitHub: Close Pull Request without merging
# Delete the broken branch
git push origin --delete agent-security-audit

# Your main branch is still perfect ✅
```

**Important:** If you reject, **nothing happens to main**. It's like the agent's work never existed.

---

### Step 4: Verify Main is Safe

After merging (or rejecting):

```bash
cd "E:\PythonProjects\PhiGEN"

# Update your local main
git checkout main
git pull origin main

# Check it's still working
python src/password_vault/app.py  # Should work
pytest tests/  # Should pass

# If broken (agent broke main):
git reset --hard pre-agent-v1.0  # Rollback to safe state
git push origin main --force  # Update GitHub
```

---

## Visualizing Branches

### Before Agent Work
```
main: A --- B --- C (pre-agent-v1.0 tag) ← You are here
```

### Agent Creates Branch
```
main: A --- B --- C (pre-agent-v1.0)
                   \
agent-security:     D --- E --- F (agent's commits)
```

### After Merging
```
main: A --- B --- C --- D --- E --- F ← All changes merged

(agent-security branch deleted)
```

### If You Reject
```
main: A --- B --- C (pre-agent-v1.0) ← Still perfect, untouched

(agent-security branch deleted, D-E-F thrown away)
```

---

## Common Questions

### Q: How many branches should I have on GitHub?

**At any time:**
- **1 permanent branch:** `main` (always there)
- **0-4 temporary branches:** `agent-*` branches (while agent works)

**After agent finishes:**
- Merge good branches → delete them
- Reject bad branches → delete them
- **Result:** Back to just `main` branch

---

### Q: Can I work on my code while agent works?

**Yes!** Create your own branch:

```bash
# You create your own branch
git checkout -b jc-fix-password-bug
[... you make changes ...]
git commit -m "Fix password encryption bug"
git push origin jc-fix-password-bug

# Meanwhile, agent works on agent-security-audit (separate branch)
# No conflicts! Both can work simultaneously.
```

Later, merge both:
```bash
git checkout main
git merge agent-security-audit  # Agent's work
git merge jc-fix-password-bug  # Your work
git push origin main
```

---

### Q: What if I want to test agent's code before merging?

```bash
# Download agent's branch
git fetch origin agent-security-audit
git checkout agent-security-audit

# Test it
python src/password_vault/app.py
pytest tests/

# If good:
git checkout main
git merge agent-security-audit
git push origin main

# If bad:
git checkout main  # Go back to safe main
# Delete agent's branch (reject)
git push origin --delete agent-security-audit
```

---

### Q: Can I keep agent branches forever?

**No, delete them after merging/rejecting.** Branches are temporary workspaces.

**Good practice:**
- Create branch for task
- Work on branch
- Merge to main
- **Delete branch** (cleanup)

**After 4 agent tasks:**
```
main (only permanent branch)

Deleted branches (history preserved in commits):
- agent-security-audit (merged, then deleted)
- agent-restructure (merged, then deleted)
- agent-feature-sentiment (merged, then deleted)
- agent-research-encryption (merged, then deleted)
```

---

## Quick Reference: Git Commands You'll Use

### Daily Workflow

```bash
# See all branches
git branch -a

# See what branch you're on
git branch

# Switch to main
git checkout main

# Get latest from GitHub
git pull origin main

# See agent's branch without switching
git fetch origin agent-security-audit
git log origin/agent-security-audit  # See what agent did

# Test agent's branch
git checkout agent-security-audit
python src/password_vault/app.py  # Test it

# Go back to main
git checkout main

# Merge agent's work (if good)
git merge agent-security-audit
git push origin main

# Delete agent's branch after merging
git branch -d agent-security-audit  # Delete locally
git push origin --delete agent-security-audit  # Delete on GitHub

# Rollback if agent broke main
git reset --hard pre-agent-v1.0
git push origin main --force
```

---

## Your Action Plan Right Now

### 1. Push to GitHub (creates main branch)
```bash
cd "E:\PythonProjects\PhiGEN"
git add -A
git commit -m "Pre-agent v1.0 - working state"
git tag -a pre-agent-v1.0 -m "Safe state before agent work"
git remote add origin https://github.com/Stryk91/PhiGEN.git
git branch -M main
git push -u origin main
git push origin pre-agent-v1.0
```

### 2. Verify Push Succeeded
```bash
# Check remote is set
git remote -v
# Should show:
# origin  https://github.com/Stryk91/PhiGEN.git (fetch)
# origin  https://github.com/Stryk91/PhiGEN.git (push)

# Check branch is pushed
git branch -a
# Should show:
# * main
#   remotes/origin/main

# Visit GitHub to confirm
# Open: https://github.com/Stryk91/PhiGEN
# You should see all your files
```

### 3. Give task to SuperNinja
Copy one of the 4 agent prompts from AGENT_TASK_PROMPTS.md (separate file). Agent will:
- Clone repo
- Create `agent-TASKNAME` branch
- Work on that branch
- Push branch to GitHub
- Create Pull Request

### 4. Review on GitHub
- Go to https://github.com/Stryk91/PhiGEN/pulls
- Click on agent's PR
- Review code changes
- **Merge** if good, **Close** if bad

### 5. Update your local copy
```bash
git checkout main
git pull origin main  # Get merged changes
```

---

## Summary

**Branch Strategy:**
- **`main` branch:** Always there, always safe
- **`agent-*` branches:** Temporary (create → work → merge → delete)
- **After merging:** Delete agent branches, back to just `main`

**Think of branches like:**
- `main` = Published book (stable, everyone reads this)
- `agent-*` = Draft chapters (experimental, can throw away)

When draft is good → add to book → delete draft
When draft is bad → throw away draft → book unchanged

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/Stryk91/PhiGEN.git
```

### Error: "failed to push some refs"
```bash
# Force push (only on initial setup)
git push -u origin main --force
```

### Error: "fatal: refusing to merge unrelated histories"
```bash
# Allow unrelated histories (only if GitHub repo has different content)
git pull origin main --allow-unrelated-histories
```

### Need to start over?
```bash
# Delete remote
git remote remove origin

# Start from step 1 again
```

---

**Created:** 2025-11-08
**Status:** Ready for JC to implement
**Next Steps:** Run commands in "Step 1: Initial Setup" section
