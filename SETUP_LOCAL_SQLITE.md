# 📚 Local SQLite Setup Guide - Complete

## What You Need

You need **Node.js** installed on your computer. That's it!

### Install Node.js

1. Go to: https://nodejs.org/
2. Download **LTS version** (Long Term Support)
3. Install it (click Next > Next > Install)
4. Restart your computer

**Verify installation:**
```bash
node --version
npm --version
```

Both should show version numbers.

---

## 🚀 Quick Setup (After Node.js)

### Step 1: Open Terminal
Go to: `c:\evalleRecords\EVALanguage`

In VS Code:
- Terminal → New Terminal
- Or press: `Ctrl + `

### Step 2: Install Dependencies
```bash
npm install
```

Wait for it to finish. You'll see lots of text. That's normal!

### Step 3: Start Server
```bash
npm start
```

You should see:
```
🚀 Server running on port 3000
✅ Database initialized at: c:\evalleRecords\EVALanguage\quiz_scores.db
```

### Step 4: Test & Use

**Test connection:**
```
http://localhost:3000/api/health
```

Should show:
```json
{
  "status": "Server is running",
  "database": "SQLite (local file)",
  "location": "c:\\evalleRecords\\EVALanguage\\quiz_scores.db"
}
```

**Open quiz:**
```
c:\evalleRecords\EVALanguage\pages\quiz1.html
```

**View progress:**
```
c:\evalleRecords\EVALanguage\pages\progress.html
```

---

## 📊 Your Local Database

**Location:**
```
c:\evalleRecords\EVALanguage\quiz_scores.db
```

**What's stored:**
- Quiz number
- Your score
- Total questions
- Percentage
- Date and time

**It's just a file!**
- You can backup it
- You can share it
- You can delete it (and start fresh)
- All your data is local, private, and yours

---

## 🔄 Daily Workflow

1. Open terminal
2. Run: `npm start`
3. Leave it running
4. Open: `pages/quiz1.html`
5. Take quiz
6. View: `pages/progress.html`
7. Done!

**Stop server:**
Press `Ctrl + C` in terminal

**Start again:**
```bash
npm start
```

---

## 📁 Files Structure

```
c:\evalleRecords\EVALanguage\
│
├── server.js ..................... Backend (SQLite)
├── package.json .................. Config
│
├── quiz_scores.db ................ YOUR DATA (created automatically)
│
├── pages/
│   ├── quiz1.html ................ Quiz
│   ├── progress.html ............. Calendar view ⭐
│   └── progress-tracker.js ....... Auto-save
│
└── LOCAL_SETUP.md ................ This file
```

---

## ✅ What Works

✅ Automatic score saving
✅ Calendar view with colors
✅ Statistics dashboard
✅ 30-day progress history
✅ Offline (no internet needed)
✅ Local data (your computer only)
✅ No accounts needed
✅ No signup needed

---

## 🛠 Troubleshooting

### "npm: The term 'npm' is not recognized"
**Fix:** Install Node.js from https://nodejs.org/

### "Connection refused" 
**Fix:** Make sure you ran `npm start`

### "Cannot find module"
**Fix:** Run `npm install` again

### "Database not initialized"
**Fix:** Delete `quiz_scores.db` and restart server

### "Port 3000 already in use"
**Fix:** Another app is using port 3000
- Close other terminals
- Or change PORT in code to 3001

---

## 🔐 Privacy & Security

✅ **All data stored locally** - No cloud, no servers
✅ **No internet needed** - Works completely offline
✅ **No tracking** - Just your computer
✅ **No accounts** - Nothing to sign up for
✅ **You own your data** - It's a file on your computer

---

## 📱 Can I Use This on Mobile?

Currently it's desktop only. To use on mobile/tablet:

1. Need to deploy to cloud (Render, Heroku, etc.)
2. Or use mobile app development

For now, use on your laptop/desktop.

---

## 🆘 Still Stuck?

1. Check Node.js is installed: `node --version`
2. Check npm is installed: `npm --version`
3. Check you're in right folder: `cd c:\evalleRecords\EVALanguage`
4. Try reinstalling: `npm install`
5. Check console for error messages (scroll up)

---

## 🎯 That's It!

**The only things you need:**
1. Node.js installed
2. Run: `npm install` (once)
3. Run: `npm start` (every time)
4. Visit: localhost:3000 (in browser)

**Simple. Local. Private. Yours! 🚀**
