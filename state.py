#"\"\"\"Runtime state — conversation, task registry, photo cache.\"\"\"
import asyncio
from typing import Any

# Conversation state: user_id -> {\"action\": ..., ...}
conv: dict[int, dict[str, Any]] = {}

# Task registry: bot_id -> set of running tasks (raid, broadcast etc.)
_tasks: dict[int, set[asyncio.Task]] = {}


def register_task(bot_id: int, task: asyncio.Task) -> None:
    _tasks.setdefault(bot_id, set()).add(task)
    task.add_done_callback(lambda t: _tasks.get(bot_id, set()).discard(t))


async def cancel_all(bot_id: int) -> int:
    tasks = list(_tasks.get(bot_id, set()))
    for t in tasks:
        t.cancel()
    for t in tasks:
        try:
            await t
        except (asyncio.CancelledError, Exception):
            pass
    _tasks.pop(bot_id, None)
    return len(tasks)


# Profile photo cache: bot_id -> file_id
_photos: dict[int, str] = {}


def cache_profile_photo(bot_id: int, file_id: str) -> None:
    _photos[bot_id] = file_id


def get_profile_photo(bot_id: int) -> str | None:
    return _photos.get(bot_id)


# Running clone clients: bot_id -> Client
running_clones: dict[int, Any] = {}
