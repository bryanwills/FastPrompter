$ErrorActionPreference = "Stop"
$msg = "deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

git checkout --orphan temp-deploy-branch
git add -A
git commit -m $msg
git branch -D main
git branch -m main
git push -f origin main
git gc --prune=all

Write-Host "`nGitHub wiped & replaced with current state @ $(Get-Date -Format 'HH:mm:ss')"
