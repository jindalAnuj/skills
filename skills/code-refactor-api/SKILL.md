---
name: code-refactor-api
description: Use when refactoring, cleaning up, or improving an existing API while preserving external behavior. Triggers include requests to improve code quality, reduce complexity, extract utilities, or make controlled logic changes without breaking existing functionality.
---

# API Refactoring Skill (Behavior-Preserving)

Refactor existing APIs while guaranteeing external behavior remains unchanged.

---

## Phase 1: Contract & Behavior Lock

**Freeze external behavior before ANY code changes.**

| Lock These | Status |
|------------|--------|
| API request shape | 🔒 Immutable |
| Response shape | 🔒 Immutable |
| Side effects | 🔒 Immutable |

### Document Current Behavior

Before refactoring, identify and document:
- ✅ Inputs (query params, body, headers)
- ✅ Outputs (response structure, status codes)
- ✅ Edge cases (null handling, empty arrays, error states)
- ✅ Implicit behavior (default values, side effects)

> [!CAUTION]
> **No refactoring before behavior is fully understood**

---

## Phase 2: Codebase Analysis

### Map Responsibilities

| Layer | Identify |
|-------|----------|
| Controller | HTTP routing, guards, validation |
| Orchestrator | Business logic, workflow coordination |
| Utils | Pure functions, helpers (strategy candidates) |
| Services | Data operations, external APIs |

### Identify Code Smells

| Smell | Indicator |
|-------|-----------|
| Long functions | Methods > 100 lines |
| Deep nesting | `if` depth > 3 levels |
| Magic strings | Hardcoded values instead of enums |
| Mixed responsibilities | DB + logic + transforms in one method |
| Weak typing | Missing DTOs, `any` types |

---

## Phase 3: Refactor Strategy Selection

### Choose Refactor Scope

| Scope | Description | Approval Required |
|-------|-------------|-------------------|
| **Structural only** | File organization, extraction | ❌ No |
| **Typing improvements** | DTOs, enums, return types | ❌ No |
| **Logic change** | Behavior modifications | ✅ **Yes** |

### Confirm if Changes Include

> [!WARNING]
> Explicitly state what **will** and **will not** change before proceeding:
> - Schema changes
> - DTO changes  
> - Logic changes

---

## Phase 4: Refactor Execution (Strict Order)

Execute in this **exact order**:

### Step 1: Improve Typing
```diff
- function process(data: any) { ... }
+ function process(data: ProcessRequestDto): ProcessResponseDto { ... }
```
- Add DTOs for request/response
- Replace magic strings with enums
- Add explicit return types

### Step 2: Extract Utilities
Move to `util/` folder:
- Pure functions (no DB access)
- Repeated logic across methods
- Transformation helpers

### Step 3: Break Down Functions
Each function should have:
- ✅ One responsibility
- ✅ Intention-revealing name
- ✅ < 50 lines preferred

### Step 4: Introduce Strategies (if needed)
Replace complex conditionals with strategy pattern:
```typescript
// Before: 100+ line if-else
if (type === 'NSAT') { /* 50 lines */ }
else if (type === 'SAT') { /* 50 lines */ }

// After: Strategy pattern
const strategy = this.strategyFactory.create(type);
return strategy.execute(params);
```

### Step 5: Re-validate Layer Boundaries

| Layer | Rule |
|-------|------|
| Controller | Thin - routing only, injects Orchestrator |
| Orchestrator | Coordinates services, contains business logic |
| Services | Stateless, data operations only |

---

## Phase 5: Minimal Logic Change (Optional)

> [!IMPORTANT]
> Only proceed with user confirmation

### Schema/DTO Changes
- Add fields cautiously
- Preserve backward compatibility
- Update DTO validation

### Logic Updates
- Apply only targeted changes
- Avoid rewriting unrelated logic

### Impact Review
Ensure:
- Old flows still work
- New behavior is isolated

---

## Phase 6: Safety Verification

### Behavior Parity Check

| Check | Status |
|-------|--------|
| Old vs new outputs match | ⬜ |
| Edge cases handled identically | ⬜ |
| Error responses unchanged | ⬜ |

### Code Quality Audit

| Metric | Target |
|--------|--------|
| Readability | Improved |
| Responsibilities | Clearer separation |
| Coupling | No new hidden dependencies |

### Document Changes
Explain:
- What improved
- Why structure is better
- What was intentionally NOT changed

---

## Phase 7: Final Gate

### Rule Compliance Checklist

- [ ] DTO-first validation (no raw `any` inputs)
- [ ] Enum usage (no magic strings)
- [ ] Utils extracted (pure functions in `util/`)
- [ ] Orchestrator discipline (no DB calls, only service calls)
- [ ] Build passes: `npm run build`

### User Confirmation

Highlight any:
- ⚠️ Risks
- ⚖️ Trade-offs
- 🔜 Deferred improvements

---

## Quick Reference: Refactoring Order

```
1. Lock Behavior → 2. Analyze → 3. Select Scope → 4. Execute → 5. Verify → 6. Confirm
```

| Step | Description |
|------|-------------|
| Lock | Document inputs, outputs, edge cases |
| Analyze | Map layers, identify smells |
| Scope | Structural vs logic changes |
| Execute | Types → Utils → Functions → Strategies → Layers |
| Verify | Behavior parity, quality audit |
| Confirm | Compliance check, user sign-off |
