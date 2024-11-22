import { useState, useEffect } from 'react';
import '../styles/GameSetup.css';

interface BotType {
  id: string;
  name: string;
}

interface GameSetupProps {
  onStartGame: (settings: {
    whitePlayerType: 'human' | 'bot';
    blackPlayerType: 'human' | 'bot';
    difficulty?: 'easy' | 'medium' | 'hard';
  }) => void;
}

export function GameSetup({ onStartGame }: GameSetupProps) {
  const [botTypes, setBotTypes] = useState<BotType[]>([]);
  const [whitePlayerType, setWhitePlayerType] = useState<'human' | 'bot'>('human');
  const [blackPlayerType, setBlackPlayerType] = useState<'human' | 'bot'>('human');
  const [whiteBotType, setWhiteBotType] = useState<string>('');
  const [blackBotType, setBlackBotType] = useState<string>('');

  useEffect(() => {
    const fetchBotTypes = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/bot-types');
        const data = await response.json();
        setBotTypes(data.bot_types);
      } catch (error) {
        console.error('Failed to fetch bot types:', error);
        // Fallback bot types if API fails
        setBotTypes([
          { id: 'smart', name: 'Smart AI' },
          { id: 'random', name: 'Random AI' }
        ]);
      }
    };

    fetchBotTypes();
  }, []);

  const handleStartGame = () => {
    onStartGame({
      whitePlayerType,
      blackPlayerType,
      ...(whitePlayerType === 'bot' && { whiteBotType }),
      ...(blackPlayerType === 'bot' && { blackBotType })
    });
  };

  return (
    <div className="game-setup-container">
      <div className="game-setup-menu">
        <h1>Chess Game Setup</h1>
        
        <div className="player-setup">
          <div className="player-section">
            <h3>White Player</h3>
            <select 
              value={whitePlayerType} 
              onChange={(e) => setWhitePlayerType(e.target.value as 'human' | 'bot')}
            >
              <option value="human">Human</option>
              <option value="bot">Bot</option>
            </select>
            
            {whitePlayerType === 'bot' && (
              <select 
                value={whiteBotType}
                onChange={(e) => setWhiteBotType(e.target.value)}
              >
                <option value="">Select Bot Type</option>
                {botTypes.map(bot => (
                  <option key={bot.id} value={bot.id}>{bot.name}</option>
                ))}
              </select>
            )}
          </div>

          <div className="player-section">
            <h3>Black Player</h3>
            <select 
              value={blackPlayerType}
              onChange={(e) => setBlackPlayerType(e.target.value as 'human' | 'bot')}
            >
              <option value="human">Human</option>
              <option value="bot">Bot</option>
            </select>
            
            {blackPlayerType === 'bot' && (
              <select 
                value={blackBotType}
                onChange={(e) => setBlackBotType(e.target.value)}
              >
                <option value="">Select Bot Type</option>
                {botTypes.map(bot => (
                  <option key={bot.id} value={bot.id}>{bot.name}</option>
                ))}
              </select>
            )}
          </div>
        </div>

        <button 
          onClick={handleStartGame}
          disabled={
            (whitePlayerType === 'bot' && !whiteBotType) || 
            (blackPlayerType === 'bot' && !blackBotType)
          }
        >
          Start Game
        </button>
      </div>
    </div>
  );
} 