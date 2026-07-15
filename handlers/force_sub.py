"\"\"\"Force-sub management commands + callbacks.\"\"\"
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import RPCError

from .. import database as db, state
from ..config import Config
from ..messages import bold, DIV, small_caps, CHECK, CROSS, ADMIN_ONLY
from ..keyboards import fsub_list_kb, back_kb
from ..utils import edit_or_send, safe_answer


async def _auth(uid: int) -> bool:
    return uid == Config.DEV_ID or await db.is_admin(uid)


async def addfsub_cmd(client: Client, message: Message) -> None:
    if not await _auth(message.from_user.id):
        return await message.reply_text(ADMIN_ONLY)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text(\"Usage: `/addfsub <@channel or -100xxxx>`\")
        return
    target = args[1].strip()
    me = await client.get_me()
    try:
        chat = await client.get_chat(target)
        invite = \"\"
        try:
            invite = (await client.export_chat_invite_link(chat.id)) or \"\"
        except RPCError:
            pass
        await db.add_force_channel(me.id, chat.id, chat.title or str(chat.id), invite)
        await message.reply_text(f\"{CHECK} Added: {chat.title} (`{chat.id}`)\")
    except RPCError as e:
        await message.reply_text(f\"{CROSS} Failed: {e}\")


async def delfsub_cmd(client: Client, message: Message) -> None:
    if not await _auth(message.from_user.id):
        return await message.reply_text(ADMIN_ONLY)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text(\"Usage: `/delfsub <chat_id>`\")
        return
    try:
        cid = int(args[1])
    except ValueError:
        await message.reply_text(f\"{CROSS} Bad chat_id\")
        return
    me = await client.get_me()
    await db.del_force_channel(me.id, cid)
    await message.reply_text(f\"{CHECK} Removed {cid}\")


async def listfsub_cmd(client: Client, message: Message) -> None:
    if not await _auth(message.from_user.id):
        return await message.reply_text(ADMIN_ONLY)
    me = await client.get_me()
    chs = await db.list_force_channels(me.id)
    if not chs:
        return await message.reply_text(\"No force-sub channels.\")
    text = \"\n\".join(f\"• {c.get('chat_title','?')} — `{c['chat_id']}`\" for c in chs)
    await message.reply_text(f\"{bold('Force-Sub')}\n{DIV}\n{text}\")


async def fsub_cb(client: Client, cb: CallbackQuery) -> None:
    if not await _auth(cb.from_user.id):
        return await safe_answer(cb, \"Not allowed\", alert=True)
    data = cb.data
    me = await client.get_me()

    if data == \"fsub:add\":
        state.conv[cb.from_user.id] = {\"action\": \"fsub_add\"}
        await edit_or_send(cb,
            f\"{bold('Send @username or -100xxxx of the channel')}\n{DIV}\n\"
            f\"{small_caps('bot must be admin there')}\",
            reply_markup=back_kb(\"dev:home\"))
        return await safe_answer(cb)

    if data.startswith(\"fsub:del:\"):
        cid = int(data.split(\":\")[-1])
        await db.del_force_channel(me.id, cid)
        chs = await db.list_force_channels(me.id)
        await edit_or_send(cb, f\"{bold('Force-Sub Channels')}\n{DIV}\n\"
                               f\"{small_caps('total')}: {len(chs)}\",
                           reply_markup=fsub_list_kb(chs))
        return await safe_answer(cb, \"Removed\")

    await safe_answer(cb)


def register(app: Client) -> None:
    app.add_handler(MessageHandler(addfsub_cmd, filters.command(\"addfsub\")))
    app.add_handler(MessageHandler(delfsub_cmd, filters.command(\"delfsub\")))
    app.add_handler(MessageHandler(listfsub_cmd, filters.command(\"listfsub\")))
    app.add_handler(CallbackQueryHandler(fsub_cb, filters.regex(r\"^fsub:(add|del)\")))
"
