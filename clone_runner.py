"\"\"\"Clone-bot manager — spins Pyrogram Client per token.\"\"\"
import logging
from pyrogram import Client
from pyrogram.errors import AccessTokenInvalid, AccessTokenExpired

from .config import Config
from . import database as db, state
from .handlers import register_all
from .utils import cache_bot_profile_photo

log = logging.getLogger(\"bot.clone_runner\")


async def start_clone(token: str, owner_id: int) -> dict:
    session_name = f\"clone_{token.split(':')[0]}\"
    app = Client(
        name=session_name,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=token,
        in_memory=True,
    )
    register_all(app, is_clone=True)
    app.owner_id = owner_id
    app.developer_id = Config.DEV_ID

    try:
        await app.start()
    except (AccessTokenInvalid, AccessTokenExpired) as e:
        raise RuntimeError(f\"Invalid token: {e}\")

    me = await app.get_me()
    state.running_clones[me.id] = app
    await cache_bot_profile_photo(app)
    await db.add_clone(me.id, token, owner_id, me.username or \"\")
    log.info(\"Clone started: @%s (%s)\", me.username, me.id)
    return {\"bot_id\": me.id, \"username\": me.username or \"\"}


async def stop_clone(bot_id: int) -> bool:
    app = state.running_clones.pop(bot_id, None)
    if app:
        try:
            await app.stop()
        except Exception as e:
            log.warning(\"stop clone %s: %s\", bot_id, e)
    await db.set_stop_flag(bot_id, True)
    await db.remove_clone(bot_id)
    return True


async def resume_saved_clones() -> None:
    clones = await db.list_clones()
    for c in clones:
        try:
            await start_clone(c[\"token\"], c[\"owner_id\"])
        except Exception as e:
            log.warning(\"skip clone %s: %s\", c[\"_id\"], e)
            await db.remove_clone(c[\"_id\"])
"
