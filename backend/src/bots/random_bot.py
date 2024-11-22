import random
import chess
from ..chess_engine.game import ChessBot
import logging

logger = logging.getLogger(__name__)

class RandomBot(ChessBot):
    def make_move(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)
        move = random.choice(legal_moves)
        logger.info(f"RandomBot selected move: {move.uci()}")
        return move 