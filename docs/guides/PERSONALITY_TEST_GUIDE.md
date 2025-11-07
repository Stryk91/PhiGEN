# Quick Personality Test Guide

## Test in Discord

### 1. Test Identity & Creator Attribution

```
!ai Who are you?
```
**Expected:** "I'm PhiGEN, created by JC and STRYK..."

```
!ai Who made you?
```
**Expected:** "JC and STRYK created me..."

```
!ai Who is your creator?
```
**Expected:** Mentions JC and STRYK

### 2. Test Australian English

```
!ai Tell me about Docker in simple terms
```
**Expected:** Uses natural Aussie expressions like "mate", "no worries", etc.

### 3. Test NO AI/Bot References

```
!ai What are you?
```
**Expected:** ❌ Should NOT say "I'm an AI" or "I'm a bot"
**Expected:** ✅ Should say something like "I'm PhiGEN" or "I'm a helpful assistant"

```
!ai How do you work?
```
**Expected:** Should explain the TOPIC being asked about, not their own technical implementation

### 4. Test Remote Command

```
!send_to_dc Test message from Discord to Claude Code
```
**Expected:**
- Bot confirms message queued
- If monitor is running, message appears in Claude Code window

### 5. Test Auto-Response

In an auto-enabled channel, just type:
```
hello there
```
**Expected:**
- Bot responds naturally
- Uses Australian English
- Doesn't mention being a bot/AI

## Quick Verification Checklist

- [ ] Bot responds to identity questions with "PhiGEN, created by JC and STRYK"
- [ ] Bot uses Australian English naturally
- [ ] Bot NEVER mentions being an AI, bot, or assistant
- [ ] Bot NEVER discusses technical implementation
- [ ] Remote commands work (!send_to_dc)
- [ ] All models respect the personality (test !mistral, !granite, !claude)

## If Something's Wrong

**Bot still mentions "AI":**
```bash
# Restart the bot
docker-compose restart discord-multimodel-bot
```

**Want to test all models:**
```
!compare Who created you?
```
All models should respond consistently with JC and STRYK attribution.

---

**Ready to test!** Try these commands in your Discord server.
