"# 🗑️ Deleted / Rewritten Files

Yeh files original zip mein thi lekin **corrupt** thi — inmein Python code
ki jagah AI agent ka raw trace output (`Action: file_editor create ...`,
`Observation: Create successful ...`) tha, jisse Python parse hi nahi hota tha.

## ❌ Deleted (junk / duplicate)

Ye files removed hain — poori project fresh rewrite ki gayi hai:

| Original path                        | Reason                                              |
|--------------------------------------|-----------------------------------------------------|
| `main.py`                            | Corrupt — sirf agent trace tha, actual code nahi   |
| `config.py`                          | Corrupt — agent trace                              |
| `utils.py`                           | Corrupt — agent trace                              |
| `state.py`                           | Corrupt — agent trace                              |
| `clone_runner.py`                    | Corrupt — agent trace                              |
| `keyboards.py`                       | Corrupt — agent trace                              |
| `messages.py`                        | Corrupt — agent trace                              |
| `requirements.txt`                   | Corrupt — agent trace                              |
| `.env.example`                       | Corrupt — agent trace                              |
| `README.md`                          | Corrupt — agent trace                              |
| `run.sh`                             | Corrupt — agent trace                              |
| `__init__.py`                        | Corrupt — agent trace                              |
| `plugins/__init__.py`                | Corrupt — agent trace                              |
| `plugins/start.py`                   | Corrupt — agent trace                              |
| `plugins/inputs.py`                  | Corrupt — agent trace                              |
| `plugins/stats.py`                   | Corrupt — agent trace                              |
| `plugins/join_requests.py`           | Corrupt — agent trace                              |
| `plugins/clone.py`                   | Corrupt — agent trace                              |
| `plugins/ping.py`                    | Corrupt — agent trace                              |
| `plugins/broadcast.py`               | Corrupt — agent trace                              |
| `plugins/help.py`                    | Corrupt — agent trace                              |
| `plugins/mirror.py`                  | Corrupt — agent trace                              |
| `plugins/pelo.py`                    | Duplicate raid — merged into `handlers/raid.py`    |
| `plugins/force_sub.py`               | Corrupt — agent trace                              |
| `plugins/dev_panel.py`               | Corrupt — agent trace                              |
| `plugins/raid.py`                    | Corrupt — agent trace                              |
| `plugins/stop.py`                    | Corrupt — agent trace                              |
| `plugins/premium_raid.py`            | Contained slur/abuse content — removed             |
| `plugins/bodyguard.py`               | Rewritten cleanly                                  |
| `plugins/identity.py`                | Rewritten cleanly                                  |
| `plugins/mirror_echo.py`             | Duplicate — merged into `handlers/mirror.py`       |
| `plugins/sniper.py`                  | Rewritten cleanly                                  |
| `plugins/branding.py`                | Merged into `messages.py` / `utils.py`             |
| `shayaris.py` (original)             | **Extremely vulgar/abusive slurs** — replaced with clean roast lines |

## 🧹 Only file kept as-is
- `database.py` — was the only file with real (working) code. Even so, we
  rebuilt it with proper indexes + more collections in the new
  `bot/database.py`.

---

## ✅ Everything is now in `CloneBotMaker/bot/` — see `README.md`.
"
