"\"\"\"Identity clone — `.steal` (reply) / `.reset`.\"\"\"
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import database as db
from ..config import Config

CLONED: dict[int, dict] = {}  # uid -> {orig, target_id, target_name}


async def _auth(uid: int) -> bool:
    return uid == Config.DEV_ID or await db.is_admin(uid)


async def steal_cmd(client: Client, message: Message) -> None:
    if not await _auth(message.from_user.id):
        return
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply_text(\"Reply to a user's message\")
    target = message.reply_to_message.from_user
    CLONED[message.from_user.id] = {
        \"orig\": message.from_user.first_name,
        \"target_id\": target.id,
        \"target_name\": target.first_name,
    }
    await message.reply_text(
        f\"🎭 **Identity Cloned**\nOriginal: {message.from_user.first_name}\n\"
        f\"Cloned: {target.first_name}\n\nUse `.reset` to restore\"
    )


async def reset_cmd(client: Client, message: Message) -> None:
    p = CLONED.pop(message.from_user.id, None)
    if not p:
        return await message.reply_text(\"❌ No cloned profile\")
    await message.reply_text(
        f\"✅ Restored — back to {p['orig']} (was: {p['target_name']})\"
    )


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(steal_cmd, filters.regex(r\"^\.steal(\s|$)\")))
    app.add_handler(MessageHandler(reset_cmd, filters.regex(r\"^\.reset(\s|$)\")))
"
