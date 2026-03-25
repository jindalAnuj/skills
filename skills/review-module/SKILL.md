---
name: review-module
description: Use when reviewing entire modules or folders for architectural violations, layer boundary issues, cross-cutting concerns, or structural health. Triggers include "review module", "module audit", "folder review", "check module health", "architecture review", or requests to assess overall module quality and structure.
---

# Module Review Skill (Holistic Architecture Audit)

A comprehensive code review skill that audits entire modules or folders—from structure to cross-cutting concerns—for architectural violations, layer boundary issues, and production-readiness.

---

## Overview

**Core principle:** Evaluate the forest, not just the trees. Assess the overall health of a module's architecture, dependencies, and adherence to established patterns before diving into line-by-line code review.

This skill produces an **artifact-first** review document with actionable findings.

---

## When to Use

**Triggers:**
- ✅ Before major refactoring (understand current state)
- ✅ Onboarding to unfamiliar module (architecture understanding)
- ✅ After inheriting legacy code (health assessment)
- ✅ Periodic architecture health checks
- ✅ Before splitting or merging modules
- ✅ When module complexity is growing uncontrollably
- ✅ When debugging cross-module issues

**Don't Use When:**
- ❌ Reviewing a single API (use `api-review` skill)
- ❌ Quick bug fixes in well-understood modules
- ❌ Code you just created (too fresh, use api-review instead)
- ❌ External dependencies or node_modules

---

## Output Strategy: Artifact-First Approach

> [!IMPORTANT]
> **Always create artifacts FIRST** in the brain folder, then copy to codebase after user approval.

### Step 1: Create Artifact (Always)

```
<appDataDir>/brain/<conversation-id>/module-review.md
```

Use `IsArtifact: true` when writing to ensure visibility in Antigravity IDE.

### Step 2: Copy to Codebase (After Approval)

```
{module}/code-review/module-review.md
```

Only copy after user reviews and approves the artifact.

---

## Artifact-First Workflow

### Artifact Directory Structure

```
<appDataDir>/brain/<conversation-id>/
├── task.md                          # Track review progress
├── implementation_plan.md           # Document review scope & approach
├── module-review.md                 # Main review artifact
└── walkthrough.md                   # Final summary with proofs
```

### Workflow with task_boundary

**1. PLANNING Mode:**
- Create `implementation_plan.md` with:
  - Module/folder path to review
  - Review criteria to apply
  - Expected deliverables
- Use `notify_user` for approval before execution

**2. EXECUTION Mode:**
- Create `module-review.md` as structured artifact
- Update `task.md` checkboxes as review progresses:
  - `[/]` Module structure analysis
  - `[x]` Layer boundaries check
  - `[ ]` Dependency health
  - `[ ]` Cross-cutting concerns
  - `[ ]` Code metrics
  - `[ ]` Findings documentation

**3. VERIFICATION Mode:**
- Create `walkthrough.md` with:
  - Summary metrics (Critical/Warning/Suggestion counts)
  - Architecture health score
  - Prioritized action items
  - Links to generated review file

### Artifact Metadata

```markdown
---
ArtifactType: other
Summary: Module review for {Module Name} with X critical, Y warnings, Z suggestions. Health Score: X/10
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
# Module Review: {Module Name}

## Summary
- **Module Path:** {path}
- **Total Files:** {count}
- **Total Lines of Code:** {approx}
- **Architecture Health Score:** {X}/10
- **Critical Issues:** {count}
- **Warnings:** {count}
- **Suggestions:** {count}

## Review Criteria Checklist
[x] Module Structure
[x] Layer Boundaries
[x] Dependency Health
[x] Cross-Cutting Concerns
[x] Code Metrics & Complexity
[x] Naming Conventions
[x] Documentation Coverage
[x] Separation of Concerns
[x] Function vs Injectable Class Patterns

## Module Structure Overview
[Directory tree with file counts and annotations]

## Findings

### 🔴 Critical (Must Fix)
### 🟡 Warning (Should Fix)
### 🟢 Suggestion (Nice to Have)

## Dependency Graph
[Visual representation of module dependencies]

## Recommendations
[Prioritized action items with effort estimates]
```

---

## Review Criteria

### 1. Module Structure

| Check | Expected | Violation Indicator |
|-------|----------|---------------------|
| **Directory Layout** | Follows standard module structure | Missing folders (dto/, entities/, controllers/) |
| **Single Responsibility** | Module does ONE thing well | Multiple unrelated features in same module |
| **File Organization** | Related files grouped logically | Scattered files, no clear organization |
| **Naming Convention** | `kebab-case` files, `PascalCase` classes | Mixed naming styles |
| **Index Exports** | Clean barrel exports | Missing or cluttered index.ts |
| **Module Definition** | Proper imports/exports/providers | Circular dependencies, missing exports |

