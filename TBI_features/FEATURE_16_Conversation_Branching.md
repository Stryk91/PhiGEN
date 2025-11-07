# Feature #16: Conversation Branching

**Status:** TBI (To Be Implemented)
**Priority:** Low-Medium
**Complexity:** Medium-High
**Estimated Time:** 2.5 days

---

## Overview

Fork conversations to explore alternatives, create "what if" scenarios, compare different approaches without losing original thread.

**Commands:**
```
!branch create <name>                # Fork current conversation
!branch list                         # List all branches
!branch switch <name>                # Switch to branch
!branch merge <source> <target>      # Merge branches
!branch diff <branch1> <branch2>     # Compare branches
!branch delete <name>                # Delete branch
!branch save <name>                  # Save branch point
!branch visualize                    # Show branch tree
```

---

## Architecture

```
Main Conversation Thread
        ↓
Branch Point (snapshot state)
        ↓
Fork A          Fork B
        ↓              ↓
Independent    Independent
Messages       Messages
        ↓
Optional Merge Back
```

---

## Tech Stack

- Tree data structure for branches
- JSONL for conversation storage
- State snapshots
- Diff algorithms

---

## Usage Examples

### Create Branch

```
[Current conversation about OAuth implementation]
User: Let me try a different approach
User: !branch create "alternative-oauth"

Bot: 🌿 **Branch Created: alternative-oauth**

     Forked from: main (message #12)
     Current branch: alternative-oauth

     You can now explore this approach independently.
     Switch back: !branch switch main
```

### Continue on Branch

```
[Now on "alternative-oauth" branch]
User: !ai What if we use JWT instead of OAuth2?
Bot: [Responds with JWT approach]

User: !ai Show me JWT implementation
Bot: [Shows JWT code]

[Main branch remains unchanged]
```

### Switch Branches

```
User: !branch switch main
Bot: 🔀 **Switched to: main**

     Last message: "Show me OAuth2 token refresh"
     Messages since fork: 0

     Available branches:
     - alternative-oauth (2 messages ahead)

[Continue on main branch]
User: !ai Continue with OAuth2
Bot: [Continues original OAuth2 discussion]
```

### List Branches

```
User: !branch list
Bot: 🌳 **Conversation Branches**

     **main** (current) ⭐
     ├─ 14 messages
     └─ Last: 2 min ago

     **alternative-oauth**
     ├─ Forked from: main #12
     ├─ 4 messages
     └─ Last: 5 min ago

     **experimental-setup**
     ├─ Forked from: main #8
     ├─ 2 messages
     └─ Last: 1 hour ago

     Switch: !branch switch <name>
```

### Compare Branches

```
User: !branch diff main alternative-oauth
Bot: 📊 **Branch Comparison**

     **Diverged at:** Message #12 (15 min ago)

     **main (3 messages since fork):**
     #13: User: "Show me OAuth2 token refresh"
     #14: Bot: [OAuth2 implementation]
     #15: User: "How to handle token expiry?"

     **alternative-oauth (4 messages since fork):**
     #13: User: "What if we use JWT instead?"
     #14: Bot: [JWT explanation]
     #15: User: "Show me JWT implementation"
     #16: Bot: [JWT code]

     **Key Differences:**
     - main: OAuth2 approach
     - alternative-oauth: JWT approach
```

### Visualize Branch Tree

```
User: !branch visualize
Bot: 🌳 **Conversation Tree**

     main (14 msgs)
     ├─── #8 ──┬── experimental-setup (2 msgs)
     │         └── [merged back]
     │
     └─── #12 ──┬── alternative-oauth (4 msgs) ⚡ Active
                └── jwt-only (1 msg)

     Legend:
     ⭐ Current branch
     ⚡ Recently active
     [merged] Merged back to parent
```

### Merge Branches

```
User: !branch merge alternative-oauth main
Bot: 🔀 **Merging: alternative-oauth → main**

     Analyzing differences...

     **Changes to merge:**
     - 4 new messages from alternative-oauth
     - 3 messages in main after fork point

     **Conflict Strategy:**
     Keep both threads? (react ✅)
     Or choose one? (react A=main, B=alt)

[User reacts ✅]
Bot: ✅ **Merge Complete**

     main now contains:
     - Original OAuth2 discussion
     - Alternative JWT approach
     - Both paths preserved

     **Summary:**
     We explored two authentication methods:
     1. OAuth2 (original)
     2. JWT (alternative)

     Choose implementation: !ai Compare OAuth2 vs JWT for our use case
```

### Save Branch Point

```
User: !branch save "before-refactor"
Bot: 💾 **Saved Branch Point: before-refactor**

     Current state saved at message #18
     Can fork from here later: !branch create <name> --from before-refactor

     Use case: Safe experimentation
```

### Delete Branch

```
User: !branch delete experimental-setup
Bot: ⚠️ **Delete Branch: experimental-setup?**

     This will permanently delete:
     - 2 messages
     - All history in this branch

     Confirm: react ✅

[User reacts ✅]
Bot: 🗑️ **Branch Deleted: experimental-setup**
```

