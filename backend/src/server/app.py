from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from ..api.websocket import ChessGameWebSocket
import logging
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get('/api/health-check')
def health_check():
    return {"status": "ok"}

@app.get('/api/bot-types')
def get_bot_types():
    return {
        "bot_types": [
            {"id": "smart", "name": "Smart AI"},
            {"id": "random", "name": "Random AI"}
        ]
    }

@app.websocket("/ws/game")
async def websocket_endpoint(
    websocket: WebSocket,
    white_bot: Optional[str] = None,
    black_bot: Optional[str] = None
):
    logger.info("New WebSocket connection")
    chess_game = ChessGameWebSocket(white_bot, black_bot)
    await chess_game.handle_connection(websocket) 