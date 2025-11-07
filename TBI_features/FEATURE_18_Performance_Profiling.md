# Feature #18: Performance Profiling

**Status:** TBI (To Be Implemented)
**Priority:** Low-Medium
**Complexity:** Medium
**Estimated Time:** 2 days

---

## Overview

Track bot performance metrics: response times, token usage, model speeds, identify bottlenecks.

**Commands:**
```
!perf stats                          # Overall performance stats
!perf model <name>                   # Model-specific metrics
!perf slowest                        # Slowest queries
!perf bottlenecks                    # Identify performance issues
!perf compare <m1> <m2>              # Compare model speeds
!perf history                        # Performance over time
!perf report                         # Generate report
!perf optimize                       # Suggest optimizations
```

---

## Architecture

```
Every Bot Interaction
        ↓
Performance Logger (track timing, tokens, model)
        ↓
Metrics Database
        ↓
Analyzer (detect patterns, bottlenecks)
        ↓
Optimization Suggestions
```

---

## Tech Stack

- Time tracking (`time.perf_counter`)
- Token counting (`tiktoken`)
- SQLite for metrics storage
- Statistical analysis

---

## Usage Examples

### Overall Stats

```
User: !perf stats
Bot: 📊 **Performance Statistics**

     **Response Times (last 24h):**
     Average: 2.3s
     Median: 1.8s
     P95: 4.5s
     P99: 7.2s

     **Breakdown by Model:**
     Claude Sonnet: 2.8s avg (45% of queries)
     Claude Haiku: 1.2s avg (30% of queries)
     Phi 3.5: 0.6s avg (15% of queries)
     Granite Code: 0.5s avg (10% of queries)

     **Token Usage:**
     Total: 1.2M tokens
     Input: 680K tokens
     Output: 520K tokens

     **Cost:**
     Today: $12.40
     Average: $0.08/query
```

### Model-Specific Metrics

```
User: !perf model sonnet
Bot: 📊 **Claude Sonnet 3.5 Performance**

     **Speed:**
     Average: 2.8s
     Fastest: 0.9s
     Slowest: 12.3s
     Variance: High ⚠️

     **Token Efficiency:**
     Input/Output ratio: 1.3:1
     Average input: 4,200 tokens
     Average output: 3,200 tokens

     **Use Patterns:**
     Most used for: Complex reasoning (65%)
     Time of day: Peak 2-4 PM

     **Cost:**
     Average: $0.12/query
     Daily: $8.40

     **Quality:**
     User satisfaction: 4.3/5
     Retry rate: 8% (low)
```

### Slowest Queries

```
User: !perf slowest
Bot: 🐌 **Slowest Queries (last 24h)**

     1. **12.3s** - "Explain quantum computing with examples"
        Model: Claude Sonnet
        Tokens: 9,200 output
        Issue: Long output

     2. **8.7s** - "Review this 500-line codebase"
        Model: Claude Sonnet
        Tokens: 15,000 input
        Issue: Large context

     3. **7.4s** - "Generate React component with tests"
        Model: Claude Sonnet
        Tokens: 6,800 output
        Issue: Code generation

     **Common Causes:**
     - Large context (40%)
     - Long outputs (35%)
     - Complex reasoning (25%)

     Optimization: !perf optimize
```

### Identify Bottlenecks

```
User: !perf bottlenecks
Bot: 🔍 **Performance Bottlenecks Detected**

     **Issue #1: Context Window Too Large**
     Impact: +1.2s average
     Frequency: 35% of queries
     Current: 15 messages avg
     Recommendation: Reduce to 10 messages
     Savings: ~0.8s per query

     **Issue #2: Using Sonnet for Simple Queries**
     Impact: +1.5s, +$0.08 per query
     Frequency: 25% of queries
     Example: "What is Python?"
     Recommendation: Use Haiku for simple questions
     Savings: 60% faster, 75% cheaper

     **Issue #3: No Caching**
     Impact: Repeated queries take full time
     Frequency: 15% are duplicates
     Example: "!git status" (asked 12 times today)
     Recommendation: Cache common queries
     Savings: ~2s on cache hits

     Apply fixes: !perf optimize --apply
```

