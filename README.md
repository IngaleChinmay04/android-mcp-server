# Android MCP Server

## Overview

This repository provides an **MCP (Model Context Protocol) server for Android device control** through ADB (Android Debug Bridge). It exposes simple tools (functions) that can be called from LLMs or clients (like Claude Desktop) to automate Android device actions such as opening Chrome and performing a search.

The goal is to make it easy for any client supporting MCP (such as Claude Desktop) to control an Android device using natural language and safe, auditable tools.

---

## Features

- **open_chrome_and_search**:  
  Opens the default browser on a connected Android device and performs a Google search for a given query.
- Easily extensible: add more ADB-powered tools as needed (launch apps, take screenshots, etc.)
- Secure: only exposes specific, whitelisted actions.

---

## Requirements

- **Python 3.10+**
- **ADB** installed and added to your system PATH
- An Android device with:
  - Developer mode enabled
  - USB debugging enabled
- [Claude Desktop](https://claude.ai/download) (or any MCP-compatible client)
- [uv](https://github.com/astral-sh/uv) Python project tool (recommended, but you can adapt to pip/venv if you wish)

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/IngaleChinmay04/android-mcp-server

cd android-mcp-server
```

### 2. Install [uv](https://github.com/astral-sh/uv) (if not already)

On Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On Mac/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal after install.

### 3. Set up the Python environment

```bash
uv venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

uv add "mcp[cli]"
```

### 4. (Optional) Test the server manually

```bash
uv run android_server.py
```

The server will wait for MCP client connections.

---

## Usage: Integrate with Claude Desktop

To connect your MCP server to Claude Desktop:

### 1. Ensure [Claude Desktop](https://claude.ai/download) is installed and **fully up to date**.

### 2. Edit/Create the Claude config file

**On Windows:**

- Location:  
  `C:\Users\<YourUsername>\AppData\Roaming\Claude\claude_desktop_config.json`

**On Mac:**

- Location:  
  `~/Library/Application Support/Claude/claude_desktop_config.json`

Create the file if it does not exist.

### 3. Add your server configuration

Example config (update the directory path if you cloned elsewhere):

```json
{
  "mcpServers": {
    "android_control": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\<YourUsername>\\Desktop\\android-mcp-server",
        "run",
        "android_server.py"
      ]
    }
  }
}
```

- Use the absolute path to your project folder.
- Save the config file.

### 4. Restart Claude Desktop

- Fully close all Claude Desktop windows (including tray icon).
- Reopen Claude Desktop.

### 5. Plug in your Android device

- Enable Developer Options and USB Debugging on your phone.
- Connect via USB.
- Approve any "Allow USB Debugging" prompts.

---

## Example Usage

In Claude Desktop, you can now use the tool by typing a natural language prompt such as:

- "Search for 'latest Android news' on my Android device."
- "Use the open_chrome_and_search tool with query: Python tutorials"

Claude will invoke the tool, and your phone's browser will open and perform the search.

---

## Adding More Tools

To extend functionality, simply add more `@mcp.tool()` decorated Python functions to `android_server.py`.  
For example, you can add tools to take a screenshot, install an app, open a specific app, etc.

---

## Troubleshooting

- **No device found?**  
  Make sure you have run `adb devices` and see your device listed.
- **MCP server not showing up in Claude?**  
  Double check your config file path and syntax, and restart Claude Desktop.
- **Unexpected token / JSON errors?**  
  Ensure there are NO print statements or logging to stdout in your server code; all outputs must go via MCP calls only.
- **Still stuck?**  
  Check the Claude logs (button in the Claude Desktop UI) for details.

---

## Credits

- [Anthropic/Claude](https://claude.ai)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.org)
- [uv by Astral](https://github.com/astral-sh/uv)

---
