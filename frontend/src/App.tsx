import { useState, useEffect } from 'react'
import { Chess, Square } from 'chess.js'
import { Chessboard } from 'react-chessboard'

interface AppProps {
  gameSettings: {
    whitePlayerType: 'human' | 'bot';
    blackPlayerType: 'human' | 'bot';
    whiteBotType?: string;
    blackBotType?: string;
    difficulty?: 'easy' | 'medium' | 'hard';
  } | null;
}

function App({ gameSettings }: AppProps) {
  const [game, setGame] = useState<Chess>(new Chess())
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    if (gameSettings?.blackPlayerType === 'bot' || gameSettings?.whitePlayerType === 'bot') {
      console.log('Attempting to connect to WebSocket...');
      const params = new URLSearchParams();
      if (gameSettings.whitePlayerType === 'bot') params.append('white_bot', gameSettings.whiteBotType || '');
      if (gameSettings.blackPlayerType === 'bot') params.append('black_bot', gameSettings.blackBotType || '');
      
      const websocket = new WebSocket(`ws://localhost:8001/ws/game?${params.toString()}`);
      
      websocket.onopen = () => {
        console.log('WebSocket Connected');
        setWsConnected(true);
      };

      websocket.onclose = () => {
        console.log('WebSocket Disconnected');
        setWsConnected(false);
      };

      websocket.onerror = (error) => {
        console.error('WebSocket Error:', error);
      };

      websocket.onmessage = (event) => {
        console.log('Received message:', event.data);
        const response = JSON.parse(event.data);
        
        if (response.type === 'game_update') {
          const gameCopy = new Chess(response.board);
          setGame(gameCopy);
          
          if (gameSettings?.whitePlayerType === 'bot' && 
              gameSettings?.blackPlayerType === 'bot' && 
              !gameCopy.isGameOver()) {
            websocket.send(JSON.stringify({ 
              type: 'bot_move' 
            }));
          }
        }
      };

      setWs(websocket);

      return () => {
        if (websocket.readyState === WebSocket.OPEN) {
          websocket.close();
        }
      };
    }
  }, [gameSettings]);

  function makeAMove(move: { from: string; to: string; promotion?: string }) {
    const gameCopy = new Chess(game.fen())
    try {
      const result = gameCopy.move(move)
      if (result) {
        setGame(gameCopy)
        return result
      }
    } catch (error) {
      return null
    }
    return null
  }

  function onDrop(sourceSquare: Square, targetSquare: Square): boolean {
    const move = makeAMove({
      from: sourceSquare,
      to: targetSquare,
      promotion: 'q'
    });

    if (move === null) return false;

    if (gameSettings?.blackPlayerType === 'bot' && ws && wsConnected) {
      const moveString = sourceSquare + targetSquare;
      console.log('Sending move to server:', moveString);
      try {
        ws.send(JSON.stringify({
          move: moveString
        }));
      } catch (error) {
        console.error('Error sending move:', error);
        return false;
      }
    }

    return true;
  }

  return (
    <div style={{ 
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'sans-serif',
      padding: '20px'
    }}>
      <h2 style={{ marginBottom: '20px' }}>
        {game.turn() === 'w' ? "White" : "Black"}'s Turn
      </h2>
      <div style={{
        width: '500px',
        marginBottom: '20px'
      }}>
        <Chessboard 
          position={game.fen()} 
          onPieceDrop={onDrop}
          boardWidth={500}
          customBoardStyle={{
            borderRadius: '4px',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.3)'
          }}
        />
      </div>
      {game.isGameOver() && (
        <h3>
          Game Over! 
          {game.isCheckmate() ? ` - ${game.turn() === 'w' ? "Black" : "White"} Wins!` : 
           game.isDraw() ? " - Draw!" : ""}
        </h3>
      )}
    </div>
  )
}

export default App