### Compare Models

```
User: !perf compare sonnet haiku
Bot: ⚡ **Model Comparison: Sonnet vs Haiku**

     **Speed:**
     Sonnet: 2.8s avg
     Haiku: 1.2s avg
     Winner: Haiku (57% faster) ⚡

     **Quality (user ratings):**
     Sonnet: 4.3/5
     Haiku: 3.9/5
     Winner: Sonnet (+10% quality) ⭐

     **Cost:**
     Sonnet: $0.12/query
     Haiku: $0.03/query
     Winner: Haiku (75% cheaper) 💰

     **Token Efficiency:**
     Sonnet: 1.3:1 input/output
     Haiku: 1.1:1 input/output
     Winner: Haiku (more concise)

     **Recommendation:**
     Use Haiku for: Quick questions, simple tasks
     Use Sonnet for: Complex reasoning, detailed analysis
```

### Performance History

```
User: !perf history
Bot: 📈 **Performance Trend (last 30 days)**

     **Response Time:**
     Week 1: 2.1s avg
     Week 2: 2.5s avg ⚠️ +19%
     Week 3: 2.8s avg ⚠️ +12%
     Week 4: 2.3s avg ✅ -18%

     **Trend:** Improving (recent optimization)

     **Notable Events:**
     - Nov 1: Context window increased (slowed queries)
     - Nov 5: Added local models (faster for code)
     - Nov 8: Enabled caching (20% speedup)

     **Token Usage:**
     Growing 15%/week
     Current: 1.2M tokens/day

     **Cost:**
     Week 1: $45
     Week 2: $68 ⚠️
     Week 3: $82 ⚠️
     Week 4: $52 ✅

     **Recommendation:**
     Continue current optimizations
```

### Generate Report

```
User: !perf report
Bot: 📄 **Performance Report Generated**

     [Attaches: performance_report_2025-11-08.pdf]

     **Contents:**
     1. Executive Summary
     2. Response Time Analysis
     3. Model Performance Breakdown
     4. Cost Analysis
     5. Bottleneck Identification
     6. Optimization Recommendations
     7. Historical Trends

     **Key Findings:**
     - Average response time: 2.3s
     - 35% of queries could use cheaper model
     - Caching could save $15/day
     - Context window too large (15→10)

     **Estimated Savings:**
     Time: 25% faster responses
     Cost: 40% reduction ($280/month → $168/month)
```

### Optimization Suggestions

```
User: !perf optimize
Bot: 💡 **Optimization Suggestions**

     Based on your usage patterns:

     **1. Auto-Switch to Haiku for Simple Queries**
     Affected: 25% of queries
     Savings: ~1.5s per query, $0.08 per query
     Total: 0.4s avg improvement, $12/day saved

     **2. Enable Query Caching**
     Affected: 15% of queries
     Savings: ~2s per cached query
     Total: 0.3s avg improvement

     **3. Reduce Context Window (15 → 10)**
     Affected: 100% of queries
     Savings: ~0.8s per query
     Total: 0.8s avg improvement

     **4. Use Local Models for Code Review**
     Affected: 10% of queries
     Savings: $0.12 per query
     Total: $4/day saved

     **Combined Savings:**
     Speed: 1.5s faster avg (39% improvement)
     Cost: $16/day saved (48% reduction)

     Apply all: !perf optimize --apply-all
     Apply specific: !perf optimize --apply 1,2,3
```

---

## Implementation Components

**Files Created:**
- `performance_profiler.py` - Track all metrics (400 lines)
- `metrics_collector.py` - Gather timing and token data
- `bottleneck_analyzer.py` - Identify issues
- `optimizer.py` - Suggest improvements
- `report_generator.py` - PDF/CSV reports
- Bot integration (~200 lines)

