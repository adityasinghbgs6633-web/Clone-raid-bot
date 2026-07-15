"\"\"\"/stop + /resume — priority kill-switch (group=-1).\"\"\"
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import database as db, state
from ..messages import STOP_MSG, RESUME_MSG
from ..config import Config


async def _is_authorized(uid: int) -> bool:
    return uid == Config.DEV_ID or await db.is_admin(uid)


async def stop_cmd(client: Client, message: Message) -> None:
    if not await _is_authorized(message.from_user.id):
        return
    me = await client.get_me()
    n = await state.cancel_all(me.id)
    await db.set_stop_flag(me.id, True)
    await db.add_log(f\"/stop by {message.from_user.id} ({n} tasks)\")
    await message.reply_text(STOP_MSG + f\"\n\n(Cancelled: {n} task(s))\")


async def resume_cmd(client: Client, message: Message) -> None:
    if not await _is_authorized(message.from_user.id):
        return
    me = await client.get_me()
    await db.set_stop_flag(me.id, False)
    await db.add_log(f\"/resume by {message.from_user.id}\")
    await message.reply_text(RESUME_MSG)


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(stop_cmd, filters.command([\"stop\"])), group=-1)
    app.add_handler(MessageHandler(resume_cmd, filters.command([\"resume\"])), group=-1)
"
