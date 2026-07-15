"\"\"\"Sniper — auto-reply when a keyword is seen in a group.\"\"\"
import random
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import database as db
from ..config import Config

SNIPER_KW: dict[int, set[str]] = {}  # bot_id -> {keywords}
RESPONSES = [
    \"💬 Kaun bola? Sniped 🎯\",
    \"📢 Trigger detected — bot on point ⚡\",
    \"🎯 Bulls-eye, keyword caught!\",
    \"🚨 Sniper activated 👀\",
]


async def _auth(uid: int) -> bool:
    return uid == Config.DEV_ID or await db.is_admin(uid)


async def sniper_cmd(client: Client, message: Message) -> None:
    if not await _auth(message.from_user.id):
        return
    args = (message.text or \"\").split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text(\"Usage: `.sniper <keyword>` or `.sniper stop`\")
    me = await client.get_me()
    kws = SNIPER_KW.setdefault(me.id, set())
    kw = args[1].strip().lower()
    if kw == \"stop\":
        kws.clear()
        return await message.reply_text(\"✅ Sniper cleared\")
    if kw in kws:
        kws.discard(kw)
        return await message.reply_text(f\"❌ Removed: `{kw}`\")
    kws.add(kw)
    await message.reply_text(f\"🎯 Sniper set: `{kw}` (total: {len(kws)})\")


async def keyword_watch(client: Client, message: Message) -> None:
    if not message.text:
        return
    me = await client.get_me()
    kws = SNIPER_KW.get(me.id)
    if not kws:
        return
    txt = message.text.lower()
    for kw in kws:
        if kw in txt:
            try:
                await message.reply_text(f\"{random.choice(RESPONSES)}\n✍️ Sniped: `{kw}`\")
            except Exception:
                pass
            return


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(sniper_cmd, filters.regex(r\"^\.sniper(\s|$)\")))
    app.add_handler(MessageHandler(keyword_watch, filters.group & filters.text & ~filters.bot))
"
