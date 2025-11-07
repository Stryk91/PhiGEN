# Feature #13: Cost Optimizer

**Status:** TBI (To Be Implemented)
**Priority:** Medium
**Complexity:** Medium
**Estimated Time:** 2 days

---

## Overview

Track API costs, auto-switch models based on budget, show usage stats, set spending limits, optimize model selection for cost efficiency.

**Commands:**
```
!cost today                          # Today's spending
!cost week                           # This week's spending
!cost month                          # This month's spending
!cost by-model                       # Cost breakdown by model
!cost by-user                        # Cost breakdown by user
!cost limit <amount>                 # Set daily/weekly/monthly limit
!cost auto-optimize on/off           # Auto-switch to cheaper models
!cost forecast                       # Predict month-end costs
!cost alert <threshold>              # Alert at spending threshold
!cost export                         # Export cost data
```

---

## Architecture

```
AI Request
        ↓
Cost Tracker (log tokens + model)
        ↓
Usage Database
        ↓
Cost Calculator (tokens × price)
        ↓
Budget Monitor (check limits)
        ↓
Auto-Optimizer (switch models if needed)
```

---

## Tech Stack

- SQLite for usage tracking
- Token counting (`tiktoken`)
- Model pricing database
- Budget monitoring logic

---

## Usage Examples

### Check Today's Costs

```
User: !cost today
Bot: 💰 **Costs Today (2025-11-08)**

     Total: $2.45

     **By Model:**
     Claude Sonnet 3.5: $1.80 (73%)
     Claude Haiku 3.5: $0.35 (14%)
     Phi 3.5 (local): $0.00 (0%)
     Granite Code (local): $0.00 (0%)
     Vision Pro: $0.30 (13%)

     **By Type:**
     Conversation: $1.20
     Code Generation: $0.80
     Vision Analysis: $0.30
     Context Injection: $0.15

     **Tokens:**
     Input: 45K tokens ($0.90)
     Output: 32K tokens ($1.55)
```

### Weekly Report

```
User: !cost week
Bot: 📊 **Weekly Costs (Nov 2-8)**

     Total: $18.45
     Average: $2.64/day
     Peak: $4.20 (Nov 5)

     **Daily Breakdown:**
     Mon: $2.10
     Tue: $3.50
     Wed: $2.80
     Thu: $4.20 ⚠️ Peak
     Fri: $2.45
     Sat: $1.80
     Sun: $1.60

     **Top Models:**
     1. Claude Sonnet: $12.40 (67%)
     2. Vision Pro: $3.20 (17%)
     3. Claude Haiku: $2.85 (16%)
     4. Local models: $0.00 (0%)

     Trend: ↑ 15% vs last week
```

### Monthly Forecast

```
User: !cost forecast
Bot: 📈 **Cost Forecast**

     **Current Month (Nov 1-8):**
     Spent: $18.45 (8 days)
     Average: $2.31/day

     **Projected:**
     End of month: $69.30
     Days remaining: 22
     Estimated: $50.85 more

     **Comparison:**
     Last month: $52.40
     Projected: $69.30
     Change: ↑ 32% ($16.90 more)

     ⚠️ Above typical spending
     Consider: !cost auto-optimize on
```

### Set Spending Limit

```
User: !cost limit daily $5
Bot: 🚨 **Daily Limit Set: $5.00**

     Current today: $2.45
     Remaining: $2.55

     When limit reached:
     1. Switch to local models (free)
     2. Use Claude Haiku (cheaper)
     3. Notify you

     Alerts:
     - 80% ($4.00): Warning
     - 100% ($5.00): Switch to free models

User: !cost limit monthly $100
Bot: 🚨 **Monthly Limit Set: $100.00**

     Current month: $18.45
     Remaining: $81.55
     Days left: 22
     Daily budget: $3.71/day
```

### Cost Breakdown by Model

```
User: !cost by-model
Bot: 💰 **Costs by Model (This Month)**

     **API Models:**
     1. Claude Sonnet 3.5: $12.40
        - Requests: 234
        - Avg cost: $0.053/request
        - Input: 234K tokens
        - Output: 178K tokens

     2. Claude Haiku 3.5: $2.85
        - Requests: 456
        - Avg cost: $0.006/request
        - Input: 180K tokens
        - Output: 95K tokens

     3. Vision Pro: $3.20
        - Requests: 12
        - Avg cost: $0.267/request
        - Images analyzed: 12

     **Local Models (Free):**
     - Phi 3.5: 89 requests
     - Mistral 7B: 45 requests
     - Granite Code: 67 requests

     **Recommendation:**
     Use local models when possible to reduce costs
     Current free usage: 201 requests (30% of total)
```

### Cost Breakdown by User

```
User: !cost by-user
Bot: 👥 **Costs by User (This Month)**

     1. @STRYK: $12.80 (69%)
        - Requests: 345
        - Favorite model: Claude Sonnet

     2. @JC: $4.20 (23%)
        - Requests: 156
        - Favorite model: Claude Haiku

     3. @Dev1: $1.45 (8%)
        - Requests: 67
        - Favorite model: Phi 3.5 (free)

     Total: $18.45
     Most cost-effective user: @Dev1 ($0.022/request)
```

### Auto-Optimize Mode

```
User: !cost auto-optimize on
Bot: 🤖 **Cost Auto-Optimizer Enabled**

     **Rules:**
     1. Simple queries → Claude Haiku ($)
     2. Complex tasks → Claude Sonnet ($$)
     3. Code review → Granite Code (free)
     4. Near limit → Local models only

     **Savings Potential:**
     Based on last week: ~35% ($6.45 saved)

     Disable: !cost auto-optimize off

[Later - auto-switch happens]
Bot: 💡 **Switched to Claude Haiku**
     Reason: Query complexity low
     Savings: ~$0.04 per request
```

