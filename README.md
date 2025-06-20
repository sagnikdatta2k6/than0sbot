# than0sbot 🤖💥

> A powerful, AI-enhanced Discord bot built with Python & Gemini API — bringing intelligence, automation, and engagement to your server.

---

## 🌟 Features

| Category      | Functionality                           |
| ------------- | --------------------------------------- |
| 💬 AI Chat    | Responds to messages using Gemini API   |
| 🧠 Summarizer | Summarizes long messages & threads      |
| 📊 Polling    | Create polls with reaction-based voting |
| ⏰ Reminders   | Set and manage personal reminders       |
| 👋 Welcome    | Sends personalized welcome messages     |
| 🔌 Modular    | Clean architecture for easy extension   |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/sagnikdatta2k6/than0sbot.git
cd than0sbot
```

### 2️⃣ Setup Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Configure API Keys

Create a `.env` file (or use `.env.example`) and add:

```env
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

---

## 🧠 Usage

### ▶️ Start the Bot

```bash
python than0sbot_maincode.py
```

### 💬 Example Commands

```text
!poll "Which feature next?" "Slash Commands" "Better UI"
!summarize <message_link>
!remindme 15m "Submit report"
```

Bot also **auto-replies** to messages using Gemini's conversational model when mentioned or triggered.

---

## 🧱 Architecture Overview

* **discord.py** for bot framework
* **Gemini API** for intelligent interactions
* **Command-handler design** for scalability
* **Poll & reminder modules** built with simplicity and efficiency
* `.env` based config for environment safety

---

## 📌 Roadmap

* [x] Core modules: Polls, Reminders, Summarizer
* [x] Gemini chat integration
* [ ] Slash commands with Discord Interactions API
* [ ] Persistent DB-backed reminders (SQLite/Redis)
* [ ] Docker containerization
* [ ] CI/CD with GitHub Actions

---

## 🧪 Tests

Currently manual testing. Auto-test support (pytest) coming soon.

✅ Pull Requests with test coverage are encouraged.

---

## 📜 License

**MIT License** — free to use, modify, and distribute.

---

## 🙌 Acknowledgments

* [discord.py](https://github.com/Rapptz/discord.py) for bot foundation
* [Gemini API](https://ai.google.dev) for LLM-based intelligence
* Inspiration from community-built Discord bots

---

## 🛠️ Maintainer

**Sagnik Datta**
📧 [sagnikdatta2k6@gmail.com](mailto:sagnikdatta2k6@gmail.com)
🌐 [GitHub Profile](https://github.com/sagnikdatta2k6)