### 2. Layer Boundaries

| Layer | Allowed Dependencies | Violation |
|-------|---------------------|-----------|
| **Controller** | Orchestrator only | Controller → Repository (skip layers) |
| **Orchestrator** | Services, Strategies, Mappers | Orchestrator → Repository directly |
| **Service** | Repository, External APIs | Service → Controller (reverse dependency) |
| **Repository** | DatabaseService only | Repository → Service (circular) |
| **Mapper** | None (pure functions) | Mapper with DB calls |

**Anti-Patterns to Detect:**
- Controller calling Repository directly
- Service injecting another module's Repository
- Orchestrator with direct database queries
- Circular dependencies between layers

### 3. Dependency Health

| Issue | Indicator | Severity |
|-------|-----------|----------|
| **Circular Dependencies** | Module A → Module B → Module A | 🔴 Critical |
| **God Module** | Module imported by 10+ others | 🟡 Warning |
| **Orphan Module** | Module with no dependents | 🟡 Warning |
| **Tight Coupling** | Direct class imports instead of interfaces | 🟡 Warning |
| **Missing Abstraction** | Same service duplicated in multiple modules | 🟡 Warning |
| **Leaky Abstraction** | Internal details exposed in exports | 🟢 Suggestion |
| **Over-Injection** | Constructor with 10+ dependencies | 🔴 Critical |

### 4. Cross-Cutting Concerns

| Concern | Check | Violation |
|---------|-------|-----------|
| **Error Handling** | Consistent across module | Mixed patterns (return null vs throw) |
| **Logging** | PpLoggerService with context | console.log or missing context |
| **Validation** | class-validator on all DTOs | Manual if checks instead |
| **Swagger** | All endpoints documented | Missing @ApiOperation, @ApiResponse |
| **Guards** | Proper authentication/authorization | Missing guards on protected routes |
| **Transactions** | Multi-doc writes use sessions | Updates without transaction safety |
| **Caching** | Dedicated cache class per service module | Missing cache file, cache logic in service |
| **Cache Pattern** | `{service-name}.cache.ts` with CacheService | No cache class, inline caching |

### 5. Code Metrics & Complexity

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| **File Count** | <30 files | 30-50 files | >50 files |
| **Total LOC** | <3000 lines | 3000-5000 lines | >5000 lines |
| **Largest File** | <300 lines | 300-500 lines | >500 lines |
| **Deepest Nesting** | ≤3 levels | 4 levels | >4 levels |
| **Max Method Length** | <50 lines | 50-100 lines | >100 lines |
| **Constructor Params** | ≤5 | 6-8 | >8 |
| **Cyclomatic Complexity** | <10 per method | 10-15 | >15 |

### 6. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| **Files** | `kebab-case` | `user-registration.service.ts` |
| **Classes** | `PascalCase` | `UserRegistrationService` |
| **Variables/Methods** | `camelCase` | `getUserById`, `userId` |
| **Enums** | `PascalCase` + `Enum` suffix | `UserStatusEnum` |
| **Interfaces** | `I` prefix or descriptive | `IUserRepository`, `CreateUserDto` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |

### 7. Documentation Coverage

| Check | Expected | Missing |
|-------|----------|---------|
| **README** | Module overview, usage examples | No README.md |
| **JSDoc** | Public methods documented | Missing @param, @returns |
| **Swagger** | All DTOs with @ApiProperty | Missing descriptions |
| **Inline Comments** | Complex logic explained | Magic numbers, unclear algorithms |
| **CHANGELOG** | Major changes tracked | No history |

### 8. Separation of Concerns

| Issue | Indicator | Severity |
|-------|-----------|----------|
| **Mixed Responsibilities** | Single class handles DB + business logic + HTTP | 🔴 Critical |
| **God Class** | Class with 10+ public methods doing unrelated things | 🔴 Critical |
| **Utility Bloat** | Utils file with 500+ lines of mixed helpers | 🟡 Warning |
| **Controller Logic** | Business logic in controller instead of orchestrator | 🟡 Warning |
| **Repository with Logic** | Repository containing business rules | 🟡 Warning |
| **Mapper with Side Effects** | Mapper making DB calls or API requests | 🔴 Critical |
| **Service Doing Orchestration** | Service coordinating multiple services | 🟡 Warning |
| **Orchestrator Doing Data Access** | Orchestrator with direct DB queries | 🔴 Critical |
| **DTO with Logic** | DTO containing business methods | 🟢 Suggestion |
| **Mixed Transform + Fetch** | Same method fetching data AND transforming it | 🟡 Warning |

