from abc import ABC, abstractmethod
import chess
from enum import Enum

class GameMode(Enum):
    HUMAN_VS_HUMAN = "human_vs_human"
    HUMAN_VS_BOT = "human_vs_bot"
    BOT_VS_BOT = "bot_vs_bot"

class ChessBot(ABC):
    @abstractmethod
    def make_move(self, board: chess.Board) -> chess.Move:
        """Abstract method that bots must implement"""
        pass

class ChessGame:
    def __init__(self, white_player, black_player, mode: GameMode):
        self.board = chess.Board()
        self.white_player = white_player
        self.black_player = black_player
        self.current_player = 'white'
        self.mode = mode
    
    def make_move(self, move: chess.Move) -> bool:
        if self.board.is_legal(move):
            self.board.push(move)
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            return True
        return False
    
    def get_current_player_bot(self):
        """Returns the bot for the current player if it exists"""
        return self.white_player if self.current_player == 'white' else self.black_player
    
    def is_current_player_bot(self):
        """Check if current player is a bot"""
        current_bot = self.get_current_player_bot()
        return isinstance(current_bot, ChessBot)
    
    def get_legal_moves(self):
        return list(self.board.legal_moves)
    
    def get_board_state(self):
        return self.board.fen()
    
    def play_turn(self):
        """Plays a single turn. Returns True if move was made, False if game is over"""
        if self.board.is_game_over():
            return False
        
        current_bot = self.get_current_player_bot()
        if self.is_current_player_bot():
            # Bot's turn
            move = current_bot.make_move(self.board)
            self.make_move(move)
            return True
        
        # If we reach here, it's a human player's turn
        # Return without making a move - the frontend/UI should handle human moves
        return True
    