"\"\"\"Central config — env loader.\"\"\"
import os
from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int = 0) -> int:
    val = os.environ.get(name, \"\").strip()
    try:
        return int(val) if val else default
    except ValueError:
        return default


class Config:
    API_ID: int = _int(\"API_ID\")
    API_HASH: str = os.environ.get(\"API_HASH\", \"\").strip()
    BOT_TOKEN: str = os.environ.get(\"BOT_TOKEN\", \"\").strip()

    DEV_ID: int = _int(\"DEV_ID\")
    DEV_USERNAME: str = os.environ.get(\"DEV_USERNAME\", \"Developer\").strip().lstrip(\"@\")

    MONGO_URL: str = os.environ.get(\"MONGO_URL\", \"mongodb://localhost:27017\")
    DB_NAME: str = os.environ.get(\"DB_NAME\", \"clone_bot_maker\")

    BOT_NAME: str = os.environ.get(\"BOT_NAME\", \"Clone Bot Maker\")
    SUPPORT_CHAT: str = os.environ.get(\"SUPPORT_CHAT\", \"\").strip().lstrip(\"@\")
    SESSION_NAME: str = os.environ.get(\"SESSION_NAME\", \"clonebotmaker\")

    # Optional force-subscribe channel (username, without @)
    FORCE_CHANNEL: str = os.environ.get(\"FORCE_CHANNEL\", \"\").strip().lstrip(\"@\")

    @classmethod
    def validate(cls) -> None:
        missing = [k for k in (\"API_ID\", \"API_HASH\", \"BOT_TOKEN\", \"DEV_ID\")
                   if not getattr(cls, k)]
        if missing:
            raise RuntimeError(
                f\"Missing required env vars: {', '.join(missing)}. \"
                f\"Copy .env.example -> .env and fill them.\"
            )
