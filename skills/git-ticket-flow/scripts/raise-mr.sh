#!/usr/bin/env bash
# raise-mr.sh — Create an MR for an already-existing branch via glab
#
# Usage:
#   bash raise-mr.sh \
#     --source-branch feat/VP-18144-unleash-singleton \  # optional, defaults to current branch
#     --target-branch staging \                          # optional, defaults to main
#     --mr-title "feat(VP-18144): Unleash singleton" \   # optional, inferred from branch name
#     --mr-body  "..." \                                 # optional, uses template
#     --assignee anuj.jindal \                           # optional
#     --draft                                            # optional flag

set -euo pipefail

SOURCE_BRANCH=""
TARGET_BRANCH="main"
MR_TITLE=""
MR_BODY=""
ASSIGNEE=""
DRAFT=false

# ── Parse args ────────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --source-branch)  SOURCE_BRANCH="$2";  shift 2 ;;
    --target-branch)  TARGET_BRANCH="$2";  shift 2 ;;
    --mr-title)       MR_TITLE="$2";       shift 2 ;;
    --mr-body)        MR_BODY="$2";        shift 2 ;;
    --assignee)       ASSIGNEE="$2";       shift 2 ;;
    --draft)          DRAFT=true;          shift 1 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

# ── Resolve source branch ─────────────────────────────────────────────────────
if [[ -z "$SOURCE_BRANCH" ]]; then
  SOURCE_BRANCH=$(git branch --show-current)
fi

if [[ -z "$SOURCE_BRANCH" ]]; then
  echo "Error: could not determine source branch. Pass --source-branch explicitly." >&2
  exit 1
fi

# ── Infer MR title from branch name if not provided ───────────────────────────
# Branch format: {type}/VP-{KEY}-{desc}  →  "{type}(VP-{KEY}): {desc}"
if [[ -z "$MR_TITLE" ]]; then
  BRANCH_BASE=$(basename "$SOURCE_BRANCH")
  # Extract type prefix (feat, fix, chore, refactor, hotfix)
  TYPE=$(echo "$BRANCH_BASE" | grep -oE '^[a-z]+' || true)
  # Extract ticket key (VP-XXXXX)
  TICKET=$(echo "$BRANCH_BASE" | grep -oE 'VP-[0-9]+' || true)
  # Extract description portion (everything after VP-XXXXX-)
  DESC_RAW=$(echo "$BRANCH_BASE" | sed "s|^${TYPE}/${TICKET}-||" | tr '-' ' ' || true)
  # Capitalize first letter
  DESC_CAP=$(echo "$DESC_RAW" | awk '{$1=toupper(substr($1,1,1))substr($1,2); print}')

  if [[ -n "$TICKET" && -n "$DESC_CAP" ]]; then
    MR_TITLE="${TYPE}(${TICKET}): ${DESC_CAP}"
  else
    MR_TITLE="$SOURCE_BRANCH → $TARGET_BRANCH"
  fi
fi

# ── Infer ticket key for MR body ─────────────────────────────────────────────
TICKET_IN_BODY=$(echo "$SOURCE_BRANCH" | grep -oE 'VP-[0-9]+' || true)

# ── Build default MR body if not provided ────────────────────────────────────
if [[ -z "$MR_BODY" ]]; then
  JIRA_LINK=""
  if [[ -n "$TICKET_IN_BODY" ]]; then
    JIRA_LINK="Jira: https://physicswallah001.atlassian.net/browse/${TICKET_IN_BODY}"
  fi

  MR_BODY="## What changed
$(echo "$MR_TITLE" | sed 's/.*: //')

## Why
${JIRA_LINK}

## How to test
- [ ] Local testing steps here

## Checklist
- [ ] Unit tests added/updated
- [ ] Tested on local/staging
- [ ] Swagger docs updated (if API changes)"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Raising MR: $SOURCE_BRANCH → $TARGET_BRANCH"
echo "   Title: $MR_TITLE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Build glab args ───────────────────────────────────────────────────────────
GLAB_ARGS=(
  mr create
  --source-branch "$SOURCE_BRANCH"
  --target-branch "$TARGET_BRANCH"
  --title         "$MR_TITLE"
  --description   "$MR_BODY"
  --yes
)

if [[ "$DRAFT" == "true" ]]; then
  GLAB_ARGS+=(--draft)
fi

if [[ -n "$ASSIGNEE" ]]; then
  GLAB_ARGS+=(--assignee "$ASSIGNEE")
fi

# ── Create MR ─────────────────────────────────────────────────────────────────
MR_OUTPUT=$(glab "${GLAB_ARGS[@]}" 2>&1)
echo "$MR_OUTPUT"

# ── Extract and surface MR URL ────────────────────────────────────────────────
MR_URL=$(echo "$MR_OUTPUT" | grep -oE 'https://gitlab\.com[^ ]+' | head -1 || true)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ -n "$MR_URL" ]]; then
  echo "✅ MR raised : $MR_URL"
else
  echo "⚠️  MR may already exist or glab output had no URL."
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
