"""Message templates with premium branding."""
import random
from .config import Config

# ─── Unicode font maps ───
_BOLD = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"
)
_MONO = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"
)
_SC = str.maketrans("abcdefghijklmnopqrstuvwxyz", "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢ")


def bold(s: str) -> str:
    return s.translate(_BOLD)

def mono(s: str) -> str:
    return s.translate(_MONO)

def small_caps(s: str) -> str:
    return s.lower().translate(_SC)


FIRE, SKULL, ZAP, DIAMOND = "🔥", "💀", "⚡", "💎"
CROWN, SPARK, SHIELD, BOT = "👑", "✨", "🛡️", "🤖"
STAR, ROCKET, LOCK, KEY = "⭐", "🚀", "🔒", "🔑"
CHECK, CROSS, WARN, INFO = "✅", "❌", "⚠️", "📌"
GEAR, TROPHY, GHOST = "⚙️", "🏆", "👻"
BOMB, TARGET, FLAME = "💣", "🎯", "🌹"

SPINNER = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
DIV = "━━━━━━━━━━━━━━━"


def footer() -> str:
    dev = Config.DEV_USERNAME or "Developer"
    return f"{DIV}\n{DIAMOND} {small_caps('powered by')} {bold(Config.BOT_NAME)}\n{CROWN} {small_caps('dev')} • @{dev}"


def header(title: str, emoji: str = FIRE) -> str:
    return f"{emoji} {bold(title.upper())} {emoji}\n{DIV}"


START_VARIANTS = [
    "{h}\n\n{s} {hi}, {name}!\n\n{f} {tag1}\n{z} {tag2}\n\n{d} {choose}",
    "{h}\n\n{c} {hi2}, {name}\n\n{s} {tag1}\n{f} {tag2}\n\n{d} {choose}",
    "{h}\n\n{r} {hi2}, {name} {sp}\n\n{d} {tag1}\n{z} {tag2}\n\n{f} {choose}",
]


def start_text(first_name: str) -> str:
    v = random.choice(START_VARIANTS)
    return v.format(
        h=header(Config.BOT_NAME, FIRE),
        s=SPARK, c=CROWN, r=ROCKET, f=FIRE, z=ZAP, d=DIAMOND, sp=SPARK,
        hi=bold("Welcome"), hi2=small_caps("welcome"),
        name=bold(first_name or "User"),
        tag1=mono("Clone. Control. Conquer."),
        tag2=small_caps("premium clone bot maker at your fingertips"),
        choose=bold("Choose an option below") + " " + ZAP,
    ) + "\n\n" + footer()


CLONE_ASK = [
    f"{BOT} {bold('Send your Bot Token')}\n{DIV}\n{mono('From @BotFather -> /newbot')}\n{ZAP} {small_caps('paste it below')}\n{FIRE} <i>Premium Deploy Incoming!</i>",
    f"{CROWN} {bold('Bot Token Chahiye')}\n{DIV}\n{mono('Grab it from @BotFather')}\n{FIRE} {small_caps('drop the token here')}\n{ZAP} <i>Instant Premium Clone!</i>",
    f"{DIAMOND} {bold('Feed me your Token')}\n{DIV}\n{ZAP} {mono('@BotFather -> /newbot -> copy token')}\n{BOMB} {small_caps('paste. execute. dominate.')}\n{CHECK} <i>Premium Features Locked & Ready</i>",
]


def clone_success(username: str) -> str:
    return (
        f"{CROWN} {bold('🔥 PREMIUM CLONE DEPLOYED 🔥')}\n{DIV}\n"
        f"{DIAMOND} {small_caps('your clone is live')}\n"
        f"{BOT} • @{username}\n"
        f"{FIRE} {bold('Status: ONLINE')} {CHECK}\n"
        f"{SPARK} <b>Premium Features Activated!</b>\n\n" + footer()
    )


