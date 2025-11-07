# Feature #2: Code Execution Sandbox

**Status:** TBI (To Be Implemented)
**Priority:** High
**Complexity:** Medium
**Estimated Time:** 1-2 days

---

## Overview

Execute code snippets instantly in isolated Docker containers. Test code without leaving Discord.

**Commands:**
```
!run python <code>         # Execute Python code
!run javascript <code>     # Execute JavaScript
!run bash <code>           # Execute bash commands
!run rust <code>           # Execute Rust code
!run-test python <code>    # Run with unit tests
!run-timeout 60            # Set execution timeout
!languages                 # List supported languages
!run-project               # Execute multi-file project
```

---

## Implementation Details

### Tech Stack
- Docker SDK for Python - Container management
- `subprocess` - Process execution
- `asyncio` - Async execution
- Language-specific containers (python:3.11-alpine, node:18-alpine, etc.)

### Architecture
```
Discord Command (!run python <code>)
        ↓
Code Validator (syntax check, safety)
        ↓
Docker Container (isolated sandbox)
        ↓
Execute Code (timeout: 30s)
        ↓
Capture Output (stdout, stderr)
        ↓
Return Result to Discord
```

### Security Model
- Read-only filesystem
- No network access
- Memory limit (128MB)
- CPU limit (1 core, 50% usage)
- Execution timeout (30s default)
- No privileged operations
- Pattern blacklist (dangerous functions)
- Auto-cleanup after execution

---

## Supported Languages

| Language | Image | Default Timeout |
|----------|-------|-----------------|
| Python | python:3.11-alpine | 30s |
| JavaScript | node:18-alpine | 30s |
| Bash | alpine:latest | 30s |
| Rust | rust:1.70-alpine | 60s (compilation) |

---

## Core Components

**Files Created:**
- `sandbox_manager.py` - Docker container management (320 lines)
- `code_validator.py` - Safety checks
- `multi_file_sandbox.py` - Multi-file project execution
- Bot command integration (~150 lines)

**Key Classes:**
- `SandboxManager` - Container lifecycle, execution
- `CodeValidator` - Pattern detection, safety
- `LanguageConfig` - Per-language settings

---

## Usage Examples

### Example 1: Simple Python
```
User: !run python print("Hello World")
Bot: ⏳ Executing python code...
Bot: ```
     Hello World
     ```
     ⏱️ Executed in 0.23s
```

### Example 2: With Code Block
```
User: !run python
```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
print(factorial(5))
```
Bot: ```
     120
     ```
     ⏱️ Executed in 0.31s
```

### Example 3: Error Handling
```
User: !run python print(undefined_var)
Bot: ❌ **Error:**
     ```
     NameError: name 'undefined_var' is not defined
     ```
```

### Example 4: Timeout Protection
```
User: !run python
```python
import time
time.sleep(60)  # Exceeds 30s timeout
```
Bot: ❌ **Error:** Execution timeout (30s)
```

### Example 5: JavaScript
```
User: !run javascript console.log([1,2,3].map(x => x*2))
Bot: ```
     [ 2, 4, 6 ]
     ```
     ⏱️ Executed in 0.19s
```

### Example 6: With Tests
```
User: !run-test python
```python
def add(a, b):
    return a + b
```
Bot: 📝 Paste your test code (pytest format):
User:
```python
assert add(2, 3) == 5
assert add(-1, 1) == 0
```
Bot: ✅ **Tests passed!**
```

---

## Security Features

1. **Isolated containers** - Each execution in fresh container
2. **Network disabled** - No internet access
3. **Read-only filesystem** - Can't modify system
4. **Resource limits** - 128MB RAM, 50% CPU
5. **Timeout protection** - Max 30s (configurable)
6. **Pattern blacklist** - Block dangerous functions
   - Python: `eval()`, `exec()`, `__import__`
   - JavaScript: `eval()`, `Function()`, `child_process`
   - Bash: `rm -rf`, fork bombs
7. **Auto-cleanup** - Containers removed after execution
8. **Code length limit** - Max 5000 characters

---

## Resource Limits

