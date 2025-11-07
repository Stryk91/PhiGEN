# Feature #20: Sentiment Analysis

**Status:** TBI (To Be Implemented)
**Priority:** Low
**Complexity:** Medium
**Estimated Time:** 2 days

---

## Overview

Detect user frustration, satisfaction, mood. Adjust bot responses accordingly, escalate issues, track user happiness.

**Commands:**
```
!sentiment analyze                   # Analyze current mood
!sentiment history                   # Sentiment over time
!sentiment team                      # Team sentiment overview
!sentiment alerts on/off             # Alert on negative sentiment
!sentiment report                    # Generate report
```

---

## Architecture

```
User Message
        ↓
Sentiment Classifier (positive/negative/neutral)
        ↓
Emotion Detection (frustration, satisfaction, confusion, etc.)
        ↓
Response Adapter (adjust tone/style)
        ↓
Sentiment Database (track trends)
```

---

## Tech Stack

- `transformers` - Sentiment models (BERT, RoBERTa)
- Emotion detection models
- SQLite for sentiment history
- Statistical analysis

---

## Usage Examples

### Automatic Detection

```
[User sends message]
User: This doesn't work and I've been stuck for hours!

Bot: [Detects: High frustration, negative sentiment]

     I can tell you're frustrated - let me help fix this quickly.

     **Immediate Actions:**
     1. Analyzing your issue...
     2. Searching for solutions...
     3. Escalating to priority support if needed

     [Provides solution with empathetic tone]
```

### Analyze Current Mood

```
User: !sentiment analyze

Bot: 📊 **Your Current Sentiment**

     **Overall Mood:** Slightly Frustrated 😐
     Confidence: 78%

     **Detected Emotions:**
     - Frustration: 65%
     - Determination: 45%
     - Impatience: 30%

     **Analysis:**
     Last 5 messages show increasing frustration.
     You've been working on authentication for 2 hours.

     **Bot Adjustment:**
     I'll provide more direct solutions and skip explanations
     unless you ask for them.

     Need a break or want to try a different approach?
```

### Sentiment History

```
User: !sentiment history

Bot: 📈 **Your Sentiment History**

     **Today:**
     9 AM: 😊 Positive (started new feature)
     11 AM: 😐 Neutral
     2 PM: 😤 Frustrated (bug discovered)
     4 PM: 😊 Positive (bug fixed!)

     **This Week:**
     Mon: 😊 Positive (6h)
     Tue: 😐 Neutral (4h)
     Wed: 😤 Frustrated (3h) ⚠️
     Thu: 😊 Positive (5h)
     Fri: 😊 Positive (7h)

     **Insights:**
     - You're most productive Mon/Thu/Fri
     - Wednesday had frustration spike (bug day)
     - Overall trend: 65% positive, 25% neutral, 10% frustrated

     **Frustration Triggers:**
     - Authentication bugs (3 times this week)
     - Build failures (2 times)
```

### Team Sentiment Overview

```
User: !sentiment team

Bot: 👥 **Team Sentiment (Last 7 Days)**

     **Overall Team Mood:** 😊 Mostly Positive
     Average: 72% positive

     **By Person:**
     @STRYK: 😊 Positive (75%)
     @JC: 😐 Neutral (55%)
     @Dev1: 😊 Very Positive (85%)

     **Trends:**
     - Team morale improved 15% this week
     - @JC seems stuck on a problem (offer help?)
     - @Dev1 very productive lately

     **Team Frustration Points:**
     - Docker build issues (mentioned 5 times)
     - Test flakiness (mentioned 3 times)

     **Recommendation:**
     Address Docker build reliability
```

### Sentiment-Based Alerts

```
User: !sentiment alerts on

Bot: 🔔 **Sentiment Alerts Enabled**

     I'll notify you when:
     - Your frustration level is high (>70%)
     - You've been stuck for >30 minutes
     - Pattern of declining sentiment detected

[Later - after prolonged frustration]
Bot: ⚠️ **Frustration Alert**

     You've been frustrated for 40 minutes working on OAuth

     **Suggestions:**
     1. Take a 10-minute break
     2. Try a different approach: !branch create oauth-alt
     3. Ask for help: @mention a teammate
     4. Switch tasks temporarily

     I'm here to help - want to try something different?
```

### Adaptive Responses

```
[Frustrated user]
User: Nothing is working

Bot: [Detects high frustration]

     I understand - let's fix this together.

     **Quick Action:**
     Show me the exact error you're seeing
     I'll give you a direct solution, no theory

[Happy user]
User: That worked perfectly!

Bot: [Detects high satisfaction]

     Awesome! 🎉

     Want to explore why this solution works?
     Or ready to move on to the next feature?
```

### Generate Report

```
User: !sentiment report

Bot: 📄 **Sentiment Report Generated**

     [Attaches: sentiment_report_2025-11-08.pdf]

     **Executive Summary:**
     Overall positive development experience (68% positive)

     **Key Findings:**
     1. Most productive hours: 9-11 AM (85% positive)
     2. Frustration spike: Wed 2-4 PM (authentication debugging)
     3. Team collaboration boosts mood (+20% when pairing)
     4. Friday afternoons most positive (wrapping up work)

     **Frustration Analysis:**
     - Top frustration: Build/test failures (40%)
     - Secondary: Authentication/security issues (30%)
     - Minor: Documentation gaps (15%)

     **Recommendations:**
     1. Improve build reliability
     2. Better auth debugging tools
     3. Expand documentation
     4. Encourage more pair programming (mood booster)

     **Emotional Trajectory:**
     Week started strong, mid-week dip (normal), strong finish
```

