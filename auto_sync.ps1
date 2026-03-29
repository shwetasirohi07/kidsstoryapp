# Auto-sync script - watches for changes and commits to GitHub
# Run this in a separate terminal while developing

param(
    [int]$IntervalSeconds = 60
)

$RepoPath = "c:\Users\Gagan EDU India\storyappkids"
$LastCommitHash = ""

Write-Host "Starting auto-sync to GitHub (every $IntervalSeconds seconds)..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Yellow

while ($true) {
    try {
        cd $RepoPath
        
        # Check if there are any changes
        $Status = git status --porcelain
        
        if ($Status) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Changes detected!" -ForegroundColor Cyan
            Write-Host "Changed files:" -ForegroundColor Yellow
            $Status | ForEach-Object { Write-Host "  $_" }
            
            # Stage all changes
            git add -A
            
            # Create commit message with timestamp
            $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            $CommitMsg = "Auto-commit: Changes at $Timestamp"
            
            # Commit
            git commit -m $CommitMsg
            Write-Host "✓ Committed: $CommitMsg" -ForegroundColor Green
            
            # Push to GitHub
            git push
            Write-Host "✓ Pushed to GitHub" -ForegroundColor Green
            Write-Host ""
        }
        else {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] No changes" -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "[ERROR] $_" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds $IntervalSeconds
}
