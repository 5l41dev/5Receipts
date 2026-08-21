# 💜 5Receipts

A purple-themed Discord receipt generator — cook 1:1 receipts for 50+ brands, send them
spoofed (from the brand's own domain) or normal, manage licenses, whitelist staff, and
sell access with built-in PayPal flow & support tickets.

> Built as a public drop by **5l41** — [5l41.nex4.xyz](https://5l41.nex4.xyz).
> Everything is purple, every reply is re-written, and setup is a single `config.json` away.

---

## ✨ Features

- 🧾 **50+ brand receipts** — StockX, Nike, Apple, Adidas, Bape, Dior, LV, Zara, Zalando & more
- 📮 **Two delivery modes** — Spoofed (brand domain) or Normal (your SMTP domain)
- 🛒 **PayPal checkout flow** with Friends & Family note generator
- 👑 **Staff system** — whitelist/unwhitelist, admin panel, license management
- ⚙️ **Live bot settings** — change bot name, avatar, activity & customer role in Discord
- 🎫 **Support tickets** — one-click Buy / Question / Partner / Support tickets
- 🌍 **Regions** — US, DE & AUTH receipt packs, gated by role
- 💜 **Fully purple themed** — one constant controls every embed color
- 💾 **Zero manual DB setup** — database + output folder created automatically on first run

---

## 🚀 Quick Start (2 minutes)

### 1. Download

```bash
git clone https://github.com/5l41dev/5Receipts.git
cd 5Receipts
```

Or download the ZIP from GitHub and extract it.

### 2. Install

**Windows (double-click):**
```
install.bat
```

**All platforms:**
```bash
pip install -r requirements.txt
```

### 3. Configure

Copy the example config:
```bash
cp config.example.json config.json
```

Open `config.json` and fill in **every value** (see [Configuration](#-configuration) below).

### 4. Run

**Windows (double-click):**
```
start.bat
```

**All platforms:**
```bash
python main.py
```

The bot will:
- Create `data.db` (license database) automatically
- Create `receipt/updatedrecipies/` automatically
- Whitelist your `owner_id` automatically

---

## 📋 Configuration

All settings live in `config.json`. Every placeholder must be filled before the bot works.

| Key | What to put there | Required |
| --- | --- | --- |
| `tokens.main` | Your bot token from the [Developer Portal](https://discord.com/developers/applications) | ✅ |
| `owner_id` | Your Discord user ID (auto-whitelisted on first run) | ✅ |
| `client_role_id` | The role buyers get (gates `/generate` + settings) | ✅ |
| `staff_role_id` | Staff role for ticket access | ⬜ |
| `paper_access_role_id` | Paper access role | ⬜ |
| `emu_access_role_id` | Emu access role | ⬜ |
| `paypal_ping_role_id` | Role pinged when `/paypal` is used | ⬜ |
| `bot_name` | Name shown on panels (e.g. `5Receipts`) | ✅ |
| `activity` | Text under the bot's status | ⬜ |
| `invite` | Your server invite link | ⬜ |
| `paypal_email` | Your PayPal address | ⬜ |
| `pic_channel` | Channel where posting an image replies with its URL | ⬜ |
| `general_channel` | General channel ID | ⬜ |
| `ticket_category_id` | Category where tickets are created | ⬜ |
| `ticket_panel_channel` | Channel where `/ticket` posts the panel | ⬜ |
| `setup_guide_channel` | Setup guide channel (linked in auto-replies) | ⬜ |
| `vouch_channel` | Vouch channel (shown in admin panel) | ⬜ |
| `sales_channel` | Channel where access-granted embeds get posted | ⬜ |
| `smtp.server` | SMTP server (e.g. `smtp.mailersend.net`) | ✅ |
| `smtp.port` | SMTP port (usually `587`) | ✅ |
| `smtp.username` | SMTP username | ✅ |
| `smtp.password` | SMTP password | ✅ |
| `smtp.sender_domain` | Sender email domain (e.g. `noreply@yourdomain.com`) | ✅ |
| `zyte.api_key` | Your [Zyte](https://zyte.com) API key | ✅ |

> ⚠️ `config.json` is **gitignored** — it will never be committed. Fill it in locally.

---

## 🧾 Commands

| Command | Who | What it does |
| --- | --- | --- |
| `/generate` | Customers | Open the receipt generator — pick region, brand, fill the form |
| `/paypal` | Customers | Show PayPal details for purchasing a plan |
| `/panel @user` | Owner | Inspect or manage a user's access (Add/Remove access, check info) |
| `/edit @user` | Owner | Alias for `/panel` |
| `/whitelist @user` | Owner | Grant a user staff access |
| `/unwhitelist @user` | Owner | Revoke a user's staff access |
| `/settings` | Staff | Change bot name, avatar, activity & customer role live |
| `/ticket` | Staff | Post the support ticket panel in the configured channel |
| `/help` | Everyone | Show the full command list |

---

## 🧠 How Selling Works

1. Customer hits **Buy** on the ticket panel → ticket opens
2. You agree on a plan, they run `/paypal` → they send via Friends & Family
3. You run `/panel @customer` → **Add Access** → pick `1 Month` or `Lifetime`
4. Bot grants the role, writes the license, and posts the confirmation in `sales_channel`
5. Customer runs `/generate` → picks region → picks brand → fills the form
6. They choose **Spoofed** or **Normal** → receipt lands in their inbox

---

## 📁 Project Structure

```
5Receipts/
├── main.py              # Bot entrypoint, auto-replies, startup setup
├── config.json          # Your local config (gitignored — never committed)
├── config.example.json  # Template — copy this to config.json
├── install.bat          # Windows one-click installer
├── start.bat            # Windows one-click launcher
├── requirements.txt     # Python dependencies
├── commands/            # Slash commands (help, generate, panel, paypal, ticket, settings, whitelists)
├── addons/              # Views, modals & settings UI (RegionalView, emailmodal, botsettings, etc.)
├── modals/              # Brand-specific receipt forms (52 brands)
├── emails/              # SMTP senders (normal + spoofed) & delivery choice
├── receipt/             # Brand HTML receipt templates (do not edit unless you know what you're doing)
│   └── updatedrecipies/ # Generated receipts land here (gitignored)
├── utils/               # Theme (purple), config loader, database init, admin panel
│   ├── theme.py         # All colors, branding & developer credit
│   ├── config.py        # Loads config.json into constants
│   ├── database.py      # Auto-creates the licenses table
│   └── adminpanel.py    # Admin panel views (buttons + dropdown)
├── data.db              # License database (gitignored — created on first run)
└── whitelist.txt        # Staff whitelist (gitignored)
```

---

## 🛠️ Bot Intents

The bot uses `discord.Intents.all()`. In the [Developer Portal](https://discord.com/developers/applications) → **Bot** tab, enable:

- ✅ Presence Intent
- ✅ Server Members Intent
- ✅ Message Content Intent
- ✅ All privileged intents

Without **Message Content Intent**, the auto-replies (e.g. answering "how to generate") will not work.

---

## 🔗 Inviting the Bot

When inviting via OAuth2, use these scopes and permissions:

**Scopes:** `bot` + `applications.commands`

**Permissions:** Send Messages, Embed Links, Attach Files, Manage Messages, Manage Roles (for auto-assigning buyer role), Use Slash Commands

A ready-made invite link (replace `YOUR_CLIENT_ID` with your bot's Application ID from config):

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=379968
```

---

## 🎨 Theming

Every embed color comes from one constant:

```python
# utils/theme.py
PURPLE = 0xA855F7        # change once, the whole bot follows
DEVELOPER = "5l41"       # shown in every footer credit
DEV_URL = "https://5l41.nex4.xyz"
```

The brand name lives in `config.json` (`bot_name`) and `utils/theme.py` (`BRAND`).
The dev credit is stamped across every embed footer, modal, and source file header.

---

## 🛡️ Before You Push to GitHub

- [ ] `config.json` filled locally, **not** committed
- [ ] `data.db` absent from the repo (gitignored)
- [ ] `receipt/updatedrecipies/` absent from the repo (gitignored)
- [ ] `whitelist.txt` absent from the repo (gitignored)
- [ ] Your own Zyte key + SMTP credentials in your local `config.json`
- [ ] No real bot tokens left in any file

---

## ❓ Troubleshooting

| Problem | Fix |
| --- | --- |
| `LoginFailure: Improper token has been passed` | Your bot token is invalid. Reset it in the [Developer Portal](https://discord.com/developers/applications) and paste the new one into `config.json` |
| `5Receipts didn't respond in time` | The bot lacks a permission (usually Manage Roles). Check the bot's role hierarchy — its role must be **above** the buyer role |
| Auto-replies don't work | Enable **Message Content Intent** in the Developer Portal |
| Receipts not sending | Check your SMTP credentials in `config.json`. Make sure `smtp.username` and `smtp.password` are correct |
| Product images missing | Your Zyte API key may be invalid or expired. Check `zyte.api_key` in `config.json` |
| `config.json not found` | Run `install.bat` or copy `config.example.json` to `config.json` |
| Bot runs but commands don't show | The bot needs the `applications.commands` scope when invited. Re-invite with the correct scopes |

---

## 💜 Credits

Developed by **5l41** — [5l41.nex4.xyz](https://5l41.nex4.xyz)) 💜
