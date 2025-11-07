# Feature #15: A/B Testing

**Status:** TBI (To Be Implemented)
**Priority:** Low-Medium
**Complexity:** Medium
**Estimated Time:** 2 days

---

## Overview

Compare model performance, test prompt variations, measure response quality, find optimal settings.

**Commands:**
```
!ab-test start <name>                # Start A/B test
!ab-test add-variant <config>        # Add test variant
!ab-test run <prompt>                # Run test on prompt
!ab-test results                     # Show test results
!ab-test winner                      # Declare winning variant
!ab-test stop                        # Stop test
!ab-test history                     # Past test results
!ab-test compare <v1> <v2>           # Compare two variants
```

---

## Architecture

```
User Query
        ↓
A/B Test Manager (route to variants)
        ↓
Parallel Execution (multiple models/configs)
        ↓
Response Collection
        ↓
Quality Metrics (speed, length, user rating)
        ↓
Statistical Analysis
```

---

## Tech Stack

- Parallel async execution
- SQLite for test results
- Statistical analysis (`scipy`)
- Performance metrics tracking

---

## Usage Examples

### Start A/B Test

```
User: !ab-test start "model-comparison"
Bot: 🧪 **A/B Test Started: model-comparison**

     Test ID: test_001
     Status: Active

     Add variants: !ab-test add-variant <config>
```

### Add Variants

```
User: !ab-test add-variant model=sonnet temp=50
Bot: ✅ **Variant A added**
     Config: Claude Sonnet, temp=50

User: !ab-test add-variant model=haiku temp=50
Bot: ✅ **Variant B added**
     Config: Claude Haiku, temp=50

User: !ab-test add-variant model=phi temp=50
Bot: ✅ **Variant C added**
     Config: Phi 3.5 (local), temp=50

Bot: 📊 **Test Ready: 3 variants**
     Run test: !ab-test run "<your prompt>"
```

### Run Test

```
User: !ab-test run "Explain OAuth2 in simple terms"
Bot: 🧪 **Running A/B Test...**

     Testing 3 variants on:
     "Explain OAuth2 in simple terms"

     ⏳ Variant A (Sonnet)... Done (2.3s)
     ⏳ Variant B (Haiku)... Done (1.1s)
     ⏳ Variant C (Phi)... Done (0.8s)

     **Variant A Response:**
     OAuth2 is like a valet key for your car. Instead of giving...
     [Full response]

     **Variant B Response:**
     OAuth2 allows apps to access your data without knowing...
     [Full response]

     **Variant C Response:**
     OAuth2 is an authorization framework that lets...
     [Full response]

     Rate each response (1-5):
     React: A=1️⃣, B=2️⃣, C=3️⃣

[User reacts: A=5️⃣, B=4️⃣, C=3️⃣]
Bot: ✅ Ratings recorded
```

### View Results

```
User: !ab-test results
Bot: 📊 **A/B Test Results: model-comparison**

     **Runs:** 12
     **Variants:** 3

     **Performance:**
     | Variant | Avg Speed | Avg Length | Avg Rating | Cost |
     |---------|-----------|------------|------------|------|
     | A (Sonnet) | 2.1s | 245 words | 4.2/5 ⭐ | $0.04 |
     | B (Haiku) | 1.0s | 180 words | 3.8/5 ⭐ | $0.01 |
     | C (Phi) | 0.7s | 210 words | 3.3/5 ⭐ | $0.00 |

     **Statistical Significance:**
     A vs B: p=0.03 ✓ (significant)
     A vs C: p=0.01 ✓ (significant)
     B vs C: p=0.12 ✗ (not significant)

     **Winner: Variant A (Sonnet)**
     - Best quality (4.2/5)
     - Worth the cost for this use case

     Apply: !ab-test winner A
```

### Detailed Comparison

```
User: !ab-test compare A B
Bot: 🔍 **Variant A vs B Comparison**

     **Speed:**
     A: 2.1s avg
     B: 1.0s avg
     Winner: B (52% faster) ⚡

     **Quality:**
     A: 4.2/5
     B: 3.8/5
     Winner: A (+11% quality) ⭐

     **Length:**
     A: 245 words
     B: 180 words
     Difference: A is 36% longer

     **Cost:**
     A: $0.04
     B: $0.01
     Winner: B (75% cheaper) 💰

     **Recommendation:**
     Use A when: Quality is priority
     Use B when: Speed/cost is priority
```

### Declare Winner

```
User: !ab-test winner A
Bot: 🏆 **Winner Declared: Variant A**

     Config: Claude Sonnet, temp=50

     This will become your default for similar queries.
     Apply now? (react ✅)

[User reacts ✅]
Bot: ✅ **Default Updated**
     Now using: Claude Sonnet, temp=50
```

### Test History

```
User: !ab-test history
Bot: 📜 **A/B Test History**

     1. **model-comparison** (Completed)
        Variants: 3
        Runs: 12
        Winner: Variant A (Sonnet)
        Completed: 2 days ago

     2. **temperature-test** (Completed)
        Variants: 5 (temp 20-100)
        Runs: 25
        Winner: Variant C (temp=50)
        Completed: 1 week ago

     3. **prompt-style** (Active)
        Variants: 2
        Runs: 4
        Winner: TBD

     View: !ab-test load <name>
```

---

## Implementation Components

