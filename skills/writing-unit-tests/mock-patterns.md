# Mock Patterns Reference

Reusable mock patterns for NestJS/Jest unit tests.

## Repository Mock

```typescript
const repoMock = {
  find: jest.fn().mockResolvedValue([]),
  findOne: jest.fn().mockResolvedValue(null),
  findById: jest.fn().mockResolvedValue(null),
  create: jest.fn().mockResolvedValue({}),
  updateOne: jest.fn().mockResolvedValue({ modifiedCount: 1 }),
  findOneAndUpdate: jest.fn().mockResolvedValue(null),
  deleteOne: jest.fn().mockResolvedValue({ deletedCount: 1 }),
  count: jest.fn().mockResolvedValue(0),
  aggregate: jest.fn().mockResolvedValue([]),
};
```

## Service Mock

```typescript
const serviceMock = {
  getDetails: jest.fn().mockResolvedValue({ data: [] }),
  create: jest.fn().mockResolvedValue({ _id: 'newId' }),
  update: jest.fn().mockResolvedValue({ _id: 'updatedId' }),
  delete: jest.fn().mockResolvedValue({ deletedCount: 1 }),
};
```

## Cache Service Mock

```typescript
const cacheServiceMock = {
  get: jest.fn().mockResolvedValue(null),
  set: jest.fn().mockResolvedValue(undefined),
  del: jest.fn().mockResolvedValue(undefined),
  hGet: jest.fn().mockResolvedValue(null),
  hSet: jest.fn().mockResolvedValue(undefined),
};
```

## User/Auth Mock

```typescript
const mockUser = {
  userId: new Types.ObjectId('507f1f77bcf86cd799439011'),
  organizationId: new Types.ObjectId('507f1f77bcf86cd799439012'),
};
```

## Logger Mock

```typescript
const loggerMock = {
  log: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  debug: jest.fn(),
  verbose: jest.fn(),
};
```

## Database Service Mock

```typescript
jest.mock('src/common/database/database.service');
jest.mock('src/bootstrap/cache/cache.service');
```

## External API Service Mock

```typescript
const externalApiMock = {
  get: jest.fn().mockResolvedValue({ data: {} }),
  post: jest.fn().mockResolvedValue({ data: {} }),
  put: jest.fn().mockResolvedValue({ data: {} }),
};
```

## Utils Service Mock

```typescript
const utilsMock = {
  getPagination: jest.fn().mockReturnValue({ limit: 10, skip: 0, page: 1 }),
  transformFeeStructure: jest.fn().mockReturnValue({ amount: 0, tax: 0, total: 0 }),
  getNestedProperty: jest.fn(),
  isValidDate: jest.fn().mockReturnValue(true),
};
```
