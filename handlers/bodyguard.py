"\"\"\"Bodyguard — auto-defend when someone replies to a protected user.\"\"\"
import random
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import database as db
from ..config import Config
from ..shayaris import SHAYARI_LIST

ACTIVE: dict[int, bool] = {}  # protected_user_id -> on/off


async def _auth(uid: int) -> bool:
    return uid == Config.DEV_ID or await db.is_admin(uid)


async def bodyguard_cmd(client: Client, message: Message) -> None:
    if not await _auth(message.from_user.id):
        return
    args = (message.text or \"\").split()
    on = len(args) > 1 and args[1].lower() == \"on\"
    ACTIVE[message.from_user.id] = on
    await message.reply_text(f\"🛡️ Bodyguard {'enabled' if on else 'disabled'}\")


async def protect_watch(client: Client, message: Message) -> None:
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return
    victim = message.reply_to_message.from_user
    if not ACTIVE.get(victim.id):
        return
    if message.from_user and message.from_user.id == victim.id:
        return
    try:
        mention = (f\"[{message.from_user.first_name}]\"
                   f\"(tg://user?id={message.from_user.id})\")
        await message.reply_text(
            f\"⚠️ {mention} — mere sahab ko disrespect?\n\n{random.choice(SHAYARI_LIST)}\"
        )
    except Exception:
        pass


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(bodyguard_cmd, filters.regex(r\"^\.bodyguard(\s|$)\")))
    app.add_handler(MessageHandler(protect_watch, filters.group & filters.reply & ~filters.bot))
"