**Files Created:**
- `ab_tester.py` - Core testing logic (400 lines)
- `variant_runner.py` - Parallel execution
- `metrics_collector.py` - Performance and quality metrics
- `statistical_analyzer.py` - Statistical significance
- Bot integration (~200 lines)

**Key Classes:**
- `ABTester` - Test management
- `VariantRunner` - Execute variants in parallel
- `MetricsCollector` - Track speed, quality, cost
- `StatisticalAnalyzer` - Significance testing

---

## Advanced Features

### Automated Testing

```
User: !ab-test auto on
Bot: 🤖 **Auto A/B Testing Enabled**

     Will randomly test variants on 10% of queries
     Results collected automatically

[After 100 queries]
Bot: 📊 **Auto-Test Results (100 queries)**

     Variant A (Sonnet): 4.1/5 avg
     Variant B (Haiku): 3.7/5 avg

     Recommendation: Keep Variant A
```

### Prompt Variations

```
User: !ab-test start "prompt-style"
User: !ab-test add-variant prompt="Explain {topic} simply"
User: !ab-test add-variant prompt="ELI5: {topic}"
User: !ab-test add-variant prompt="What is {topic}?"

User: !ab-test run topic="quantum computing"
Bot: 🧪 **Testing 3 prompt styles...**
     [Runs all 3 prompts with same model]

     **Results:**
     Style 1: 4.5/5
     Style 2: 4.8/5 ⭐ Winner
     Style 3: 3.9/5
```

### Multi-Metric Optimization

```
User: !ab-test optimize-for quality,speed,cost
Bot: 🎯 **Multi-Objective Optimization**

     Weights:
     - Quality: 50%
     - Speed: 30%
     - Cost: 20%

     **Scores:**
     Variant A: 8.4/10 (high quality, slow, expensive)
     Variant B: 8.9/10 ⭐ (balanced)
     Variant C: 7.2/10 (fast, cheap, lower quality)

     **Winner: Variant B**
     Best overall score
```

### Temperature Sweeps

```
User: !ab-test sweep temp 0-100 step=20
Bot: 🌡️ **Temperature Sweep Test**

     Testing: temp=0, 20, 40, 60, 80, 100
     Model: Claude Sonnet
     Prompt: "Write a creative story"

     [Runs 6 variants]

     **Results:**
     temp=0: Creative 2/5, Coherent 5/5
     temp=20: Creative 3/5, Coherent 5/5
     temp=40: Creative 4/5, Coherent 4/5
     temp=60: Creative 4/5, Coherent 4/5
     temp=80: Creative 5/5, Coherent 3/5 ⚠️
     temp=100: Creative 5/5, Coherent 2/5 ⚠️

     **Optimal: temp=40**
     Best balance of creativity and coherence
```

### Context Window Testing

```
User: !ab-test start "context-size"
User: !ab-test sweep ctx 5-20 step=5
Bot: 🔍 **Context Window Test**

     Testing: ctx=5, 10, 15, 20
     Measuring: Response relevance

     **Results:**
     ctx=5: Relevance 3.2/5 (too little context)
     ctx=10: Relevance 4.5/5 ⭐
     ctx=15: Relevance 4.4/5 (no improvement)
     ctx=20: Relevance 4.3/5 (worse, too much noise)

     **Optimal: ctx=10**
     More context ≠ better results
```

### User Preference Learning

```
[After many A/B tests]
Bot: 🧠 **Learned Your Preferences**

     Based on 50 ratings:

     - You prefer: Quality > Speed
     - You rate Sonnet 15% higher than Haiku
     - You prefer concise responses (180-220 words)
     - You like code examples

     Auto-configuring:
     - Model: Claude Sonnet
     - Length: 200 words target
     - Style: Technical with examples
```

---

## Database Schema

```sql
CREATE TABLE ab_tests (
    id TEXT PRIMARY KEY,
    name TEXT,
    user_id TEXT,
    created_at TIMESTAMP,
    status TEXT,  -- active, completed
    winner_variant TEXT
);

CREATE TABLE test_variants (
    id INTEGER PRIMARY KEY,
    test_id TEXT,
    variant_name TEXT,  -- A, B, C, ...
    config TEXT  -- JSON
);

CREATE TABLE test_runs (
    id INTEGER PRIMARY KEY,
    test_id TEXT,
    variant_name TEXT,
    prompt TEXT,
    response TEXT,
    response_time_ms INTEGER,
    response_length INTEGER,
    cost_usd DECIMAL(10, 6),
    user_rating INTEGER,  -- 1-5
    ran_at TIMESTAMP
);
```

---

## Use Cases

1. **Model Selection** - Find best model for your use case
2. **Prompt Engineering** - Test prompt variations
3. **Parameter Tuning** - Optimize temperature, length, etc.
4. **Cost Optimization** - Find cheapest acceptable model
5. **Quality Assurance** - Ensure consistent quality
6. **Team Standards** - Establish evidence-based defaults
7. **Continuous Improvement** - Ongoing optimization

---

## Pros & Cons

### Pros
- Data-driven model selection
- Find optimal parameters
- Compare multiple variants simultaneously
- Statistical significance testing
- Cost vs quality tradeoffs
- Automated testing option
- Learn user preferences

### Cons
- Requires multiple API calls (costly)
- Manual rating can be tedious
- Small sample sizes may not be significant
- Takes time to accumulate data
- Subjective quality ratings
- May not generalize to all queries

---

**Created:** 2025-11-08
**Status:** Awaiting approval
**ROI:** Medium (optimizes settings but requires effort)
