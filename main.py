"\"\"\"Entry — boot main bot, resume clones, idle.\"\"\"
import asyncio
import logging
import sys
from pyrogram import Client, idle

from .config import Config
from . import database as db, state
from .handlers import register_all
from .utils import cache_bot_profile_photo
from .clone_runner import resume_saved_clones

logging.basicConfig(
    level=logging.INFO,
    format=\"%(asctime)s | %(name)s | %(levelname)s | %(message)s\",
)
log = logging.getLogger(\"bot.main\")


async def main() -> None:
    Config.validate()
    await db.ensure_indexes()

    app = Client(
        name=Config.SESSION_NAME,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        workdir=\"./sessions\",
    )
    register_all(app, is_clone=False)
    app.owner_id = Config.DEV_ID
    app.developer_id = Config.DEV_ID

    await app.start()
    await cache_bot_profile_photo(app)
    me = await app.get_me()
    log.info(\"Main bot online: @%s (%s)\", me.username, me.id)

    await resume_saved_clones()
    log.info(\"Ready — awaiting updates.\")
    await idle()

    log.info(\"Shutting down...\")
    for bot_id, cli in list(state.running_clones.items()):
        try:
            await cli.stop()
        except Exception:
            pass
    await app.stop()


if __name__ == \"__main__\":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        log.error(\"Fatal: %s\", e, exc_info=True)
        sys.exit(1)
"