CLONE_FAIL = [
    f"{SKULL} {bold('Token Rejected')}\n{DIV}\n{CROSS} {mono('Invalid or in-use token')}\n{WARN} {small_caps('fresh token from @BotFather')}\n{ZAP} {bold('Try again!')}",
    f"{CROSS} {bold('Deploy Failed')}\n{DIV}\n{SKULL} {mono('bad token / network glitch')}\n{ZAP} {small_caps('retry with a valid token')}\n{FIRE} {bold('Keep trying!')}",
]


def ping_text(ms: int) -> str:
    return (
        f"{ZAP} {bold('PONG ⚡')}\n{DIV}\n"
        f"{DIAMOND} {mono('Latency check complete')}\n"
        f"{FIRE} {small_caps('response time')} {ms}ms\n"
        f"{CHECK} {bold('Premium Speed Active!')}\n\n" + footer()
    )


def force_sub_text(n: int) -> str:
    return (
        f"{SHIELD} {bold('ACCESS LOCKED')}\n{DIV}\n"
        f"{LOCK} {mono(f'Join {n} channel(s) to unlock premium features')}\n"
        f"{WARN} {small_caps('tap join then hit joined-refresh')}\n\n" + footer()
    )


STOP_MSG = (f"{SKULL} {bold('KILL-SWITCH ENGAGED')}\n{DIV}\n"
            f"{ZAP} {mono('All running tasks cancelled')}\n"
            f"{CHECK} {small_caps('bot silenced')}\n{FIRE} {bold('Status: STOPPED')}")

RESUME_MSG = (f"{FIRE} {bold('RESUMED ⚡')}\n{DIV}\n"
              f"{ZAP} {mono('Stop-flag cleared')}\n"
              f"{CHECK} {small_caps('back online')}\n{ROCKET} {bold('Ready for action!')}")

BANNED_MSG = f"{SKULL} {bold('ACCESS DENIED')}\n{DIV}\n{LOCK} {mono('You are banned from this bot')}\n{CROSS} {small_caps('contact developer')}"
DEV_ONLY = f"{LOCK} {bold('Restricted')}\n{DIV}\n{CROWN} {small_caps('developer-only zone')}\n{WARN} {bold('You are not authorized')}"
ADMIN_ONLY = f"{LOCK} {bold('Restricted')}\n{DIV}\n{SHIELD} {small_caps('admin-only access')}"


def clone_start_text(owner_username: str, first_name: str) -> str:
    return (
        f"{header('PREMIUM CLONE BOT', DIAMOND)}\n\n"
        f"{CROWN} {bold('Welcome')}, {bold(first_name or 'User')}!\n{DIV}\n"
        f"{DIAMOND} {mono(f'Premium Clone by @{owner_username}')}\n"
        f"{FIRE} {small_caps('tap a button below to start raiding')}\n"
        f"{ROCKET} <b>All Premium Features Active!</b>"
    )