**Single Responsibility Checks:**

| Component | Should Do | Should NOT Do |
|-----------|-----------|---------------|
| **Controller** | Route, validate input, call orchestrator | Business logic, DB access, transformations |
| **Orchestrator** | Coordinate services, apply business rules | Direct DB queries, HTTP handling |
| **Service** | Single domain operations, stateless helpers | Cross-domain coordination, multiple repos |
| **Repository** | CRUD operations, query building | Business logic, validation |
| **Mapper** | Pure data transformation | API calls, DB access, side effects |
| **Utils** | Pure helper functions, shared utilities | State, business rules, DB access |

**Anti-Patterns to Detect:**
- "Fat" controllers with business logic
- "Smart" repositories with business rules
- Orchestrators directly calling `this.db.xyz`
- Mappers that fetch additional data
- Utils that import services or repositories
- Services that inject multiple unrelated services
- Missing cache file in service modules (should have `{name}.cache.ts`)
- Utils/mappers/transformers embedded in orchestrators (should be separate files)
- Filename typos (e.g., `scholarsip` → `scholarship`)
- **Wrapper methods** that just delegate to utils (call utils directly instead)

### 9. Function vs Injectable Class (NestJS Pattern)

**When to use standalone functions (utils):**

| Use Case | Example |
|----------|---------|
| **Pure functions** - no side effects, no dependencies | `parseRequestHeaders()`, `isEmptyTestDetails()` |
| **Stateless transformations** | Date formatting, string manipulation |
| **Simple validators** | `isDateExpired()`, `checkIfRotationPossible()` |
| **Mappers** | Entity → DTO conversions |

```typescript
// ✅ GOOD - Pure function, no dependencies
export function parseRequestHeaders(headers: TestRequestHeaders): ParsedTestHeaders {
  return {
    deviceId: headers?.Randomid || headers?.randomid,
    ipAddress: headers?.['X-Real-Ip'] || headers?.['x-real-ip'],
  };
}

// ✅ GOOD - Call utils directly in orchestrator
const parsedHeaders = parseRequestHeaders(userHeaders);
```

**When to use Injectable classes (services):**

| Use Case | Example |
|----------|---------|
| **Has dependencies** - needs other services | Database, HTTP, Logger |
| **Needs state** | Caching, configuration |
| **Requires lifecycle hooks** | `onModuleInit`, `onModuleDestroy` |
| **Cross-module coordination** | Orchestrators |

```typescript
// ✅ GOOD - Has dependencies, needs DI
@Injectable()
export class TestCategoryService {
  constructor(
    private readonly dbService: DatabaseService,
    private readonly logger: PpLoggerService,
  ) {}
}
```

**Anti-pattern: Wrapper methods (AVOID)**

```typescript
// ❌ BAD - Unnecessary wrapper
private isEmptyTestDetails(testDetails): boolean {
  return isEmptyTestDetails(testDetails);  // just calls util
}

// ❌ BAD - Calling wrapper instead of util directly
if (this.isEmptyTestDetails(mockTestDetails)) { ... }

// ✅ GOOD - Call util directly
if (isEmptyTestDetails(mockTestDetails)) { ... }
```

**Quick Decision Tree:**

```
Does this function need injected dependencies?
├─ YES → Use @Injectable() class
└─ NO → Is it a pure transformation/validation?
        ├─ YES → Use standalone function in utils
        └─ NO → Consider if it should be split
```

---

## Review Workflow

```
1. STRUCTURE ANALYSIS
   └── List all files in module
       └── Categorize by type (controller, service, etc.)
           └── Check against expected structure
               └── Document deviations

2. DEPENDENCY MAPPING
   └── Extract all imports/exports
       └── Build dependency graph
           └── Identify violations
               └── Document circular deps

3. LAYER BOUNDARY CHECK
   └── For each file:
       └── Verify injection patterns
           └── Check call directions
               └── Document violations

4. CROSS-CUTTING SCAN
   └── Error handling patterns
   └── Logging usage
   └── Validation coverage
   └── Documentation completeness

5. METRICS CALCULATION
   └── File counts
   └── Line counts
   └── Complexity estimates
   └── Health score
```

---

## Quick Reference: Review Commands

