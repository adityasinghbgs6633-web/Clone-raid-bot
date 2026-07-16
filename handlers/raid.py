"""Enhanced raid handler with tag mentions, activity logging, and premium features."""
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from .. import state, database as db
from ..config import Config
from ..shayaris import SHAYARI_LIST
from ..messages import raid_log_msg, BOMB, CHECK


async def _auth(uid: int) -> bool:
    return uid == Config.DEV_ID or await db.is_admin(uid)


async def raid_cmd(client: Client, message: Message) -> None:
    """Enhanced raid with @mentions and logging."""
    if not await _auth(message.from_user.id):
        return
    
    args = (message.text or "").split(maxsplit=3)
    if len(args) < 2:
        return await message.reply_text(
            "💣 <b>Usage:</b>\n"
            "• <code>.raid <count></code> — Raid current chat\n"
            "• <code>.raid <count> @user</code> — Tag user in raid\n"
            "• <code>.raid stop</code> — Cancel raid\n"
            "• <code>.raid list</code> — Preview lines"
        )
    
    sub = args[1].lower()
    me = await client.get_me()

    if sub == "stop":
        n = await state.cancel_all(me.id)
        await db.set_stop_flag(me.id, True)
        await db.add_log(raid_log_msg(me.username or me.id, 0, 0, message.from_user.id))
        return await message.reply_text(f"🛑 Cancelled {n} raid task(s)")

    if sub == "list":
        preview = "\n".join(f"{i+1}. {s.splitlines()[0][:50]}" for i, s in enumerate(SHAYARI_LIST[:5]))
        return await message.reply_text(f"🔥 <b>Raid Preview:</b>\n\n{preview}")

    try:
        count = int(sub)
    except ValueError:
        return await message.reply_text("❌ Invalid count")

    count = max(1, min(count, 200))
    target_chat = message.chat.id
    reply_to = message.reply_to_message.id if message.reply_to_message else None
    
    # Extract tag if provided
    tagged_user = None
    if len(args) > 2:
        tag = args[2].lstrip("@")
        tagged_user = f"@{tag}"

    await db.set_stop_flag(me.id, False)
    
    # Log the raid
    await db.add_log(raid_log_msg(me.username or me.id, target_chat, count, message.from_user.id))
    
    status = await message.reply_text(f"{BOMB} <b>Raid starting...</b>\n0/{count}\n\n{CHECK} Premium Raid Active!")

    async def _run():
        sent = 0
        for i in range(count):
            if await db.get_stop_flag(me.id):
                break
            try:
                raid_msg = random.choice(SHAYARI_LIST)
                
                # Add tag mention if provided
                if tagged_user and i % 5 == 0:
                    raid_msg = f"{tagged_user}\n\n{raid_msg}"
                
                await client.send_message(
                    target_chat, 
                    raid_msg,
                    reply_to_message_id=reply_to
                )
                sent += 1
                if (i + 1) % 10 == 0:
                    try:
                        await status.edit_text(
                            f"{BOMB} <b>Raid Progress</b>\n{sent}/{count}\n\n{CHECK} Premium Active!"
                        )
                    except Exception:
                        pass
            except Exception as e:
                await db.add_log(f"❌ Raid error: {str(e)[:50]}")
                break
            await asyncio.sleep(random.uniform(0.5, 1.8))
        
        try:
            final_msg = f"{CHECK} <b>✅ RAID FINISHED!</b>\n{BOMB} Sent: {sent}/{count}"
            if sent == count:
                final_msg += f"\n🔥 <b>PERFECT! All {count} shots connected!</b>"
            await status.edit_text(final_msg)
        except Exception:
            pass

    task = asyncio.create_task(_run())
    state.register_task(me.id, task)


def register(app: Client, is_clone: bool = False) -> None:
    app.add_handler(MessageHandler(raid_cmd, filters.regex(r"^\.raid(\s|$)")))
