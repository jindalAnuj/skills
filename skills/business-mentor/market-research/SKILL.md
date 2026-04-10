---
name: market-research
description: >-
  Conduct structured market research before committing to an idea. Use when validating
  assumptions, sizing a market, analyzing competitors, or understanding customer segments.
  Helps avoid building products nobody wants.
---

# Market Research

Validate your assumptions before building. This skill guides you through essential market research to avoid costly mistakes.

## When to Use

- After idea scores well in **idea-evaluator**
- Before writing any code
- When unsure about market size or competition
- When you can't clearly describe your ideal customer

## Research Phases

### Phase 1: Problem Validation (30 min)

**Goal:** Confirm the problem exists and people care.

```markdown
## Problem Validation

**Problem statement:** [One sentence describing the pain]

### Evidence Gathering

1. **Reddit/Forum Search**
   - Search: "[problem] site:reddit.com" 
   - Posts found: [count]
   - Engagement level: [high/medium/low]
   - Key complaints noted:
     - 
     - 

2. **Review Mining**
   - Look at 1-star reviews of competitors
   - Common complaints:
     - 
     - 

3. **Google Trends**
   - Search volume trend: [growing/stable/declining]
   - Related queries:
     - 
     - 

### Verdict
- [ ] Problem is real and people actively complain
- [ ] Problem exists but low engagement
- [ ] Problem may be fabricated/assumed
```

### Phase 2: Market Sizing (20 min)

**Goal:** Understand the revenue potential.

```markdown
## Market Sizing

### TAM/SAM/SOM Framework

**TAM (Total Addressable Market):**
- [Industry] market size: $___
- Source: [where you found this]

**SAM (Serviceable Addressable Market):**
- Your specific segment: $___
- Calculation: [TAM × segment %]

**SOM (Serviceable Obtainable Market):**
- Realistic 3-year capture: $___
- Calculation: [SAM × realistic market share %]

### Quick Validation

Answer: Can this market support $1M ARR?
- Total potential customers: ___
- Average price point: $___/month
- Needed customers for $83K MRR: ___
- Is this <1% of market? [ ] Yes [ ] No

**If No:** Market may be too small or price too low.
```

### Phase 3: Competitor Analysis (30 min)

**Goal:** Understand what exists and find gaps.

```markdown
## Competitor Analysis

### Direct Competitors

| Competitor | Pricing | Strengths | Weaknesses | Reviews |
|------------|---------|-----------|------------|---------|
| [Name 1] | $__/mo | | | ⭐___ |
| [Name 2] | $__/mo | | | ⭐___ |
| [Name 3] | $__/mo | | | ⭐___ |

### Indirect Competitors

What else solves this problem (even if poorly)?
- Manual workarounds:
- Spreadsheets/tools:
- Hiring people:

### Gap Analysis

What do competitors NOT do well?
1. 
2. 
3. 

Can you win on ONE of these gaps? [ ] Yes [ ] No

### Pricing Intelligence

- Lowest competitor price: $___
- Highest competitor price: $___
- Your target price: $___
- Justification for price:
```

### Phase 4: Customer Segmentation (20 min)

**Goal:** Define exactly who you're selling to.

```markdown
## Customer Segmentation

### Primary Segment

**Who:** [Job title / Role / Type of person]
**Where:** [Where do they hang out online/offline?]
**Budget:** [What do they typically pay for tools?]
**Decision:** [Do they decide alone or need approval?]

### Ideal Customer Profile (ICP)

```
Company size: [solo/small/medium/enterprise]
Industry: [specific vertical]
Tech savviness: [low/medium/high]
Current solution: [what they use today]
Trigger event: [what makes them search for solutions]
```

### Customer Acquisition Channels

Where can you reach this customer?
- [ ] Marketplace (which one?): ___
- [ ] SEO (what keywords?): ___
- [ ] Social (which platform?): ___
- [ ] Communities (which ones?): ___
- [ ] Paid ads (viable at what CAC?): $___

### Validation Questions

To confirm this segment:
1. Can you find 10 people matching this profile in 1 hour?
2. Can you reach them without spending money?
3. Would they take a 15-min call with you?
```

## Research Output Template

After completing all phases, summarize:

```markdown
# Market Research Summary: [Idea Name]

## Verdict: [GO / ITERATE / NO-GO]

### Key Findings

**Problem Validation:** [Strong/Moderate/Weak]
- Evidence: [1-2 sentences]

**Market Size:** $___M SAM
- Path to $1M: [describe]

**Competition:** [Crowded/Moderate/Blue Ocean]
- Differentiation angle: [1 sentence]

**Customer Clarity:** [Clear/Fuzzy]
- ICP: [1 sentence description]
- Best channel: [where to reach them]

### Critical Assumptions to Test

1. [Assumption that could kill the idea]
2. [Second assumption]

### Next Step

- [ ] Proceed to **monetization-mapper**
- [ ] Need more research on: ___
- [ ] Pivot idea based on findings
- [ ] Kill the idea
```

## Quick Research Hacks

### Finding Willingness to Pay

1. Search "[problem] software" + look at pricing pages
2. Check Product Hunt for similar products + see comments
3. Search Twitter/X for "[competitor] pricing" complaints
4. Look at job postings - what are companies hiring for that your tool replaces?

### Validating Without Building

1. Create landing page, run $50 in ads, measure signups
2. Post in relevant subreddit asking "would you pay for X?"
3. Find 5 potential customers, offer to solve problem manually
4. Pre-sell: "Building X, 50% off for early supporters"

## Related Skills

- Start with **idea-evaluator** before market research
- After validation, use **monetization-mapper** to design revenue model
- Use **marketing-strategy** to plan GTM based on research findings