| Step | Action |
|------|--------|
| 1. List Structure | `find_by_name` to get all files in module |
| 2. Map Dependencies | `grep_search` for imports and injections |
| 3. Check Layers | `view_file_outline` for each major file |
| 4. Scan Patterns | `grep_search` for error handling, logging |
| 5. Calculate Metrics | Count files, lines, complexity |
| 6. Document Findings | Create artifact with severity |
| 7. Prioritize | Sort by severity (Critical → Warning → Suggestion) |
| 8. Output | Create artifact in brain folder FIRST |

---

## Finding Template

For each issue found, document:

```markdown
### Finding: {Short Title}

| Attribute | Value |
|-----------|-------|
| **Severity** | 🔴 Critical / 🟡 Warning / 🟢 Suggestion |
| **Category** | {Structure / Layer Boundary / Dependency / etc.} |
| **Location** | `{file or folder}` |
| **Issue** | {What's wrong} |
| **Impact** | {Why it matters} |
| **Risk** | {What could happen at scale} |
| **Fix** | {How to fix, with effort estimate} |
```

---

## Health Score Calculation

| Category | Weight | Score Range |
|----------|--------|-------------|
| **Layer Boundaries** | 20% | 0-10 |
| **Separation of Concerns** | 20% | 0-10 |
| **Dependency Health** | 15% | 0-10 |
| **Code Metrics** | 15% | 0-10 |
| **Cross-Cutting** | 15% | 0-10 |
| **Structure** | 10% | 0-10 |
| **Documentation** | 5% | 0-10 |

**Overall = Weighted Average**

| Score | Grade | Action |
|-------|-------|--------|
| 8-10 | 🟢 Healthy | Maintain |
| 6-7 | 🟡 Needs Attention | Plan improvements |
| 4-5 | 🟠 At Risk | Prioritize refactoring |
| 0-3 | 🔴 Critical | Immediate action required |

---

## Quick Pattern Detectors

| Pattern to Grep | Likely Issue |
|-----------------|--------------|
| `this.db.` in orchestrator | Layer boundary violation |
| `@InjectModel` in service | Should use repository |
| `import.*Repository.*from '../` | Cross-module repo access |
| `console.log` | Logging violation |
| `as any` | Type safety issue |
| `catch (e) {}` | Silent error swallowing |
| `// TODO` | Incomplete implementation |
| `extends BaseService` missing | Inconsistent patterns |
| `constructor(.*,.*,.*,.*,.*,.*,.*,` | Over-injection (8+) |
| No `.cache.ts` file in service | Missing cache layer |
| `Utils` class > 200 LOC | Utility bloat, needs splitting |
| Typos in filenames | Professionalism/searchability issue |
| `DatabaseService` in orchestrator | Layer violation (should use service) |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing directly to codebase | Always create artifact in brain folder FIRST |
| Reviewing only high-level structure | Also check cross-cutting concerns |
| Missing severity classification | Every finding MUST have 🔴/🟡/🟢 |
| No health score | Always calculate and report overall health |
| Generic recommendations | Provide specific, actionable fixes with effort |
| Ignoring dependency graph | Visualize and document module dependencies |
| Skipping documentation check | Review README, Swagger, JSDoc coverage |

---

## Checklist Before Completion

- [ ] All files in module cataloged
- [ ] Directory structure validated against standard
- [ ] Layer boundaries verified for all major classes
- [ ] Separation of concerns validated
- [ ] Dependency graph constructed
- [ ] Circular dependencies identified
- [ ] Cross-cutting concerns audited
- [ ] Code metrics calculated
- [ ] Health score computed
- [ ] Findings prioritized by severity
- [ ] Recommendations include effort estimates
- [ ] Artifact created in brain folder first
- [ ] User approval obtained before codebase copy

---

## Example Usage

**Prompt:** "Review the scholarship module for architecture health"

**Output (Artifact-First):**
1. `<appDataDir>/brain/<conversation-id>/module-review.md` - Artifact created first
2. User reviews findings and health score
3. `scholarship/code-review/module-review.md` - Copied to codebase after approval

---

## Comparison: API Review vs Module Review

| Aspect | API Review | Module Review |
|--------|------------|---------------|
| **Scope** | Single API endpoint | Entire module/folder |
| **Focus** | Line-by-line code quality | Architecture & structure |
| **Depth** | Deep (every helper function) | Broad (all files, patterns) |
| **Output** | Function trace with findings | Health score with recommendations |
| **When** | Before deploying specific API | Before refactoring or onboarding |
| **Time** | 30-60 min | 1-2 hours |
