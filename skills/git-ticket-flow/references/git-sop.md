# Git SOP — Vidyapeeth POD

Source: https://physicswallah001.atlassian.net/wiki/spaces/EN/pages/1247281169/Git+SOP+Vidyapeeth+POD

## Branch Naming Convention

**Pattern:** `{type}/VP-{TICKET_ID}-{short-description}`

| Type | When to use |
|---|---|
| `feat` | New feature or enhancement |
| `fix` | Bug fix |
| `chore` | Maintenance, deps, configs, tooling |
| `refactor` | Code restructure with no behavior change |
| `hotfix` | Urgent production fix |

**Rules:**
- `short-description` must be kebab-case, 2–4 words
- Always contains the Jira ticket ID (`VP-XXXXX`)
- Branch off from `main` only; always pull latest before branching

**Examples:**
```
feat/VP-18200-rate-limiting-scholarship
fix/VP-18050-login-redirect-bug
chore/VP-18100-upgrade-mongoose
refactor/VP-17900-phase-service-cleanup
hotfix/VP-18199-prod-crash-fix
```

## Commit Message Convention

**Pattern:** `{type}({VP-XXXXX}): {short description}`

**Rules:**
- Use imperative mood: "Add", "Fix", "Remove" (not "Added", "Fixed")
- Body (optional): explain *why*, not *what*
- Footer: reference Jira ticket

**Examples:**
```
feat(VP-18200): Add rate limiting to scholarship API
fix(VP-18050): Fix login redirect after OAuth callback
chore(VP-18100): Upgrade mongoose to v7.5
```

## MR (Merge Request) Standards

- **Target branch:** `main`
- **Title format:** Same as the primary commit message
- **Draft:** Open as Draft when targeting `main`; open as **ready** (non-draft) when targeting `staging`
- **Description template:**
```
## What changed
<short explanation>

## Why
<jira link and context>

## How to test
<testing steps>

## Checklist
- [ ] Unit tests added/updated
- [ ] Tested on local/staging
- [ ] Swagger docs updated (if API changes)
```
- **Assignee:** Author of the MR
- **Reviewer:** At least one team member

## Base Branch

Always branch from `main`. Pull `origin/main` before creating branch:
```bash
git checkout main && git pull origin main
```
