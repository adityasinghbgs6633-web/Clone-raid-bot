"\"\"\"Stats view.\"\"\"
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import database as db
from ..messages import bold, DIV


async def stats_cmd(client: Client, message: Message) -> None:
    starts = await db.get_stat(\"starts\")
    clones_n = await db.clone_count()
    users_n = await db.user_count()
    await message.reply_text(
        f\"{bold('📊 Stats')}\n{DIV}\n\"
        f\"👥 Users: {users_n}\n🤖 Clones: {clones_n}\n🚀 /start: {starts}\"
    )


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(stats_cmd, filters.command(\"stats\")))
"
