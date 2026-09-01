#!/usr/bin/env bash
# Publish this site to GitHub Pages. Safe to re-run.
set -uo pipefail
REPO="newsuperpolymers"
cd "$(dirname "$0")"

OWNER=$(gh api user --jq .login 2>/dev/null) || { echo "FAIL: gh not authenticated. Run: gh auth login"; exit 1; }
echo "==> account: $OWNER"

if [ -z "$(git status --porcelain)" ]; then echo "==> working tree clean"; else
  git add -A && git commit -q -m "Update site" && echo "==> committed pending changes"
fi

if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "==> repo exists"
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$OWNER/$REPO.git"
  git push -u origin main || { echo "FAIL: push rejected"; exit 1; }
else
  echo "==> creating repo (public)"
  gh repo create "$REPO" --public --source=. --remote=origin --push \
     --description "New Super Polymers India Pvt Ltd — PVC lay flat tubing & sheet roll manufacturer" \
     || { echo "FAIL: could not create repo"; exit 1; }
fi
echo "==> pushed"

echo "==> enabling Pages (branch main, root)"
gh api -X POST "repos/$OWNER/$REPO/pages" \
   -f "build_type=legacy" -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
 || gh api -X PUT "repos/$OWNER/$REPO/pages" \
   -f "build_type=legacy" -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
 || echo "   (Pages API did not respond — enable manually: Settings > Pages > Deploy from a branch > main > /root)"

URL="https://$OWNER.github.io/$REPO/"
echo "==> waiting for first build"
for i in $(seq 1 40); do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
  [ "$CODE" = "200" ] && { echo; echo "LIVE: $URL"; exit 0; }
  printf "."; sleep 10
done
echo; echo "Still building. Check: https://github.com/$OWNER/$REPO/settings/pages"
echo "It should come up shortly at: $URL"
