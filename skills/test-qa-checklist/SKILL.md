---
name: test-qa-checklist
description: Use when asked for QA checklists, manual test plans, acceptance criteria, or non-technical test documentation for stakeholders
---

# QA Checklist

## Overview

Creates non-technical test documentation for stakeholders in plain English. Core principle: translate technical API behavior into user-facing scenarios that anyone can validate.

## When to Use

Use this skill when:
- PM or stakeholder requests acceptance criteria
- QA team needs manual test scenarios for validation
- Creating test plans for non-technical team members
- Documenting expected behavior for user acceptance testing
- Keywords: "QA checklist", "manual test plan", "acceptance criteria", "test scenarios"

## When NOT to Use

Don't use this skill for:
- Writing automated tests (Jest, TypeScript unit tests) - use TDD skill instead
- Technical API testing documentation - use test-api skill instead
- Code-level integration tests

---

## File Location & Naming

**REQUIRED:** Save the generated checklist in the controller's module directory.

**Steps:**
1. **Locate the controller file** being tested
   - Example: `src/modules/scholarship/controllers/rank-scholarship.controller.ts`
2. **Create `qa-checklist/` folder** in the same module directory (if it doesn't exist)
3. **Name the file** after the API endpoint using kebab-case
   - Format: `[api-name]-api.md`
   - Example: `rank-scholarship-api.md`

**Directory structure example:**
```
src/modules/scholarship/
  controllers/
    rank-scholarship.controller.ts
  qa-checklist/                      ← Create this folder
    rank-scholarship-api.md          ← Save checklist here
    another-api.md                   ← Additional checklists here
```

**File naming rules:**
- Use kebab-case (lowercase with hyphens)
- Include `-api` suffix
- Match the controller or feature name
- Extension: `.md` (Markdown)

---

## Quick Reference

| Section | Purpose | Example |
|---------|---------|---------|
| **Happy Path** | Standard success scenarios | "User successfully registers with valid data" |
| **Validation Errors** | User mistakes, invalid input | "Email field left blank" |
| **Business Logic** | Domain-specific rules | "Cannot register during closed enrollment" |
| **Security & Permissions** | Access control | "Student cannot access teacher dashboard" |
| **Edge Cases** | Boundaries, rare situations | "Name with 100 characters" |

**Test case format:**
```markdown
| ID | Scenario | Steps to Test | Expected Result |
|----|----------|---------------|-----------------|
| TC-01 | [Name] | 1. Step one<br>2. Step two | User sees [specific outcome] |
```

---

## Test Scenario Categories

Structure your test plan using these standardized categories:

### 1. Happy Path (Standard Success)
- What happens when a user does everything right?
- **Example**: "User successfully verifies phone number with valid OTP."

### 2. Validation Errors (User Mistakes)
- What happens with missing or invalid data?
- **Example**: "User tries to register without an email address."

### 3. Business Logic Rules
- Constraints specific to the business.
- **Example**: "User cannot upgrade subscription if they already have a pending change."

### 4. Security & Permissions
- access control and authentication.
- **Example**: "Student tries to access a Teacher-only API."

### 5. Edge Cases
- Boundaries and rare situations.
- **Example**: "User registers with a name containing emojis."

---

## Document Format

Use the following table format for readability:

### Test Plan: `[Feature Name]`

| ID | Scenario | Steps to Test | Expected Result |
|----|----------|---------------|-----------------|
| **TC-01** | **Successful Registration** | 1. Open the app<br>2. Enter valid Name, Email, Phone<br>3. Click 'Register' | Success message is shown.<br>User is redirected to Dashboard. |
| **TC-02** | **Duplicate Email** | 1. Enter an email that is already registered<br>2. Click 'Register' | Error popup: "Email already exists".<br>Registration is blocked. |
| **TC-03** | **Invalid Phone Number** | 1. Enter a 5-digit phone number<br>2. Click 'Register' | 'Invalid Phone' error applies.<br>Submit button is disabled. |

---

## Writing Guidelines for Stakeholders

- **Avoid Jargon**: Use "Success Message" instead of "200 OK". Use "Data is saved" instead of "Database commit".
- **Focus on User Action**: Start steps with "User enters...", "User clicks...".
- **Be Specific**: Don't say "Invalid data". Say "Enters an expiry date in the past".
- **Define Success Clearly**: State exactly what the user sees (popup, page change, button state).

---

## Common Scenario Templates

### Search & Filter
- **Empty Search**: Search with no keywords -> Should show all result or prompt.
- **No Results**: Search for "Unknown Item" -> "No results found" message.
- **Pagination**: Scroll down/Customer Page 2 -> More items load.

### Forms & Input
- **Required Fields**: Leave mandatory fields blank -> "Required" error.
- **Max Length**: Type a very long text -> Limit validation kicks in.
- **Special Characters**: Enter "Testing @#$%" -> System handles or rejects politely.

### Permissions
- **Logged Out**: Try to access page without login -> Redirect to Login screen.
- **Wrong Role**: Student accesses Admin page -> "Access Denied" page.

---

## Test Data Requirements

List any specific data needed to run the tests:

- **Pre-conditions**: "User must have an active subscription."
- **Test Accounts**: "Use a student account with no prior purchases."
- **Environment**: "Tests can be run on Staging or Dev environment."

---

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| **Using technical jargon** | "Returns 200 OK", "Database commit" | Use "Success message shown", "Data is saved" |
| **Vague expected results** | "Should work correctly" | "User sees confirmation popup with text 'Registration successful'" |
| **Missing pre-conditions** | Testing login without mentioning account exists | State: "Pre-condition: User account exists in system" |
| **Generic error descriptions** | "Invalid data" | "Enters phone number with only 5 digits" |
| **Forgetting file location** | Saving checklist in wrong directory | Always save in module's `qa-checklist/` folder next to controller |
| **Skipping edge cases** | Only testing happy path | Include boundaries (max length, empty strings, special characters) |
| **Not specifying exact UI feedback** | "Error is shown" | "Red error text appears below email field: 'Email already exists'" |
