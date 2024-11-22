# Chess Engine Project

A full-stack chess application featuring human vs human, human vs bot, and bot vs bot gameplay with multiple AI implementations.

## Features
- 🎮 Multiple game modes (Human vs Human, Human vs Bot, Bot vs Bot)
- 🤖 Multiple bot types (Smart AI, Random AI)
- 🌐 Real-time gameplay using WebSocket
- 🎯 Extensible bot framework for custom AI implementations

## Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- pip
- npm or yarn

### Backend Setup
1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install fastapi uvicorn websockets python-chess
```

4. Start the backend server:

```bash
uvicorn src.server.app:app --reload --port 8001
```

### Frontend Setup
1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

## Common Issues and Solutions

### WebSocket Connection Failed
If you see "WebSocket connection failed" in the console:
1. Verify the backend server is running on port 8001
2. Check if the WebSocket URL in `App.tsx` matches your backend URL
3. Ensure CORS settings in `backend/src/server/app.py` include your frontend origin

### Bot Moves Not Working
If bots aren't making moves:
1. Check the browser console for WebSocket messages
2. Verify bot types in game setup match the backend's available bot types
3. Ensure the WebSocket connection is established before starting a bot game

### Python Import Errors
If you get module import errors:
1. Ensure you're running Python from the project root
2. Verify your virtual environment is activated
3. Check that all dependencies are installed in the virtual environment

## Creating Your Own Bot

To implement a custom bot:

1. Create a new file in `backend/src/bots/` (e.g., `my_bot.py`)

2. Implement the ChessBot interface:

```python
from ..chess_engine.game import ChessBot
import chess

class MyBot(ChessBot):
    def make_move(self, board: chess.Board) -> chess.Move:
        # Your move selection logic here
        legal_moves = list(board.legal_moves)
        # Return a valid chess.Move object
        return legal_moves[0] # Example: returns first legal move
```

3. Register your bot in `backend/src/api/websocket.py`:

```python
def get_bot(bot_type):
    if bot_type == 'smart':
        return SmartBot()
    elif bot_type == 'random':
        return RandomBot()
    elif bot_type == 'my_bot': # Add your bot type
        return MyBot()
    return "human"
```

4. Add your bot to the available types in `backend/src/server/app.py`:

```python
@app.get('/api/bot-types')
def get_bot_types():
    return {
        "bot_types": [
            {"id": "smart", "name": "Smart AI"},
            {"id": "random", "name": "Random AI"},
            {"id": "my_bot", "name": "My Custom Bot"} # Add your bot
        ]
    }
```

## Project Structure

├── backend/  
│ └── src/  
│ ├── api/  
│ ├── bots/  
│ ├── chess_engine/  
│ └── server/  
└── frontend/  
└── src/  
├── components/  
├── styles/  
└── App.tsx  
