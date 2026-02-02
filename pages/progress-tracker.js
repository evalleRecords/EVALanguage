/**
 * Progress Tracker Utility
 * Use this to save quiz scores to the database
 */

// Configure your API endpoint
const PROGRESS_API_URL = 'http://localhost:3000/api'; // Change this to your deployed server URL

/**
 * Save quiz score to database
 * @param {number} quizId - Quiz ID (1-10)
 * @param {number} score - Number of correct answers
 * @param {number} totalQuestions - Total number of questions
 */
async function saveQuizScore(quizId, score, totalQuestions) {
    try {
        const response = await fetch(`${PROGRESS_API_URL}/save-score`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                quizId,
                score,
                totalQuestions
            })
        });

        if (!response.ok) {
            throw new Error(`Failed to save score: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Score saved:', data);
        
        // Show success notification
        showNotification(`✅ Skoor salvestatud: ${score}/${totalQuestions}`);
        
        return data;
    } catch (error) {
        console.error('Error saving score:', error);
        showNotification(`❌ Viga skoori salvestamisel: ${error.message}`);
    }
}

/**
 * Get today's progress
 */
async function getTodayProgress() {
    try {
        const response = await fetch(`${PROGRESS_API_URL}/today-progress`);
        const data = await response.json();
        console.log('Today progress:', data);
        return data;
    } catch (error) {
        console.error('Error fetching today progress:', error);
    }
}

/**
 * Show notification
 */
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #333;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        z-index: 9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
