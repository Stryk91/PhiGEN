# Communicate with JC via Discord 🎮→💻

## 🎯 Overview

You can now **assign tasks and send messages to JC** directly from Discord (even from your phone)!

The bot writes to the agent feed, and JC reads it just like any other task assignment.

---

## 📋 Commands

### 1. Assign Task with Priority

```
!assign_task <PRIORITY> <task description>
```

**Priorities:** LOW, MEDIUM, HIGH, CRITICAL

**Aliases:** `!assign`, `!task`

**Examples:**
```
!assign_task HIGH Fix the critical bug in password validation
!task MEDIUM Add unit tests for the new function
!assign LOW Update documentation for API endpoints
```

---

### 2. Quick Task (Default: MEDIUM Priority)

```
!quick_task <task description>
```

Faster way to assign tasks with default MEDIUM priority.

**Alias:** `!qt`

**Examples:**
```
!quick_task Add error handling to the upload function
!qt Refactor the validation logic for better readability
```

---

### 3. Send Message to JC

```
!message_jc <your message>
```

Send a note, question, or feedback to JC through the agent feed.

**Aliases:** `!msg_jc`, `!tell_jc`

**Examples:**
```
!message_jc Great work on Task 3! The tests look comprehensive.
!msg_jc Question: Should we add rate limiting to the API?
!tell_jc Ready for Task 4 when you are!
```

---

## 📊 What Gets Written to Agent Feed

### Task Assignment Entry:
```json
{
  "timestamp": "2025-11-06T18:45:00.000000+00:00",
  "agent": "DC",
  "action": "task_assigned",
  "details": {
    "task": "Fix the critical bug in password validation",
    "priority": "HIGH",
    "assigned_via": "Discord",
    "assigned_by": "Stryker#1234"
  }
}
```

### Message Entry:
```json
{
  "timestamp": "2025-11-06T18:45:00.000000+00:00",
  "agent": "DC",
  "action": "message_to_jc",
  "details": {
    "message": "Great work on Task 3!",
    "from": "Stryker#1234",
    "via": "Discord"
  }
}
```

---

## 🔄 Complete Workflow Example

**Scenario:** You're on your phone, want JC to work on something

### Step 1: Assign the Task
```
!assign_task HIGH Add password strength meter to UI
```

**Bot Response:**
```
✅ Task Assigned to JC!

Priority: HIGH
Task: Add password strength meter to UI
Timestamp: 2025-11-06T18:45:00.000000+00:00

📢 Tell JC to check the agent feed!
```

### Step 2: Check It Was Added
```
!feed 1
```

You'll see your task as the latest entry!

### Step 3: Tell JC (via another chat/message)
"Hey JC, check the agent feed - new task assigned!"

### Step 4: Monitor Progress
```
!check_jc
```

See when JC completes the task!

---

## 💡 Use Cases

### 1. Quick Task Assignment From Anywhere
```
# You're at lunch, think of something
!quick_task Add validation for email addresses
```

### 2. Follow-up After Task Completion
```
# JC just completed Task 3
!message_jc Excellent work! Can you also add edge case tests?
```

### 3. Urgent Bug Fix
```
# Critical issue found
!assign_task CRITICAL Fix null pointer exception in user login
```

### 4. Planning Next Sprint
```
!assign_task MEDIUM Implement user dashboard
!assign_task LOW Update README with new features
!message_jc These are lower priority, take your time!
```

---

## 🎮 Multi-Command Workflow

**Assign multiple tasks:**
```
!task HIGH Fix authentication bug
!task MEDIUM Add password reset feature  
!task LOW Update documentation
!message_jc Three tasks queued up - prioritize the HIGH one first!
```

**Check status:**
```
!feed 5
!check_jc
```

---

## 🔒 Security

- ✅ Only YOU (user ID: 821263652899782656) can assign tasks
- ✅ All tasks are logged with your Discord username
- ✅ Timestamps track when tasks were assigned
- ✅ Full audit trail in agent feed

---

## 📱 Phone → JC Workflow

**The complete flow:**
1. You (on phone) → Type command in Discord
2. Discord bot (on desktop) → Writes to agent-feed.jsonl
3. JC (in JetBrains) → Reads agent feed, sees new task
4. JC → Completes task, logs completion
5. You → Check status: `!check_jc`

**All from your phone!** 📱→🤖→💻→✅

---

## 🆚 Task Assignment vs Message

**Use `!assign_task` when:**
- You want JC to implement something
- It's actual work with deliverables
- Needs tracking and completion status

**Use `!message_jc` when:**
- Giving feedback or praise
- Asking questions
- Providing context or notes
- Not requiring a specific action

---

## ⚡ Quick Reference

```
# Assign tasks
!assign_task HIGH <task>      # Specific priority
!quick_task <task>            # Default MEDIUM
!qt <task>                    # Shortest form

# Communicate
!message_jc <message>         # Send message
!msg_jc <message>             # Shorter
!tell_jc <message>            # Alternative

# Check status
!check_jc                     # JC's latest
!feed <count>                 # Recent activity
```

---

## 🚀 Examples in Action

**Morning task planning:**
```
!qt Review and test Task 3 implementation
!message_jc Morning! Let's wrap up the password security series today.
```

**Mid-day check-in:**
```
!check_jc
# See what JC has been working on
```

**Afternoon assignment:**
```
!assign_task HIGH Start Task 4 - common password blacklist
!message_jc Task 4 details are in the feed, let me know if you have questions!
```

**Evening status:**
```
!feed 5
# Review what got done today
```

---

## 🎉 This Changes Everything!

**Before:**
- Had to be at desktop to assign tasks
- Manual editing of agent-feed.jsonl
- Multiple steps to communicate with JC

**Now:**
- Assign tasks from your phone 📱
- One Discord command ⚡
- Instant communication with JC 💬
- Full coordination while mobile 🚀

**You can now manage your entire development workflow from anywhere!**

---

## 📝 Pro Tips

1. **Be specific in task descriptions:**
   ```
   ✅ !task HIGH Add validation for minimum 8 characters in password field
   ❌ !task HIGH Fix password thing
   ```

2. **Use priority appropriately:**
   - HIGH: Bugs, blockers, critical features
   - MEDIUM: Regular features, improvements
   - LOW: Nice-to-haves, documentation

3. **Follow up with messages:**
   ```
   !assign_task HIGH Fix login bug
   !message_jc This is blocking production deployment, priority #1
   ```

4. **Check before assigning:**
   ```
   !check_jc
   # Make sure JC isn't already working on something
   !assign_task ...
   ```

---

**Your phone is now a powerful development command center!** 📱⚡💻
