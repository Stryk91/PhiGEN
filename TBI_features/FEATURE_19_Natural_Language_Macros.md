# Feature #19: Natural Language Macros

**Status:** TBI (To Be Implemented)
**Priority:** Medium
**Complexity:** Medium
**Estimated Time:** 2 days

---

## Overview

Create custom commands using natural language. Define workflows, shortcuts, multi-step actions - no coding required.

**Commands:**
```
!macro create <name> "<description>"  # Create macro
!macro <name>                         # Execute macro
!macro list                           # List all macros
!macro edit <name>                    # Edit macro
!macro delete <name>                  # Delete macro
!macro share <name> @user             # Share with user
!macro export                         # Export all macros
!macro import <file>                  # Import macros
```

---

## Architecture

```
Natural Language Macro Definition
        ↓
AI Parser (convert to actions)
        ↓
Action Sequence Storage
        ↓
Execution Engine (run steps)
        ↓
Results to User
```

---

## Tech Stack

- NLP for macro parsing
- Action templating system
- Variable substitution
- YAML/JSON for macro storage

---

## Usage Examples

### Create Simple Macro

```
User: !macro create morning-standup "Check git status, show today's tasks, and summarize unread messages"

Bot: 🎯 **Macro Created: morning-standup**

     Parsed actions:
     1. Run: !git status
     2. Run: !todo list
     3. Run: !messages unread

     Test it: !macro morning-standup
```

### Execute Macro

```
User: !macro morning-standup

Bot: 🎯 **Running Macro: morning-standup**

     **Step 1: Git Status**
     📊 Repo Status: PhiGEN
     Branch: main
     Modified: 2 files
     Ready to commit

     **Step 2: Today's Tasks**
     📋 Tasks (3 pending):
     - Review PR #45
     - Fix encryption bug
     - Write tests

     **Step 3: Unread Messages**
     📬 Unread: 5 messages
     - @JC: "Can you review my code?"
     - @Dev1: "Build failed"
     ...

     ✅ **Macro Complete**
```

### Complex Macro with Parameters

```
User: !macro create deploy-project "Ask which environment, run tests, build docker image, deploy to that environment, and notify team"

Bot: 🎯 **Macro Created: deploy-project**

     Detected parameters:
     - {environment} - deployment target

     Parsed actions:
     1. Ask user: "Which environment? (dev/staging/prod)"
     2. Run: !test run
     3. If tests pass:
        - Run: !docker build
        - Run: !deploy {environment}
        - Send message: "Deployed to {environment}"
     4. Else:
        - Stop with error

     This is a conditional macro with user input

User: !macro deploy-project

Bot: 🎯 **Running Macro: deploy-project**

     **Step 1: User Input**
     Which environment? (dev/staging/prod)

User: staging

Bot: ✅ Environment: staging

     **Step 2: Running Tests**
     ⏳ Testing...
     ✅ All tests passed (48/48)

     **Step 3: Building Docker Image**
     🐳 Building phigen-bot:latest...
     ✅ Build complete (2m 15s)

     **Step 4: Deploying to staging**
     🚀 Deploying...
     ✅ Deployed successfully
     URL: https://staging.phigen.app

     **Step 5: Notifying Team**
     📢 Sent to #dev channel:
     "✅ Deployed to staging - @STRYK"

     ✅ **Macro Complete**
```

### Macro with Variables

```
User: !macro create quick-commit "Add all files, commit with message '{message}', and push"

Bot: 🎯 **Macro Created: quick-commit**

     Required parameters:
     - {message} - commit message

     Usage: !macro quick-commit message="fix bug"

User: !macro quick-commit message="Fix encryption bug"

Bot: 🎯 **Running Macro: quick-commit**

     **Step 1: Git Add**
     Added 3 files

     **Step 2: Git Commit**
     Committed with message: "Fix encryption bug"

     **Step 3: Git Push**
     Pushed to origin/main

     ✅ **Macro Complete**
```

### List Macros

```
User: !macro list

Bot: 📚 **Your Macros (8)**

     **Daily Workflows:**
     - morning-standup (3 steps)
     - end-of-day (5 steps)

     **Development:**
     - quick-commit (3 steps)
     - deploy-project (5 steps, conditional)
     - code-review-flow (4 steps)

     **Team:**
     - standup-summary (2 steps)
     - weekly-report (6 steps)

     **Shared (from others):**
     - bug-investigation (@JC) (7 steps)

     Run: !macro <name>
```

### Conditional Logic

```
User: !macro create smart-test "Run tests, if they fail run debug assistant on the failures, then run tests again"

Bot: 🎯 **Macro Created: smart-test**

     Parsed logic:
     1. Run: !test run
     2. If failed:
        - Run: !debug-trace <failure>
        - Apply suggested fixes
        - Retry: !test run
     3. Report final result

     This macro has retry logic

User: !macro smart-test

Bot: 🎯 **Running Macro: smart-test**

     **Step 1: Running Tests**
     ❌ Failed: 3/48 tests

     **Step 2: Debugging Failures**
     Analyzing failures...
     - test_encryption: KeyError
     - test_auth: AssertionError
     - test_api: ConnectionError

     **Suggested Fixes:**
     [Shows fixes for each]

     **Step 3: Retry Tests**
     ✅ All tests passed (48/48)

     ✅ **Macro Complete**
```

### Loops in Macros

