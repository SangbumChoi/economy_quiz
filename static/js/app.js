class QuizApp {
    constructor() {
        this.currentQuiz = null;
        this.stats = {
            correct: 0,
            incorrect: 0
        };
        this.loadStats();
        this.loadRandomQuiz();
    }

    async loadRandomQuiz() {
        try {
            const response = await fetch('/api/quizzes/random');
            if (!response.ok) {
                throw new Error('퀴즈를 불러올 수 없습니다.');
            }
            this.currentQuiz = await response.json();
            this.displayQuiz();
        } catch (error) {
            console.error('Error loading quiz:', error);
            this.showError('퀴즈를 불러오는 중 오류가 발생했습니다.');
        }
    }

    displayQuiz() {
        const questionText = document.getElementById('questionText');
        const resultSection = document.getElementById('resultSection');
        const trueBtn = document.getElementById('trueBtn');
        const falseBtn = document.getElementById('falseBtn');

        questionText.textContent = this.currentQuiz.question;
        resultSection.style.display = 'none';
        trueBtn.disabled = false;
        falseBtn.disabled = false;
        
        // Reset button styles
        trueBtn.style.opacity = '1';
        falseBtn.style.opacity = '1';
        trueBtn.style.transform = 'scale(1)';
        falseBtn.style.transform = 'scale(1)';
    }

    selectAnswer(userAnswer) {
        if (!this.currentQuiz) return;

        const trueBtn = document.getElementById('trueBtn');
        const falseBtn = document.getElementById('falseBtn');
        const resultSection = document.getElementById('resultSection');
        const resultMessage = document.getElementById('resultMessage');
        const explanation = document.getElementById('explanation');

        // Disable buttons
        trueBtn.disabled = true;
        falseBtn.disabled = true;

        const isCorrect = userAnswer === this.currentQuiz.answer;
        
        // Update stats
        if (isCorrect) {
            this.stats.correct++;
        } else {
            this.stats.incorrect++;
        }
        this.saveStats();
        this.updateStatsDisplay();

        // Show result
        resultSection.style.display = 'block';
        
        if (isCorrect) {
            resultMessage.textContent = '정답입니다! 🎉';
            resultMessage.className = 'result-message correct';
        } else {
            resultMessage.textContent = '틀렸습니다! 😅';
            resultMessage.className = 'result-message incorrect';
        }

        // Show explanation if available
        if (this.currentQuiz.explanation) {
            explanation.textContent = `설명: ${this.currentQuiz.explanation}`;
        } else {
            explanation.textContent = '설명이 없습니다.';
        }

        // Highlight correct answer
        if (this.currentQuiz.answer) {
            trueBtn.style.background = 'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)';
            trueBtn.style.transform = 'scale(1.05)';
        } else {
            falseBtn.style.background = 'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)';
            falseBtn.style.transform = 'scale(1.05)';
        }

        // Dim incorrect answer
        if (this.currentQuiz.answer) {
            falseBtn.style.opacity = '0.5';
        } else {
            trueBtn.style.opacity = '0.5';
        }
    }

    loadNextQuiz() {
        this.loadRandomQuiz();
    }

    updateStatsDisplay() {
        document.getElementById('correctCount').textContent = this.stats.correct;
        document.getElementById('incorrectCount').textContent = this.stats.incorrect;
        
        const total = this.stats.correct + this.stats.incorrect;
        const accuracy = total > 0 ? Math.round((this.stats.correct / total) * 100) : 0;
        document.getElementById('accuracy').textContent = `${accuracy}%`;
    }

    saveStats() {
        localStorage.setItem('quizStats', JSON.stringify(this.stats));
    }

    loadStats() {
        const savedStats = localStorage.getItem('quizStats');
        if (savedStats) {
            this.stats = JSON.parse(savedStats);
        }
        this.updateStatsDisplay();
    }

    resetStats() {
        this.stats = { correct: 0, incorrect: 0 };
        this.saveStats();
        this.updateStatsDisplay();
    }

    showError(message) {
        const questionText = document.getElementById('questionText');
        questionText.textContent = message;
        questionText.style.color = '#e74c3c';
    }
}

// Global functions for HTML onclick events
let quizApp;

function selectAnswer(answer) {
    quizApp.selectAnswer(answer);
}

function loadNextQuiz() {
    quizApp.loadNextQuiz();
}

function loadRandomQuiz() {
    quizApp.loadRandomQuiz();
}

function resetStats() {
    quizApp.resetStats();
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', function() {
    quizApp = new QuizApp();
});