**Key Classes:**
- `PerformanceProfiler` - Main profiling logic
- `MetricsCollector` - Capture all metrics
- `BottleneckAnalyzer` - Detect performance issues
- `Optimizer` - Generate optimization suggestions
- `ReportGenerator` - Create reports

---

## Tracked Metrics

**Per Query:**
- Response time (total, model only)
- Input tokens
- Output tokens
- Cost
- Model used
- User
- Timestamp
- Query type (code, question, chat)

**Aggregate:**
- Average response time
- P50/P95/P99 latency
- Token usage rates
- Cost per day/week/month
- Model usage distribution
- Peak usage times
- Error rates

---

## Advanced Features

### Real-Time Monitoring

```
User: !perf monitor on
Bot: 👁️ **Real-Time Monitoring Active**

     Will show metrics for every query

[Next query]
User: !ai What is Python?
Bot: [Response]

     ⚡ **Performance:**
     Model: Claude Haiku
     Time: 1.1s
     Tokens: 2,300 (1,200 in, 1,100 out)
     Cost: $0.03
```

### Alerting

```
User: !perf alert-if "response_time > 5s"
Bot: 🔔 **Alert Configured**

     Condition: Response time > 5s
     Will notify you

[Later - slow query occurs]
Bot: ⚠️ **Performance Alert**

     Query took 6.2s (threshold: 5s)
     Model: Claude Sonnet
     Reason: Large context (18 messages)

     Suggestions:
     - Reduce context: !ctx=10
     - Use faster model: !m haiku
```

### Heatmaps

```
User: !perf heatmap
Bot: 🔥 **Performance Heatmap**

     **By Hour of Day:**
     12 AM: 1.8s ❄️
     6 AM: 2.1s
     9 AM: 2.5s
     12 PM: 3.2s 🔥 Peak
     3 PM: 2.8s
     6 PM: 2.4s
     9 PM: 2.0s

     **By Day of Week:**
     Mon: 2.5s
     Tue: 2.8s
     Wed: 3.1s 🔥 Slowest
     Thu: 2.6s
     Fri: 2.2s
     Sat: 1.9s ❄️
     Sun: 2.0s

     **Insight:** Wednesday afternoons are slowest
     Cause: High query volume
```

### Regression Detection

```
Bot: ⚠️ **Performance Regression Detected**

     Response times increased 25% in last 24h

     Before: 2.3s avg
     Now: 2.9s avg

     **Likely Causes:**
     1. Context window increased (14 → 18)
     2. More complex queries
     3. Model API slower

     Investigate: !perf diff yesterday today
```

---

## Database Schema

```sql
CREATE TABLE performance_metrics (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP,
    user_id TEXT,
    model TEXT,
    query_type TEXT,
    response_time_ms INTEGER,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd DECIMAL(10, 6),
    context_size INTEGER
);

CREATE TABLE bottlenecks (
    id INTEGER PRIMARY KEY,
    detected_at TIMESTAMP,
    issue_type TEXT,
    impact_ms INTEGER,
    frequency_percent DECIMAL(5, 2),
    recommendation TEXT
);
```

---

## Use Cases

1. **Performance Monitoring** - Track bot responsiveness
2. **Cost Analysis** - Understand spending patterns
3. **Optimization** - Find and fix bottlenecks
4. **Capacity Planning** - Predict future resource needs
5. **Model Selection** - Choose optimal model for use case
6. **SLA Tracking** - Ensure response time targets met
7. **Debugging** - Investigate slow queries

---

## Pros & Cons

### Pros
- Visibility into performance
- Identify bottlenecks automatically
- Data-driven optimization
- Track improvements over time
- Cost-performance tradeoffs
- Alerts for regressions
- Historical trending

### Cons
- Overhead of metric collection (minimal)
- Storage for metrics
- Requires analysis to be useful
- Can be overwhelming with too much data
- May not capture all bottlenecks

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**ROI:** Medium (helps optimize but not critical)
