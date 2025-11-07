# Feature #14: Snippet Library

**Status:** TBI (To Be Implemented)
**Priority:** Medium
**Complexity:** Low-Medium
**Estimated Time:** 1.5 days

---

## Overview

Save and retrieve code snippets, templates, commands. Tag and search snippets, share with team, quick insertion.

**Commands:**
```
!snip save <name> <code>             # Save snippet
!snip get <name>                     # Retrieve snippet
!snip list                           # List all snippets
!snip search <query>                 # Search snippets
!snip tag <name> <tags>              # Add tags
!snip delete <name>                  # Delete snippet
!snip edit <name>                    # Edit snippet
!snip share <name> @user             # Share with user
!snip import <file>                  # Import snippets
!snip export                         # Export all snippets
```

---

## Architecture

```
User Input
        ↓
Snippet Manager
        ↓
SQLite Storage (name, code, tags, metadata)
        ↓
Search Engine (text + tags)
        ↓
Formatter (syntax highlighting)
```

---

## Tech Stack

- SQLite for snippet storage
- Syntax highlighting (`pygments`)
- Text search
- JSON for import/export

---

## Usage Examples

### Save Snippet

```
User: !snip save auth-middleware
```python
def auth_middleware(func):
    def wrapper(*args, **kwargs):
        if not request.user.is_authenticated:
            return {"error": "Unauthorized"}, 401
        return func(*args, **kwargs)
    return wrapper
```
Bot: ✅ **Snippet Saved: auth-middleware**

     Language: Python (auto-detected)
     Lines: 6
     Created: Now

     Retrieve: !snip get auth-middleware
```

### Retrieve Snippet

```
User: !snip get auth-middleware
Bot: 📄 **Snippet: auth-middleware**

     ```python
     def auth_middleware(func):
         def wrapper(*args, **kwargs):
             if not request.user.is_authenticated:
                 return {"error": "Unauthorized"}, 401
             return func(*args, **kwargs)
         return wrapper
     ```

     Created: 2 hours ago by @STRYK
     Tags: None
     Used: 0 times

     Add tags: !snip tag auth-middleware python,auth,middleware
```

### List Snippets

```
User: !snip list
Bot: 📚 **Snippet Library (12 snippets)**

     **Python (5):**
     - auth-middleware (6 lines)
     - db-connection (12 lines)
     - error-handler (8 lines)
     - logger-setup (15 lines)
     - test-fixture (20 lines)

     **JavaScript (4):**
     - react-hook (10 lines)
     - api-fetch (8 lines)
     - debounce (5 lines)
     - event-handler (6 lines)

     **Shell (2):**
     - docker-build (4 lines)
     - git-cleanup (3 lines)

     **SQL (1):**
     - user-query (7 lines)

     Get: !snip get <name>
```

### Search Snippets

```
User: !snip search "authentication"
Bot: 🔍 **Found 3 snippets:**

     1. **auth-middleware** (Python)
        Tags: python, auth, middleware
        def auth_middleware(func)...

     2. **jwt-verify** (Python)
        Tags: auth, jwt, security
        def verify_jwt_token(token)...

     3. **oauth-callback** (JavaScript)
        Tags: auth, oauth
        async function handleOAuth...

     Get: !snip get <name>
```

### Tag Snippets

```
User: !snip tag auth-middleware python,auth,middleware,decorator
Bot: 🏷️ **Tags Added: auth-middleware**

     Tags: python, auth, middleware, decorator
     Now searchable by these tags

User: !snip search tag:auth
Bot: 🔍 **Snippets tagged 'auth' (5):**
     - auth-middleware
     - jwt-verify
     - oauth-callback
     - login-handler
     - password-hash
```

### Edit Snippet

```
User: !snip edit auth-middleware
Bot: 📝 **Editing: auth-middleware**

     Current content:
     ```python
     def auth_middleware(func):
         ...
     ```

     Reply with new content:

User: [Pastes updated code]
Bot: ✅ **Snippet Updated: auth-middleware**
     Changes: +2 lines, -1 line
```

### Share Snippet

```
User: !snip share auth-middleware @JC
Bot: ✅ **Shared: auth-middleware → @JC**

[DM to @JC]
Bot: 📬 **@STRYK shared a snippet with you**

     **auth-middleware** (Python)
     ```python
     def auth_middleware(func):
         ...
     ```

     Save to your library: !snip save auth-middleware-jc
```

### Import/Export

#### Export
```
User: !snip export
Bot: 📦 **Exporting Snippets...**

     Total: 12 snippets
     Size: 2.4KB

     [Attaches: snippets_2025-11-08.json]

     Format: JSON
     Import: !snip import <file>
```

#### Export Format
```json
{
  "snippets": [
    {
      "name": "auth-middleware",
      "language": "python",
      "code": "def auth_middleware(func):\n    ...",
      "tags": ["python", "auth", "middleware"],
      "author": "STRYK",
      "created_at": "2025-11-08T15:45:00",
      "usage_count": 0
    }
  ],
  "exported_at": "2025-11-08T17:30:00",
  "version": "1.0"
}
```