HELP_PAGES = [
    (f"{header('USER COMMANDS', DIAMOND)}\n"
     f"{DIAMOND} {mono('/start')} — {small_caps('open main menu')}\n"
     f"{DIAMOND} {mono('/help')} — {small_caps('this menu')}\n"
     f"{DIAMOND} {mono('/ping')} — {small_caps('check latency')}\n"
     f"{DIAMOND} {mono('/clone')} — {small_caps('clone your own premium bot')}\n"
     f"{DIAMOND} {mono('/stats')} — {small_caps('view statistics')}\n"
     f"{DIV}\n{SPARK} {bold('Page 1 / 4')}"),
    (f"{header('ADMIN COMMANDS', SHIELD)}\n"
     f"{SHIELD} {mono('/addadmin <id>')} — {small_caps('add admin (dev only)')}\n"
     f"{SHIELD} {mono('/deladmin <id>')} — {small_caps('remove admin (dev only)')}\n"
     f"{SHIELD} {mono('/addfsub')} — {small_caps('add force-sub channel')}\n"
     f"{SHIELD} {mono('/delfsub')} — {small_caps('remove channel')}\n"
     f"{SHIELD} {mono('/listfsub')} — {small_caps('list all channels')}\n"
     f"{SHIELD} {mono('/broadcast')} — {small_caps('mass message (reply)')}\n"
     f"{SHIELD} {mono('/stop')} • {mono('/resume')} — {small_caps('kill-switch')}\n"
     f"{DIV}\n{SPARK} {bold('Page 2 / 4')}"),
    (f"{header('DEVELOPER COMMANDS', CROWN)}\n"
     f"{CROWN} {mono('/panel')} — {small_caps('open dev panel')}\n"
     f"{CROWN} {mono('/ban <id>')} — {small_caps('ban user permanently')}\n"
     f"{CROWN} {mono('/unban <id>')} — {small_caps('unban user')}\n"
     f"{CROWN} {mono('/killclone <id>')} — {small_caps('shut a clone')}\n"
     f"{CROWN} {mono('/logs')} — {small_caps('view activity logs')}\n"
     f"{CROWN} {mono('/stats')} — {small_caps('full system stats')}\n"
     f"{DIV}\n{SPARK} {bold('Page 3 / 4')}"),
    (f"{header('FUN / RAID PREMIUM', FIRE)}\n"
     f"{FIRE} {mono('.raid <count> [@user]')} — {small_caps('tag + raid (reply)')}\n"
     f"{FIRE} {mono('.raid stop')} — {small_caps('cancel raid')}\n"
     f"{FIRE} {mono('.sniper <keyword>')} — {small_caps('auto-reply on keyword')}\n"
     f"{FIRE} {mono('.mirror')} — {small_caps('echo target (reply)')}\n"
     f"{FIRE} {mono('.steal / .reset')} — {small_caps('identity clone')}\n"
     f"{FIRE} {mono('.bodyguard on/off')} — {small_caps('auto-defend owner')}\n"
     f"{DIV}\n{SPARK} {bold('Page 4 / 4 — PREMIUM FEATURES')}"),
]


def loading(step: int = 0) -> str:
    return f"{SPINNER[step % len(SPINNER)]} {small_caps('processing')}..."


def raid_log_msg(bot_name: str, target: int, count: int, sender: int) -> str:
    """Log message for raid activity."""
    return f"{BOMB} [{bot_name}] Raided {target} with {count} shots by {sender}"


def admin_added_msg(uid: int) -> str:
    """Message when admin is added."""
    return (f"{CHECK} {bold('✅ ADMIN PROMOTED')}\n{DIV}\n"
            f"👤 <code>{uid}</code>\n"
            f"{FIRE} {small_caps('they now have admin powers!')}\n"
            f"{CROWN} {bold('Premium access granted')}")


def fsub_added_msg(title: str) -> str:
    """Message when force-sub channel is added."""
    return (f"{CHECK} {bold('✅ FORCE-SUB ADDED')}\n{DIV}\n"
            f"📢 {title}\n"
            f"{ZAP} {small_caps('users must join now')}\n"
            f"{SHIELD} {bold('Channel enforced!')}")


def stats_msg(users: int, clones: int, starts: int, raids: int) -> str:
    """Detailed statistics message."""
    return (f"{CROWN} {bold('📊 PREMIUM STATS 📊')}\n{DIV}\n"
            f"👥 Users: {users}\n"
            f"🤖 Active Clones: {clones}\n"
            f"🚀 Starts: {starts}\n"
            f"{BOMB} Raids: {raids}\n\n"
            f"{CHECK} {bold('System Healthy!')}")


def broadcast_complete_msg(total: int, sent: int) -> str:
    """Broadcast completion message."""
    return (f"{CHECK} {bold('✅ BROADCAST COMPLETE')}\n{DIV}\n"
            f"📊 Total: {total}\n"
            f"✅ Delivered: {sent}\n"
            f"❌ Failed: {total - sent}\n"
            f"{FIRE} {bold('Premium broadcast done!')}")
