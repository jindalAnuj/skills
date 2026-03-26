# Jira Required Fields Reference — VP Project (Backend Team)

> **Do NOT call `getJiraIssueTypeMetaWithFields`** — all static field IDs are documented here.

## Static Fields (hardcoded, never change)

| Field Key | Name | Value to send |
|---|---|---|
| `customfield_10218` | Teams | `{"id": "10193"}` → Backend |
| `customfield_10314` | Project Element | `{"id": "10425"}` → Internal Excellence |
| `fixVersions` | Fix Version | `[{"id": "21074"}]` → VP-Tech Excellence JFM 26 |
| `timetracking` | Time Tracking | `{"originalEstimate": "1d", "remainingEstimate": "1d"}` |
| `customfield_10015` | Start Date | `"YYYY-MM-DD"` string — default to **today's date** |
| `duedate` | Due Date | `"YYYY-MM-DD"` string — always ask the user |

### Other Project Element options (if user specifies different work category)
| Value | id |
|---|---|
| PRD - Feature | `10423` |
| Central Task | `11072` |
| Cross Pod Task | `11460` |
| Internal Excellence | `10425` ← default |
| Production Issues | `10427` |
| Miscellaneous | `10428` |

---

## Dynamic Fields (read from `~/.git-ticket-flow/sprint-context.md`)

| Field Key | Name | Format |
|---|---|---|
| `customfield_10020` | Sprint | **Bare integer** e.g. `11173` — NOT `[{"id": 11173}]` |
| `customfield_10014` | Epic Link | Epic key string e.g. `"VP-17568"` |

### How to refresh when cache is expired:
Run one JQL: `project = VP AND sprint in openSprints() ORDER BY created DESC`  
From the first result:
- `customfield_10020[0].id` → sprint ID (integer)  
- `customfield_10014` → epic key

---

## Error → Fix Map (from live run learnings)

| Error message | Root cause | Fix |
|---|---|---|
| `"Project Element is required"` | Missing `customfield_10314` | Add `{"id": "10425"}` |
| `"Teams is required"` | Missing `customfield_10218` | Add `{"id": "10193"}` |
| `"Fix versions is required"` | Missing `fixVersions` | Add `[{"id": "21074"}]` |
| `"Please Link Correct EPIC with Task"` | Missing `customfield_10014` | Add epic key from cache |
| `"Please select correct Sprint"` | Missing `customfield_10020` | Add sprint ID (bare int) from cache |
| `"Number value expected as the Sprint id"` | Sprint passed as `[{"id": N}]` | Pass as bare int: `11173` |
| `"Remaining Estimate is required"` | Missing `timetracking` | Add `{"originalEstimate":"1d","remainingEstimate":"1d"}` |
