#!/usr/bin/env bash
# create-branch-and-mr.sh — Checkout main, create branch, push, open draft MR via glab
#
# Usage:
#   bash create-branch-and-mr.sh \
#     --ticket  VP-18200 \
#     --type    feat \
#     --desc    "rate-limiting-scholarship" \
#     --mr-title "feat(VP-18200): Add rate limiting to scholarship API" \
#     --mr-body  "..." \
#     --assignee anuj.jindal   # optional
#     --target-branch stage    # optional, defaults to main

set -euo pipefail

TICKET=""
TYPE=""
DESC=""
MR_TITLE=""
MR_BODY=""
ASSIGNEE=""
TARGET_BRANCH="main"

# ── Parse args ────────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --ticket)    TICKET="$2";    shift 2 ;;
    --type)      TYPE="$2";      shift 2 ;;
    --desc)      DESC="$2";      shift 2 ;;
    --mr-title)  MR_TITLE="$2";  shift 2 ;;
    --mr-body)   MR_BODY="$2";   shift 2 ;;
    --assignee)  ASSIGNEE="$2";  shift 2 ;;
    --target-branch) TARGET_BRANCH="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

# ── Validate ─────────────────────────────────────────────────────────────────
if [[ -z "$TICKET" || -z "$TYPE" || -z "$DESC" || -z "$MR_TITLE" ]]; then
  echo "Error: --ticket, --type, --desc, and --mr-title are required." >&2
  exit 1
fi

# ── Sanitize desc: lowercase kebab-case, strip special chars ─────────────────
DESC=$(echo "$DESC" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

# ── Construct branch name per Git SOP ────────────────────────────────────────
BRANCH="${TYPE}/${TICKET}-${DESC}"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌿 Branch: $BRANCH"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Branch already exists guard ───────────────────────────────────────────────
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "⚠️  Branch '$BRANCH' already exists locally. Checking it out..."
  git checkout "$BRANCH"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✅ Switched to existing branch: $BRANCH"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  exit 0
fi


STASH_NAME="git-ticket-flow/pre-branch-$(date +%s)"
STASHED=false
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "📦 Stashing local changes as '$STASH_NAME'..."
  git stash push -m "$STASH_NAME"
  STASHED=true
fi

# ── Checkout main and pull latest ─────────────────────────────────────────────
echo "📥 Checking out main and pulling latest..."
git checkout main
git pull origin main

# ── Create and checkout new branch ───────────────────────────────────────────
echo "🌿 Creating branch $BRANCH..."
git checkout -b "$BRANCH"

# ── Restore stashed changes onto new branch ───────────────────────────────────
if [[ "$STASHED" == "true" ]]; then
  echo "📬 Restoring stashed changes onto $BRANCH..."
  git stash pop
fi

# ── Push branch upstream ─────────────────────────────────────────────────────
echo "📤 Pushing branch to origin..."
git push -u origin "$BRANCH"

# ── Build default MR body if not provided ────────────────────────────────────
if [[ -z "$MR_BODY" ]]; then
  MR_BODY="## What changed
$(echo "$MR_TITLE" | sed 's/.*: //')

## Why
Jira: https://physicswallah001.atlassian.net/browse/$TICKET

## How to test
- [ ] Local testing steps here

## Checklist
- [ ] Unit tests added/updated
- [ ] Tested on local/staging
- [ ] Swagger docs updated (if API changes)"
fi

# ── Create draft MR via glab ─────────────────────────────────────────────────
echo "🚀 Creating draft MR on GitLab..."

GLAB_ARGS=(
  mr create
  --draft
  --title "$MR_TITLE"
  --description "$MR_BODY"
  --target-branch "$TARGET_BRANCH"
  --remove-source-branch
  --yes
)

if [[ -n "$ASSIGNEE" ]]; then
  GLAB_ARGS+=(--assignee "$ASSIGNEE")
fi

MR_OUTPUT=$(glab "${GLAB_ARGS[@]}" 2>&1)
echo "$MR_OUTPUT"

# ── Extract MR URL from glab output ──────────────────────────────────────────
MR_URL=$(echo "$MR_OUTPUT" | grep -oE 'https://gitlab\.com[^ ]+' | head -1 || true)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Branch created : $BRANCH"
if [[ -n "$MR_URL" ]]; then
  echo "✅ Draft MR       : $MR_URL"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
