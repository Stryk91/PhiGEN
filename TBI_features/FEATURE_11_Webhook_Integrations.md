# Feature #11: Webhook Integrations

**Status:** TBI (To Be Implemented)
**Priority:** Medium
**Complexity:** Medium
**Estimated Time:** 2 days

---

## Overview

Centralize all dev notifications in Discord. Receive GitHub events, Docker builds, CI/CD pipelines, custom webhooks.

**Commands:**
```
!hook github on                      # Enable GitHub webhooks
!hook docker on                      # Docker build notifications
!hook ci on                          # CI/CD pipeline updates
!hook custom <url>                   # Add custom webhook
!hook list                           # List all webhooks
!hook delete <id>                    # Remove webhook
!hook test <id>                      # Send test payload
!hook format <id> <template>         # Customize message format
```

---

## Architecture

```
External Service (GitHub/Docker/CI)
        ↓
Webhook Endpoint (FastAPI)
        ↓
Event Parser
        ↓
Message Formatter
        ↓
Discord Channel Notification
```

---

## Tech Stack

- `FastAPI` - Webhook endpoints
- `uvicorn` - ASGI server
- `PyGithub` - GitHub API
- `docker-py` - Docker events
- ngrok/cloudflare tunnel - Expose local endpoint

---

## Usage Examples

### GitHub Integration

```
User: !hook github on
Bot: 🔗 **GitHub Webhook Setup**

     Webhook URL: https://phigen.ngrok.io/webhook/github
     Secret: gh_abc123xyz...

     Add this to your repo settings:
     Settings → Webhooks → Add webhook

     Events to subscribe:
     ✓ Push events
     ✓ Pull requests
     ✓ Issues
     ✓ Releases
     ✓ Workflow runs

[Push event occurs]
Bot: 🚀 **Push to main**
     Repo: PhiGEN
     Author: @STRYK
     Commits: 3

     Latest: "Fix encryption bug"
     Files: src/encryption.py (+15, -8)

     View: https://github.com/user/PhiGEN/commit/abc123

[PR opened]
Bot: 📋 **New Pull Request #45**
     Title: Add OAuth support
     Author: @JC
     Status: Open
     Files: 8 changed (+450, -120)

     Review: !review-queue add #45

[CI/CD workflow completes]
Bot: ✅ **Workflow "Tests" completed**
     Status: Success
     Duration: 3m 24s
     Branch: feature-oauth

     All checks passed ✓
```

### Docker Build Notifications

```
User: !hook docker on
Bot: 🐳 **Docker Monitoring Active**
     Watching: All containers
     Events: build, start, stop, error

[Build starts]
Bot: 🔨 **Building: phigen-bot**
     Image: phigen-bot:latest
     Context: .

[Build completes]
Bot: ✅ **Build Complete: phigen-bot**
     Duration: 2m 15s
     Size: 450MB
     Layers: 12

     Ready to deploy

[Container crashes]
Bot: 🚨 **Container Stopped: phigen-bot**
     Exit code: 137 (OOM)
     Uptime: 2h 15m

     Last logs:
     MemoryError: Out of memory
```

### CI/CD Integration

```
User: !hook ci on
Bot: 🔧 **CI/CD Webhook Ready**

     Supported platforms:
     - Jenkins
     - GitLab CI
     - CircleCI
     - GitHub Actions

     Webhook: https://phigen.ngrok.io/webhook/ci

[Pipeline starts]
Bot: ⚙️ **Pipeline Started**
     Project: PhiGEN
     Branch: main
     Stage: Build

     Triggered by: @STRYK

[Stage completes]
Bot: ✅ **Stage "Build" passed**
     Duration: 1m 45s
     Next: Test

[Pipeline fails]
Bot: ❌ **Pipeline Failed**
     Stage: Test
     Job: unit-tests
     Error: 3 tests failed

     View logs: !ci-logs 1234
```

### Custom Webhooks

```
User: !hook custom https://api.monitoring.com/events
Bot: 🔗 **Custom Webhook Added**
     ID: hook_001
     URL: https://api.monitoring.com/events
     Format: JSON

     Send test: !hook test hook_001

User: !hook format hook_001 "🔔 {{event}}: {{message}}"
Bot: ✅ **Message Template Updated**
     Will use custom format for hook_001

[Event received]
Bot: 🔔 Server Alert: CPU usage at 95%
```

