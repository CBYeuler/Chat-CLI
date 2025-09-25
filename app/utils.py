import asyncio
from datetime import datetime
from typing import Dict, List
from .config import RATE_LIMIT, RATE_LIMIT_WINDOW

lock = asyncio.Lock()
# In-memory store for rate limiting
user_message_times: Dict[str, List[datetime]] = defaultdict(list)

# Function to check if a user is rate limited
async def rate_limited(username: str) -> bool:
    async with lock:
        return _check_rate_limit(username)

    now = datetime.utcnow()
    time = user_message_times[username]
    # prune
    times = [t for t in times if (now - t).total_seconds() < RATE_LIMIT_WINDOW]
    user_message_times[username] = times
    if len(times) >= RATE_LIMIT:
        return True
    time.append(now)
    return False
