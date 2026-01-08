# Gemini Code Reviewer for VS Code

A lightweight Python tool integrated into VS Code to perform AI-powered code reviews on selected snippets using the Google Gemini API.

## Features

- Analyzes selected code directly from the VS Code editor.
- Uses **Gemini 3.0 Pro** for deep, high-quality analysis.
- Evaluates code based on 6 key pillars:
  1. Reliability & Stability
  2. Asserts & Verifiability
  3. Readability
  4. Hardcoding & Test Data
  5. DRY Principles
  6. Architecture

## Setup

### 1. Prerequisites
- Python 3.8+
- VS Code

### 2. Installation

1. Open a terminal in the `code_reviewer` folder:
   ```bash
   cd code_reviewer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure API Key:
   - Rename `.env.example` to `.env`:
     - **Windows (CMD):** `ren .env.example .env`
     - **PowerShell:** `Rename-Item .env.example .env`
     - **Linux/Mac:** `mv .env.example .env`
   - Open `.env` and paste your Google Gemini API key.

### 3. Usage

1. Open any code file in VS Code.
2. **Select the code** you want to review.
3. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).
4. Type **"Run Task"** and select it.
5. Choose **"Local Code Reviewer"**.

The results will appear in the VS Code Terminal panel.

### 4. (Optional) Keybinding Shortcut

To make it feel like a native feature, add a keyboard shortcut:

1. Open `File > Preferences > Keyboard Shortcuts` (`Ctrl+K Ctrl+S`).
2. Click the `Open Keyboard Shortcuts (JSON)` icon in the top right.
3. Add this entry:

```json
{
    "key": "ctrl+alt+r",
    "command": "workbench.action.tasks.runTask",
    "args": "Local Code Reviewer"
}
```

Now you can simply select code and press `Ctrl+Alt+R`!

## 📦 Using in Other Projects

This tool is designed to be standalone. You can easily add it to any other workspace:

1.  **Copy Folder:** Copy the entire `code_reviewer` directory to the root of your target project.
2.  **Install Deps:** Run `pip install -r code_reviewer/requirements.txt`.
3.  **Setup Key:** Create the `.env` file with your key inside `code_reviewer/`.
4.  **Run:** You can either:
    *   Use the VS Code Tasks integration (copy the `.vscode/tasks.json` configuration).
    *   OR install the local VS Code Extension included in `vscode_extension/` for a nicer context menu integration.
