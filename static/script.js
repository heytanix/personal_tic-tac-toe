let gameActive = true;

document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const message = document.getElementById('message');
    const resetBtn = document.getElementById('reset-btn');

    cells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });

    resetBtn.addEventListener('click', resetGame);

    async function handleCellClick(e) {
        const cell = e.target;
        const position = parseInt(cell.dataset.index);

        if (!gameActive || cell.textContent !== '') {
            return;
        }

        // Disable board during processing
        gameActive = false;
        disableBoard();

        try {
            const response = await fetch('/make_move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ position: position })
            });

            const data = await response.json();

            // Update player move
            cell.textContent = 'X';
            cell.classList.add('x');

            // Small delay before computer move
            await new Promise(resolve => setTimeout(resolve, 300));

            // Update computer move if exists
            if (data.computer_move !== undefined) {
                const computerCell = document.querySelector(`[data-index="${data.computer_move}"]`);
                computerCell.textContent = 'O';
                computerCell.classList.add('o');
            }

            if (data.game_over) {
                handleGameOver(data);
            } else {
                gameActive = true;
                enableBoard();
            }

        } catch (error) {
            console.error('Error:', error);
            message.textContent = 'An error occurred!';
            gameActive = true;
            enableBoard();
        }
    }

    function handleGameOver(data) {
        if (data.winner === 'Player') {
            message.textContent = '🎉 You Win!';
            message.className = 'message win';
        } else if (data.winner === 'Computer') {
            message.textContent = '🤖 Computer Wins!';
            message.className = 'message lose';
        } else {
            message.textContent = '🤝 It\'s a Tie!';
            message.className = 'message tie';
        }

        // Highlight winning line
        if (data.winning_line) {
            data.winning_line.forEach(index => {
                const cell = document.querySelector(`[data-index="${index}"]`);
                cell.classList.add('winning');
            });
        }

        disableBoard();
    }

    async function resetGame() {
        try {
            const response = await fetch('/reset', {
                method: 'POST'
            });

            const data = await response.json();

            // Clear board
            cells.forEach(cell => {
                cell.textContent = '';
                cell.className = 'cell';
            });

            // Reset message
            message.textContent = '';
            message.className = 'message';

            gameActive = true;
            enableBoard();

        } catch (error) {
            console.error('Error:', error);
        }
    }

    function disableBoard() {
        cells.forEach(cell => {
            cell.classList.add('disabled');
        });
    }

    function enableBoard() {
        cells.forEach(cell => {
            if (cell.textContent === '') {
                cell.classList.remove('disabled');
            }
        });
    }
});
