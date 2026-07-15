"\"\"\"/help + inline pagination.\"\"\"
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, CallbackQuery

from ..messages import HELP_PAGES, footer
from ..keyboards import help_kb
from ..utils import edit_or_send, safe_answer


async def help_cmd(client: Client, message: Message) -> None:
    total = len(HELP_PAGES)
    await message.reply_text(HELP_PAGES[0] + \"\n\n\" + footer(),
                             reply_markup=help_kb(0, total),
                             disable_web_page_preview=True)


async def help_cb(client: Client, cb: CallbackQuery) -> None:
    data = cb.data
    if data == \"help:noop\":
        return await safe_answer(cb)
    try:
        page = int(data.split(\":\", 1)[1])
    except ValueError:
        return await safe_answer(cb)
    total = len(HELP_PAGES)
    page = page % total
    await edit_or_send(cb, HELP_PAGES[page] + \"\n\n\" + footer(),
                       reply_markup=help_kb(page, total))
    await safe_answer(cb)


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(help_cmd, filters.command(\"help\")))
    app.add_handler(CallbackQueryHandler(help_cb, filters.regex(r\"^help:\")))
"
