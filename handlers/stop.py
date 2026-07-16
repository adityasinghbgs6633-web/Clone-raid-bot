"""/stop priority handler (group=-1) — cancels raid/broadcast on all clones."""
import logging
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import state, database as db
from ..messages import STOP_MSG

log = logging.getLogger("bot.stop")


async def stop_cmd(client: Client, message: Message) -> None:
    me = await client.get_me()
    n = await state.cancel_all(me.id)
    await db.set_stop_flag(me.id, True)
    await db.add_log(f"🛑 STOP triggered by {message.from_user.id} - cancelled {n} tasks")
    await message.reply_text(STOP_MSG)


async def resume_cmd(client: Client, message: Message) -> None:
    me = await client.get_me()
    await db.set_stop_flag(me.id, False)
    await db.add_log(f"▶️ RESUME triggered by {message.from_user.id}")
    from ..messages import RESUME_MSG
    await message.reply_text(RESUME_MSG)


def register(app: Client, is_clone: bool = False) -> None:
    # Priority: group=-1 fires BEFORE any other handler
    app.add_handler(MessageHandler(stop_cmd, filters.command("stop")), group=-1)
    app.add_handler(MessageHandler(resume_cmd, filters.command("resume")), group=-1)
