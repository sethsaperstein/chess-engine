import { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';

export default function ChessBoard() {
  const [game, setGame] = useState(new Chess());
  const [socket, setSocket] = useState<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/game');
    
    ws.onopen = () => {
      console.log('Connected to server');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const newGame = new Chess(data.board);
      setGame(newGame);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  function makeMove(sourceSquare: string, targetSquare: string) {
    try {
      if (socket) {
        socket.send(JSON.stringify({
          move: sourceSquare + targetSquare
        }));
        return true;
      }
      return false;
    } catch (error) {
      return false;
    }
  }

  return (
    <div style={{ width: '600px', margin: 'auto' }}>
      <Chessboard 
        position={game.fen()}
        onPieceDrop={(sourceSquare, targetSquare) => {
          return makeMove(sourceSquare, targetSquare);
        }}
      />
    </div>
  );
}