---
name: review-code-practices
description: Use when reviewing APIs for code smells, DRY/YAGNI/KISS violations, NestJS best practices, type safety, or error handling. Triggers include "review code quality", "find code smells", "check best practices", "NestJS audit", "type safety review", or requests to audit helper functions end-to-end.
---

# Review Code Practices (Quality Audit)

A comprehensive code review skill that audits every line of an API—from controller to helper function—for LLD violations, best practices, and production-readiness.

---

## Overview

**Core principle:** Leave no stone unturned. Trace every helper function, mapper, and service call to uncover hidden issues before they become production incidents.

This skill produces an **artifact-first** review document with actionable findings.

---

## When to Use

**Triggers:**
- ✅ Before deploying to production (final audit)
- ✅ After major refactoring (validation check)
- ✅ When debugging mysterious production bugs
- ✅ When performance degrades at scale
- ✅ When onboarding to unfamiliar code
- ✅ When auditing code from contractors/third-parties

**Don't Use When:**
- ❌ Simple line-level review (use PR review)
- ❌ Minor bug fixes (overkill)
- ❌ Code you just wrote (bias risk)

---

## Output Strategy: Artifact-First Approach

> [!IMPORTANT]
> **Always create artifacts FIRST** in the brain folder, then copy to codebase after user approval.

### Step 1: Create Artifact (Always)

```
<appDataDir>/brain/<conversation-id>/api-review.md
```

Use `IsArtifact: true` when writing to ensure visibility in Antigravity IDE.

### Step 2: Copy to Codebase (After Approval)

```
{module}/code-review/{api-name}-review.md
```

Only copy after user reviews and approves the artifact.

---

## Artifact-First Workflow

### Artifact Directory Structure

```
<appDataDir>/brain/<conversation-id>/
├── task.md                          # Track review progress
├── implementation_plan.md           # Document review scope & approach
├── api-review.md                    # Main review artifact
└── walkthrough.md                   # Final summary with proofs
```

### Workflow with task_boundary

**1. PLANNING Mode:**
- Create `implementation_plan.md` with:
  - API entry point and route
  - Functions to be traced
  - Review criteria to apply
- Use `notify_user` for approval before execution

**2. EXECUTION Mode:**
- Create `api-review.md` as structured artifact
- Update `task.md` checkboxes as review progresses:
  - `[/]` Tracing function calls
  - `[x]` Code Smells analysis
  - `[ ]` Database Misuse check
  - `[ ]` Scalability review
  - `[ ]` Findings documentation

**3. VERIFICATION Mode:**
- Create `walkthrough.md` with:
  - Summary metrics (Critical/Warning/Suggestion counts)
  - Prioritized action items
  - Links to generated review file

### Artifact Metadata

```markdown
---
ArtifactType: other
Summary: API code review for {API Name} with X critical, Y warnings, Z suggestions
---
```

### User Review Points

Use `notify_user` with `PathsToReview` at:
1. **After planning** - Confirm review scope and criteria
2. **After execution** - Review findings and prioritization
3. **Final review** - Request approval before copying to codebase

---

## Review Artifact Structure

```markdown
# API Review: {API Name}

## Summary
- **API Path:** {route}
- **Entry Point:** {orchestrator/service method}
- **Total Functions Reviewed:** {count}
- **Critical Issues:** {count}
- **Warnings:** {count}
- **Suggestions:** {count}

## Review Criteria Checklist
[x] Code Smells
[x] DRY/YAGNI/KISS Violations
[x] NestJS Best Practices
[x] Database Misuse
[x] Scalability Issues
[x] Null Safety & Type Safety
[x] Error Handling

## Findings

### 🔴 Critical (Must Fix)
### 🟡 Warning (Should Fix)
### 🟢 Suggestion (Nice to Have)

## Function Trace
[Complete call graph with findings per function]
```

---

## Review Criteria

### 1. Code Smells

| Smell | Indicator | Severity |
|-------|-----------|----------|
| **God Method** | Method > 200 lines | 🔴 Critical |
| **Deep Nesting** | `if` depth > 4 levels | 🔴 Critical |
| **Magic Strings** | Hardcoded values instead of enums | 🟡 Warning |
| **Dead Code** | Commented code, unused variables | 🟡 Warning |
| **Unclear Naming** | `data`, `temp`, `x`, `processData` | 🟡 Warning |
| **Long Parameter List** | > 5 parameters | 🟡 Warning |
| **Duplicate Code Blocks** | Same logic in multiple places | 🟡 Warning |
| **Primitive Obsession** | String IDs never validated as ObjectId | 🟡 Warning |
| **Feature Envy** | Method uses more from another class | 🟢 Suggestion |
| **Middle Man** | Class just delegates to another | 🟢 Suggestion |

