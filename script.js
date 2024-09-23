let playerScore = 0;
let tieScore = 0;
let computerScore = 0;

const cells = document.querySelectorAll('.cell');
const playerScoreElement = document.getElementById('player-score');
const tieScoreElement = document.getElementById('tie-score');
const computerScoreElement = document.getElementById('computer-score');
const historyBody = document.getElementById('history-body');

// Handle cell click
cells.forEach(cell => {
    cell.addEventListener('click', () => {
        const index = cell.getAttribute('data-index');
        makeMove(index);
    });
});

// Make a move by sending it to the server
function makeMove(position) {
    fetch('/make_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ position: parseInt(position) })
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data.board);
        if (data.winner) {
            if (data.winner === 'X') {
                playerScore++;
                playerScoreElement.textContent = playerScore;
            } else if (data.winner === 'O') {
                computerScore++;
                computerScoreElement.textContent = computerScore;
            } else if (data.winner === 'Draw') {
                tieScore++;
                tieScoreElement.textContent = tieScore;
            }
            fetchGameHistory();  // Update the game history after each game
            setTimeout(resetGame, 2000);  // Reset game after 2 seconds
        }
    });
}

// Update the game board with new moves
function updateBoard(board) {
    cells.forEach((cell, index) => {
        cell.textContent = board[index];
    });
}

// Function to reset the game board
function resetGame() {
    fetch('/reset_game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data.board);
    });
}

// Fetch and display the game history
function fetchGameHistory() {
    fetch('/game_history')
        .then(response => response.json())
        .then(history => {
            historyBody.innerHTML = '';  // Clear the history table
            history.forEach(item => {
                const row = `<tr>
                    <td>${item.id}</td>
                    <td>${item.winner}</td>
                    <td>${item.duration}</td>
                </tr>`;
                historyBody.innerHTML += row;
            });
        });
}

// Initial load: Fetch game history when the page loads
fetchGameHistory();
