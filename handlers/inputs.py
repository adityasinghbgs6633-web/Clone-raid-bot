"\"\"\"Conversation router — free-form text based on state.conv[user_id].\"\"\"
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import state, database as db
from ..messages import CHECK, CROSS, DIV, bold, small_caps
from ..keyboards import main_menu_kb
from ..config import Config


async def input_router(client: Client, message: Message) -> None:
    uid = message.from_user.id
    ctx = state.conv.get(uid)
    if not ctx:
        return
    action = ctx.get(\"action\")

    if action == \"clone_token\":
        state.conv.pop(uid, None)
        from .clone import process_clone_token
        await process_clone_token(client, message)
        return

    if action == \"fsub_add\":
        state.conv.pop(uid, None)
        target = (message.text or \"\").strip()
        me = await client.get_me()
        try:
            chat = await client.get_chat(target)
            invite = \"\"
            try:
                invite = (await client.export_chat_invite_link(chat.id)) or \"\"
            except Exception:
                pass
            await db.add_force_channel(me.id, chat.id, chat.title or str(chat.id), invite)
            await message.reply_text(f\"{CHECK} Added: {chat.title} (`{chat.id}`)\")
        except Exception as e:
            await message.reply_text(f\"{CROSS} Failed: {e}\")
        return

    if action == \"adm_add\":
        state.conv.pop(uid, None)
        try:
            target = int((message.text or \"\").strip())
        except ValueError:
            return await message.reply_text(f\"{CROSS} bad id\")
        await db.add_admin(target)
        await message.reply_text(f\"{CHECK} Admin added: {target}\")
        return

    if action == \"ban_ask\":
        state.conv.pop(uid, None)
        raw = (message.text or \"\").strip()
        unban = raw.startswith(\"-\")
        try:
            target = int(raw.lstrip(\"-\"))
        except ValueError:
            return await message.reply_text(f\"{CROSS} bad id\")
        if unban:
            await db.unban_user(target)
            await message.reply_text(f\"{CHECK} Unbanned {target}\")
        else:
            await db.ban_user(target)
            await message.reply_text(f\"{CHECK} Banned {target}\")
        return

    if action == \"bcast_ask\":
        state.conv.pop(uid, None)
        me = await client.get_me()
        uids = await db.all_users()
        import asyncio
        from pyrogram.errors import FloodWait, RPCError
        status = await message.reply_text(f\"📣 Broadcasting to {len(uids)} users...\")

        async def _run():
            sent = fail = 0
            for target in uids:
                if await db.get_stop_flag(me.id):
                    break
                try:
                    await message.copy(target)
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

        task = asyncio.create_task(_run())
        state.register_task(me.id, task)
        return


def register(app: Client) -> None:
    # Only messages with text/media, from private, when conv is set
    app.add_handler(MessageHandler(
        input_router,
        filters.private & ~filters.command([\"start\", \"help\", \"ping\", \"clone\",
                                            \"panel\", \"stop\", \"resume\",
                                            \"addfsub\", \"delfsub\", \"listfsub\",
                                            \"addadmin\", \"deladmin\", \"ban\", \"unban\",
                                            \"killclone\", \"logs\", \"stats\", \"broadcast\"])
    ))
"
