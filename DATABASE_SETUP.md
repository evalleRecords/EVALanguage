# EVA Language Quiz - Database Setup Guide

## Overview
This guide will help you set up your PostgreSQL database on Render and connect it to your quiz application for tracking daily scores and progress in a calendar view.

## Step 1: Get Your Render PostgreSQL Connection String

1. Go to [Render.com](https://render.com) and log in to your account
2. Navigate to your PostgreSQL database
3. In the database settings, find the **External Database URL** or **Connection String**
4. It should look like:
   ```
   postgresql://username:password@dpg-xxxxx.render.com:5432/database_name
   ```

## Step 2: Create Environment File

1. Create a `.env` file in the root directory of your project (same level as `server.js`):
   ```
   DATABASE_URL=postgresql://username:password@dpg-xxxxx.render.com:5432/database_name
   PORT=3000
   ```

2. Replace the values with your actual Render database credentials

## Step 3: Install Dependencies

Run this command in your project directory:

```bash
npm install
```

This will install:
- `express` - Web framework
- `pg` - PostgreSQL client
- `cors` - Cross-Origin Resource Sharing
- `dotenv` - Environment variables management

## Step 4: Start the Server Locally

Run:
```bash
npm start
```

The server should start on `http://localhost:3000`

## Step 5: Test the Connection

Open your browser and go to:
```
http://localhost:3000/api/health
```

You should see:
```json
{"status": "Server is running"}
```

## Step 6: Update API URL in Quiz Pages

### In `progress-tracker.js`:
Find this line:
```javascript
const PROGRESS_API_URL = 'http://localhost:3000/api';
```

For local testing, keep it as is.

### In `progress.html`:
Find this line:
```javascript
const API_URL = 'http://localhost:3000/api';
```

For local testing, keep it as is.

## Step 7: Access the Progress Calendar

1. Open `pages/progress.html` in your browser
2. You should see:
   - Calendar view of the current month
   - Statistics dashboard
   - Progress list

## Step 8: Take a Quiz

1. Open `pages/quiz1.html`
2. Answer the questions
3. Click "Check All Answers"
4. Your score will be automatically saved to the database
5. You'll see a confirmation notification

## Step 9: Deploy to Render (Optional)

When ready to deploy:

1. **Create a Web Service:**
   - Go to Render.com
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Set Build Command: `npm install`
   - Set Start Command: `npm start`

2. **Set Environment Variables:**
   - In Service settings, add environment variable:
   - Key: `DATABASE_URL`
   - Value: Your Render PostgreSQL URL

3. **Update API URLs:**
   - In `progress-tracker.js`, change:
     ```javascript
     const PROGRESS_API_URL = 'https://your-render-service.onrender.com/api';
     ```
   - In `progress.html`, change:
     ```javascript
     const API_URL = 'https://your-render-service.onrender.com/api';
     ```

## Database Schema

The system automatically creates these tables:

### quiz_scores
```sql
id (SERIAL PRIMARY KEY)
quiz_id (INTEGER) - Quiz number (1-10)
score (INTEGER) - Correct answers
total_questions (INTEGER) - Total questions
percentage (INTEGER) - Calculated percentage
created_at (TIMESTAMP) - When the quiz was taken
user_date (DATE) - The date the quiz was taken
```

### daily_progress
```sql
id (SERIAL PRIMARY KEY)
quiz_id (INTEGER)
score (INTEGER)
total (INTEGER)
progress_date (DATE)
created_at (TIMESTAMP)
```

## API Endpoints

### POST /api/save-score
Save a quiz score
```json
{
  "quizId": 1,
  "score": 8,
  "totalQuestions": 10
}
```

### GET /api/today-progress
Get today's quiz scores

### GET /api/calendar-data?year=2026&month=1
Get calendar data for a specific month

### GET /api/all-progress
Get the last 30 days of progress

### GET /api/health
Health check

## Using the Progress Tracker in Your Quiz

In any quiz HTML file:

1. Add the script reference in `<head>`:
   ```html
   <script src="progress-tracker.js"></script>
   ```

2. After calculating the score, call:
   ```javascript
   saveQuizScore(quizId, score, totalQuestions);
   ```

   Example:
   ```javascript
   saveQuizScore(1, 8, 10); // Quiz 1, 8 correct out of 10
   ```

## Troubleshooting

### "Connection refused" error
- Make sure server is running: `npm start`
- Check that DATABASE_URL is correct in .env file

### "Cannot POST /api/save-score"
- Make sure server is running
- Check that API_URL matches your server URL

### No data showing in calendar
- Take a quiz first to generate data
- Check browser console for errors (F12)
- Verify server is saving data: Check database directly

### CORS errors
- CORS is enabled in server.js
- Make sure you're accessing from correct origin

## File Structure

```
c:\evalleRecords\EVALanguage\
├── server.js                 # Backend server
├── package.json             # Dependencies
├── .env                      # Environment variables (KEEP SECRET)
├── .env.example             # Template for .env
└── pages/
    ├── quiz1.html           # Quiz 1 with tracker
    ├── quiz2-7.html         # Other quizzes
    ├── progress.html        # Calendar view
    ├── progress-tracker.js  # Tracker utility
    ├── EVALanguage.html     # Main page
    └── api/
        └── tts.js           # Text-to-speech
```

## Next Steps

1. Add progress tracking to other quiz files (quiz2-7.html)
2. Customize the calendar styling
3. Add features like:
   - Export progress to CSV
   - Set daily goals
   - Achievements/badges
   - Study streak counter

---

**Need help?** Check:
- Console for error messages (F12)
- Server logs for backend errors
- Render PostgreSQL dashboard for data verification
