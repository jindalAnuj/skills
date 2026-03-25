# Test Case Mapping: [Old API Name] → [New API Name]

> **Generated:** [DATE]  
> **OLD API:** `[/path/to/old-qa-checklist.md]`  
> **NEW API:** `[/path/to/new-qa-checklist.md]`

---

## Summary Metrics

| Metric | Count | Status |
|--------|-------|--------|
| **OLD Test Cases** | X | - |
| **NEW Test Cases** | X | - |
| **Accepted** | X | ✅ All Approved |
| **Dropped** | X | ⏳ X Pending Review |
| **Added** | X | ✅ All Approved |
| **Helper Methods Identified** | X | 📋 TODO |

---

## API Comparison

| Aspect | OLD API | NEW API |
|--------|---------|---------|
| **Endpoint** | `GET /old/path` | `GET /new/path` |
| **Controller** | `old.controller.ts` | `new.controller.ts` |
| **Service/Orchestrator** | `old.service.ts` | `new.orchestrator.ts` |
| **Auth Required** | No/Yes | No/Yes |
| **Key Differences** | - | - |

---

## Normalized Use Cases

> All test cases from both files converted to common language format.

### Category: [CATEGORY_NAME] (e.g., VALIDATION, BUSINESS_LOGIC)

| UC-ID | Description | OLD Source | NEW Source | Status |
|-------|-------------|------------|------------|--------|
| UC-001 | Description of use case | UC-01.1 | TC-05 | ✅ |
| UC-002 | Description of use case | UC-02.1 | - | ❌ |
| UC-003 | Description of use case | - | TC-10 | ➕ |

---

## ✅ ACCEPTED Test Cases

> Tests that exist in BOTH old and new APIs - Automatically approved.

| Status | OLD ID | NEW ID | Description | Modifications |
|--------|--------|--------|-------------|---------------|
| ✅ APPROVED | UC-XX | TC-XX | Description | Any changes needed |
| ✅ APPROVED | UC-XX | TC-XX | Description | None |

**Total Accepted:** X cases

---

## ❌ DROPPED Test Cases

> Tests that exist in OLD only - Require classification.

| Status | OLD ID | Description | Drop Reason | Notes |
|--------|--------|-------------|-------------|-------|
| ✅ CLASSIFIED | UC-XX | Description | `CODE_SUPPORT` | Feature removed |
| ✅ CLASSIFIED | UC-XX | Description | `EXPECTED_BEHAVIOR` | Behavior changed by design |
| ⏳ PENDING | UC-XX | Description | `[ ] CODE_SUPPORT` `[ ] EXPECTED_BEHAVIOR` | Needs review |

### Drop Reason Legend

- **CODE_SUPPORT**: The code no longer supports this scenario (feature removed, input changed fundamentally)
- **EXPECTED_BEHAVIOR**: The behavior changed intentionally (business rule update, design decision)

**Total Dropped:** X cases (Y pending classification)

---

## ➕ ADDED Test Cases

> Tests that exist in NEW only - Automatically approved.

| Status | NEW ID | Description | Reason Added |
|--------|--------|-------------|--------------|
| ✅ APPROVED | TC-XX | Description | New validation rule |
| ✅ APPROVED | TC-XX | Description | New feature |

**Total Added:** X cases

---

## 🔬 Deep Dive: Helper Method Analysis

### Level 2: Service/Orchestrator Methods

| Method | File | Coverage | Tests Needed | Priority |
|--------|------|----------|--------------|----------|
| `methodName` | `file.ts` | ⚠️ PARTIAL | 3 | P1 |
| `methodName` | `file.ts` | ❌ MISSING | 5 | P1 |
| `methodName` | `file.ts` | ✅ COVERED | 0 | - |

### Level 3: Internal Helpers

| Helper | Parent Method | Coverage | Scenarios to Test |
|--------|---------------|----------|-------------------|
| `helperName` | `parentMethod` | ❌ MISSING | Scenario 1, Scenario 2 |
| `helperName` | `parentMethod` | ⏳ TODO | Scenario 1 |

---

## 📋 Unit Test TODO Planner

### Summary

| Level | Methods | Total Tests | Implemented | Pending |
|-------|---------|-------------|-------------|---------|
| Level 1 (API) | X | X | 0 | X |
| Level 2 (Services) | X | X | 0 | X |
| Level 3 (Helpers) | X | X | 0 | X |
| **Total** | **X** | **X** | **0** | **X** |

---

### Level 1: Main API Method

#### `[mainMethodName]` (Orchestrator/Controller) - X tests
- [ ] Happy path with valid inputs
- [ ] Entity not found → NotFoundException
- [ ] Validation error → BadRequestException
- [ ] [Add more scenarios...]

---

### Level 2: Service Methods

#### `[serviceMethod1]` (ServiceName) - X tests
- [ ] Scenario 1
- [ ] Scenario 2
- [ ] Scenario 3
- [ ] [Add more scenarios...]

#### `[serviceMethod2]` (ServiceName) - X tests
- [ ] Scenario 1
- [ ] Scenario 2
- [ ] [Add more scenarios...]

---

### Level 3: Internal Helpers (Private Methods)

#### `[helperMethod1]` - X tests
- [ ] Scenario 1
- [ ] Scenario 2
- [ ] Scenario 3
- [ ] [Add more scenarios...]

#### `[helperMethod2]` - X tests
- [ ] Scenario 1
- [ ] Scenario 2
- [ ] [Add more scenarios...]

#### `[helperMethod3]` - X tests
- [ ] Scenario 1
- [ ] Scenario 2
- [ ] [Add more scenarios...]

---

## Implementation Checklist

### Pre-Implementation
- [ ] All DROPPED cases classified with reason
- [ ] All ACCEPTED cases reviewed for modifications
- [ ] ALL helper methods identified at every level

### Test Implementation
- [ ] Create test file: `<module>/tests/<file>.spec.ts`
- [ ] Level 1 API tests implemented
- [ ] Level 2 Service tests implemented
- [ ] Level 3 Helper tests implemented

### Verification
- [ ] All tests passing: `npm run test -- <path>`
- [ ] Coverage reviewed

---

## Run Tests

```bash
npm run test -- <path-to-spec-file>
npm run test:cov -- <path-to-spec-file>
```
