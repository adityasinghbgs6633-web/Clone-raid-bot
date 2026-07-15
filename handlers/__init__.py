"\"\"\"Register all handlers on a given Pyrogram Client.\"\"\"
from pyrogram import Client
from . import stop, start, help as help_h, ping, clone, force_sub, dev_panel
from . import inputs, join_requests, broadcast, stats, raid, sniper, mirror, identity, bodyguard


def register_all(app: Client, is_clone: bool = False) -> None:
    # stop must be first (priority)
    stop.register(app, is_clone)
    start.register(app, is_clone)
    help_h.register(app, is_clone)
    ping.register(app, is_clone)
    stats.register(app, is_clone)

    if not is_clone:
        clone.register(app)
        force_sub.register(app)
        dev_panel.register(app)
        broadcast.register(app)
        join_requests.register(app)

    # Fun / raid on both
    raid.register(app, is_clone)
    sniper.register(app, is_clone)
    mirror.register(app, is_clone)
    identity.register(app, is_clone)
    bodyguard.register(app, is_clone)

    # inputs (conv router) — always last, main only
    if not is_clone:
        inputs.register(app)
"
