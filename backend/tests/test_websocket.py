import asyncio
import websockets
import json
import pytest

@pytest.mark.asyncio
async def test_chess_websocket():
    uri = "ws://localhost:8000/ws/game"
    try:
        print(f"Attempting to connect to {uri}")
        async with websockets.connect(uri, ping_interval=None) as websocket:
            print("Successfully connected to WebSocket server")
            # Verify connection is open
            assert websocket.open, "WebSocket connection failed to open"
            
            # Test a legal move (e2 to e4)
            await websocket.send(json.dumps({"move": "e2e4"}))
            response = await websocket.recv()
            print("Response to e2e4:", json.loads(response))
            
            # Wait for bot's response
            bot_response = await websocket.recv()
            print("Bot's move:", json.loads(bot_response))
            
            # Test an illegal move
            await websocket.send(json.dumps({"move": "e2e4"}))  # Same pawn can't move twice
            response = await websocket.recv()
            print("Response to illegal move:", json.loads(response))
    except websockets.exceptions.ConnectionClosedError as e:
        pytest.fail(f"WebSocket connection closed unexpectedly: {e}")
    except ConnectionRefusedError as e:
        pytest.fail(f"Connection refused - Please ensure the server is running on port 8000. Error: {e}")
    except websockets.exceptions.InvalidStatusCode as e:
        pytest.fail(f"Invalid status code (HTTP {e.status_code}) - Check if the endpoint '/ws/game' exists")
    except websockets.exceptions.WebSocketException as e:
        pytest.fail(f"WebSocket error: {e}. Check if the server is running and the endpoint is correct")
    except Exception as e:
        pytest.fail(f"Unexpected error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test_chess_websocket())