### 2. DRY / YAGNI / KISS Violations

| Principle | Violation | Example |
|-----------|-----------|---------|
| **DRY** | Same code duplicated | Same query in 3 places |
| **DRY** | Similar code with minor diff | Same logic, different field names |
| **YAGNI** | Unused parameters passed around | `buildResponse(a, b, c, d, e)` only using `a`, `b` |
| **YAGNI** | Over-engineered abstractions | Strategy pattern for 2 simple cases |
| **YAGNI** | Future-proofing without need | Extra fields "just in case" |
| **KISS** | Overcomplicated logic | Nested ternaries, complex one-liners |
| **KISS** | Premature optimization | Caching single-use data |
| **KISS** | Excessive abstraction layers | 5 layers for simple CRUD |

### 3. NestJS Best Practices

| Category | Check | Violation Example |
|----------|-------|-------------------|
| **Layer Boundaries** | Controller → Orchestrator → Service → Repository | Controller calling Repository directly |
| **Dependency Injection** | Services injected via constructor | `new Service()` inside methods |
| **DTO Validation** | All inputs validated via class-validator | Manual `if (!x)` checks |
| **Error Handling** | NestJS exceptions thrown, not null returned | `return null` for not found |
| **Logging** | PpLoggerService used with context | `console.log()` or missing context |
| **Swagger** | All endpoints documented | Missing @ApiOperation, @ApiResponse |
| **Stateless Services** | No instance state in services | `this.currentUser` stored in service |
| **Type Safety** | No `any` types | `any` used for laziness |

### 4. Database Misuse

| Issue | Indicator | Impact |
|-------|-----------|--------|
| **N+1 Query** | Loop with await inside | Exponential DB calls |
| **Missing Index** | Query on non-indexed field | Slow queries at scale |
| **Unbounded Query** | `.find({})` without limit | Memory explosion |
| **Unnecessary Fields** | Fetch full doc, use 2 fields | Wasted bandwidth |
| **Missing Projection** | No `project` in query | Returns all fields |
| **Repeated Queries** | Same data fetched multiple times | Unnecessary DB load |
| **Cross-Boundary Access** | Orchestrator calling repository | Layer violation |
| **Missing Transaction** | Multi-doc write without session | Data inconsistency |
| **Cache Ignored** | Repeated calls, no @useCache | Redundant DB hits |

### 5. Scalability Issues

| Issue | Pattern | Risk |
|-------|---------|------|
| **Synchronous in Loop** | `for (const x of items) await f(x)` | Linear slowdown |
| **Unbatched External Calls** | Individual API calls in loop | Rate limits, timeouts |
| **Memory Accumulation** | Large array built in memory | OOM at scale |
| **Missing Pagination** | No limit/skip in list APIs | Response size explosion |
| **CPU-Bound in Request** | Heavy computation inline | Request timeout |
| **Missing Circuit Breaker** | External API without timeout | Cascading failure |
| **Global State** | Static mutable variables | Race conditions |
| **Missing Rate Limiting** | Open endpoints | DDoS vulnerability |

### 6. Null Safety & Type Safety

| Issue | Pattern | Fix |
|-------|---------|-----|
| **Null Pointer** | `user.profile.name` without check | Optional chaining `user?.profile?.name` |
| **Missing Null Check** | Return value not checked before use | Guard clause or throw |
| **Implicit Any** | Parameter without type annotation | Add explicit types |
| **Type Assertion** | `as any` or `as unknown` | Proper type guards |
| **Non-Nullable Assumption** | Assuming DB always returns data | Add null check or `??` |
| **Array Access** | `arr[0]` without length check | Check `arr?.length` first |
| **Optional Property** | Accessing `.foo.bar` on optional | Use `?.` or null coalescing |
| **Falsy Confusion** | `if (value)` when 0/"" is valid | Explicit `!== null && !== undefined` |

### 7. Error Handling

