# Feature #3: Project Context Injection

**Status:** TBI (To Be Implemented)
**Priority:** HIGHEST (Biggest impact on usefulness)
**Complexity:** High
**Estimated Time:** 3-4 days

---

## Overview

Load entire codebases into bot memory so it understands your actual project structure and can give relevant, context-aware answers.

**Commands:**
```
!project load phigen              # Load PhiGEN codebase
!project add-file src/main.py     # Add specific file
!project add-dir src/             # Add directory
!project show                     # Show loaded context
!project files                    # List all loaded files
!project clear                    # Clear context
!project search <query>           # Search loaded code
!project summary                  # AI summary of project
```

---

## Architecture

```
Load Project Command
        ↓
File Scanner (recursive, .gitignore aware)
        ↓
Code Parser (extract structure)
        ↓
Vector Embedding (semantic search)
        ↓
Context Storage (per-user, per-project)
        ↓
RAG Integration (retrieve relevant files for queries)
```

---

## Tech Stack

- `GitPython` - Parse repos, respect .gitignore
- `tree-sitter` - Parse code structure (AST)
- `sentence-transformers` - Embeddings for semantic search
- `chromadb` - Vector database for fast retrieval
- `tiktoken` - Token counting for context limits

---

## Key Features

### 1. Smart Loading
- Respects .gitignore patterns
- Excludes binaries, node_modules, venv
- Detects programming languages
- Extracts imports, classes, functions
- Creates dependency graph

### 2. Semantic Search
- Vector embeddings of code chunks
- Find relevant files by natural language query
- "Where is authentication handled?" → auth.py, middleware.py
- "Show me database models" → models/ directory

### 3. Context-Aware Responses
- Bot knows your project structure
- References actual file paths
- Suggests fixes based on existing code patterns
- Understands your naming conventions

### 4. Token Management
- Auto-select most relevant files (top 10)
- Stay within model context limits (8K, 32K, 128K)
- Priority: modified files > imported files > related files

---

## Implementation Components

**Files Created:**
- `project_context.py` - Context manager (450 lines)
- `code_parser.py` - AST parsing, structure extraction
- `vector_store.py` - ChromaDB integration
- `rag_retriever.py` - Retrieve relevant context
- Bot integration (~200 lines)

**Key Classes:**
- `ProjectContext` - Manage loaded projects
- `CodeParser` - Extract structure from files
- `VectorStore` - Embedding storage and retrieval
- `RAGRetriever` - Context selection for queries

---

## Usage Example

```
User: !project load phigen
Bot: 📂 Scanning E:/PythonProjects/PhiGEN...
     Found: 47 Python files, 12,450 lines
     Parsing structure...
     Creating embeddings...
     ✅ Loaded PhiGEN (5.2MB)

User: !ai how does the encryption work in this project?
Bot: (automatically retrieves src/encryption.py, src/vault.py)
     The encryption in PhiGEN uses Fernet (AES-256) with PBKDF2 key derivation.

     Key files:
     - src/encryption.py:45 - `derive_key()` function
     - src/vault.py:120 - `encrypt_password()` method

     Note: There's a critical bug on line 125 where a random key is used
     instead of the derived key. See SECURITY_ANALYSIS_REPORT.md

User: !project search discord bot
Bot: 🔍 Found 3 matches:
     - ai_tools/discord_multimodel_bot.py (850 lines) - Main bot
     - ai_tools/model_router.py - Model selection
     - start_dc_bridge.bat - Bridge startup

User: !project summary
Bot: **PhiGEN Project Summary:**

     Type: Password manager with multi-agent AI coordination
     Languages: Python (95%), Shell (5%)
     Structure:
     - src/ - Core vault logic
     - ai_tools/ - Discord bot, multi-model integration
     - tests/ - Security tests

     Key Features:
     - AES-256 encryption
     - Multi-model AI (4 local + Claude)
     - Discord remote control
     - Autonomous worker agents

     Active Issues: 2 CRITICAL security bugs (see docs/SECURITY_*)
```

---

## Context Limits

