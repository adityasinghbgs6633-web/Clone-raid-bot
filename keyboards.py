"""Updated keyboards with premium buttons and new features."""
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_kb(is_dev: bool = False, is_admin: bool = False) -> InlineKeyboardMarkup:
    """Main menu with all premium features."""
    rows = [
        [InlineKeyboardButton("🤖 Clone Bot", callback_data="menu:clone"),
         InlineKeyboardButton("📢 Join Channel", callback_data="menu:fsub")],
        [InlineKeyboardButton("👨‍💻 Admin Panel", callback_data="menu:admin"),
         InlineKeyboardButton("📊 Stats", callback_data="menu:stats")],
        [InlineKeyboardButton("❓ Help", callback_data="help:0"),
         InlineKeyboardButton("🏓 Ping", callback_data="menu:ping")],
    ]
    if is_dev:
        rows.append([InlineKeyboardButton("👑 Developer Panel", callback_data="dev:home")])
    elif is_admin:
        rows.append([InlineKeyboardButton("🛡️ Admin Panel", callback_data="dev:home")])
    return InlineKeyboardMarkup(rows)


def clone_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ Help", callback_data="help:0"),
         InlineKeyboardButton("🏓 Ping", callback_data="menu:ping")],
    ])


def dev_panel_kb() -> InlineKeyboardMarkup:
    """Enhanced developer panel with all controls."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Manage Admins", callback_data="dev:admins"),
         InlineKeyboardButton("✅ Requests", callback_data="dev:requests")],
        [InlineKeyboardButton("📢 Force Channels", callback_data="dev:fsub"),
         InlineKeyboardButton("🚫 Ban/Unban", callback_data="dev:ban")],
        [InlineKeyboardButton("📣 Broadcast", callback_data="dev:bcast"),
         InlineKeyboardButton("🔌 Kill Clone", callback_data="dev:kill")],
        [InlineKeyboardButton("📜 Logs", callback_data="dev:logs"),
         InlineKeyboardButton("🧹 Reset Stats", callback_data="dev:reset")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu:home")],
    ])


def admin_panel_kb() -> InlineKeyboardMarkup:
    """Admin panel with restricted features."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Requests", callback_data="dev:requests")],
        [InlineKeyboardButton("📢 Force Channels", callback_data="dev:fsub")],
        [InlineKeyboardButton("📣 Broadcast", callback_data="dev:bcast")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu:home")],
    ])


def help_kb(page: int, total: int) -> InlineKeyboardMarkup:
    prev_p = (page - 1) % total
    next_p = (page + 1) % total
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️", callback_data=f"help:{prev_p}"),
         InlineKeyboardButton(f"{page+1}/{total}", callback_data="help:noop"),
         InlineKeyboardButton("▶️", callback_data=f"help:{next_p}")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu:home")],
    ])


def back_kb(target: str = "menu:home") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data=target)]])


def mandatory_join_kb(channel: dict) -> InlineKeyboardMarkup:
    """Keyboard for mandatory force-join channel."""
    link = channel.get("invite_link") or f"https://t.me/{channel.get('chat_title', 'channel')}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"📢 Join {channel.get('chat_title', 'Channel')}", url=link)],
        [InlineKeyboardButton("✅ Joined — Verify", callback_data="mandatory:check")],
    ])


def force_sub_kb(channels: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for c in channels:
        link = c.get("invite_link") or f"https://t.me/c/{str(c['chat_id']).replace('-100', '')}/1"
        rows.append([InlineKeyboardButton(f"📢 Join {c.get('chat_title', 'Channel')}", url=link)])
    rows.append([InlineKeyboardButton("✅ Joined — Refresh", callback_data="fsub:check")])
    return InlineKeyboardMarkup(rows)


def confirm_kb(action: str, target: str = "") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Yes", callback_data=f"confirm:{action}:{target}"),
        InlineKeyboardButton("❌ No", callback_data="dev:home"),
    ]])


def approve_kb(chat_id: int, user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Approve", callback_data=f"req:ok:{chat_id}:{user_id}"),
        InlineKeyboardButton("❌ Decline", callback_data=f"req:no:{chat_id}:{user_id}"),
    ]])


def fsub_list_kb(channels: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for c in channels:
        rows.append([InlineKeyboardButton(
            f"❌ {c.get('chat_title', c['chat_id'])}",
            callback_data=f"fsub:del:{c['chat_id']}"
        )])
    rows.append([
        InlineKeyboardButton("➕ Add Channel", callback_data="fsub:add"),
        InlineKeyboardButton("🔙 Back", callback_data="dev:home"),
    ])
    return InlineKeyboardMarkup(rows)


def admins_list_kb(admin_docs: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for a in admin_docs:
        rows.append([InlineKeyboardButton(
            f"❌ Remove {a['_id']}", callback_data=f"adm:del:{a['_id']}"
        )])
    rows.append([
        InlineKeyboardButton("➕ Add Admin", callback_data="adm:add"),
        InlineKeyboardButton("🔙 Back", callback_data="dev:home"),
    ])
    return InlineKeyboardMarkup(rows)


def clones_list_kb(clones: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for c in clones[:20]:
        status = "🟢" if not c.get("stopped") else "🔴"
        rows.append([InlineKeyboardButton(
            f"{status} @{c.get('username', c['_id'])}",
            callback_data=f"kill:{c['_id']}"
        )])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="dev:home")])
    return InlineKeyboardMarkup(rows)
