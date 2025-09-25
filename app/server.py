import asyncio
import json
import logging
import websockets
from websockets import WebSocketServerProtocol
from app.config import PORT
from app.logger import logger
from app.handlers import (
    register_user,
    unregister_user,
    handle_message,
    handle_create_room,
    handle_join_room,
    handle_leave_room,
    handle_list_rooms,
    handle_list_users,
    handle_history,
)

async def handler(websocket: WebSocketServerProtocol, path: str):
    # Handle new WebSocket connection
    try:
        register_msg = await websocket.recv()
        register_data = json.loads(register_msg)
        # Ensure the first message is registration
        if register_data.get("type") != "register" or "username" not in register_data:
            await websocket.send(json.dumps({
                "type": "error", 
                "message": "First message must be registration with a username."
            }))
            return
        username = register_data["username"].strip()
        if not username:
            # Username cannot be empty
            await websocket.send(json.dumps({
                "type": "error", 
                "message": "Username cannot be empty."
            }))
            return
        
        # Register user in DB and in-memory maps
    user = await register_user(username, websocket)
    await websocket.send(json.dumps({
        "type": "registered", 
        "data": user.dict(by_alias=True)
    }))
    logger.info(f"User {username} connected.")
    
    # Main message handling loop
    async for message in websocket:
        # Handle incoming messages
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            # Dispatch based on message type
            if msg_type == "message":
                await handle_message(username, data)
            elif msg_type == "create_room":
                await handle_create_room(username, data)
            elif msg_type == "join_room":
                await handle_join_room(username, data)
            elif msg_type == "leave_room":
                await handle_leave_room(username, data)
            elif msg_type == "list_rooms":
                await handle_list_rooms(username)
            elif msg_type == "list_users":
                await handle_list_users(username)
            elif msg_type == "history":
                await handle_history(username, data)
            else:
                # Unknown message type
                await websocket.send(json.dumps({
                    "type": "error", 
                    "message": f"Unknown message type: {msg_type}"
                }))
        except json.JSONDecodeError:
            # Invalid JSON
            await websocket.send(json.dumps({
                "type": "error", 
                "message": "Invalid JSON format."
            }))
        except Exception as e:
            # Log and notify user of internal error
            logger.error(f"Error handling message from {username}: {e}")
            await websocket.send(json.dumps({
                "type": "error", 
                "message": "Internal server error."
            }))
    except websockets.ConnectionClosed:
        # Handle disconnection
        pass
    finally:
        # Unregister user on disconnect
        if 'username' in locals():
            await unregister_user(username)
            logger.info(f"User {username} disconnected.")

async def main():
    # Start the WebSocket server
    logger.info(f"Starting server on port {PORT}")
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
