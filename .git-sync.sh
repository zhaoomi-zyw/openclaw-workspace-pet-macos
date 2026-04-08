#!/bin/bash
# OpenClaw workspace auto-sync every 30 minutes
cd ~/.openclaw/workspace-pet-macos
git add -A
if git diff --cached --quiet; then
  echo "$(date): no changes" >> /tmp/git-sync.log
else
  git commit -m "auto-sync: $(date +'%Y-%m-%d %H:%M')"
  git push >> /tmp/git-sync.log 2>&1
  echo "$(date): pushed" >> /tmp/git-sync.log
fi