---

## Implementation Components

**Files Created:**
- `conversation_brancher.py` - Branch management (500 lines)
- `branch_storage.py` - Persist branches to disk
- `branch_merger.py` - Merge logic
- `branch_visualizer.py` - Tree visualization
- Bot integration (~250 lines)

**Key Classes:**
- `ConversationBrancher` - Create, switch, delete branches
- `BranchStorage` - Save/load branch states
- `BranchMerger` - Merge strategies
- `BranchVisualizer` - ASCII tree generation

---

## Advanced Features

### Automatic Branching

```
User: !branch auto-fork on
Bot: 🤖 **Auto-Fork Enabled**

     Will auto-create branches when:
     - You say "let me try X"
     - You say "what if..."
     - Major topic shift detected

[Later]
User: Let me try a different database approach
Bot: 🌿 **Auto-forked to: database-alt-1**
     Detected: Topic shift
     Continue on new branch
```

### Branch Annotations

```
User: !branch annotate "This approach uses JWT for simplicity"
Bot: 📝 **Annotation Added**
     Branch: alternative-oauth
     Note: "This approach uses JWT for simplicity"

User: !branch list
Bot: 🌳 **Branches**

     alternative-oauth
     📝 "This approach uses JWT for simplicity"
     4 messages, last 5m ago
```

### Conditional Merging

```
User: !branch merge alternative-oauth main --if-better
Bot: 🤖 **Evaluating Branches...**

     Comparing:
     - main: OAuth2 (complex, secure)
     - alternative-oauth: JWT (simple, flexible)

     Metrics:
     - Simplicity: JWT wins
     - Security: OAuth2 wins
     - Maintenance: JWT wins

     **Recommendation:** Merge JWT approach
     It's better for your use case (internal API)

     Merge? (react ✅)
```

### Branch Snapshots

```
User: !branch snapshot
Bot: 📸 **Snapshot Created**

     Branch: main
     Message: #18
     State saved

     All branches backed up to:
     snapshots/2025-11-08_17-45.json

     Restore later: !branch restore 2025-11-08_17-45
```

### Parallel Exploration

```
User: !branch create option-a
User: !ai Implement with Redis
Bot: [Redis implementation on option-a]

User: !branch create option-b --from main
User: !ai Implement with PostgreSQL
Bot: [PostgreSQL implementation on option-b]

User: !branch compare option-a option-b --evaluate
Bot: 📊 **Evaluation**

     **option-a (Redis):**
     + Fast
     + Simple
     - No persistence
     - Memory intensive

     **option-b (PostgreSQL):**
     + Durable
     + Relational
     - Slower
     - More complex

     Recommendation: PostgreSQL for production
     Use Redis for caching layer
```

### Branch Templates

```
User: !branch create-template "comparison"
Bot: 📋 **Template Created: comparison**

     Auto-creates 3 branches:
     - approach-a
     - approach-b
     - approach-c

     Use: !branch apply-template comparison

User: !branch apply-template comparison
Bot: 🌿 **Created 3 branches from template**
     - approach-a (current)
     - approach-b
     - approach-c

     Explore each independently, then:
     !branch compare-all
```

---

## Database Schema

```sql
CREATE TABLE conversation_branches (
    id TEXT PRIMARY KEY,
    name TEXT,
    parent_branch TEXT,
    forked_at_message INTEGER,
    created_at TIMESTAMP,
    user_id TEXT,
    annotation TEXT
);

CREATE TABLE branch_messages (
    id INTEGER PRIMARY KEY,
    branch_id TEXT,
    message_index INTEGER,
    author TEXT,
    content TEXT,
    timestamp TIMESTAMP
);

CREATE TABLE branch_snapshots (
    id TEXT PRIMARY KEY,
    name TEXT,
    branches_state TEXT,  -- JSON
    created_at TIMESTAMP
);
```

---

## Use Cases

1. **Experimentation** - Try different approaches without losing progress
2. **Comparison** - Compare multiple solutions side-by-side
3. **Safe Exploration** - Test risky ideas on branches
4. **What-If Scenarios** - Explore alternative decisions
5. **Parallel Problem Solving** - Work on multiple solutions simultaneously
6. **Documentation** - Keep record of all approaches considered
7. **Teaching** - Show why one approach was chosen over another

---

## Pros & Cons

### Pros
- Explore alternatives without losing main thread
- Compare approaches side-by-side
- Safe experimentation
- Can merge best ideas back
- Visual branch tree
- Preserve all decision paths
- Roll back to any point

### Cons
- Complex to manage many branches
- Can become overwhelming with too many forks
- Memory overhead (multiple conversation states)
- Potential confusion about which branch is active
- Merge conflicts require manual resolution
- Storage grows with branches

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**ROI:** Medium (powerful for exploration, may be overkill for simple chats)
