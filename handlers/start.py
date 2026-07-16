"""/start + main menu callbacks + banned/fsub gates."""
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from .. import database as db
from ..config import Config
from ..messages import (
    start_text, clone_start_text, BANNED_MSG,
    force_sub_text, CHECK, small_caps, bold, DIV,
    FIRE, ZAP
)
from ..keyboards import main_menu_kb, clone_menu_kb, force_sub_kb
from ..utils import check_force_sub, send_with_photo, edit_or_send, safe_answer


async def start_cmd(client: Client, message: Message) -> None:
    uid = message.from_user.id
    await db.add_user(uid, message.from_user.username or "")
    await db.bump_stat("starts")

    if await db.is_banned(uid):
        await message.reply_text(BANNED_MSG)
        return

    me = await client.get_me()
    # Force-sub check (uses same bot's channels)
    missing = await check_force_sub(client, me.id, uid)
    if missing:
        await message.reply_text(force_sub_text(len(missing)),
                                 reply_markup=force_sub_kb(missing))
        return

    is_dev = uid == Config.DEV_ID
    is_admin = await db.is_admin(uid)

    if getattr(client, "is_clone_instance", False):
        owner_username = getattr(client, "owner_username", "owner")
        await send_with_photo(client, message.chat.id,
                              clone_start_text(owner_username, message.from_user.first_name),
                              reply_markup=clone_menu_kb())
    else:
        await send_with_photo(client, message.chat.id,
                              start_text(message.from_user.first_name),
                              reply_markup=main_menu_kb(is_dev=is_dev, is_admin=is_admin))


async def menu_cb(client: Client, cb: CallbackQuery) -> None:
    data = cb.data
    uid = cb.from_user.id

    if data == "menu:home":
        is_dev = uid == Config.DEV_ID
        is_admin = await db.is_admin(uid)
        await edit_or_send(cb, start_text(cb.from_user.first_name),
                           reply_markup=main_menu_kb(is_dev=is_dev, is_admin=is_admin))
        return await safe_answer(cb)

    if data == "menu:clone":
        from ..messages import CLONE_ASK
        import random
        from .. import state as st
        st.conv[uid] = {"action": "clone_token"}
        await edit_or_send(cb, random.choice(CLONE_ASK))
        return await safe_answer(cb, "Send token")

    if data == "menu:fsub":
        from ..keyboards import fsub_list_kb
        me = await client.get_me()
        chs = await db.list_force_channels(me.id)
        text = f"{bold('📢 Force-Sub Channels')}\n{DIV}\n"
        text += f"{small_caps('total')}: {len(chs)}"
        await edit_or_send(cb, text, reply_markup=fsub_list_kb(chs))
        return await safe_answer(cb)

    if data == "menu:admin":
        is_dev = uid == Config.DEV_ID
        is_admin = await db.is_admin(uid)
        if is_dev:
            from ..keyboards import dev_panel_kb
            await edit_or_send(cb, f"{bold('👑 Developer Panel')}\n{DIV}", reply_markup=dev_panel_kb())
        elif is_admin:
            from ..keyboards import admin_panel_kb
            await edit_or_send(cb, f"{bold('🛡️ Admin Panel')}\n{DIV}", reply_markup=admin_panel_kb())
        else:
            return await safe_answer(cb, "Not admin", alert=True)
        return await safe_answer(cb)

    if data == "menu:raid":
        text = (f"{FIRE} {bold('🔥 RAID CONTROL 🔥')}\n{DIV}\n"
                f"{ZAP} {small_caps('use .raid <count> in a group')}"
                f"\n{ZAP} {small_caps('use .raid <count> @user to tag')}\n"
                f"{ZAP} {small_caps('use /stop to cancel')}\n"
                f"{ZAP} {small_caps('use /resume to reset')}")
        from ..keyboards import back_kb
        await edit_or_send(cb, text, reply_markup=back_kb())
        return await safe_answer(cb)

    if data == "menu:stats":
        starts = await db.get_stat("starts")
        clones_n = await db.clone_count()
        users_n = await db.user_count()
        raids = await db.get_stat("raids")
        text = (f"{bold('📊 PREMIUM STATS 📊')}\n{DIV}\n"
                f"👥 Users: {users_n}\n"
                f"🤖 Clones: {clones_n}\n"
                f"🚀 /start hits: {starts}\n"
                f"{CHECK} Raids: {raids}")
        from ..keyboards import back_kb
        await edit_or_send(cb, text, reply_markup=back_kb())
        return await safe_answer(cb)

    if data == "menu:ping":
        import time
        t = time.time()
        from ..messages import ping_text
        await safe_answer(cb, "Pinging...")
        ms = int((time.time() - t) * 1000)
        from ..keyboards import back_kb
        await edit_or_send(cb, ping_text(ms), reply_markup=back_kb())
        return

    await safe_answer(cb)


async def fsub_check_cb(client: Client, cb: CallbackQuery) -> None:
    me = await client.get_me()
    missing = await check_force_sub(client, me.id, cb.from_user.id)
    if missing:
        await safe_answer(cb, "Still not joined all channels", alert=True)
        return
    await safe_answer(cb, "Verified ✅", alert=True)
    is_dev = cb.from_user.id == Config.DEV_ID
    is_admin = await db.is_admin(cb.from_user.id)
    await edit_or_send(cb, start_text(cb.from_user.first_name),
                       reply_markup=main_menu_kb(is_dev=is_dev, is_admin=is_admin))


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(__import__("pyrogram").handlers.MessageHandler(
        start_cmd, filters.command("start") & filters.private))
    from pyrogram.handlers import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(menu_cb, filters.regex(r"^menu:")))
    app.add_handler(CallbackQueryHandler(fsub_check_cb, filters.regex(r"^fsub:check$")))
