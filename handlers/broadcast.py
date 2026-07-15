"\"\"\"Broadcast — reply to a message with /broadcast, or use panel flow.\"\"\"
import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram.errors import FloodWait, RPCError

from .. import database as db, state
from ..config import Config
from ..messages import DEV_ONLY, CHECK


async def _auth(uid: int) -> bool:
    return uid == Config.DEV_ID or await db.is_admin(uid)


async def broadcast_cmd(client: Client, message: Message) -> None:
    if not await _auth(message.from_user.id):
        return await message.reply_text(DEV_ONLY)
    if not message.reply_to_message:
        return await message.reply_text(\"Reply to a message with /broadcast\")
    src = message.reply_to_message
    me = await client.get_me()
    uids = await db.all_users()
    status = await message.reply_text(f\"📣 Broadcasting to {len(uids)} users...\")

    async def _run():
        sent = fail = 0
        for uid in uids:
            if await db.get_stop_flag(me.id):
                break
            try:
                await src.copy(uid)
                sent += 1
            except FloodWait as f:
                await asyncio.sleep(f.value + 1)
            except RPCError:
                fail += 1
            except Exception:
                fail += 1
            await asyncio.sleep(0.05)
        try:
            await status.edit_text(f\"{CHECK} Done. Sent: {sent}, Failed: {fail}\")
        except Exception:
            pass
        await db.add_log(f\"broadcast by {message.from_user.id}: {sent} ok, {fail} fail\")

    task = asyncio.create_task(_run())
    state.register_task(me.id, task)


def register(app: Client) -> None:
    app.add_handler(MessageHandler(broadcast_cmd, filters.command(\"broadcast\")))
"
