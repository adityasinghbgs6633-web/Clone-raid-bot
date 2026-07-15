"# 🔥 Clone Bot Maker — v2 (Clean Rebuild)

Premium Telegram Clone-Bot Maker on **Pyrogram v2 + MongoDB (Motor)**.
Runs on **Termux / VPS / any Linux** with `python -m bot.main`.

---

## ✨ Features

- 🤖 **Multi-clone system** — deploy unlimited bots from just a token
- 👨‍💻 **Developer Panel** — button-driven admin, requests, bans, broadcast, kill, logs, reset
- 🛡️ **Sub-Admins** with full permission set (broadcast, force-sub, approve, ban)
- 📢 **Multi-channel Force-Sub** — panel + `/addfsub` `/delfsub` `/listfsub`
- ✅ **Chat-Join-Request** approve/decline from panel
- 🔌 **Kill Clone** button + `/killclone`
- 📣 **Broadcast** — reply-and-copy to every stored user (FloodWait aware)
- 🧹 **Reset Stats** with confirm dialog
- 📜 **Activity logs** feed
- 🛑 **Raid-safe `/stop` / `/resume`** — priority handler (group=-1)
- 🏓 **`/ping`** on main + all clones
- ❓ **Paginated `/help`** — user / admin / dev / fun
- 🎯 **Sniper** — auto-reply on keyword (`.sniper <kw>`)
- 🪞 **Mirror Echo** — echo target user (`.mirror` reply)
- 🎭 **Identity Clone** — `.steal` / `.reset`
- 🛡️ **Bodyguard** — auto-defend when someone replies rude
- 🔥 **Shayari raid** — `.raid <count>` (clean, non-vulgar)

---

## 🚀 Quick Start (Termux / VPS)

```bash
# Install python + build tools
pkg install python git binutils build-essential -y      # Termux
# or on Ubuntu: apt install -y python3 python3-venv python3-pip git

# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Config
cp .env.example .env
nano .env                     # fill API_ID / API_HASH / BOT_TOKEN / DEV_ID

# Run (auto-restart wrapper)
chmod +x run.sh
./run.sh
```

Run in background:
```bash
# tmux (VPS)
tmux new -s clonebot './run.sh'   # detach: Ctrl+B then D
# screen (Termux)
screen -S clonebot ./run.sh       # detach: Ctrl+A then D
```

## systemd service (VPS)

`/etc/systemd/system/clonebot.service`:
```ini
[Unit]
Description=Clone Bot Maker
After=network.target mongod.service

[Service]
Type=simple
WorkingDirectory=/opt/clonebot
ExecStart=/opt/clonebot/run.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable --now clonebot
journalctl -u clonebot -f
```

---

## 🔑 Required env

| Key            | Where to get                                        |
|----------------|-----------------------------------------------------|
| `API_ID`/`API_HASH` | https://my.telegram.org → API development tools |
| `BOT_TOKEN`    | @BotFather                                          |
| `DEV_ID`       | Your Telegram ID (@userinfobot)                     |
| `DEV_USERNAME` | Your @username (no `@`)                             |
| `MONGO_URL`    | Local mongo or Atlas URI                            |
| `DB_NAME`      | e.g. `clone_bot_maker`                              |

---

## 🧠 Roles

| Role         | Access                                                    |
|--------------|-----------------------------------------------------------|
| **Developer** (`DEV_ID`) | Everything — full panel                       |
| **Sub-Admin**            | Panel minus: admins, kill clones, reset stats |
| **Clone Owner**          | Their clone only                              |
| **User**                 | Bot features                                  |

---

## 🛑 Raid-safe `/stop`

- Registered at `group=-1` so it fires **before** every other handler
- Sets `stop_flag=True` per-bot in Mongo
- Cancels every task in the in-memory registry
- Broadcast & raid loops honour the flag

Turn back on with `/resume`.

---

## 📁 File layout

```
CloneBotMaker/
├── bot/
│   ├── main.py             # entry
│   ├── config.py           # env loader
│   ├── database.py         # motor + collections
│   ├── messages.py         # fonts, emojis, variants
│   ├── keyboards.py        # inline keyboards
│   ├── utils.py            # helpers
│   ├── state.py            # task registry, conv state
│   ├── clone_runner.py     # spawn/kill clones
│   ├── shayaris.py         # clean roast lines
│   └── handlers/
│       ├── __init__.py     # register_all()
│       ├── stop.py         # priority /stop (group=-1)
│       ├── start.py
│       ├── help.py
│       ├── ping.py
│       ├── stats.py
│       ├── clone.py
│       ├── force_sub.py
│       ├── dev_panel.py
│       ├── broadcast.py
│       ├── join_requests.py
│       ├── inputs.py
│       ├── raid.py
│       ├── sniper.py
│       ├── mirror.py
│       ├── identity.py
│       └── bodyguard.py
├── requirements.txt
├── .env.example
├── run.sh
├── README.md
└── DELETED_FILES.md        # list of removed junk
```

---

## 📜 License
MIT — do what you want, just don't be evil. 💎
"
