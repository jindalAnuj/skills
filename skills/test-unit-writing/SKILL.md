---
name: test-unit-writing
description: Use when writing or updating Jest/TypeScript unit test CODE (.spec.ts files). Triggers include "write unit tests", "create test file", "add test coverage", "update tests", "mock dependencies", "Cannot spy on property", "mock not working", or requests to generate test code for controllers/services/orchestrators/repositories. Do NOT use for plain English QA checklists - use qa-checklist skill instead.
---

# Writing Unit Tests

Write comprehensive Jest/TypeScript unit tests for NestJS APIs following established patterns.

**Core principle:** Test behavior, not implementation. Mock dependencies, verify interactions.

---

## When to Use

✅ **Use for:**
- Writing `.spec.ts` test files
- Mocking repositories, services, external APIs
- Testing controllers, orchestrators, services, repositories
- Adding test coverage to existing code

❌ **Do NOT use for:**
- Plain English QA checklists → use `qa-checklist` skill
- API test design/planning → use `api-test-design` skill
- Integration tests with real databases

---

## Quick Reference

| Layer | Focus | Mock What |
|-------|-------|-----------|
| **Controller** | HTTP routing, delegation | Service/Orchestrator |
| **Orchestrator** | Business logic, workflows | Services, Repositories |
| **Service** | Data operations | Repositories, External APIs |
| **Repository** | Query correctness | Mongoose Model |

---

## Test File Structure

### Location & Naming

```
src/modules/<module>/tests/<filename>.spec.ts

# Examples:
src/modules/batch-center-mapping/tests/batch-center-mapping.service.spec.ts
src/modules/phase-handler/tests/phase-handler.service.spec.ts
```

### Template

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { Types } from 'mongoose';
import { BadRequestException } from '@nestjs/common';

import { MyService } from '../my.service';
import { MyRepository } from '../my.repository';

describe('MyService', () => {
  let service: MyService;
  let repo: jest.Mocked<MyRepository>;

  beforeEach(async () => {
    const repoMock = {
      find: jest.fn().mockResolvedValue([]),
      findOne: jest.fn().mockResolvedValue(null),
      create: jest.fn().mockResolvedValue({}),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        MyService,
        { provide: MyRepository, useValue: repoMock },
      ],
    }).compile();

    service = module.get<MyService>(MyService);
    repo = module.get(MyRepository) as jest.Mocked<MyRepository>;
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('methodName', () => {
    it('should return expected result with valid inputs', async () => {
      // Arrange
      repo.find.mockResolvedValue([{ _id: 'id1' }]);
      
      // Act
      const result = await service.methodName({});
      
      // Assert
      expect(result).toBeDefined();
      expect(repo.find).toHaveBeenCalledTimes(1);
    });

    it('should return empty array when no data found', async () => {
      repo.find.mockResolvedValue([]);
      const result = await service.methodName({});
      expect(result).toEqual([]);
    });

    it('should throw BadRequestException for invalid input', async () => {
      await expect(service.methodName(null))
        .rejects.toThrow(BadRequestException);
    });

    it('should handle repository errors gracefully', async () => {
      repo.find.mockRejectedValue(new Error('DB Error'));
      await expect(service.methodName({}))
        .rejects.toThrow('DB Error');
    });
  });
});
```

---

## Test Categories Checklist

For EACH method, cover these categories:

| Category | Example |
|----------|---------|
| **Happy Path** | Valid input → expected output |
| **Empty Data** | No records → empty array/null |
| **Validation** | Invalid input → throws exception |
| **Not Found** | Missing entity → appropriate error |
| **Error Handling** | Repository/service errors → propagate correctly |
| **Dependency Calls** | Correct params passed to dependencies |
| **Edge: Null** | Null/undefined handling |
| **Edge: ObjectId** | String ↔ ObjectId conversion |
| **Edge: Pagination** | Missing page/limit defaults |

---

## Orchestrator Test Pattern

Orchestrators coordinate multiple services - test workflow logic:

```typescript
describe('MyOrchestrator', () => {
  let orchestrator: MyOrchestrator;
  let serviceA: jest.Mocked<ServiceA>;
  let serviceB: jest.Mocked<ServiceB>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        MyOrchestrator,
        { provide: ServiceA, useValue: { getData: jest.fn() } },
        { provide: ServiceB, useValue: { process: jest.fn() } },
      ],
    }).compile();

    orchestrator = module.get<MyOrchestrator>(MyOrchestrator);
    serviceA = module.get(ServiceA) as jest.Mocked<ServiceA>;
    serviceB = module.get(ServiceB) as jest.Mocked<ServiceB>;
  });

  it('should coordinate services correctly', async () => {
    serviceA.getData.mockResolvedValue({ id: '1' });
    serviceB.process.mockResolvedValue({ success: true });

    const result = await orchestrator.execute({});

    expect(serviceA.getData).toHaveBeenCalledBefore(serviceB.process);
    expect(result.success).toBe(true);
  });

  it('should handle partial failures', async () => {
    serviceA.getData.mockResolvedValue({ id: '1' });
    serviceB.process.mockRejectedValue(new Error('Process failed'));

    await expect(orchestrator.execute({}))
      .rejects.toThrow('Process failed');
  });
});
```

---

## Mock Patterns

See [mock-patterns.md](mock-patterns.md) for complete mock templates.

**Quick mocks:**

```typescript
// Repository
const repoMock = { find: jest.fn().mockResolvedValue([]) };

// Cache
const cacheMock = { get: jest.fn(), set: jest.fn(), del: jest.fn() };

// User context
const mockUser = { userId: new Types.ObjectId(), organizationId: new Types.ObjectId() };
```

---

## Running Tests

```bash
# Single file
npm run test -- src/modules/<module>/tests/<file>.spec.ts

# Module tests
npm run test -- --testPathPattern=<module-name>

# Watch mode
npm run test:watch -- src/modules/<module>/tests/<file>.spec.ts

# With coverage
npm run test:cov -- src/modules/<module>/tests/<file>.spec.ts
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `jest.clearAllMocks()` | Add in `afterEach` block |
| Not awaiting async assertions | Use `await expect(...).rejects.toThrow()` |
| Testing implementation details | Test public API behavior only |
| Missing mock for decorator deps | Mock CacheService if using @ClearCache |
| Inconsistent ObjectId handling | Use `new Types.ObjectId('valid24charstring')` |

---

## Codebase Examples

Reference these existing test files:

| Layer | Example File |
|-------|--------------|
| **Service** | `src/modules/batch-center-mapping/tests/batch-center-mapping.service.spec.ts` |
| **Repository** | `src/modules/batch-center-mapping/tests/batch-center-mapping.repository.spec.ts` |
| **Controller** | `src/modules/rfid-machine/tests/unit/rfid-machine.controller.spec.ts` |
| **Utils** | `src/modules/phase-handler/tests/phase-handler.utils.spec.ts` |
