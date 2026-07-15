"\"\"\"/ping — works on main & clones.\"\"\"
import time
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from ..messages import ping_text


async def ping_cmd(client: Client, message: Message) -> None:
    t = time.time()
    m = await message.reply_text(\"🏓 Pinging...\")
    ms = int((time.time() - t) * 1000)
    await m.edit_text(ping_text(ms), disable_web_page_preview=True)


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(ping_cmd, filters.command(\"ping\")))
"
