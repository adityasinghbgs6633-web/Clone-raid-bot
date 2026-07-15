"\"\"\"Track incoming chat-join-requests for the panel.\"\"\"
from pyrogram import Client
from pyrogram.handlers import ChatJoinRequestHandler
from .. import database as db


async def on_join_request(client: Client, req) -> None:
    me = await client.get_me()
    await db.save_request(me.id, req.chat.id, req.from_user.id)


def register(app: Client) -> None:
    app.add_handler(ChatJoinRequestHandler(on_join_request))
"
