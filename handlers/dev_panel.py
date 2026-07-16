"""
📋 Developer Panel with enhanced admin management + ban/unban + kill clone + logs
"""
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, CallbackQuery

from .. import database as db, state
from ..config import Config
from ..messages import (
    bold, DIV, small_caps, DEV_ONLY, ADMIN_ONLY,
    CHECK, CROSS, CROWN, SHIELD, admin_added_msg, fsub_added_msg
)
from ..keyboards import (
    dev_panel_kb, admin_panel_kb, back_kb,
    admins_list_kb, clones_list_kb, confirm_kb,
    approve_kb
)
from ..utils import edit_or_send, safe_answer


def _is_dev(uid: int) -> bool:
    return uid == Config.DEV_ID


async def panel_cmd(client: Client, message: Message) -> None:
    uid = message.from_user.id
    if _is_dev(uid):
        await message.reply_text(f"{CROWN} {bold('👑 Developer Panel')}\n{DIV}",
                                 reply_markup=dev_panel_kb())
    elif await db.is_admin(uid):
        await message.reply_text(f"{SHIELD} {bold('🛡️ Admin Panel')}\n{DIV}",
                                 reply_markup=admin_panel_kb())
    else:
        await message.reply_text(DEV_ONLY)


async def addadmin_cmd(client: Client, message: Message) -> None:
    """Add admin via command or button flow."""
    if not _is_dev(message.from_user.id):
        return await message.reply_text(DEV_ONLY)
    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text(f"{bold('Send user ID to make admin')}\n\nUsage: `/addadmin <user_id>`")
    try:
        uid = int(args[1])
    except ValueError:
        return await message.reply_text(f"{CROSS} Invalid ID")
    await db.add_admin(uid)
    await db.add_log(f"👤 Admin added: {uid} by {message.from_user.id}")
    await message.reply_text(admin_added_msg(uid))


async def deladmin_cmd(client: Client, message: Message) -> None:
    if not _is_dev(message.from_user.id):
        return await message.reply_text(DEV_ONLY)
    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text("Usage: `/deladmin <user_id>`")
    try:
        uid = int(args[1])
    except ValueError:
        return await message.reply_text(f"{CROSS} bad id")
    await db.remove_admin(uid)
    await db.add_log(f"❌ Admin removed: {uid} by {message.from_user.id}")
    await message.reply_text(f"{CHECK} Admin removed: {uid}")


async def ban_cmd(client: Client, message: Message) -> None:
    if not _is_dev(message.from_user.id):
        return await message.reply_text(DEV_ONLY)
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        return await message.reply_text("Usage: `/ban <user_id> [reason]`")
    try:
        uid = int(args[1])
    except ValueError:
        return await message.reply_text(f"{CROSS} bad id")
    reason = args[2] if len(args) > 2 else ""
    await db.ban_user(uid, reason)
    await db.add_log(f"🚫 User {uid} banned: {reason}")
    await message.reply_text(f"{CHECK} Banned {uid}")


async def unban_cmd(client: Client, message: Message) -> None:
    if not _is_dev(message.from_user.id):
        return await message.reply_text(DEV_ONLY)
    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text("Usage: `/unban <user_id>`")
    try:
        uid = int(args[1])
    except ValueError:
        return await message.reply_text(f"{CROSS} bad id")
    await db.unban_user(uid)
    await db.add_log(f"✅ User {uid} unbanned")
    await message.reply_text(f"{CHECK} Unbanned {uid}")


async def killclone_cmd(client: Client, message: Message) -> None:
    if not _is_dev(message.from_user.id):
        return await message.reply_text(DEV_ONLY)
    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text("Usage: `/killclone <bot_id>`")
    try:
        bot_id = int(args[1])
    except ValueError:
        return await message.reply_text(f"{CROSS} bad id")
    from ..clone_runner import stop_clone
    await stop_clone(bot_id)
    await db.add_log(f"🔌 Clone {bot_id} killed")
    await message.reply_text(f"{CHECK} Clone {bot_id} killed")


