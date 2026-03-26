---
name: git-ticket-flow
description: Handles all Jira and Git operations for the Vidyapeeth POD. Use this skill whenever the user mentions: starting a feature, fix, chore, or refactor; creating or updating a Jira ticket; making a commit; staging changes; raising or opening an MR; closing or resolving a VP-XXXXX ticket; getting a branch; pushing changes; syncing with main or staging; or anything involving the git or Jira workflow for this project. When in doubt, invoke it — it covers the entire dev loop from ticket creation to merge.
---

# git-ticket-flow

Handles all Jira + Git operations for the VP POD. Run the **Prerequisites Check** before any operation.

**Atlassian MCP cloudId:** `ba5d328f-f4a3-4652-ba4d-aba5e33ecabd`  
**Jira project board:** https://physicswallah001.atlassian.net/jira/software/c/projects/VP/boards/189

---

## ⚙️ Prerequisites Check (ALWAYS run first)

Before doing anything else, verify both dependencies are available:

**1. Atlassian MCP**
- Call `getAccessibleAtlassianResources`
- If it errors → **STOP** and tell the user:
  > ❌ **Atlassian MCP is not configured.**
  > 
  > Please configure the Atlassian MCP server. You can find instructions or install it using the [MCP Settings]. Provide me with your Cloud ID when ready.

**2. glab CLI**
- Run `glab auth status`
- If it fails → **STOP** and tell the user:
  > ❌ **glab CLI is not authenticated.**
  > 
  > Please run the following command in your terminal to authenticate:
  > ```bash
  > glab auth login
  > ```
  > Let me know when you've completed this so we can continue.

If either check fails, do not proceed with any operation until the user confirms they have fixed it.

---

## 📦 Sprint Cache (read before every ticket creation)

Sprint ID and Epic Key change every ~2 weeks. They are cached locally at **`~/.git-ticket-flow/sprint-context.md`** (not in the repo, gitignored by default).

**Before calling `createJiraIssue`:**
1. Read `~/.git-ticket-flow/sprint-context.md`
2. Check `sprint_end_date`:
   - **Not expired** → use `sprint_id` and `epic_key` directly. Skip JQL.
   - **Expired or file missing** → run **one** JQL:  
     `project = VP AND sprint in openSprints() ORDER BY created DESC`  
     → from first result: `customfield_10020[0].id` = sprint ID, `customfield_10014` = epic key
   - After fetching → write updated values back to `~/.git-ticket-flow/sprint-context.md`

**All other required field IDs:** see `references/jira-fields.md`. Do NOT call `getJiraIssueTypeMetaWithFields`.

---

## Operation A — Create a Feature/Chore Task + Branch + MR

*Triggers: "create a ticket for", "start a new feature/chore/refactor"*

### A1 — Gather Input

Ask in one message: `summary` (2–3 sentences), `priority` (`High`/`Medium`/`Low`), and `due_date` (`DD MMM YYYY` or `YYYY-MM-DD`).

**Defaults (do not ask unless explicitly mentioned):**
- `type` → `feat`
- `priority` → `Medium`
- `start_date` → today's date (always default silently, never ask)

Only ask for `type` if the user mentions bug/fix/chore/refactor/hotfix.

### A2 — Create Jira Task via MCP

Read sprint cache (see section above). Then call `createJiraIssue`:

```json
{
  "cloudId": "ba5d328f-f4a3-4652-ba4d-aba5e33ecabd",
  "projectKey": "VP",
  "issueTypeName": "Task",
  "summary": "<title>",
  "description": "<see description template>",
  "additional_fields": {
    "customfield_10014": "<epic_key from cache>",
    "customfield_10020": <sprint_id from cache as bare integer>,
    "customfield_10015": "<start_date as YYYY-MM-DD, default today>",
    "duedate":           "<due_date as YYYY-MM-DD>",
    "customfield_10218": { "id": "10193" },
    "customfield_10314": { "id": "10425" },
    "fixVersions":       [{ "id": "21074" }],
    "timetracking":      { "originalEstimate": "1d", "remainingEstimate": "1d" }
  }
}
```

> ⚠️ Sprint format: pass as bare integer `11173`, NOT `[{"id": 11173}]`

Extract the **issue key** (e.g. `VP-18200`) from the response.

### A3 — Create Branch & Draft MR

```bash
bash .agent/skills/git-ticket-flow/scripts/create-branch-and-mr.sh \
  --ticket   "VP-18200" \
  --type     "feat" \
  --desc     "2-4-word-kebab-desc" \
  --mr-title "feat(VP-18200): <title>" \
  --mr-body  "<see MR template in references/git-sop.md>" \
  --assignee "anuj.jindal" \
  --target-branch "main" # optional, defaults to main
```

Branch is auto-named: `{type}/VP-{KEY}-{desc}`. Script handles stashing local changes automatically.

### A4 — Report

```
✅ Jira Task : VP-18200 → https://physicswallah001.atlassian.net/browse/VP-18200
✅ Branch    : feat/VP-18200-short-desc
✅ Draft MR  : <MR_URL>
```

Then immediately run **Operation E**.

---

## Operation B — Create a Bug Ticket + Branch + MR

*Triggers: "create a bug for", "report a bug", "fix a bug"*

