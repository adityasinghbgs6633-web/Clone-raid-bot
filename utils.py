"\"\"\"Helpers — join checks, photo cache, safe edits.\"\"\"
import logging
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    UserNotParticipant, ChatAdminRequired, RPCError,
    MessageNotModified, PeerIdInvalid, ChannelPrivate,
)
from . import database as db, state

log = logging.getLogger(\"bot.utils\")

JOINED = {
    ChatMemberStatus.OWNER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.MEMBER,
    ChatMemberStatus.RESTRICTED,
}


async def get_bot_id(client: Client) -> int:
    me = await client.get_me()
    return me.id


async def cache_bot_profile_photo(client: Client) -> str | None:
    me = await client.get_me()
    if not me.photo:
        return None
    async for p in client.get_chat_photos(me.id, limit=1):
        state.cache_profile_photo(me.id, p.file_id)
        return p.file_id
    return None


async def is_user_in_channel(client: Client, chat_id, user_id: int) -> bool:
    try:
        m = await client.get_chat_member(chat_id, user_id)
        return m.status in JOINED
    except UserNotParticipant:
        return False
    except (ChatAdminRequired, PeerIdInvalid, ChannelPrivate):
        log.warning(\"Bot has no access to %s\", chat_id)
        return True
    except RPCError as e:
        log.warning(\"membership check err %s: %s\", chat_id, e)
        return True


async def check_force_sub(client: Client, bot_id: int, user_id: int) -> list[dict]:
    channels = await db.list_force_channels(bot_id)
    if not channels:
        return []
    missing = []
    for ch in channels:
        if not await is_user_in_channel(client, ch[\"chat_id\"], user_id):
            missing.append(ch)
    return missing


async def send_with_photo(client: Client, chat_id: int, text: str, reply_markup=None):
    bot_id = client.me.id if getattr(client, \"me\", None) else await get_bot_id(client)
    photo = state.get_profile_photo(bot_id)
    if photo:
        try:
            return await client.send_photo(chat_id, photo=photo, caption=text,
                                           reply_markup=reply_markup)
        except RPCError as e:
            log.warning(\"send_photo failed: %s\", e)
    return await client.send_message(chat_id, text, reply_markup=reply_markup,
                                     disable_web_page_preview=True)


async def edit_or_send(cb_or_msg, text: str, reply_markup=None):
    try:
        msg = getattr(cb_or_msg, \"message\", cb_or_msg)
        if msg.photo or msg.caption is not None:
            return await msg.edit_caption(caption=text, reply_markup=reply_markup)
        return await msg.edit_text(text, reply_markup=reply_markup,
                                   disable_web_page_preview=True)
    except MessageNotModified:
        return None
    except RPCError as e:
        log.warning(\"edit failed: %s\", e)
        return None


async def safe_answer(cb, text: str = \"\", alert: bool = False) -> None:
    try:
        await cb.answer(text, show_alert=alert)
    except RPCError:
        pass
"