---

## Implementation Components

**Files Created:**
- `sentiment_analyzer.py` - Core sentiment detection (350 lines)
- `emotion_classifier.py` - Emotion detection
- `response_adapter.py` - Adjust bot tone
- `sentiment_tracker.py` - Historical tracking
- Bot integration (~200 lines)

**Key Classes:**
- `SentimentAnalyzer` - Classify sentiment (pos/neg/neutral)
- `EmotionClassifier` - Detect specific emotions
- `ResponseAdapter` - Adjust bot behavior based on mood
- `SentimentTracker` - Store and analyze trends

---

## Detected Sentiments

**Basic:**
- Positive 😊
- Neutral 😐
- Negative 😤

**Detailed Emotions:**
- Frustration 😤
- Confusion 😕
- Excitement 🤩
- Satisfaction 😊
- Determination 💪
- Impatience ⏰
- Curiosity 🤔
- Boredom 😑

---

## Response Adjustments

**When User is Frustrated:**
- Skip long explanations
- Provide direct solutions
- Offer to escalate
- More empathetic tone
- Suggest breaks

**When User is Confused:**
- Simplify language
- Use more examples
- Break into smaller steps
- Offer ELI5 explanations

**When User is Happy:**
- Match their energy
- Offer to explore deeper
- Suggest advanced features
- Celebrate wins

**When User is Impatient:**
- Fast, concise responses
- Skip preamble
- Direct answers only
- Offer quick alternatives

---

## Advanced Features

### Context-Aware Detection

```
Bot: 🧠 **Context Understanding**

     Message: "This is taking forever"

     **Without Context:** Neutral/Slightly Negative
     **With Context:**
     - Working on same issue for 2 hours
     - Previous messages show declining patience
     - Recent test failures

     **Actual Sentiment:** High Frustration
     **Response:** Immediate assistance + alternative approach
```

### Pattern Recognition

```
Bot: 📊 **Pattern Detected**

     You show frustration every time:
     - Working on authentication
     - Test failures occur
     - Docker build issues

     **Proactive Suggestion:**
     Would you like me to:
     1. Create debugging macros for these scenarios
     2. Set up better error handling
     3. Alert you earlier when these patterns start
```

### Mood-Based Routing

```
[User very frustrated]
Bot: Routing to human support...

[User slightly confused]
Bot: Providing extra guidance...

[User happy and productive]
Bot: Minimal interruptions, quick responses only
```

### Sentiment Triggers

```
User: !sentiment trigger "if frustrated > 60% for 30min then suggest-break"

Bot: ✅ **Trigger Set**

     Condition: Frustration >60% for 30+ minutes
     Action: Suggest taking a break

[30 minutes of frustration later]
Bot: 💡 **Break Suggestion**

     You've been frustrated for 30 minutes.
     Research shows 10-minute breaks improve problem-solving.

     Want to:
     1. Take a short break
     2. Switch to different task
     3. Get help from teammate
```

### Team Mood Dashboard

```
User: !sentiment dashboard

Bot: 📊 **Team Mood Dashboard**

     **Right Now:**
     🟢 @Dev1 - Working smoothly
     🟡 @STRYK - Slightly frustrated (debugging)
     🟢 @JC - Productive
     🔴 @Dev2 - Very frustrated (needs help!) ⚠️

     **Team Energy:** 65%
     **Morale Trend:** ↑ Improving

     **Needs Attention:**
     @Dev2 has been stuck for 45 minutes on API issue
     Consider reaching out?
```

---

## Database Schema

```sql
CREATE TABLE sentiment_log (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP,
    user_id TEXT,
    message TEXT,
    sentiment TEXT,  -- positive, negative, neutral
    sentiment_score DECIMAL(5, 2),  -- -1.0 to 1.0
    emotions TEXT,  -- JSON {"frustration": 0.65, ...}
    context TEXT  -- What user was working on
);

CREATE TABLE sentiment_alerts (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    condition TEXT,
    action TEXT,
    enabled BOOLEAN
);
```

---

## Use Cases

1. **User Experience** - Detect frustration early, provide better support
2. **Team Management** - Monitor team morale and productivity
3. **Bot Adaptation** - Adjust responses to user mood
4. **Issue Escalation** - Route frustrated users to human support
5. **Productivity Insights** - Understand emotional impact on work
6. **Team Health** - Track overall team sentiment
7. **Proactive Support** - Offer help before users ask

---

## Pros & Cons

### Pros
- Early frustration detection
- Improves user experience
- Adaptive bot behavior
- Team morale insights
- Proactive support
- Historical mood tracking
- Identifies pain points

### Cons
- Privacy concerns (emotional tracking)
- Not always accurate (sarcasm, jokes)
- Requires large message history
- Can feel intrusive
- Model accuracy varies
- Cultural/language differences affect detection

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**ROI:** Medium (improves UX but not critical)
