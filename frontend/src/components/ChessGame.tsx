import { useState, useEffect } from 'react';
import { GameSetup } from './GameSetup';
import '../styles/ChessGame.css';
import '../styles/GameSetup.css';
import App from '../App';

export function ChessGame() {
  const [gameStarted, setGameStarted] = useState(false);
  const [gameSettings, setGameSettings] = useState<{
    whitePlayerType: 'human' | 'bot';
    blackPlayerType: 'human' | 'bot';
    difficulty?: 'easy' | 'medium' | 'hard';
  } | null>(null);

  // Add this to verify backend connection
  useEffect(() => {
    const checkBackendConnection = async () => {
      try {
        const response = await fetch('/api/health-check');
        if (response.ok) {
          console.log('Backend connected successfully');
        } else {
          console.error('Backend connection failed');
        }
      } catch (error) {
        console.error('Backend connection error:', error);
      }
    };
    
    checkBackendConnection();
  }, []);

  const handleStartGame = (settings: {
    whitePlayerType: 'human' | 'bot';
    blackPlayerType: 'human' | 'bot';
    difficulty?: 'easy' | 'medium' | 'hard';
  }) => {
    setGameSettings(settings);
    setGameStarted(true);
  };

  if (!gameStarted) {
    return <GameSetup onStartGame={handleStartGame} />;
  }

  return <App gameSettings={gameSettings} />;
} 