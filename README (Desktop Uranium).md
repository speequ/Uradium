# Uradium

Uradium is a Windows desktop AI assistant that lets you chat with different AI providers from one app. Bring your own API key, choose a model, and keep your chats and preferences on your computer.

## What you can do

- **Chat with different AI providers** without changing applications.
- **Choose a model** from the available presets or enter a model ID supported by your account.
- **Keep conversations and memories** between sessions.
- **Save custom instructions** to guide the assistant's responses.
- **Open text files** and ask the assistant to explain or help edit them.
- **Customize the app** with themes and a wallpaper.
- **Export conversations** as Markdown or text.

## Before you start

Uradium uses your own API key. It does not include an AI subscription or free API access. Each provider has its own pricing, usage limits, and model availability.

Supported providers:

| Provider | Where to get an API key |
|---|---|
| Groq | [Groq Console](https://console.groq.com/keys) |
| OpenAI | [OpenAI API Keys](https://platform.openai.com/api-keys) |
| Anthropic Claude | [Anthropic Console](https://console.anthropic.com/settings/keys) |
| Google Gemini | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| OpenRouter | [OpenRouter Keys](https://openrouter.ai/keys) |
| Together AI | [Together AI Settings](https://api.together.ai/settings/api-keys) |
| DeepSeek | [DeepSeek Platform](https://platform.deepseek.com/api_keys) |
| Mistral | [Mistral Console](https://console.mistral.ai/api-keys/) |
| Cerebras | [Cerebras Cloud](https://cloud.cerebras.ai/) |
| Custom | An OpenAI-compatible API endpoint, its API key, and a model ID |

A model appearing in Uradium does not guarantee that your account can use it. Access depends on the provider, your account, and the model's current availability.

## Install and set up Uradium

1. Download the latest Windows installer from the repository's **[Releases](../../releases)** page.
2. Run the installer and open Uradium.
3. On the home screen, open **Menu → Settings & Memory**.
4. Select your provider.
5. Paste your API key and choose **Save key**.
6. Open the model selector and choose a model available to your account. You can also enter a custom model ID.
7. Start a conversation.

Each provider has its own saved key. Switching providers does not intentionally replace the keys saved for other providers.

## Everyday use

| Action | How to use it |
|---|---|
| Start a chat | Choose **Start a conversation** on the home screen. |
| Send a message | Type in the box at the bottom and press **Enter** or click **Send**. |
| Add a new line | Press **Shift + Enter**. |
| Attach a file | Use the paperclip button or choose **Open a file**. |
| Change provider or API key | Open **Menu → Settings & Memory**. |
| Change model | Use the **AI model** selector on the home screen or in the menu. |
| Start a new chat | Choose **New chat** from the menu. Permanent facts are kept. |
| Save a useful fact | Add it under **Permanent memory** in Settings & Memory. |
| Export a conversation | Choose **Export conversation** from the menu. |

For screenshots and more detailed usage instructions, see the [Desktop App Guide](docs/DESKTOP-APP-GUIDE.md).

## Prepare the project from source (Windows)

Use this section if you want to run the project from its source files or build your own installer. If you only want to use Uradium, download the installer from **Releases** instead.

### Requirements

- Windows 10 or Windows 11, 64-bit.
- [Node.js](https://nodejs.org/) with npm.
- [Python 3](https://www.python.org/downloads/) and the Windows `py` launcher.
- [Rust](https://www.rust-lang.org/tools/install) and the Windows C++ build tools required by Rust/Tauri.

### 1. Get the project files

Download the repository as a ZIP from GitHub and extract it, or clone it with Git. Open PowerShell in the extracted project folder. The folder should contain `package.json`, `src`, `backend`, and `src-tauri`.

### 2. Install the project dependencies

From the project folder, run:

```powershell
npm install
py -m pip install fastapi uvicorn pydantic pyinstaller
```

### 3. Prepare the Windows app files

Close Uradium before building. Make sure nothing else is using port `8000`, then run the build script from `src-tauri`:

```powershell
cd src-tauri
powershell -ExecutionPolicy Bypass -File .\build-uradium-sidecar.ps1
```

The script checks the required files and tools, builds the app's bundled service executable, and tests it before replacing the existing copy. If the script reports that port `8000` is in use, close the running Uradium app or other process using that port and try again.

### 4. Run Uradium in development mode

Return to the project folder and run:

```powershell
cd ..
npm run tauri dev
```

Do not start a second copy of the service with `py mybot.py` while the desktop app is running. The desktop app starts its own copy.

### 5. Build an installer

From the project folder, run:

```powershell
npm run tauri build
```

The generated Windows installer or bundle will be placed under:

```text
src-tauri/target/release/bundle/
```

The available installer formats depend on the release settings in the project.

## Your data and privacy

Uradium stores its local data in:

```text
%APPDATA%\Uradium\
```

- `config.json` contains saved provider settings, API keys, the selected model, and custom instructions.
- `bot_memory.json` contains saved chat history, the conversation summary, and permanent facts.

**Back up this folder before reinstalling or moving to another computer.** In the current version, API keys are stored as readable text in `config.json`; they are not encrypted. Never upload this file, add it to a public repository, or include it in a support ZIP. Your memory file may also contain private conversation content.

Your messages and any file contents you submit are sent to the provider you selected so it can generate a response. Review that provider's privacy policy and terms before sending sensitive information.

> **Important when editing files:** Uradium's file assistance is for text files. The current editing behavior may write the first code block in the AI's response directly to the selected original file. Make a backup before asking for changes, and review the result before using it. Do not use this feature on important files without a backup.

## Troubleshooting

### Uradium cannot connect or stays on the loading screen

Close and reopen the installed app. If you recently changed source files, rebuild the app's bundled files and then rebuild the installer. Updating a source file alone does not update an already-installed copy.

### `Port 8000 is already in use` or `WinError 10048`

Only one Uradium instance can use port `8000` at a time. Close other Uradium windows and make sure you have not started a separate copy with `py mybot.py` while the desktop app is open.

To identify the process using the port, run:

```powershell
netstat -ano | findstr :8000
```

Then identify the PID shown at the end of the line:

```powershell
tasklist /FI "PID eq <PID>"
```

Only stop the process after confirming that it belongs to Uradium.

### Provider switching reports `404` or a missing route

The installed app may contain an older bundled copy. Rebuild the bundled app files using the steps above, then build and install a fresh version. Restarting the app without rebuilding does not replace an outdated bundled copy.

### API key or authentication error

Check that the correct provider is selected, the key was saved for that provider, and the key is still active. Some providers require billing details or account verification before API access is enabled.

### Model not found or unavailable

Try another model preset or enter a model ID shown in your provider's current model catalogue. Model access and model IDs are controlled by the provider and can change over time.

### Groq returns Cloudflare Error 1010

This is an access-denied response from Cloudflare and does not necessarily mean the API key is invalid. Do not repeatedly retry an error that says the client signature is blocked. Keep the Ray ID from the error and contact the provider if the block persists.

---

If you find a problem, open a GitHub issue and include the steps to reproduce it and the exact error message. **Do not include API keys, `config.json`, `bot_memory.json`, or private conversation contents.**
