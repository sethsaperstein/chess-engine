import chess
import random
from ..chess_engine.game import ChessBot
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class SmartBot(ChessBot):
    # Piece-Square tables for positional scoring
    PAWN_TABLE = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ]

    KNIGHT_TABLE = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]

    BISHOP_TABLE = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]

    ROOK_TABLE = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0
    ]

    QUEEN_TABLE = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ]

    KING_TABLE_MIDDLEGAME = [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20
    ]

    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    PIECE_TABLES = {
        chess.PAWN: PAWN_TABLE,
        chess.KNIGHT: KNIGHT_TABLE,
        chess.BISHOP: BISHOP_TABLE,
        chess.ROOK: ROOK_TABLE,
        chess.QUEEN: QUEEN_TABLE,
        chess.KING: KING_TABLE_MIDDLEGAME
    }

    def get_piece_square_value(self, piece: chess.Piece, square: chess.Square, is_endgame: bool) -> int:
        """Get the position value for a piece on a given square."""
        piece_type = piece.piece_type
        if piece.color:
            square = chess.square_mirror(square)
        
        return self.PIECE_TABLES[piece_type][square]

    def is_endgame(self, board: chess.Board) -> bool:
        """Determine if the current position is in the endgame."""
        queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
        minors = len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.KNIGHT, chess.BLACK)) + \
                len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.BLACK))
        return queens == 0 or (queens == 2 and minors <= 2)

    def evaluate_position(self, board: chess.Board) -> float:
        """Evaluates the current board position."""
        if board.is_checkmate():
            return -9999999 if board.turn else 9999999
        if board.is_stalemate() or board.is_insufficient_material():
            return 0
        
        is_endgame = self.is_endgame(board)
        score = 0
        
        # Material and position evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
                
            value = self.PIECE_VALUES[piece.piece_type]
            position_value = self.get_piece_square_value(piece, square, is_endgame)
            
            if piece.color:
                score += value + position_value
            else:
                score -= value + position_value

        # Mobility (number of legal moves)
        board_copy = board.copy()
        board_copy.turn = chess.WHITE
        white_mobility = len(list(board_copy.legal_moves))
        board_copy.turn = chess.BLACK
        black_mobility = len(list(board_copy.legal_moves))
        score += (white_mobility - black_mobility) * 10

        # Pawn structure
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        black_pawns = board.pieces(chess.PAWN, chess.BLACK)
        score += (len(white_pawns) - len(black_pawns)) * 5

        # King safety
        if not is_endgame:
            white_king_square = board.king(chess.WHITE)
            black_king_square = board.king(chess.BLACK)
            score += self.evaluate_king_safety(board, white_king_square, True)
            score -= self.evaluate_king_safety(board, black_king_square, False)

        return score if board.turn else -score

    def evaluate_king_safety(self, board: chess.Board, king_square: chess.Square, is_white: bool) -> int:
        """Evaluate king safety based on pawn shield and piece attacks."""
        score = 0
        rank = chess.square_rank(king_square)
        file = chess.square_file(king_square)
        
        # Check pawn shield
        for f in range(max(0, file - 1), min(8, file + 2)):
            pawn_square = chess.square(f, rank + (1 if is_white else -1))
            if board.piece_at(pawn_square) == chess.Piece(chess.PAWN, is_white):
                score += 30

        # Penalty for open files near king
        for f in range(max(0, file - 1), min(8, file + 2)):
            if not any(board.piece_at(chess.square(f, r)) == chess.Piece(chess.PAWN, is_white) 
                      for r in range(8)):
                score -= 25

        return score

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[chess.Move]]:
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None

        best_move = None
        if maximizing:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def make_move(self, board: chess.Board) -> chess.Move:
        """Makes the best move using minimax with alpha-beta pruning."""
        depth = 4  # Adjust based on desired strength/performance
        _, best_move = self.minimax(board, depth, float('-inf'), float('inf'), True)
        
        if best_move is None:
            # Fallback to first legal move if something goes wrong
            best_move = list(board.legal_moves)[0]
            
        logger.info(f"SmartBot selected move: {best_move.uci()}")
        return best_move