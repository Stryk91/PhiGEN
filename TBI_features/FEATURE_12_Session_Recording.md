# Feature #12: Session Recording

**Status:** TBI (To Be Implemented)
**Priority:** Medium-Low
**Complexity:** Low-Medium
**Estimated Time:** 1.5 days

---

## Overview

Record full conversation sessions to JSONL files. Replay conversations, export transcripts, analyze patterns, resume sessions.

**Commands:**
```
!record start <name>                 # Start recording session
!record stop                         # Stop current recording
!record pause                        # Pause recording
!record resume                       # Resume recording
!record save <filename>              # Save to custom file
!record list                         # List saved sessions
!record load <name>                  # Load/replay session
!record export <name> <format>       # Export as txt/md/json
!record stats <name>                 # Session statistics
```

---

## Architecture

```
Discord Message
        ↓
Session Manager (track active sessions)
        ↓
Message Logger (JSONL format)
        ↓
File Writer (append to session file)
        ↓
Export/Replay System
```

---

## Tech Stack

- JSONL for message storage
- Python's `json` module
- `datetime` for timestamps
- Markdown/text formatters for export

---

## Usage Examples

### Start Recording

```
User: !record start "oauth-implementation"
Bot: 🔴 **Recording Started**

     Session: oauth-implementation
     File: sessions/oauth-implementation_2025-11-08.jsonl
     Time: 3:45 PM

     All messages will be recorded
     Stop: !record stop
```

### During Session

```
User: !ai How do I implement OAuth2?
Bot: [Normal response about OAuth2]

[Message automatically logged to JSONL]

User: !ai Show me the code for token refresh
Bot: [Code example]

[Also logged]
```

### Stop Recording

```
User: !record stop
Bot: ⏹️ **Recording Stopped**

     Session: oauth-implementation
     Duration: 1h 23m
     Messages: 45
     Size: 234KB

     Saved: sessions/oauth-implementation_2025-11-08.jsonl
     Load: !record load oauth-implementation
```

### List Sessions

```
User: !record list
Bot: 📚 **Saved Sessions**

     1. oauth-implementation (1h 23m, 45 msgs) - Today
     2. encryption-fix (2h 10m, 67 msgs) - Yesterday
     3. docker-setup (45m, 23 msgs) - 3 days ago
     4. code-review (1h 5m, 38 msgs) - 1 week ago

     Total: 4 sessions, 173 messages
     Load: !record load <name>
```

### Load/Replay Session

```
User: !record load oauth-implementation
Bot: 📖 **Loading Session: oauth-implementation**

     Date: 2025-11-08 3:45 PM
     Duration: 1h 23m
     Messages: 45

     **First 5 messages:**

     [3:45 PM] STRYK: !ai How do I implement OAuth2?
     [3:46 PM] Bot: OAuth2 is an authorization framework...

     [3:48 PM] STRYK: !ai Show me the code for token refresh
     [3:49 PM] Bot: Here's a token refresh implementation...

     [3:52 PM] STRYK: !run python [code]
     [3:52 PM] Bot: Output: Token refreshed successfully

     View full: !record export oauth-implementation md
```

### Export Formats

#### Text Export
```
User: !record export oauth-implementation txt
Bot: 📄 **Exporting to TXT...**

     [Attaches: oauth-implementation.txt]

     Contents:
     =====================================
     Session: oauth-implementation
     Date: 2025-11-08 3:45 PM
     Duration: 1h 23m
     Messages: 45
     =====================================

     [3:45 PM] STRYK: !ai How do I implement OAuth2?
     [3:46 PM] Bot: OAuth2 is an authorization framework...
     ...
```

#### Markdown Export
```
User: !record export oauth-implementation md
Bot: 📄 **Exporting to Markdown...**

     [Attaches: oauth-implementation.md]

     # Session: oauth-implementation
     **Date:** 2025-11-08 3:45 PM
     **Duration:** 1h 23m
     **Messages:** 45

     ---

     ## Conversation

     ### 3:45 PM - STRYK
     !ai How do I implement OAuth2?

     ### 3:46 PM - Bot
     OAuth2 is an authorization framework...
     ...
```

#### JSON Export
```
User: !record export oauth-implementation json
Bot: 📄 **Exporting to JSON...**

     [Attaches: oauth-implementation.json]

     {
       "session": "oauth-implementation",
       "date": "2025-11-08T15:45:00",
       "duration_seconds": 4980,
       "messages": [
         {
           "timestamp": "2025-11-08T15:45:00",
           "author": "STRYK",
           "content": "!ai How do I implement OAuth2?",
           "type": "user_message"
         },
         {
           "timestamp": "2025-11-08T15:46:00",
           "author": "Bot",
           "content": "OAuth2 is...",
           "type": "bot_response"
         }
       ]
     }
```

### Session Statistics

