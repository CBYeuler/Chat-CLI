#!/usr/bin/env python3
"""
client/cli.py

Simple async CLI websocket client for the chat server.

How to run:
    python -m client.cli

Features:
- Register a username on connect.
- Commands:
    /create <room>   -> create a room
    /join <room>     -> join a room
    /leave <room>    -> leave a room
    /rooms           -> list rooms
    /users <room>    -> list users in room
    /history <room>  -> get history for room
    /room <room>     -> set your current room (for sending messages)
    /quit            -> exit cleanly
- Plain lines (not starting with /) are sent as messages to the current room.
- Reads server URI and optional username from environment (via .env) if present.
"""

import asyncio
import json
import os
import sys
from typing import Optional
import websockets
from dotenv import load_dotenv

load_dotenv()  # optional .env in project root

DEFAULT_URI = os.getenv("CLIENT_SERVER_URI", "ws://127.0.0.1:8765")
DEFAULT_ROOM = os.getenv("DEFAULT_ROOM", "global")

PROMPT = "> "


def pretty_print_system(obj: dict):
    """Print non-message server events in a readable single-line format."""
    typ = obj.get("type")
    if typ == "error":
        print(f"[ERROR] {obj.get('message')}")
    elif typ in ("registered", "room_created", "room_joined", "room_left", "room_list", "user_list", "history"):
        print(f"[SERVER] {json.dumps(obj, ensure_ascii=False)}")
    else:
        # fallback
        print(f"[SERVER] {obj}")

# Async input reader
async def input_reader(loop):
    """
    Async wrapper around blocking sys.stdin.readline using executor.
    Returns a stripped line or empty string on EOF.
    """
    return (await loop.run_in_executor(None, sys.stdin.readline)).rstrip("\n")

# Send loop
async def send_loop(ws: websockets.WebSocketClientProtocol, username: str):
    """
    Reads user input and sends relevant JSON commands to server.
    Maintains a `current_room` used for plain messages.
    """
    loop = asyncio.get_event_loop()
    current_room: Optional[str] = DEFAULT_ROOM
    print(f"(Current room: {current_room}) — type /help for commands")
    # Main input loop
    while True:
        try:
            line = await input_reader(loop)
            if line is None:
                continue
            line = line.strip()
            if not line:
                continue

            # Commands
            if line.startswith("/"):
                parts = line.split(maxsplit=1)
                cmd = parts[0].lower()

                if cmd == "/quit":
                    await ws.close()
                    return

                if cmd == "/help":
                    help_text = (
                        "/create <room>   create a room\n"
                        "/join <room>     join room\n"
                        "/leave <room>    leave room\n"
                        "/rooms           list rooms\n"
                        "/users <room>    list users in a room\n"
                        "/history <room>  get room history\n"
                        "/room <room>     set current room for messages\n"
                        "/quit            exit\n"
                    )
                    print(help_text)
                    continue

                arg = parts[1].strip() if len(parts) > 1 else ""
                # Handle commands with arguments
                if cmd == "/create" and arg:
                    await ws.send(json.dumps({"type": "create_room", "name": arg}, ensure_ascii=False))
                    continue
                # Handle commands with arguments
                if cmd == "/join" and arg:
                    await ws.send(json.dumps({"type": "join_room", "name": arg}, ensure_ascii=False))
                    current_room = arg
                    print(f"(Current room set to: {current_room})")
                    continue
                # Handle commands with arguments
                if cmd == "/leave" and arg:
                    await ws.send(json.dumps({"type": "leave_room", "name": arg}, ensure_ascii=False))
                    if current_room == arg:
                        current_room = None
                        print("(Current room cleared)")
                    continue
                # Handle commands without arguments
                if cmd == "/rooms":
                    await ws.send(json.dumps({"type": "list_rooms"}, ensure_ascii=False))
                    continue
                # Handle commands with arguments
                if cmd == "/users" and arg:
                    await ws.send(json.dumps({"type": "list_users", "name": arg}, ensure_ascii=False))
                    continue
                # Handle commands with arguments
                if cmd == "/history" and arg:
                    await ws.send(json.dumps({"type": "history", "name": arg, "limit": 50}, ensure_ascii=False))
                    continue
                # Handle commands with arguments
                if cmd == "/room" and arg:
                    current_room = arg
                    print(f"(Current room set to: {current_room})")
                    continue

                print("Unknown or malformed command. Type /help for commands.")
                continue

            # Non-command: send as chat message to current_room
            if not current_room:
                print("No current room set. Use /join <room> or /room <room>.")
                continue

            payload = {"type": "message", "room": current_room, "content": line}
            await ws.send(json.dumps(payload, ensure_ascii=False))
        # Handle connection closed or other exceptions
        except websockets.ConnectionClosed:
            print("Connection closed. Exiting send loop.")
            return
        except Exception as e:
            print(f"Send loop error: {e}")
            return

# Receive loop
async def recv_loop(ws: websockets.WebSocketClientProtocol):
    """
    Receives messages from server and prints them.
    Expects messages with shape: {"type":"message","data":{...}} for chat messages.
    """
    try:
        async for raw in ws:
            try:
                data = json.loads(raw)
            except Exception:
                print(f"<raw> {raw}")
                continue

            typ = data.get("type")
            if typ == "message":
                d = data.get("data", {})
                room = d.get("room", "?")
                sender = d.get("sender", "unknown")
                content = d.get("content", "")
                print(f"[{room}] {sender}: {content}")
            else:
                pretty_print_system(data)
    except websockets.ConnectionClosed:
        print("Connection closed by server.")
    except Exception as e:
        print(f"Receive loop error: {e}")

# Main entry point
async def main():
    """
    Connects to server, registers username, and runs send/recv loops concurrently.
    """
    default_uri = DEFAULT_URI
    uri = input(f"server uri (default {default_uri}): ").strip() or default_uri
    username = input("username: ").strip()
    if not username:
        print("username required. exiting.")
        return

    try:
        async with websockets.connect(uri) as ws:
            # Register
            await ws.send(json.dumps({"type": "register", "username": username}, ensure_ascii=False))

            # Wait for registered ack (optional — not strictly required if server doesn't ack)
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
                data = json.loads(raw)
                if data.get("type") == "registered":
                    print(f"Registered as {username}.")
                else:
                    # print server message (could be error)
                    pretty_print_system(data)
            except asyncio.TimeoutError:
                # server didn't reply in time — proceed anyway
                pass

            # Run send and receive concurrently
            send_task = asyncio.create_task(send_loop(ws, username))
            recv_task = asyncio.create_task(recv_loop(ws))

            done, pending = await asyncio.wait(
                [send_task, recv_task],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for t in pending:
                t.cancel()

    except Exception as e:
        print(f"Could not connect to server at {uri}: {e}")

#  Entry point
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nbye")