```
User: !macro create check-all-prs "For each open PR, run code review and summarize results"

Bot: 🎯 **Macro Created: check-all-prs**

     Detected loop:
     For each PR in open PRs:
     - Run: !review-next
     - Collect results
     Summary at end

     This macro iterates over items

User: !macro check-all-prs

Bot: 🎯 **Running Macro: check-all-prs**

     Found 3 open PRs

     **PR #45: Add OAuth**
     🔍 Reviewing...
     ✅ APPROVE (good code, tests included)

     **PR #46: Fix bug**
     🔍 Reviewing...
     ⚠️ REQUEST CHANGES (missing tests)

     **PR #47: Update docs**
     🔍 Reviewing...
     ✅ APPROVE (documentation clear)

     **Summary:**
     Reviewed: 3 PRs
     Approved: 2
     Changes requested: 1

     ✅ **Macro Complete**
```

---

## Implementation Components

**Files Created:**
- `macro_parser.py` - NLP parsing of macro definitions (450 lines)
- `macro_executor.py` - Execute action sequences
- `macro_storage.py` - Save/load macros
- `action_templates.py` - Predefined action types
- Bot integration (~200 lines)

**Key Classes:**
- `MacroParser` - Parse natural language to actions
- `MacroExecutor` - Run macro steps
- `ActionTemplate` - Define action types
- `MacroStorage` - Persist macros

---

## Action Types

**Built-in actions:**
- `command` - Run bot command
- `ask` - Get user input
- `conditional` - If/else logic
- `loop` - Iterate over items
- `wait` - Delay execution
- `notify` - Send message
- `variable` - Store/retrieve values

**Example:**
```yaml
name: morning-standup
steps:
  - action: command
    command: "!git status"
  - action: command
    command: "!todo list"
  - action: command
    command: "!messages unread"
```

---

## Advanced Features

### Macro Chaining

```
User: !macro create full-workflow "Run morning-standup, then code-review-flow, then end-of-day"

Bot: 🎯 **Macro Created: full-workflow**

     Chains 3 existing macros:
     - morning-standup → code-review-flow → end-of-day
     Total: 12 steps across all macros
```

### Time-Based Triggers

```
User: !macro create daily-summary "..." --schedule 5pm
Bot: ⏰ **Scheduled Macro**

     Macro: daily-summary
     Runs: Every day at 5 PM
     Next run: Today 5:00 PM

[At 5 PM]
Bot: 🎯 **Auto-Running: daily-summary**
     [Executes macro steps]
```

### Error Handling

```
User: !macro create resilient-build "Build project, if it fails notify me and retry 3 times"

Bot: 🎯 **Macro Created: resilient-build**

     Error handling:
     - Max retries: 3
     - Notify on failure: Yes
     - Abort on repeated failure: Yes
```

### Macro Variables

```
User: !macro create context-aware "Save current branch to {branch}, switch to main, deploy, switch back to {branch}"

Bot: 🎯 **Macro with Context**

     Captures state:
     - {branch} = current branch

     Steps preserve context across actions
```

### Macro Templates

```
User: !macro template deployment
Bot: 📋 **Deployment Macro Template**

     ```
     name: deploy-{project}
     parameters:
       - environment (dev/staging/prod)
       - notify (yes/no)
     steps:
       - Run tests
       - Build Docker
       - Deploy to {environment}
       - If {notify}: Notify team
     ```

     Customize and save as new macro
```

### Team Macro Library

```
User: !macro library
Bot: 📚 **Team Macro Library**

     **Public Macros (12):**

     Most used:
     1. morning-standup (@STRYK) - 234 uses
     2. code-review-flow (@JC) - 189 uses
     3. bug-investigation (@STRYK) - 145 uses

     By category:
     - Development (5 macros)
     - Testing (3 macros)
     - Deployment (2 macros)
     - Reporting (2 macros)

     Clone: !macro clone <name> <new-name>
```

---

## Database Schema

```sql
CREATE TABLE macros (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE,
    author_id TEXT,
    description TEXT,
    actions TEXT,  -- JSON
    parameters TEXT,  -- JSON
    is_public BOOLEAN,
    created_at TIMESTAMP,
    usage_count INTEGER DEFAULT 0
);

CREATE TABLE macro_executions (
    id INTEGER PRIMARY KEY,
    macro_id TEXT,
    user_id TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status TEXT,  -- success, failed, cancelled
    output TEXT
);
```

---

## Example Macro Definitions

### Morning Routine
```yaml
name: morning-standup
description: "Daily standup routine"
steps:
  - action: command
    command: "!git status"
  - action: command
    command: "!todo list --today"
  - action: command
    command: "!messages unread"
```

### Deploy Pipeline
```yaml
name: deploy-to-prod
description: "Full deployment pipeline"
parameters:
  - name: version
    required: true
steps:
  - action: ask
    prompt: "Ready to deploy v{version} to production?"
    options: ["yes", "no"]
  - action: conditional
    if: "{response} == yes"
    then:
      - action: command
        command: "!test run"
      - action: conditional
        if: "{tests_passed}"
        then:
          - action: command
            command: "!docker build --tag v{version}"
          - action: command
            command: "!deploy prod --version v{version}"
          - action: notify
            message: "✅ Deployed v{version} to production"
        else:
          - action: notify
            message: "❌ Tests failed, deployment cancelled"
```

---

## Use Cases

1. **Daily Routines** - Automate repetitive workflows
2. **Deployment Pipelines** - Multi-step deployment with checks
3. **Code Review** - Standardized review process
4. **Bug Investigation** - Systematic debugging workflow
5. **Reporting** - Generate regular status reports
6. **Team Coordination** - Shared workflows for consistency
7. **Onboarding** - Pre-built macros for new team members

---

## Pros & Cons

### Pros
- No coding required (natural language)
- Automate repetitive workflows
- Share workflows with team
- Conditional logic and loops
- Parameters for flexibility
- Easy to create and modify
- Time-based scheduling

### Cons
- NLP parsing not always perfect
- Complex macros hard to debug
- Limited to predefined actions
- Can become complicated quickly
- Error handling tricky in macros

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**ROI:** High (automates repetitive tasks, saves time)
