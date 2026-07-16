"""MongoDB (motor) layer — collections + helpers."""
from datetime import datetime, timezone
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient
from .config import Config

_client = AsyncIOMotorClient(Config.MONGO_URL, serverSelectionTimeoutMS=5000)
_db = _client[Config.DB_NAME]

users = _db["users"]
clones = _db["clones"]
admins = _db["admins"]
fsub = _db["force_channels"]
bans = _db["bans"]
requests_col = _db["join_requests"]
stats = _db["stats"]
flags = _db["flags"]
logs = _db["logs"]


def now() -> datetime:
    return datetime.now(timezone.utc)


async def ensure_indexes() -> None:
    await users.create_index("_id")
    await clones.create_index("_id")
    await admins.create_index("_id")
    await fsub.create_index([("bot_id", 1), ("chat_id", 1)], unique=True)
    await bans.create_index("_id")


# ─── Users ───
async def add_user(uid: int, username: str = "") -> None:
    await users.update_one({"_id": uid}, {"$set": {"username": username},
                                          "$setOnInsert": {"joined_at": now()}}, upsert=True)


async def all_users() -> list[int]:
    return [d["_id"] async for d in users.find({}, {"_id": 1})]


async def user_count() -> int:
    return await users.count_documents({})


# ─── Clones ───
async def add_clone(bot_id: int, token: str, owner_id: int, username: str) -> None:
    await clones.update_one({"_id": bot_id},
        {"$set": {"token": token, "owner_id": owner_id, "username": username,
                  "stopped": False},
         "$setOnInsert": {"created_at": now()}}, upsert=True)


async def remove_clone(bot_id: int) -> None:
    await clones.delete_one({"_id": bot_id})


async def list_clones() -> list[dict]:
    return [d async for d in clones.find()]


async def clone_count() -> int:
    return await clones.count_documents({})


async def set_stop_flag(bot_id: int, val: bool) -> None:
    await flags.update_one({"_id": bot_id}, {"$set": {"stop": val, "updated": now()}}, upsert=True)


async def get_stop_flag(bot_id: int) -> bool:
    d = await flags.find_one({"_id": bot_id})
    return bool(d and d.get("stop"))


# ─── Admins ───
async def add_admin(uid: int) -> None:
    await admins.update_one({"_id": uid}, {"$set": {"added_at": now()}}, upsert=True)


async def remove_admin(uid: int) -> None:
    await admins.delete_one({"_id": uid})


async def list_admins() -> list[dict]:
    return [d async for d in admins.find()]


async def is_admin(uid: int) -> bool:
    if uid == Config.DEV_ID:
        return True
    return await admins.find_one({"_id": uid}) is not None


# ─── Force-sub channels ───
async def add_force_channel(bot_id: int, chat_id: int, title: str, invite: str = "") -> None:
    await fsub.update_one({"bot_id": bot_id, "chat_id": chat_id},
        {"$set": {"chat_title": title, "invite_link": invite, "added_at": now()}}, upsert=True)


async def del_force_channel(bot_id: int, chat_id: int) -> None:
    await fsub.delete_one({"bot_id": bot_id, "chat_id": chat_id})


async def list_force_channels(bot_id: int) -> list[dict]:
    return [d async for d in fsub.find({"bot_id": bot_id})]


# ─── Bans ───
async def ban_user(uid: int, reason: str = "") -> None:
    await bans.update_one({"_id": uid}, {"$set": {"reason": reason, "at": now()}}, upsert=True)


async def unban_user(uid: int) -> None:
    await bans.delete_one({"_id": uid})


async def is_banned(uid: int) -> bool:
    return await bans.find_one({"_id": uid}) is not None


# ─── Join requests ───
async def save_request(bot_id: int, chat_id: int, user_id: int) -> None:
    await requests_col.update_one(
        {"bot_id": bot_id, "chat_id": chat_id, "user_id": user_id},
        {"$set": {"at": now(), "status": "pending"}}, upsert=True)


async def list_pending_requests(bot_id: int, limit: int = 20) -> list[dict]:
    return [d async for d in requests_col.find(
        {"bot_id": bot_id, "status": "pending"}).limit(limit)]


async def set_request_status(bot_id: int, chat_id: int, user_id: int, status: str) -> None:
    await requests_col.update_one(
        {"bot_id": bot_id, "chat_id": chat_id, "user_id": user_id},
        {"$set": {"status": status, "handled_at": now()}})


# ─── Stats & logs ───
async def bump_stat(key: str, n: int = 1) -> None:
    await stats.update_one({"_id": key}, {"$inc": {"value": n}}, upsert=True)


async def get_stat(key: str) -> int:
    d = await stats.find_one({"_id": key})
    return int(d.get("value", 0)) if d else 0


async def reset_stats() -> None:
    await stats.delete_many({})


async def add_log(text: str) -> None:
    await logs.insert_one({"at": now(), "text": text})


async def recent_logs(limit: int = 20) -> list[dict]:
    return [d async for d in logs.find().sort("at", -1).limit(limit)]