---

## Implementation Components

**Files Created:**
- `webhook_server.py` - FastAPI webhook endpoints (400 lines)
- `event_parsers.py` - Parse payloads from different services
- `message_formatters.py` - Format Discord messages
- `webhook_manager.py` - Manage webhook subscriptions
- Bot integration (~150 lines)

**Key Classes:**
- `WebhookServer` - FastAPI app with endpoints
- `GitHubParser` - Parse GitHub webhook payloads
- `DockerParser` - Parse Docker events
- `MessageFormatter` - Template-based message formatting
- `WebhookManager` - Subscription management

---

## Advanced Features

### Smart Filtering

```
User: !hook github on --events push,pr,release
Bot: 🔗 GitHub webhook active
     Events: Push, PR, Release only

User: !hook github filter branch=main
Bot: ✅ Filter added: Only main branch events
```

### Message Templates

```
User: !hook format github-push "
📤 **{{author}}** pushed to **{{branch}}**
Commits: {{commit_count}}
Latest: {{latest_commit_message}}
"
Bot: ✅ Template saved for GitHub push events
```

### Aggregation

```
User: !hook github aggregate 5m
Bot: 📊 Events will be aggregated every 5 minutes

[After 5 minutes]
Bot: 📊 **GitHub Activity (last 5m)**
     Pushes: 3 (main, feature-oauth, dev)
     PRs: 1 opened, 2 updated
     Issues: 2 closed
```

### Conditional Alerts

```
User: !hook github alert-if "pr.status == 'approved' and pr.reviews >= 2"
Bot: 🔔 Alert rule added
     Condition: PR approved with 2+ reviews

[Condition met]
Bot: ⚡ **PR #45 Ready to Merge**
     Approvals: 2/2 ✓
     Checks: All passed ✓

     Merge: !git merge #45
```

---

## Database Schema

```sql
CREATE TABLE webhooks (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    channel_id TEXT,
    service TEXT,  -- github, docker, ci, custom
    url TEXT,
    secret TEXT,
    events TEXT,  -- JSON array
    filters TEXT,  -- JSON object
    template TEXT,
    enabled BOOLEAN,
    created_at TIMESTAMP
);

CREATE TABLE webhook_events (
    id INTEGER PRIMARY KEY,
    webhook_id TEXT,
    event_type TEXT,
    payload TEXT,  -- JSON
    received_at TIMESTAMP,
    processed BOOLEAN
);
```

---

## Supported Services

| Service | Events | Setup |
|---------|--------|-------|
| **GitHub** | Push, PR, Issues, Releases, Workflows | Add webhook in repo settings |
| **Docker** | Build, Start, Stop, Error | Enable Docker socket access |
| **GitLab** | Push, MR, Pipeline | Add webhook in project settings |
| **Jenkins** | Build, Deploy | Install webhook plugin |
| **CircleCI** | Workflow | Add webhook in project settings |
| **Custom** | Any JSON payload | POST to custom endpoint |

---

## Dependencies

```
fastapi>=0.104.0
uvicorn>=0.24.0
PyGithub>=2.1.0
docker>=6.1.0
pyngrok>=6.0.0  # For local testing
```

---

## Use Cases

1. **Development** - Get notified of code pushes instantly
2. **Code Review** - PR notifications for quick reviews
3. **CI/CD Monitoring** - Track build/deploy status
4. **Container Management** - Docker events in Discord
5. **Release Tracking** - Know when new versions ship
6. **Team Coordination** - Centralized notifications for entire team
7. **Custom Integrations** - Connect any service that supports webhooks

---

## Pros & Cons

### Pros
- Centralized notifications in Discord
- Real-time updates from multiple services
- No polling (event-driven)
- Customizable message formats
- Supports filtering and aggregation
- Easy setup for common services

### Cons
- Requires public endpoint (ngrok or hosting)
- Security: Webhook secrets must be managed
- Discord rate limits on high-volume events
- Requires service-specific configuration
- Network dependency

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**ROI:** High (centralizes all dev notifications)
