# Uradium

A lightweight Python CLI AI chatbot powered by the [Groq](https://groq.com/) API, featuring persistent local memory, automatic conversation summarization, customizable terminal colors, and local file assistance.

## Features

- **Groq API Chat** — Runs conversational completions using `openai/gpt-oss-120b` through the `groq` Python SDK.
- **Combined Persistent Memory** — Saves recent messages, permanent user facts, and a rolling conversation summary locally in `bot_memory.json`.
- **Automatic Summarization** — When active chat history grows past 16 messages, earlier turns are automatically condensed into a short summary using `openai/gpt-oss-20b` while keeping the 4 most recent messages.
- **Local File Reading & Editing (`/file`)** — Loads a local text file along with your instructions and sends it to the model. If the response contains a fenced code block, Uradium automatically writes the first code block back to that file path.
- **Customizable Terminal Colors** — Lets you pick ANSI colors (`green`, `yellow`, `cyan`, `red`, `magenta`, `white`) for your messages and AI replies, saved in `color_config.json`.

## Files

- `mybot.py` — Main CLI chatbot script
- `bot_memory.json` — Persistent storage for `permanent_facts`, `chat_history`, and `summary`
- `color_config.json` — Saved terminal color preferences for user and AI output
- `yeah.bat` — Windows batch launcher script
- `sbs tutorial.txt` — Original step-by-step setup notes

## Setup

### Requirements

- Python 3
- [`groq`](https://pypi.org/project/groq/) Python package
- A Groq API key from [console.groq.com/keys](https://console.groq.com/keys)

### Installation & Running

1. Install the Groq SDK:
   ```bash
   pip install groq
   ```
2. Set your Groq API key as the `GROQ_API_KEY` environment variable (the Groq client automatically uses it when `api_key` resolves to `None`), or update the `Groq(...)` initialization in `mybot.py`.
3. *(Optional)* Edit `default_instructions` in `mybot.py` to customize the AI's system prompt.
4. Start the bot:
   ```bash
   python mybot.py
   ```
   On Windows, you can also edit the path inside `yeah.bat` to point to this folder and run `yeah.bat`.

## Commands

| Command | Description |
| --- | --- |
| `/help` | Show the list of available commands |
| `/clear` | Wipe `bot_memory.json` (chat history, summary, and permanent facts) |
| `/stats` | Show the number of active chat history turns and saved permanent facts |
| `/remember` | Save a permanent fact to `bot_memory.json` |
| `/file` | Read a local file, send it to the AI with instructions, and auto-save returned code block edits |
| `/color` | Change terminal colors for `You` and `AI` prompts |
| `exit` | Quit the chat |

## Notes

- If you hit Groq token or rate limits on long sessions, run `/clear` to reset saved chat history or upgrade your Groq plan.
