# 🚀 Wonderloom Story App - Quick Links & Setup

## 📱 Access Your App
- **Live URL**: http://localhost:8501
- **Status**: Running ✅

## 🔗 GitHub Repository
- **URL**: https://github.com/shwetasirohi07/kidsstoryapp
- **Latest commit**: Sound effects integration (page turning + category sounds)

---

## 🔄 Auto-Sync Setup (Optional)

To automatically commit and push changes to GitHub every minute, run this in a PowerShell terminal:

```powershell
# Navigate to the app directory
cd "c:\Users\Gagan EDU India\storyappkids"

# Run the auto-sync script
.\auto_sync.ps1
```

**What it does:**
- ✅ Monitors folder for changes every 60 seconds
- ✅ Auto-commits changed files with timestamp
- ✅ Auto-pushes commits to GitHub
- ✅ Shows you what changed in the console

**To stop**: Press `Ctrl+C`

---

## 🎵 Recent Updates (Just Pushed)

### Sound Effects Added:
1. **Page Turning** - Plays when clicking Next/Previous
2. **Category Sounds** - Adventure (roar), Bedtime (bell), Funny (laugh), Magical (chime)
3. **Story Mode Sounds** - Different sounds for each mode
4. **Location Sounds** - Jungle, Space, Ocean, School, etc.
5. **Moral Sounds** - Sounds for Kindness, Honesty, Bravery, Sharing

---

## 📁 Project Structure
```
storyappkids/
├── app.py (Main Streamlit app)
├── library_stories_140_wonder.json (Story library - 150 stories)
├── storyspark.db (SQLite database)
├── requirements.txt
├── Procfile (For Render deployment)
├── render.yaml
├── auto_sync.ps1 (Auto-commit script)
└── README.md
```

---

## 🛠️ Git Commands (Manual)

If you prefer manual commits:

```powershell
# Check status
git status

# Add all changes
git add -A

# Commit with message
git commit -m "Your message here"

# Push to GitHub
git push

# View recent commits
git log --oneline -n 5
```

---

## 💡 Tips
- The app automatically reloads when you edit `app.py`
- Changes to `app.py` don't need a full restart, just refresh the browser
- Database changes are preserved across server restarts
- All 150+ stories are stored in SQLite

Enjoy building! 🎉
