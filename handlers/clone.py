"\"\"\"/clone flow — token input -> deploy.\"\"\"
import re
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import state, database as db
from ..messages import CLONE_ASK, CLONE_FAIL, clone_success
import random

TOKEN_RE = re.compile(r\"^\d{6,12}:[A-Za-z0-9_\-]{30,}$\")


async def clone_cmd(client: Client, message: Message) -> None:
    state.conv[message.from_user.id] = {\"action\": \"clone_token\"}
    await message.reply_text(random.choice(CLONE_ASK))


async def process_clone_token(client: Client, message: Message) -> None:
    from ..clone_runner import start_clone
    token = (message.text or \"\").strip()
    if not TOKEN_RE.match(token):
        await message.reply_text(random.choice(CLONE_FAIL))
        return
    try:
        info = await start_clone(token, message.from_user.id)
    except Exception as e:
        await message.reply_text(random.choice(CLONE_FAIL) + f\"\n\n`{e}`\")
        return
    await db.bump_stat(\"clones_deployed\")
    await db.add_log(f\"clone deployed @{info['username']} by {message.from_user.id}\")
    await message.reply_text(clone_success(info[\"username\"]))


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(clone_cmd, filters.command(\"clone\") & filters.private))
"
