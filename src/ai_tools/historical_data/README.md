# Historical Data Archive

This directory contains parsed Discord conversation data from previous analysis work.

## Files

### 1. personality_profile.json (1.7KB)
Statistical personality analysis from ~178,000 Discord messages.

**Contains:**
- Vocabulary richness (28,039 unique words)
- Common phrases ("gon na", "wan na", "ya reckon", "gee wizz")
- Emoji preferences (🐀, :/, 🤣)
- Punctuation patterns
- Conversation flow transitions
- Verbosity metrics

**Use for:** Personality tuning, phrase injection, emoji patterns

### 2. knowledge_base_from_discord.json (6.8MB)
Conversation flow graph mapping 85,968 messages to their actual responses.

**Contains:**
- Message → Response mappings
- Conversation chains
- Markov chain data
- Response prediction patterns

**Use for:** Response generation, conversation flow, Markov-based text generation

## Quick Stats

```
Historical Data (personality_profile.json):
  - Messages analyzed: ~178,017
  - Unique words: 28,039
  - Top word: "cain" (5,166 uses)
  - Avg message length: 26.78 words

Knowledge Graph (knowledge_base_from_discord.json):
  - Unique messages: 85,968
  - Total connections: 98,617
  - Most branching: "LOL" (389 responses)
  - Avg responses/msg: 1.15

Current Data (conversation_full_log.txt):
  - Messages: 8,950
  - Bot responses: 23
  - RAG pairs: 15
  - Top word: "mate" (262 uses)
```

## Loading Examples

### Personality Profile
```python
import json

with open('historical_data/personality_profile.json') as f:
    profile = json.load(f)

# Get common phrases
phrases = profile['common_phrases']
# {"gon na": 574, "wan na": 412, ...}

# Get emoji preferences
emojis = profile['emoji_preferences']
# {":/": 2360, "🐀": 262, ...}
```

### Knowledge Base (Large File - Stream)
```python
import json

# Option 1: Load all (requires ~100MB RAM)
with open('historical_data/knowledge_base_from_discord.json') as f:
    kb = json.load(f)

# Option 2: Stream (memory efficient)
import ijson
with open('historical_data/knowledge_base_from_discord.json', 'rb') as f:
    for key, value in ijson.kvitems(f, ''):
        # Process each message → responses pair
        print(f"{key} → {value}")
```

## Integration Ideas

1. **Phrase Library:** Import common phrases for natural Australian slang
2. **Markov Bot:** Use knowledge graph for response prediction
3. **Emoji Engine:** Apply emoji preferences to bot responses
4. **Hybrid RAG:** Combine semantic search + conversation flow
5. **User Profiling:** Detect and adapt to user communication styles

## See Also

- `HISTORICAL_DATA_SUMMARY.md` - Full analysis and recommendations
- `conversation_analysis.json` - Current data analysis
- `analyze_conversations.py` - Analysis tool for current logs

---

**Source:** `D:\PYBKPS\PythonProject\`
**Copied:** November 8, 2025
**Original analysis date:** Unknown (pre-2025)