Same as Operation A with these differences:
- `issueTypeName`: `Bug`
- `type` is always `fix`
- Ask for: `title` (what's broken), `summary` (repro steps + impact), `priority`
- Use `--type "fix"` in the branch script

Then run **Operation E**.

---

## Operation C — Add Comment / Update to a Ticket

*Triggers: "update ticket VP-XXX", "add a comment to VP-XXX", "log update on VP-XXX"*

### C1 — Gather Input
Ask: ticket key (e.g. `VP-18200`), comment text.

### C2 — Add Comment via MCP
Call `addCommentToJiraIssue`:
- `cloudId`: `ba5d328f-f4a3-4652-ba4d-aba5e33ecabd`
- `issueIdOrKey`: the ticket key
- `commentBody`: the comment in Markdown

### C3 — Confirm
```
✅ Comment added to VP-18200
   https://physicswallah001.atlassian.net/browse/VP-18200
```

---

## Operation D — Close / Resolve a Ticket

*Triggers: "close ticket VP-XXX", "mark VP-XXX as done", "resolve VP-XXX"*

### D1 — Get Transitions
Call `getTransitionsForJiraIssue` with the ticket key.

### D2 — Apply Done Transition
Find the `Done` / `Closed` / `Resolved` transition ID, then call `transitionJiraIssue`:
- `cloudId`: `ba5d328f-f4a3-4652-ba4d-aba5e33ecabd`
- `issueIdOrKey`: ticket key
- `transition`: `{ "id": "<transition_id>" }`

### D3 — Confirm
```
✅ VP-18200 marked as Done
   https://physicswallah001.atlassian.net/browse/VP-18200
```

---

## Operation F — Raise MR from Existing Branch

*Triggers: "raise an MR", "raise an MR for ... to staging/main", "create an MR for", "open a merge request", "we need to raise an MR"*

### F1 — Resolve Inputs

Determine the following (ask in **one message** only if not already clear from context):

| Input | Default |
|---|---|
| `source-branch` | Current branch (`git branch --show-current`) |
| `target-branch` | `main` (ask if not specified by user) |
| `draft` | `false` for `staging` target; `true` for `main` target |
| `mr-title` | Inferred from branch name (see script) — do **not** ask |

### F2 — Run raise-mr.sh

```bash
bash .agent/skills/git-ticket-flow/scripts/raise-mr.sh \
  --source-branch "<branch>" \
  --target-branch "<target>" \
  --assignee       "anuj.jindal"   # always include
  # add --draft if target is main
```

The script:
- Uses the current branch if `--source-branch` is omitted
- Auto-infers the MR title from the branch name (`{type}(VP-XXX): {desc}`)
- Generates a standard MR body with the Jira link
- Does **not** checkout, stash, or touch your working tree

### F3 — Report

```
✅ MR raised : <MR_URL>
   Source : <source-branch>
   Target : <target-branch>
```

Then run **Operation E**.

---

## Operation G — Stage & Commit Changes

*Triggers: "make a commit", "commit my changes", "commit these files", "stage and commit", "git commit"*

### G1 — Resolve Inputs

Determine the following (ask in **one message** if not already clear from context):

| Input | Default |
|---|---|
| `ticket` | Inferred from current branch name (`git branch --show-current`) |
| `type` | Inferred from branch prefix (`feat`, `fix`, `chore`, etc.) |
| `message` | Ask if not provided |
| `files` | All staged/modified files (`-A`) unless user specifies |

**Commit message format (from git-sop.md):**
```
{type}(VP-XXXXX): {short description in imperative mood}
```

### G2 — Stage Files

```bash
# Stage all changes (default)
git add -A

# Or stage specific files/paths if user specified
git add <file1> <file2> ...
```

### G3 — Commit

```bash
git commit -m "{type}(VP-XXXXX): {short description}"
```

**Rules (enforced):**
- Use imperative mood: "Add", "Fix", "Remove", "Update" (NOT "Added", "Fixed")
- Description must be concise (≤72 chars total)
- Must include the ticket ID from the current branch

### G4 — Report

```
✅ Committed : {type}(VP-XXXXX): {description}
   Files     : <N files changed>
   Branch    : <current branch>
```

After reporting, always ask:
> Want me to push to origin now?

- If **yes** → run `git push`
- If **no** → skip silently

Then run **Operation E**.

---

## Operation E — Post-Run Self-Learning (auto-runs after every operation)

After completing any operation, briefly reflect on the run:

1. **Did anything unexpected happen?** (e.g. extra MCP calls, a field error, a workaround, a new gotcha)
2. **If yes** → surface 1–3 concise improvement suggestions:

```
🧠 Skill learning: I noticed [X] during this run.
Want me to update the skill with these improvements?
  - [suggestion 1]
  - [suggestion 2]
Reply yes to apply, or no to skip.
```

3. **If user says yes** → update `SKILL.md` or the relevant reference file
4. **If user says no** → skip silently

**Only suggest if something genuinely new was discovered.** Do not suggest on a clean, error-free run.

---

## Jira Ticket Description Template

```
As a <user type>,
I want to <action>,
So that <goal>.

**Acceptance Criteria**
GIVEN <context>
WHEN <action>
THEN <expected outcome>

**Definition of Done**
- [ ] Code reviewed and merged
- [ ] Unit & integration tests passed
- [ ] Feature tested on staging
- [ ] Swagger docs updated (if API changes)
- [ ] Meets acceptance criteria
```

---

## References

- **Field IDs & error map:** [references/jira-fields.md](references/jira-fields.md)
- **Branch naming & MR template:** [references/git-sop.md](references/git-sop.md)
- **Sprint cache (not in repo):** `~/.git-ticket-flow/sprint-context.md`
