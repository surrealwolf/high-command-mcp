#!/bin/bash
# Setup automatic Copilot code review via GitHub rulesets
# This script configures a repository ruleset that automatically requests
# Copilot code review on all pull requests to the main branch.

set -e

OWNER="surrealwolf"
REPO="high-command-mcp"
GH_TOKEN=$(gh auth token)

echo "🤖 Setting up automatic Copilot code review via rulesets..."
echo ""

# Create ruleset with required PR review
echo "Creating repository ruleset for pull request requirements..."

RULESET_RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$OWNER/$REPO/rulesets" \
  -d '{
    "name": "Require Copilot Code Review",
    "target": "branch",
    "enforcement": "active",
    "conditions": {
      "ref_name": {
        "include": ["refs/heads/main"],
        "exclude": []
      }
    },
    "rules": [
      {
        "type": "required_pull_request_reviews",
        "parameters": {
          "required_approving_review_count": 1,
          "dismiss_stale_reviews_on_push": true
        }
      }
    ]
  }')

echo "$RULESET_RESPONSE"
echo ""

RULESET_ID=$(echo "$RULESET_RESPONSE" | jq -r '.id // empty')

if [ -z "$RULESET_ID" ]; then
  echo "❌ Failed to create ruleset"
  echo "Response: $RULESET_RESPONSE"
  exit 1
fi

echo "✅ Ruleset created with ID: $RULESET_ID"
echo ""
echo "✅ PR review ruleset configured!"
echo ""
echo "📋 Next Steps:"
echo "  1. Open: https://github.com/$OWNER/$REPO/settings/rules/$RULESET_ID"
echo "  2. Scroll to 'Branch rules'"
echo "  3. Click 'Automatically request Copilot code review'"
echo "  4. Select 'Review new pushes' and 'Review draft pull requests' (optional)"
echo "  5. Click 'Save'"
echo ""
echo "� Current Ruleset Configuration:"
echo "  • Name: Require Copilot Code Review"
echo "  • Target Branches: main"
echo "  • Required Approvals: 1"
echo "  • Dismiss Stale Reviews: Yes"
echo "  • Copilot Auto-review: Configure via GitHub UI (link above)"
echo ""
echo "🔗 Ruleset URL:"
echo "   https://github.com/$OWNER/$REPO/settings/rules"
