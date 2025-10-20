import asyncio
from app.models import User, Message, Room

# In-memory storage for demo
USERS = {}   # username -> {"user": User, "ws": websocket}
ROOMS = {}   # room_name -> Room object

# ------------------------
# User registration
# ------------------------
async def register_user(username, websocket):
    user = User(username=username, email="", hashed_password="")
    USERS[username] = {"user": user, "ws": websocket}
    return user

async def unregister_user(username):
    USERS.pop(username, None)
    for room in ROOMS.values():
        room.members.discard(username)

# ------------------------
# Message handling
# ------------------------
async def handle_message(username, data):
    room_name = data.get("room")
    content = data.get("message", "")
    if room_name in ROOMS:
        room = ROOMS[room_name]
        msg = Message(user_id=USERS[username]["user"].id, content=content)
        # Send to all members
        for member in room.members:
            ws = USERS.get(member, {}).get("ws")
            if ws:
                await ws.send(f"{username}@{room_name}: {content}")

# ------------------------
# Room management
# ------------------------
async def handle_create_room(username, data):
    room_name = data.get("room")
    if room_name and room_name not in ROOMS:
        ROOMS[room_name] = Room(name=room_name, members={username})

async def handle_join_room(username, data):
    room_name = data.get("room")
    if room_name in ROOMS:
        ROOMS[room_name].members.add(username)

async def handle_leave_room(username, data):
    room_name = data.get("room")
    if room_name in ROOMS:
        ROOMS[room_name].members.discard(username)

# ------------------------
# Listing
# ------------------------
async def handle_list_rooms(username):
    ws = USERS.get(username, {}).get("ws")
    if ws:
        await ws.send(f"Rooms: {list(ROOMS.keys())}")

async def handle_list_users(username):
    ws = USERS.get(username, {}).get("ws")
    if ws:
        await ws.send(f"Users: {list(USERS.keys())}")

# ------------------------
# History (stub)
# ------------------------
async def handle_history(username, data):
    ws = USERS.get(username, {}).get("ws")
    if ws:
        await ws.send("No history implemented yet")
