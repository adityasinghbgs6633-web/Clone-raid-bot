"\"\"\"Shayari raid — .raid <count> [reply to target].\"\"\"
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import state, database as db
from ..config import Config
from ..shayaris import SHAYARI_LIST


async def _auth(uid: int) -> bool:
    return uid == Config.DEV_ID or await db.is_admin(uid)


async def raid_cmd(client: Client, message: Message) -> None:
    if not await _auth(message.from_user.id):
        return
    args = (message.text or \"\").split(maxsplit=2)
    if len(args) < 2:
        return await message.reply_text(
            \"Usage: `.raid <count>`, `.raid stop`, `.raid list`\"
        )
    sub = args[1].lower()
    me = await client.get_me()

    if sub == \"stop\":
        n = await state.cancel_all(me.id)
        await db.set_stop_flag(me.id, True)
        return await message.reply_text(f\"🛑 Cancelled {n} raid task(s)\")

    if sub == \"list\":
        preview = \"\n\".join(f\"{i+1}. {s.splitlines()[0]}\" for i, s in enumerate(SHAYARI_LIST[:5]))
        return await message.reply_text(f\"**Raid Preview:**\n\n{preview}\")

    try:
        count = int(sub)
    except ValueError:
        return await message.reply_text(\"❌ Invalid count\")

    count = max(1, min(count, 200))
    target_chat = message.chat.id
    reply_to = message.reply_to_message.id if message.reply_to_message else None

    await db.set_stop_flag(me.id, False)
    status = await message.reply_text(f\"🚀 Raid starting... 0/{count}\")

    async def _run():
        sent = 0
        for i in range(count):
            if await db.get_stop_flag(me.id):
                break
            try:
                await client.send_message(target_chat, random.choice(SHAYARI_LIST),
                                          reply_to_message_id=reply_to)
                sent += 1
                if (i + 1) % 10 == 0:
                    try:
                        await status.edit_text(f\"🚀 Raid... {sent}/{count}\")
                    except Exception:
                        pass
            except Exception:
                break
            await asyncio.sleep(random.uniform(0.5, 1.8))
        try:
            await status.edit_text(f\"✅ Raid finished — sent {sent}/{count}\")
        except Exception:
            pass

    task = asyncio.create_task(_run())
    state.register_task(me.id, task)


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(raid_cmd, filters.regex(r\"^\.raid(\s|$)\")))
"
