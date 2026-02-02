const express = require('express');
const Database = require('sqlite3').verbose();
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

const dbPath = path.join(__dirname, 'quiz_scores.db');
const db = new Database.Database(dbPath);

// Initialize database tables
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS quiz_scores (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      quiz_id INTEGER NOT NULL,
      score INTEGER NOT NULL,
      total_questions INTEGER NOT NULL,
      percentage INTEGER NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      user_date DATE DEFAULT CURRENT_DATE
    );

    CREATE INDEX IF NOT EXISTS idx_user_date ON quiz_scores(user_date);
    CREATE INDEX IF NOT EXISTS idx_quiz_id ON quiz_scores(quiz_id);
  `, (err) => {
    if (err) console.error('Database initialization error:', err);
    else console.log('✅ Database initialized at:', dbPath);
  });
});

// Save quiz score
app.post('/api/save-score', (req, res) => {
  try {
    const { quizId, score, totalQuestions } = req.body;
    
    if (!quizId || score === undefined || !totalQuestions) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    const percentage = Math.round((score / totalQuestions) * 100);

    db.run(
      `INSERT INTO quiz_scores (quiz_id, score, total_questions, percentage) 
       VALUES (?, ?, ?, ?)`,
      [quizId, score, totalQuestions, percentage],
      function(err) {
        if (err) {
          console.error('Error saving score:', err);
          res.status(500).json({ error: 'Failed to save score' });
        } else {
          res.json({
            success: true,
            data: {
              id: this.lastID,
              percentage: percentage
            },
            message: `Score saved: ${score}/${totalQuestions} (${percentage}%)`
          });
        }
      }
    );
  } catch (err) {
    console.error('Error saving score:', err);
    res.status(500).json({ error: 'Failed to save score' });
  }
});

// Get today's progress
app.get('/api/today-progress', (req, res) => {
  try {
    const today = new Date().toISOString().split('T')[0];

    db.all(
      `SELECT quiz_id, score, total_questions, percentage, created_at 
       FROM quiz_scores 
       WHERE user_date = ? 
       ORDER BY created_at DESC`,
      [today],
      (err, rows) => {
        if (err) {
          console.error('Error fetching today progress:', err);
          res.status(500).json({ error: 'Failed to fetch progress' });
        } else {
          res.json({
            date: today,
            scores: rows || [],
            count: (rows || []).length
          });
        }
      }
    );
  } catch (err) {
    console.error('Error fetching today progress:', err);
    res.status(500).json({ error: 'Failed to fetch progress' });
  }
});

// Get calendar data for a month
app.get('/api/calendar-data', (req, res) => {
  try {
    const year = req.query.year || new Date().getFullYear();
    const month = req.query.month || new Date().getMonth() + 1;

    const startDate = `${year}-${String(month).padStart(2, '0')}-01`;
    const endDate = new Date(year, month, 0).toISOString().split('T')[0];

    db.all(
      `SELECT 
        user_date,
        COUNT(*) as quiz_count,
        CAST(AVG(percentage) AS INTEGER) as avg_percentage,
        MAX(score) as best_score,
        SUM(score) as total_score
      FROM quiz_scores 
      WHERE user_date >= ? AND user_date <= ?
      GROUP BY user_date
      ORDER BY user_date`,
      [startDate, endDate],
      (err, rows) => {
        if (err) {
          console.error('Error fetching calendar data:', err);
          res.status(500).json({ error: 'Failed to fetch calendar data' });
        } else {
          res.json({
            year,
            month,
            data: rows || []
          });
        }
      }
    );
  } catch (err) {
    console.error('Error fetching calendar data:', err);
    res.status(500).json({ error: 'Failed to fetch calendar data' });
  }
});

// Get all progress data
app.get('/api/all-progress', (req, res) => {
  try {
    db.all(
      `SELECT 
        user_date,
        COUNT(*) as quiz_count,
        CAST(AVG(percentage) AS INTEGER) as avg_percentage,
        SUM(score) as total_score
      FROM quiz_scores 
      GROUP BY user_date
      ORDER BY user_date DESC
      LIMIT 30`,
      (err, rows) => {
        if (err) {
          console.error('Error fetching all progress:', err);
          res.status(500).json({ error: 'Failed to fetch progress' });
        } else {
          res.json({
            totalDays: (rows || []).length,
            progress: rows || []
          });
        }
      }
    );
  } catch (err) {
    console.error('Error fetching all progress:', err);
    res.status(500).json({ error: 'Failed to fetch progress' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'Server is running',
    database: 'SQLite (local file)',
    location: dbPath
  });
});

// Serve static files
app.use(express.static(path.join(__dirname, 'pages')));

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`📁 Database: ${dbPath}`);
  console.log(`Server running on port ${PORT}`);
});
