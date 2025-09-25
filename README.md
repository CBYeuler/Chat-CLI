# Project

Project Structure/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── logger.py
│   ├── models.py
│   ├── server.py
│   └── utils.py
├── client/
│   ├── __init__.py
│   └── cli.py
├── tests/
│   └── test_models.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── start_server.sh
├── start_client.sh
└── docker-compose.yml   

# chat-cli

Async WebSocket chat server + minimal CLI client using Python asyncio, websockets and MongoDB.

## Quickstart (dev)

1. Copy `.env.example` to `.env` and edit if needed.
2. Start MongoDB:
   - Locally: `docker-compose up -d mongo` OR run `docker-compose up -d` to bring up mongo.
3. Create virtualenv and install deps:
   
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

Start the Server:
`./start_server.sh`

In another terminal, start client:
`./start_client.sh`

Tests:
`pytest`


Protocol (JSON)

register: {"type":"register","username":"..."}

message: {"type":"message","room":"room","content":"text"}

create_room / join_room / leave_room / list_rooms / list_users / history

Next improvements

Add JWT/auth

Dockerize server + CI

Add pytest-asyncio integration tests

- Things to fix/add (priority):
  1. **Auth** — right now anyone can register as anyone. Will add tokens/JWT to prevent impersonation and secure WebSocket handshake.
  2. **Connection health** — heartbeats/pings and reconnect logic for clients.
  3. **Error handling & logging** — more structured logs, maybe Sentry for prod.
  4. **Testing** — integration tests with test Mongo and CI.
  5. **Scaling** — in-memory maps (room_members, active_connections) won’t work across multiple server instances. Add Redis/pubsub for horizontal scaling later.
  6. **Rate limiting per-IP** — consider abusive clients that create many usernames.

