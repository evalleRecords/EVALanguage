# API Documentation

## Base URL
- **Local Development**: `http://localhost:3000`
- **Production**: `https://your-render-service.onrender.com`

---

## Endpoints

### 1. Save Quiz Score
**Endpoint:** `POST /api/save-score`

**Description:** Save a quiz attempt with score and total questions

**Request Body:**
```json
{
  "quizId": 1,
  "score": 8,
  "totalQuestions": 10
}
```

**Response Success (201):**
```json
{
  "success": true,
  "data": {
    "id": 42,
    "created_at": "2026-01-31T14:30:00.000Z",
    "percentage": 80
  },
  "message": "Score saved: 8/10 (80%)"
}
```

**Response Error (400/500):**
```json
{
  "error": "Missing required fields" 
}
```

**Usage in JavaScript:**
```javascript
const response = await fetch('/api/save-score', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    quizId: 1,
    score: 8,
    totalQuestions: 10
  })
});
const data = await response.json();
```

---

### 2. Get Today's Progress
**Endpoint:** `GET /api/today-progress`

**Description:** Get all quiz scores from today

**Response:**
```json
{
  "date": "2026-01-31",
  "scores": [
    {
      "quiz_id": 1,
      "score": 8,
      "total_questions": 10,
      "percentage": 80,
      "created_at": "2026-01-31T14:30:00.000Z"
    },
    {
      "quiz_id": 2,
      "score": 9,
      "total_questions": 10,
      "percentage": 90,
      "created_at": "2026-01-31T15:45:00.000Z"
    }
  ],
  "count": 2
}
```

**Usage:**
```javascript
const response = await fetch('/api/today-progress');
const data = await response.json();
console.log(`Today you took ${data.count} quizzes`);
console.log(`Average: ${data.scores.reduce((sum, s) => sum + s.percentage, 0) / data.scores.length}%`);
```

---

### 3. Get Calendar Data
**Endpoint:** `GET /api/calendar-data?year=2026&month=1`

**Description:** Get aggregated scores for a specific month

**Query Parameters:**
- `year` (optional): 4-digit year (default: current year)
- `month` (optional): Month number 1-12 (default: current month)

**Response:**
```json
{
  "year": 2026,
  "month": 1,
  "data": [
    {
      "user_date": "2026-01-15",
      "quiz_count": 2,
      "avg_percentage": 85,
      "best_score": 9,
      "total_score": 17
    },
    {
      "user_date": "2026-01-16",
      "quiz_count": 1,
      "avg_percentage": 90,
      "best_score": 9,
      "total_score": 9
    }
  ]
}
```

**Usage:**
```javascript
const year = new Date().getFullYear();
const month = new Date().getMonth() + 1;
const response = await fetch(`/api/calendar-data?year=${year}&month=${month}`);
const data = await response.json();
// data.data contains the calendar days with scores
```

---

### 4. Get All Progress
**Endpoint:** `GET /api/all-progress`

**Description:** Get the last 30 days of progress (used for progress list)

**Response:**
```json
{
  "totalDays": 5,
  "progress": [
    {
      "user_date": "2026-01-31",
      "quiz_count": 2,
      "avg_percentage": 85,
      "total_score": 17
    },
    {
      "user_date": "2026-01-30",
      "quiz_count": 1,
      "avg_percentage": 80,
      "total_score": 8
    }
  ]
}
```

**Usage:**
```javascript
const response = await fetch('/api/all-progress');
const data = await response.json();
console.log(`You've practiced ${data.totalDays} days`);
data.progress.forEach(day => {
  console.log(`${day.user_date}: ${day.quiz_count} quizzes, average ${day.avg_percentage}%`);
});
```

---

### 5. Health Check
**Endpoint:** `GET /api/health`

**Description:** Check if server is running

**Response:**
```json
{
  "status": "Server is running"
}
```

**Usage:**
```javascript
const response = await fetch('/api/health');
const data = await response.json();
if (data.status === "Server is running") {
  console.log("Server is online!");
}
```

---

## Error Handling

All endpoints may return errors in this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad request (missing fields)
- `500` - Server error

**Example Error Handling:**
```javascript
try {
  const response = await fetch('/api/save-score', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ quizId: 1, score: 8, totalQuestions: 10 })
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  console.log('Success:', data);
} catch (error) {
  console.error('Failed to save score:', error);
}
```

---

## Database Schema

### quiz_scores table
```sql
CREATE TABLE quiz_scores (
  id SERIAL PRIMARY KEY,
  quiz_id INTEGER NOT NULL,           -- 1-10
  score INTEGER NOT NULL,              -- correct answers
  total_questions INTEGER NOT NULL,    -- total questions
  percentage INTEGER NOT NULL,         -- calculated percentage
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- when saved
  user_date DATE DEFAULT CURRENT_DATE  -- the date
);
```

### daily_progress table
```sql
CREATE TABLE daily_progress (
  id SERIAL PRIMARY KEY,
  quiz_id INTEGER,
  score INTEGER,
  total INTEGER,
  progress_date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Indexes
For better query performance:
- `idx_user_date` on `quiz_scores(user_date)`
- `idx_progress_date` on `daily_progress(progress_date)`

---

## Rate Limiting
Currently no rate limiting is implemented. For production, consider adding rate limiting middleware.

---

## Authentication
Currently no authentication is required. For production with multiple users, add authentication.

---

## CORS
CORS is enabled for all origins (`*`). For production, restrict to specific origins:

```javascript
const cors = require('cors');
const corsOptions = {
  origin: ['https://yourdomain.com'],
  credentials: true
};
app.use(cors(corsOptions));
```

---

## Environment Variables
The server uses these environment variables:

```
DATABASE_URL=postgresql://user:pass@host:5432/db
PORT=3000
```

---

## Code Example: Complete Integration

```html
<!DOCTYPE html>
<html>
<head>
  <script src="progress-tracker.js"></script>
</head>
<body>
  <button onclick="takeQuiz()">Take Quiz</button>

  <script>
    async function takeQuiz() {
      // ... quiz logic ...
      let score = 8;
      let total = 10;
      
      // Save to database
      try {
        await saveQuizScore(1, score, total);
        console.log("Score saved!");
      } catch (error) {
        console.error("Error saving score:", error);
      }
    }
  </script>
</body>
</html>
```

---

## Testing Endpoints with curl

```bash
# Health check
curl http://localhost:3000/api/health

# Save score
curl -X POST http://localhost:3000/api/save-score \
  -H "Content-Type: application/json" \
  -d '{"quizId":1,"score":8,"totalQuestions":10}'

# Get today's progress
curl http://localhost:3000/api/today-progress

# Get calendar data
curl http://localhost:3000/api/calendar-data?year=2026&month=1

# Get all progress
curl http://localhost:3000/api/all-progress
```

---

## Troubleshooting API Issues

**Error: "Cannot POST /api/save-score"**
- Make sure server is running: `npm start`
- Check URL is correct
- Verify Content-Type header is `application/json`

**Error: "Connection refused"**
- Server is not running
- Try: `npm start`

**Error: "CORS error"**
- CORS is enabled globally
- Check that you're using the correct API URL
- Check browser console for details

**Empty responses**
- Server may be crashed
- Check server logs
- Restart with: `npm start`

---

For more help, see DATABASE_SETUP.md or README.md