### Cost Alert

```
User: !cost alert 80%
Bot: 🔔 **Alert Set: 80% of daily limit**

     Daily limit: $5.00
     Alert at: $4.00

[Later that day]
Bot: ⚠️ **Cost Alert: 80% Reached**

     Today: $4.10 / $5.00
     Remaining: $0.90

     **Actions:**
     1. Continue normally (risk limit)
     2. Switch to free models: !cost auto-optimize on
     3. Increase limit: !cost limit daily $10

     What would you like to do?
```

### Export Cost Data

```
User: !cost export
Bot: 📄 **Exporting Cost Data...**

     [Attaches: costs_2025-11.csv]

     Contents:
     date,model,user,input_tokens,output_tokens,cost
     2025-11-01,claude-sonnet-3-5,STRYK,4500,3200,0.45
     2025-11-01,claude-haiku-3-5,STRYK,2300,1800,0.12
     ...

     Import into Excel/Google Sheets for analysis
```

---

## Implementation Components

**Files Created:**
- `cost_tracker.py` - Track all API usage (350 lines)
- `cost_calculator.py` - Calculate costs from tokens
- `budget_monitor.py` - Enforce spending limits
- `cost_optimizer.py` - Auto-switch models
- `cost_reporter.py` - Generate reports
- Bot integration (~200 lines)

**Key Classes:**
- `CostTracker` - Log all requests with tokens and cost
- `CostCalculator` - Token counting and price calculation
- `BudgetMonitor` - Track limits and alerts
- `CostOptimizer` - Intelligent model selection
- `CostReporter` - Generate usage reports

---

## Model Pricing

**Current Pricing (per 1M tokens):**

| Model | Input | Output | Use Case |
|-------|-------|--------|----------|
| **Claude Sonnet 3.5** | $3.00 | $15.00 | Complex reasoning |
| **Claude Haiku 3.5** | $0.80 | $4.00 | Simple queries |
| **Vision Pro** | $4.00 | $15.00 | Image analysis |
| **Phi 3.5 (local)** | $0.00 | $0.00 | Code, free |
| **Mistral 7B (local)** | $0.00 | $0.00 | General, free |
| **Granite Code (local)** | $0.00 | $0.00 | Code review, free |

**Optimizer Strategy:**
- Simple question? → Haiku ($)
- Complex reasoning? → Sonnet ($$)
- Code generation? → Granite (free)
- Image? → Vision Pro ($$)
- Near budget? → Local models only

---

## Advanced Features

### Cost Predictions

```
User: !ai [complex query]
Bot: 💡 **Before I respond:**
     Estimated cost: $0.12
     Model: Claude Sonnet 3.5

     Continue? (react ✅)
     Or use cheaper Haiku? (react 💰)

User: (reacts 💰)
Bot: Switched to Haiku ($0.03 instead of $0.12)
     [Responds with Haiku]
```

### Usage Heatmap

```
User: !cost heatmap
Bot: 📊 **Usage Heatmap (This Week)**

     Most expensive hours:
     🔥 2-4 PM: $8.45 (peak)
     🔥 9-11 AM: $5.20
     ❄️ 6-8 AM: $0.80 (lowest)

     Most expensive days:
     🔥 Thursday: $4.20
     ❄️ Sunday: $1.60
```

### Savings Suggestions

```
User: !cost suggestions
Bot: 💡 **Cost Savings Suggestions**

     Based on your usage:

     1. **Switch 40% of queries to Haiku** → Save $6.80/month
        - Simple questions don't need Sonnet
        - Auto-optimizer can do this: !cost auto-optimize on

     2. **Use local models for code** → Save $3.20/month
        - Granite Code performs well on code review
        - Set as default: !m granite --default-for code

     3. **Reduce context length** → Save $2.40/month
        - Current avg: 15 messages
        - Try: !ctx=10

     Total potential savings: $12.40/month (67% reduction)
```

---

## Database Schema

```sql
CREATE TABLE usage_log (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP,
    user_id TEXT,
    model TEXT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd DECIMAL(10, 6),
    query_type TEXT,  -- conversation, code, vision
    response_time_ms INTEGER
);

CREATE TABLE budget_limits (
    user_id TEXT,
    period TEXT,  -- daily, weekly, monthly
    limit_usd DECIMAL(10, 2),
    alert_threshold DECIMAL(3, 2)  -- 0.0-1.0
);

CREATE TABLE model_pricing (
    model TEXT PRIMARY KEY,
    input_price_per_1m DECIMAL(10, 2),
    output_price_per_1m DECIMAL(10, 2),
    updated_at TIMESTAMP
);
```

---

## Use Cases

1. **Budget Control** - Stay within spending limits
2. **Cost Optimization** - Automatically use cheapest suitable model
3. **Usage Analysis** - Understand where money goes
4. **Team Accountability** - Track per-user costs
5. **Forecasting** - Predict month-end spending
6. **ROI Analysis** - Compare costs vs productivity gains
7. **Alerts** - Get notified before overspending

---

## Pros & Cons

### Pros
- Transparent cost tracking
- Automatic cost optimization
- Spending limits prevent overages
- Detailed analytics
- Per-user tracking
- Forecast future costs
- Suggests savings opportunities

### Cons
- Requires accurate token counting
- Pricing changes need updates
- Local model costs not tracked (electricity)
- Complex queries might suffer with cheaper models
- Requires user discipline to respect limits

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**ROI:** Very High (prevents bill shock, optimizes spending)