```
User: !record stats oauth-implementation
Bot: 📊 **Session Stats: oauth-implementation**

     **Overview:**
     Duration: 1h 23m
     Messages: 45
     User: 23 messages
     Bot: 22 responses

     **Activity:**
     Commands used: 12
     - !ai: 8
     - !run: 3
     - !git: 1

     **Timeline:**
     Most active: 4:00-4:15 PM (15 messages)
     Longest gap: 12 minutes (4:20-4:32 PM)

     **Topics discussed:**
     - OAuth2 implementation
     - Token refresh
     - Error handling
     - Testing
```

---

## Implementation Components

**Files Created:**
- `session_recorder.py` - Recording logic (300 lines)
- `session_manager.py` - Manage active sessions
- `session_exporter.py` - Export to various formats
- `session_analyzer.py` - Generate statistics
- Bot integration (~150 lines)

**Key Classes:**
- `SessionRecorder` - Record messages to JSONL
- `SessionManager` - Track active sessions
- `SessionExporter` - Export to txt/md/json
- `SessionAnalyzer` - Statistics and insights

---

## JSONL Format

```jsonl
{"timestamp": "2025-11-08T15:45:00", "author": "STRYK", "author_id": "123", "content": "!ai How do I implement OAuth2?", "type": "user_message"}
{"timestamp": "2025-11-08T15:46:00", "author": "Bot", "author_id": "bot", "content": "OAuth2 is an authorization framework...", "type": "bot_response", "model": "claude-3-5-sonnet"}
{"timestamp": "2025-11-08T15:48:00", "author": "STRYK", "author_id": "123", "content": "!ai Show me the code", "type": "user_message"}
{"timestamp": "2025-11-08T15:49:00", "author": "Bot", "author_id": "bot", "content": "```python\n...", "type": "bot_response", "model": "claude-3-5-sonnet"}
```

**Metadata fields:**
- `timestamp` - ISO 8601 format
- `author` - Username
- `author_id` - Discord user ID
- `content` - Message text
- `type` - user_message, bot_response, system_message
- `model` - AI model used (if bot response)
- `attachments` - File URLs (if any)

---

## Advanced Features

### Auto-Recording

```
User: !record auto on
Bot: 🔴 Auto-recording enabled
     All conversations will be recorded automatically
     Sessions created per-day

[Next day]
Bot: 🔴 New session started: 2025-11-09
     File: sessions/auto_2025-11-09.jsonl
```

### Tagging

```
User: !record tag "found-solution"
Bot: 🏷️ Tag added: found-solution
     Timestamp: 4:15 PM
     Easy to find this moment later

User: !record tags oauth-implementation
Bot: 🏷️ **Tags in session:**
     - found-solution (4:15 PM)
     - need-to-revisit (4:32 PM)
     - bug-discovered (4:45 PM)

     Jump to: !record goto oauth-implementation found-solution
```

### Search Within Sessions

```
User: !record search oauth-implementation "token refresh"
Bot: 🔍 **Found 3 matches in oauth-implementation:**

     1. [3:48 PM] STRYK: "Show me token refresh code"
     2. [4:02 PM] Bot: "Here's the token refresh implementation"
     3. [4:15 PM] STRYK: "Token refresh works! ✓"
```

### Resume Session

```
User: !record resume oauth-implementation
Bot: 🔴 **Resumed Session: oauth-implementation**

     Original: 2025-11-08 3:45 PM
     Resumed: 2025-11-09 2:00 PM

     Messages before pause: 45
     All new messages will be appended
```

### Merge Sessions

```
User: !record merge oauth-part1 oauth-part2 --output oauth-complete
Bot: 🔗 **Merging Sessions...**

     oauth-part1: 45 messages
     oauth-part2: 23 messages

     ✅ Merged to: oauth-complete (68 messages)
     Chronologically sorted
```

---

## Database Schema

```sql
CREATE TABLE recording_sessions (
    id TEXT PRIMARY KEY,
    name TEXT,
    user_id TEXT,
    channel_id TEXT,
    started_at TIMESTAMP,
    stopped_at TIMESTAMP,
    message_count INTEGER,
    file_path TEXT,
    status TEXT  -- active, paused, stopped
);

CREATE TABLE session_tags (
    session_id TEXT,
    tag TEXT,
    timestamp TIMESTAMP,
    message_index INTEGER
);
```

---

## Use Cases

1. **Documentation** - Record problem-solving sessions for future reference
2. **Training** - Create conversation examples for onboarding
3. **Debugging** - Replay error investigation sessions
4. **Analysis** - Study conversation patterns and effectiveness
5. **Backup** - Keep permanent record of important discussions
6. **Compliance** - Audit trail for sensitive projects
7. **Learning** - Review how problems were solved

---

## Pros & Cons

### Pros
- Permanent record of conversations
- Easy to replay and reference
- Multiple export formats
- Searchable conversation history
- Tagging for important moments
- Session statistics
- Merge and resume capabilities

### Cons
- Disk space for long sessions
- Privacy concerns (must inform users)
- Large JSONL files can be slow to process
- No automatic transcription (text only)
- Requires manual start/stop (unless auto-mode)

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**ROI:** Medium (useful for documentation and review)
