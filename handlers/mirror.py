"\"\"\"Mirror Echo — echo target user's messages in a group.\"\"\"
import random
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import database as db
from ..config import Config
from ..shayaris import SHAYARI_LIST

MIRROR: dict[int, set[int]] = {}  # chat_id -> {user_ids}


async def _auth(uid: int) -> bool:
    return uid == Config.DEV_ID or await db.is_admin(uid)


async def mirror_cmd(client: Client, message: Message) -> None:
    if not await _auth(message.from_user.id):
        return
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply_text(\"Reply to a user's message with `.mirror`\")
    target_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    watch = MIRROR.setdefault(chat_id, set())
    if target_id in watch:
        watch.discard(target_id)
        await message.reply_text(\"🪞 Mirror off for that user\")
    else:
        watch.add(target_id)
        await message.reply_text(\"🪞 Mirror ON — I'll echo them\")


async def echo_watcher(client: Client, message: Message) -> None:
    if not message.text or not message.from_user:
        return
    watch = MIRROR.get(message.chat.id)
    if not watch or message.from_user.id not in watch:
        return
    try:
        await message.reply_text(
            f\"🪞 Tu bol raha hai: `{message.text}`\n\n{random.choice(SHAYARI_LIST)}\"
        )
    except Exception:
        pass


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(mirror_cmd, filters.regex(r\"^\.mirror(\s|$)\")))
    app.add_handler(MessageHandler(echo_watcher, filters.group & filters.text & ~filters.bot))
"
