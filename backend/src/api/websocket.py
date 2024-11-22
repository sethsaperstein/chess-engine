from fastapi import WebSocket
import chess
from ..chess_engine.game import ChessGame, GameMode
from ..bots.smart_bot import SmartBot
from ..bots.random_bot import RandomBot
import logging

logger = logging.getLogger(__name__)

class ChessGameWebSocket:
    def __init__(self, white_bot_type=None, black_bot_type=None):
        logger.info(f"Initializing new chess game with white_bot: {white_bot_type}, black_bot: {black_bot_type}")
        
        def get_bot(bot_type):
            if bot_type == 'smart':
                return SmartBot()
            elif bot_type == 'random':
                return RandomBot()
            return "human"
        
        white_player = get_bot(white_bot_type)
        black_player = get_bot(black_bot_type)
        
        mode = GameMode.HUMAN_VS_HUMAN
        if isinstance(white_player, (SmartBot, RandomBot)) and isinstance(black_player, (SmartBot, RandomBot)):
            mode = GameMode.BOT_VS_BOT
        elif isinstance(white_player, (SmartBot, RandomBot)) or isinstance(black_player, (SmartBot, RandomBot)):
            mode = GameMode.HUMAN_VS_BOT
            
        self.game = ChessGame(
            white_player=white_player,
            black_player=black_player,
            mode=mode
        )

    async def handle_connection(self, websocket: WebSocket):
        await websocket.accept()
        logger.info("WebSocket connection accepted")
        
        # If it's bot vs bot, make the first move
        if self.game.mode == GameMode.BOT_VS_BOT:
            self.game.play_turn()
            await self.send_game_update(websocket)
        
        try:
            while True:
                data = await websocket.receive_json()
                logger.info(f"Received message: {data}")
                
                if data.get('type') == 'bot_move':
                    # Handle bot move request
                    if self.game.is_current_player_bot() and not self.game.board.is_game_over():
                        self.game.play_turn()
                        await self.send_game_update(websocket)
                else:
                    # Handle human move
                    move = chess.Move.from_uci(data['move'])
                    if self.game.make_move(move):
                        logger.info(f"Move made: {move}")
                        
                        # Make bot moves until it's a human's turn or game is over
                        while self.game.is_current_player_bot() and not self.game.board.is_game_over():
                            logger.info("Bot's turn to play")
                            self.game.play_turn()
                        
                        await self.send_game_update(websocket)
                    else:
                        logger.warning(f"Illegal move attempted: {move}")
                        await websocket.send_json({
                            'type': 'error',
                            'message': 'Illegal move'
                        })
                
        except Exception as e:
            logger.error(f"Error in chess game: {e}", exc_info=True)
            await websocket.send_json({
                'type': 'error',
                'message': str(e)
            })

    async def send_game_update(self, websocket: WebSocket):
        last_move = self.game.board.peek().uci() if self.game.board.move_stack else None
        response = {
            'type': 'game_update',
            'board': self.game.get_board_state(),
            'current_player': self.game.current_player,
            'is_game_over': self.game.board.is_game_over(),
            'last_move': last_move
        }
        logger.info(f"Sending game update: {response}")
        await websocket.send_json(response)