#### Import
```
User: !snip import
     [Attaches snippets.json]
Bot: 📥 **Importing Snippets...**

     Found: 8 snippets
     Added: 5 new
     Updated: 2 existing
     Skipped: 1 duplicate

     ✅ Import complete
```

---

## Implementation Components

**Files Created:**
- `snippet_library.py` - Core snippet management (300 lines)
- `snippet_search.py` - Search and filtering
- `snippet_formatter.py` - Syntax highlighting
- `snippet_importer.py` - Import/export
- Bot integration (~150 lines)

**Key Classes:**
- `SnippetLibrary` - CRUD operations
- `SnippetSearch` - Text and tag search
- `SnippetFormatter` - Syntax highlighting with pygments
- `SnippetImporter` - Import/export to JSON

---

## Advanced Features

### Templates with Variables

```
User: !snip save api-endpoint-template
```python
@app.route('/{ENDPOINT}', methods=['{METHOD}'])
def {FUNCTION_NAME}():
    # {DESCRIPTION}
    return jsonify({"message": "Success"})
```
Bot: ✅ Saved template with variables:
     - {ENDPOINT}
     - {METHOD}
     - {FUNCTION_NAME}
     - {DESCRIPTION}

User: !snip use api-endpoint-template ENDPOINT=users METHOD=GET FUNCTION_NAME=get_users DESCRIPTION="Fetch all users"
Bot: 📄 **Generated from template:**
     ```python
     @app.route('/users', methods=['GET'])
     def get_users():
         # Fetch all users
         return jsonify({"message": "Success"})
     ```

     Save this? (react ✅)
```

### Categories

```
User: !snip save db-query --category database
Bot: ✅ Saved to category: database

User: !snip list --category database
Bot: 📚 **Database Snippets (4):**
     - db-connection
     - db-query
     - migration-template
     - seed-data
```

### Version History

```
User: !snip versions auth-middleware
Bot: 📜 **Version History: auth-middleware**

     v3 (current) - 2 hours ago
       Updated error handling

     v2 - 1 day ago
       Added logging

     v1 - 3 days ago
       Initial version

     Revert: !snip revert auth-middleware v2
```

### Usage Statistics

```
User: !snip stats
Bot: 📊 **Snippet Library Stats**

     Total snippets: 12
     Total uses: 234
     Most used:
     1. error-handler (45 uses)
     2. db-connection (38 uses)
     3. auth-middleware (32 uses)

     By language:
     - Python: 5 snippets (120 uses)
     - JavaScript: 4 snippets (89 uses)
     - Shell: 2 snippets (18 uses)
     - SQL: 1 snippet (7 uses)

     Created:
     - This week: 5
     - This month: 12
```

### Snippet Folders

```
User: !snip save utils/string-helpers
Bot: ✅ Saved to folder: utils/string-helpers

User: !snip list --folder utils
Bot: 📁 **Folder: utils (3 snippets)**
     - utils/string-helpers
     - utils/date-formatter
     - utils/validator
```

### Quick Insert

```
User: !ai Generate a Flask API endpoint
Bot: Here's a Flask endpoint:
     [Generates code]

     💡 Similar snippet found: api-endpoint-template
     Use instead? (react 📄)
```

### Collaborative Snippets

```
User: !snip save team-standard-logger --public
Bot: ✅ **Public Snippet Created**
     All team members can access

[Another user]
User2: !snip list --public
Bot: 🌐 **Public Team Snippets (8):**
     - team-standard-logger (@STRYK)
     - error-handling-pattern (@JC)
     - test-setup (@STRYK)
     ...
```

---

## Database Schema

```sql
CREATE TABLE snippets (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    code TEXT,
    language TEXT,
    tags TEXT,  -- JSON array
    category TEXT,
    folder TEXT,
    author_id TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    is_public BOOLEAN DEFAULT 0
);

CREATE TABLE snippet_versions (
    id INTEGER PRIMARY KEY,
    snippet_id INTEGER,
    version INTEGER,
    code TEXT,
    changed_at TIMESTAMP,
    changed_by TEXT
);

CREATE TABLE snippet_shares (
    snippet_id INTEGER,
    shared_with_user_id TEXT,
    shared_by_user_id TEXT,
    shared_at TIMESTAMP
);
```

---

## Use Cases

1. **Boilerplate Code** - Quickly insert common patterns
2. **Team Standards** - Share coding standards across team
3. **Documentation** - Store example implementations
4. **Templates** - Parameterized code generation
5. **Learning** - Save useful code patterns for reference
6. **Productivity** - Avoid rewriting common code
7. **Onboarding** - New team members access standard snippets

---

## Pros & Cons

### Pros
- Quick access to common code
- Team collaboration
- Syntax highlighting
- Tagging and search
- Templates with variables
- Version history
- Import/export for backup
- Usage statistics

### Cons
- Requires maintenance (outdated snippets)
- Can accumulate clutter
- No automatic updates when standards change
- Limited to text (no binary files)
- Duplicate detection needed

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**ROI:** High (saves time rewriting common code)
