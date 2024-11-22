import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { ChessGame } from './components/ChessGame'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ChessGame />
  </StrictMode>,
)