| Resource | Limit | Reason |
|----------|-------|--------|
| Memory | 128MB | Prevent memory exhaustion |
| CPU | 50% of 1 core | Fair resource sharing |
| Timeout | 30s (configurable) | Prevent infinite loops |
| Output | 1900 chars | Discord message limit |
| Code Length | 5000 chars | Prevent abuse |

---

## Dependencies

**Python packages:**
```
docker>=6.1.0
```

**System requirements:**
- Docker installed and running
- Docker daemon accessible
- Images pulled: python:3.11-alpine, node:18-alpine, alpine:latest, rust:1.70-alpine

**Setup:**
```bash
# Ensure Docker is running
docker info

# Pull base images (handled automatically on bot startup)
docker pull python:3.11-alpine
docker pull node:18-alpine
docker pull alpine:latest
docker pull rust:1.70-alpine
```

---

## Limitations

1. **No persistent state** - Each run is isolated, no memory between executions
2. **No file system** - Can't save/read files (unless multi-file mode)
3. **No network** - Can't make API calls or download data
4. **Limited libraries** - Only stdlib available (unless custom images)
5. **Output size** - Discord message limit (2000 chars, truncated if exceeded)
6. **Compilation time** - Rust/C++ takes longer due to compilation

---

## Advanced Features

### Multi-File Execution
Run projects with multiple files:
```
User: !run-project
Bot: 📁 Paste files in format: filename.py```code```
User: main.py
```python
from utils import helper
print(helper())
```
User: utils.py
```python
def helper():
    return "Hello from helper!"
```
Bot: ✅ Executed project
     ```
     Hello from helper!
     ```
```

### Custom Timeout
```
User: !run-timeout 60
Bot: ✅ Timeout set to 60s

User: !run-timeout
Bot: ⏱️ Current timeout: 60s
```

### Language Support Check
```
User: !languages
Bot: **Supported languages:**
     - **python**
     - **javascript**
     - **bash**
     - **rust**
```

---

## Error Handling

**Scenario 1: Invalid Language**
```
User: !run cobol print("hello")
Bot: ❌ Unsupported language: cobol
     Use !languages to see supported languages
```

**Scenario 2: Dangerous Pattern**
```
User: !run python eval("malicious code")
Bot: ❌ Dangerous pattern detected: eval(
```

**Scenario 3: Resource Exhaustion**
```
User: !run python data = [0] * 10**9  # 1 billion items
Bot: ❌ **Error:** Container killed (out of memory)
```

**Scenario 4: Docker Not Running**
```
User: !run python print("test")
Bot: ❌ Docker daemon not accessible. Contact admin.
```

---

## Future Enhancements

1. **Package installation** - `!run python --install requests <code>`
2. **File uploads** - Execute uploaded .py files directly
3. **Interactive REPL** - Persistent Python session across messages
4. **Visualization** - matplotlib plots returned as images
5. **Performance metrics** - Memory/CPU usage stats in response
6. **Code linting** - Auto-lint before execution with suggestions
7. **More languages** - Go, C++, Ruby, PHP
8. **Custom images** - User-defined Docker images with dependencies
9. **Execution history** - `!run-history` to see past executions
10. **Share snippets** - `!run-save <name>` to save useful snippets

---

## Performance Metrics

**Expected Performance:**
- Container startup: ~0.5-1s
- Python execution: 0.2-0.5s (simple)
- JavaScript execution: 0.1-0.3s (simple)
- Rust compilation: 5-10s (first time)
- Total response time: 1-2s (Python/JS), 6-11s (Rust)

**Optimization:**
- Keep Docker images pulled and cached
- Use alpine-based images (smaller, faster)
- Parallel execution for multiple runs
- Container pooling (future enhancement)

---

## Pros & Cons

### Pros
- Instant code testing without leaving Discord
- Safe execution (isolated containers)
- Multi-language support
- No local setup required
- Team collaboration (shared testing)

### Cons
- Requires Docker daemon running
- Limited to stdlib (no external packages by default)
- Output size limited by Discord
- Can't interact with external services (no network)
- Compilation languages slower

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**Implementation Complexity:** Medium (Docker experience required)