| Issue | Pattern | Fix |
|-------|---------|-----|
| **Silent Catch** | `try {} catch (e) {}` (empty) | Log and rethrow or handle |
| **Generic Error** | `throw new Error('Something wrong')` | Use specific NestJS exceptions |
| **Missing Context** | Error without identifiers | Include IDs in error message |
| **Swallowed Promise** | No `.catch()` on promise | `await` or handle rejection |
| **Error as Flow Control** | Try-catch for normal logic | Use conditionals |
| **Unlogged Error** | Exception without logging | Log before throwing |
| **Inconsistent Error Format** | Different error shapes | Use standardized DTO |

---

## Review Workflow

```
1. ENTRY POINT
   └── Start from controller method
       └── Trace to orchestrator
           └── For each service/mapper/util called:
               └── Review against all criteria
                   └── Document findings

2. FUNCTION TRACE FORMAT

   ┌─ getCategories (Controller) ────────────────────────┐
   │  Route: GET /categories                             │
   │  File: categories.controller.ts:45                  │
   │  Issues: None                                       │
   └─────────────────────────────────────────────────────┘
           │
           ▼
   ┌─ getCategoriesByProgram (Orchestrator) ─────────────┐
   │  File: scholarship-landing-page.orchestrator.ts:180 │
   │  Lines: 180-220 (40 lines)                          │
   │  Issues:                                            │
   │    🟡 Line 192: Type cast to `any` - use interface  │
   │    🟡 Line 199: Missing null check on result        │
   └─────────────────────────────────────────────────────┘
           │
           ├───────────────────┐
           ▼                   ▼
   ┌─ getCategoriesByProgramId │ findPhasesByCategoryIdsAndLevel ─┐
   │  ...                      │  ...                             │
```

---

## Quick Reference: Review Commands

| Step | Action |
|------|--------|
| 1. Identify Entry | Find controller route and method |
| 2. Trace Calls | Map all functions called (recursively) |
| 3. Line-by-Line | Check each function against criteria |
| 4. Document | Create finding with file:line, severity, fix |
| 5. Prioritize | Sort by severity (Critical → Warning → Suggestion) |
| 6. Output | Create artifact in brain folder FIRST, copy to `{module}/code-review/` after approval |

---

## Finding Template

For each issue found, document:

```markdown
### Finding: {Short Title}

| Attribute | Value |
|-----------|-------|
| **Severity** | 🔴 Critical / 🟡 Warning / 🟢 Suggestion |
| **Category** | {Code Smell / DRY / Database / etc.} |
| **Location** | `{file}:{line}` |
| **Code** | ```typescript\n{relevant code}\n``` |
| **Issue** | {What's wrong} |
| **Risk** | {What could happen} |
| **Fix** | {How to fix} |
```

---

## Common Findings Shortcuts

### Quick Detectors

| Pattern to Grep | Likely Issue |
|-----------------|--------------|
| `as any` | Type Safety |
| `console.log` | Logging |
| `// TODO` | Incomplete Code |
| `catch (e) {}` | Silent Error |
| `.find({})` | Unbounded Query |
| `for.*await` | N+1 or Sequential |
| `return null` | Error Handling |
| `=== 'string'` | Magic String |
| `[0]` | Array Bounds |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing directly to codebase | Always create artifact in brain folder FIRST |
| Reviewing only top-level code | Trace ALL helper functions recursively |
| Missing severity classification | Every finding MUST have 🔴/🟡/🟢 |
| No file:line references | Include exact location for every finding |
| Generic "fix this" recommendations | Provide specific, actionable fixes |
| Skipping database query analysis | Check every query for N+1 and projections |
| Ignoring error paths | Review catch blocks and error handling |

---

## Checklist Before Completion

- [ ] All helper functions traced and reviewed
- [ ] All service calls traced to repository level
- [ ] All mappers and transformers reviewed
- [ ] All external API calls reviewed
- [ ] All database queries checked for N+1
- [ ] All error paths validated
- [ ] All null dereferences checked
- [ ] All type casts documented
- [ ] Findings prioritized by severity
- [ ] Artifact created in brain folder first
- [ ] User approval obtained before codebase copy

---

## Example Usage

**Prompt:** "Review the getLandingPageDetails API for code quality"

**Output (Artifact-First):**
1. `<appDataDir>/brain/<conversation-id>/api-review.md` - Artifact created first
2. User reviews findings and prioritization
3. `scholarship-landing-page/code-review/get-landing-page-details-review.md` - Copied to codebase after approval