async def logs_cmd(client: Client, message: Message) -> None:
    if not _is_dev(message.from_user.id):
        return await message.reply_text(DEV_ONLY)
    entries = await db.recent_logs(20)
    if not entries:
        return await message.reply_text("No logs.")
    text = "\n".join(f"• `{e['at'].strftime('%H:%M')}` {e['text']}" for e in entries)
    await message.reply_text(f"{bold('📜 Recent Logs')}\n{DIV}\n{text}")


async def dev_cb(client: Client, cb: CallbackQuery) -> None:
    data = cb.data
    uid = cb.from_user.id

    if data.startswith("dev:") and not _is_dev(uid) and not await db.is_admin(uid):
        return await safe_answer(cb, "Not allowed", alert=True)

    if data == "dev:home":
        if _is_dev(uid):
            await edit_or_send(cb, f"{CROWN} {bold('👑 Developer Panel')}\n{DIV}",
                               reply_markup=dev_panel_kb())
        else:
            await edit_or_send(cb, f"{SHIELD} {bold('🛡️ Admin Panel')}\n{DIV}",
                               reply_markup=admin_panel_kb())
        return await safe_answer(cb)

    if data == "admin:home":
        await edit_or_send(cb, f"{SHIELD} {bold('🛡️ Admin Panel')}\n{DIV}",
                           reply_markup=admin_panel_kb())
        return await safe_answer(cb)

    if data == "dev:admins":
        if not _is_dev(uid):
            return await safe_answer(cb, "Dev-only", alert=True)
        docs = await db.list_admins()
        await edit_or_send(cb, f"{bold('👥 Admins')}\n{DIV}\n{small_caps('total')}: {len(docs)}",
                           reply_markup=admins_list_kb(docs))
        return await safe_answer(cb)

    if data == "adm:add":
        if not _is_dev(uid):
            return await safe_answer(cb, "Dev-only", alert=True)
        state.conv[uid] = {"action": "adm_add"}
        await edit_or_send(cb, f"{bold('👤 Send user_id to promote')}\n{DIV}",
                           reply_markup=back_kb("dev:home"))
        return await safe_answer(cb)

    if data.startswith("adm:del:"):
        if not _is_dev(uid):
            return await safe_answer(cb, "Dev-only", alert=True)
        admin_id = int(data.split(":")[-1])
        await db.remove_admin(admin_id)
        await db.add_log(f"❌ Admin {admin_id} removed")
        docs = await db.list_admins()
        await edit_or_send(cb, f"{bold('👥 Admins')}\n{DIV}\n{small_caps('total')}: {len(docs)}",
                           reply_markup=admins_list_kb(docs))
        return await safe_answer(cb, "Removed")

    if data == "dev:requests":
        me = await client.get_me()
        pend = await db.list_pending_requests(me.id, 20)
        if not pend:
            await edit_or_send(cb, "No pending requests.", reply_markup=back_kb("dev:home"))
            return await safe_answer(cb)
        r = pend[0]
        text = (f"{bold('Pending Join Request')}\n{DIV}\n"
                f"User: `{r['user_id']}`\nChat: `{r['chat_id']}`\n"
                f"Remaining: {len(pend)}")
        await edit_or_send(cb, text, reply_markup=approve_kb(r['chat_id'], r['user_id']))
        return await safe_answer(cb)

    if data.startswith("req:"):
        _, act, cid, uid_target = data.split(":")
        me = await client.get_me()
        try:
            if act == "ok":
                await client.approve_chat_join_request(int(cid), int(uid_target))
                await db.set_request_status(me.id, int(cid), int(uid_target), "approved")
                await db.add_log(f"✅ Request approved: {uid_target} to {cid}")
                await safe_answer(cb, "Approved ✅")
            else:
                await client.decline_chat_join_request(int(cid), int(uid_target))
                await db.set_request_status(me.id, int(cid), int(uid_target), "declined")
                await db.add_log(f"❌ Request declined: {uid_target} to {cid}")
                await safe_answer(cb, "Declined ❌")
        except Exception as e:
            await safe_answer(cb, f"Err: {str(e)[:30]}", alert=True)
        pend = await db.list_pending_requests(me.id, 20)
        if not pend:
            await edit_or_send(cb, "No pending requests.", reply_markup=back_kb("dev:home"))
            return
        r = pend[0]
        text = (f"{bold('Pending Join Request')}\n{DIV}\n"
                f"User: `{r['user_id']}`\nChat: `{r['chat_id']}`\n"
                f"Remaining: {len(pend)}")
        await edit_or_send(cb, text, reply_markup=approve_kb(r['chat_id'], r['user_id']))
        return

    if data == "dev:ban":
        state.conv[uid] = {"action": "ban_ask"}
        await edit_or_send(cb, f"{bold('Send user_id to ban (prefix `-` to unban)')}\n{DIV}",
                           reply_markup=back_kb("dev:home"))
        return await safe_answer(cb)

    if data == "dev:bcast":
        state.conv[uid] = {"action": "bcast_ask"}
        await edit_or_send(cb, f"{bold('Send message to broadcast (or reply-forward one)')}\n{DIV}",
                           reply_markup=back_kb("dev:home"))
        return await safe_answer(cb)

    if data == "dev:kill":
        if not _is_dev(uid):
            return await safe_answer(cb, "Dev-only", alert=True)
        clones = await db.list_clones()
        await edit_or_send(cb, f"{bold('🤖 Running Clones')}\n{DIV}\n{small_caps('total')}: {len(clones)}",
                           reply_markup=clones_list_kb(clones))
        return await safe_answer(cb)

    if data.startswith("kill:"):
        if not _is_dev(uid):
            return await safe_answer(cb, "Dev-only", alert=True)
        bot_id = int(data.split(":")[-1])
        from ..clone_runner import stop_clone
        await stop_clone(bot_id)
        clones = await db.list_clones()
        await edit_or_send(cb, f"{bold('🤖 Running Clones')}\n{DIV}\n{small_caps('total')}: {len(clones)}",
                           reply_markup=clones_list_kb(clones))
        return await safe_answer(cb, "Killed")

    if data == "dev:logs":
        if not _is_dev(uid):
            return await safe_answer(cb, "Dev-only", alert=True)
        entries = await db.recent_logs(15)
        text = "\n".join(f"• `{e['at'].strftime('%H:%M')}` {e['text']}" for e in entries) or "No logs."
        await edit_or_send(cb, f"{bold('📜 Recent Logs')}\n{DIV}\n{text}",
                           reply_markup=back_kb("dev:home"))
        return await safe_answer(cb)

    if data == "dev:reset":
        if not _is_dev(uid):
            return await safe_answer(cb, "Dev-only", alert=True)
        await edit_or_send(cb, f"{bold('Reset all stats?')}\n{DIV}",
                           reply_markup=confirm_kb("reset", ""))
        return await safe_answer(cb)

    if data == "dev:fsub":
        me = await client.get_me()
        from ..keyboards import fsub_list_kb
        chs = await db.list_force_channels(me.id)
        await edit_or_send(cb, f"{bold('📢 Force-Sub Channels')}\n{DIV}\n"
                               f"{small_caps('total')}: {len(chs)}",
                           reply_markup=fsub_list_kb(chs))
        return await safe_answer(cb)

    if data.startswith("confirm:"):
        _, act, _target = data.split(":", 2)
        if act == "reset" and _is_dev(uid):
            await db.reset_stats()
            await db.add_log(f"🧹 Stats reset by {uid}")
            await edit_or_send(cb, f"{CHECK} Stats reset.", reply_markup=back_kb("dev:home"))
        else:
            await safe_answer(cb, "Not allowed", alert=True)
        return await safe_answer(cb)

    await safe_answer(cb)


def register(app: Client) -> None:
    app.add_handler(MessageHandler(panel_cmd, filters.command("panel")))
    app.add_handler(MessageHandler(addadmin_cmd, filters.command("addadmin")))
    app.add_handler(MessageHandler(deladmin_cmd, filters.command("deladmin")))
    app.add_handler(MessageHandler(ban_cmd, filters.command("ban")))
    app.add_handler(MessageHandler(unban_cmd, filters.command("unban")))
    app.add_handler(MessageHandler(killclone_cmd, filters.command("killclone")))
    app.add_handler(MessageHandler(logs_cmd, filters.command("logs")))
    app.add_handler(CallbackQueryHandler(dev_cb,
        filters.regex(r"^(dev:|admin:|adm:|req:|kill:|confirm:)")))