| Model | Context Window | Max Files |
|-------|----------------|-----------|
| Phi 3.5 | 4K tokens | ~5 files |
| Mistral 7B | 8K tokens | ~10 files |
| Claude Sonnet | 200K tokens | Full codebase |
| Granite Code | 8K tokens | ~10 files |

---

## Smart Retrieval

**Query:** "How do I add a new Discord command?"

**Retrieved Context:**
1. `discord_multimodel_bot.py` - Existing commands for reference
2. `model_router.py` - If command needs AI integration
3. `conversation_logger.py` - If command needs logging
4. Bot personality config - For response style

**AI Response uses actual project patterns**, not generic examples.

---

## Security Considerations

- Only load projects user owns/has access to
- Don't embed sensitive files (.env, keys, credentials)
- Warn if large codebase (>100MB)
- Token limits prevent context overflow
- Clear context after session timeout (30 min)
- Whitelist allowed directories (prevent loading system files)

---

## Resource Usage

### Small Project (PhiGEN ~50 files)
- Scan time: ~5s
- Embedding time: ~20s
- Storage: ~50MB (vectors)
- Memory: ~200MB

### Large Project (1000+ files)
- Scan time: ~60s
- Embedding time: ~5 min
- Storage: ~500MB
- Memory: ~2GB

---

## Workflow Integration

**Before Context Injection:**
```
User: How do I add authentication to my project?
Bot: (generic answer about authentication in general)
```

**After Context Injection:**
```
User: How do I add authentication to my project?
Bot: Looking at your PhiGEN codebase, you already have authentication
     in src/auth.py using password hashing with bcrypt.

     To add OAuth, you'd extend the Auth class on line 45.

     Example based on your existing pattern:
     [shows code matching PhiGEN's style]
```

---

## Limitations

1. **Large codebases** - Slow initial load (one-time cost)
2. **Binary files** - Can't understand compiled code
3. **Context window** - Small models can't fit full projects
4. **Stale context** - Doesn't auto-refresh on file changes (manual reload)
5. **Memory usage** - Embeddings consume RAM

---

## Future Enhancements

- Auto-reload on file change detection (watchdog)
- Multi-project context switching
- Cross-project search ("Find similar to PhiGEN's auth in PhiWave")
- Code graph visualization
- Dependency analysis ("What breaks if I change this?")
- Git integration (load specific branch/commit)
- Incremental updates (reload only changed files)
- Project templates ("Create new project like PhiGEN")

---

## Dependencies

```
GitPython>=3.1.0
tree-sitter>=0.20.0
tree-sitter-python>=0.20.0
tree-sitter-javascript>=0.20.0
sentence-transformers>=2.2.0
chromadb>=0.4.0
tiktoken>=0.5.0
watchdog>=3.0.0
```

---

## Pros & Cons

### Pros
- Massive improvement in answer quality
- Understands YOUR codebase specifically
- References actual file paths/line numbers
- No need to paste code repeatedly
- Maintains context across questions
- Learns project conventions and patterns

### Cons
- Slow initial load for large projects
- Memory intensive for embeddings
- Requires disk space for vector storage
- Can't handle extremely large repos (>10K files)
- Needs periodic reloading for updates

---

## Advanced Features

### Multi-User Context Isolation
Each user gets their own context storage, preventing cross-contamination.

### Project Switching
```
User: !project load phigen
Bot: ✅ Loaded PhiGEN

User: !project load phiwave
Bot: ✅ Loaded PhiWave (PhiGEN unloaded)

User: !project list
Bot: Available projects:
     - phigen (last loaded: 5 min ago)
     - phiwave (currently active)
```

### Dependency Tracking
```
User: !project deps src/main.py
Bot: **Dependencies for src/main.py:**
     Direct imports:
     - src/vault.py
     - src/encryption.py
     - ai_tools/model_router.py

     Indirect dependencies (8 files)

     If you modify main.py, test these files.
```

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**Implementation Complexity:** High (Requires embedding model, vector DB, AST parsing)
**ROI:** HIGHEST - Transforms bot from generic to project-specific expert
