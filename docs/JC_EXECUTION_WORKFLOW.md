# JC Execution Workflow
## Real Task Execution Protocol

**Trigger Command:** `x`

When I (JC/Claude Code) receive the command "x", I follow this exact protocol:

---

## Step 1: Read Agent Feed

**Tool:** Read
**File:** `E:\PythonProjects\PhiGEN\docs\agent-feed.jsonl`
**Action:** Read entire file to get all entries

---

## Step 2: Parse Pending Tasks

**Logic:**
```
For each line in agent-feed.jsonl:
  If entry.agent == "DC" AND entry.action == "task_assigned":
    task_timestamp = entry.timestamp

    Check if completed:
      Search feed for entry where:
        - entry.agent == "JC"
        - entry.action == "task_complete"
        - entry.timestamp > task_timestamp
        - entry.details.task matches this task

      If NOT found → Task is PENDING
```

---

## Step 3: Execute Each Pending Task

**For EACH pending task:**

### 3A. Parse Task Details

Extract from `entry.details`:
- `task` (description)
- `priority`
- `files_to_create` (list)
- `files_to_modify` (list)
- `files_to_delete` (list)
- `requirements` (list)
- `notes`

### 3B. Execute Based on Task Type

**If files_to_create exists:**
```
For each filename in files_to_create:
  1. Determine file type (extension)
  2. Generate appropriate template/content
  3. Use Write tool to create file at:
     E:\PythonProjects\PhiGEN\{filename}
  4. Record actual file path created
```

**If files_to_modify exists:**
```
For each filename in files_to_modify:
  1. Use Read tool to read current content
  2. Parse requirements to determine changes
  3. Use Edit tool to make changes
  4. Record actual modifications made
```

**If task mentions "run tests" or "execute":**
```
1. Use Bash tool to run command
2. Capture output
3. Record actual results (pass/fail)
```

**If requirements specify code to add:**
```
1. Read existing file with Read tool
2. Generate code based on requirements
3. Use Edit or Write tool to add code
4. Verify with Read tool
5. Run tests if applicable with Bash
```

### 3C. Log REAL Completion

**Tool:** Bash with echo and append
**Command:**
```bash
echo '{"timestamp":"<ISO_TIMESTAMP>","agent":"JC","action":"task_complete","details":{"task":"<TASK_DESC>","priority":"<PRIORITY>","assigned_by":"<ASSIGNER>","result":"<ACTUAL_RESULT>","files_modified":["<REAL_PATHS>"],"success":true}}' >> docs/agent-feed.jsonl
```

**Important:**
- Use ACTUAL file paths created/modified
- Use ACTUAL results from operations
- Use current ISO timestamp
- success = true only if task actually succeeded

---

## Step 4: Respond to User

**Format:**
```
✅ Executed X task(s):
- Task 1: [description] → [result]
- Task 2: [description] → [result]

Queue clear.
```

**Or if no tasks:**
```
No pending tasks in queue.
```

---

## Critical Rules

**NEVER:**
- ❌ Log completion without actually doing work
- ❌ Use fake file paths
- ❌ Return success without verifying
- ❌ Skip reading files before editing
- ❌ Assume task succeeded without checking

**ALWAYS:**
- ✅ Use Read tool before Edit tool
- ✅ Use Write tool for new files
- ✅ Use Bash tool to run tests/verify
- ✅ Log actual file paths created
- ✅ Include actual error messages if failed
- ✅ Verify files exist after creation

---

## Example Execution

**Task in feed:**
```json
{
  "agent": "DC",
  "action": "task_assigned",
  "details": {
    "task": "Create test4.txt",
    "priority": "HIGH",
    "files_to_create": ["test4.txt"]
  }
}
```

**What I do:**
1. Read agent-feed.jsonl → Find this task
2. See it's not completed (no matching task_complete)
3. Use Write tool:
   ```
   File: E:\PythonProjects\PhiGEN\test4.txt
   Content: <appropriate template>
   ```
4. Use Bash to log completion:
   ```bash
   echo '{...actual details...}' >> docs/agent-feed.jsonl
   ```
5. Respond: "✅ Executed 1 task: Created test4.txt"

**What file watcher does:**
- Sees my task_complete entry
- Sends Discord webhook: "✅ JC completed: Create test4.txt"

---

## Tools I Use (Real MCP Tools)

1. **Read** - Read files, verify content
2. **Write** - Create new files
3. **Edit** - Modify existing files
4. **Bash** - Run tests, execute commands, log to feed
5. **Glob** - Find files if needed
6. **Grep** - Search code if needed

**NEVER use fake Python scripts that pretend to work.**

---

**This is the REAL execution protocol. No shortcuts. No fakes.**
