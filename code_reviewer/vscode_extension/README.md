# Gemini Code Reviewer - VS Code Extension

This is a local wrapper extension to run the `code_reviewer/reviewer.py` script directly from the VS Code context menu.

## Installation

Since this is a local extension, you need to load it into VS Code manually.

### Option 1: Run in Debug Mode (Easiest)
1. Open this folder (`code_reviewer/vscode_extension`) in VS Code.
2. Press `F5` to launch a new Extension Development Host window.
3. Open your project in that new window.
4. Select code -> Right Click -> **Gemini: Review Selection**.

### Option 2: Package and Install
1. Ensure you have `vsce` installed: `npm install -g @vscode/vsce`
2. Run `vsce package` in this directory to generate a `.vsix` file.
3. In your main VS Code, go to Extensions -> `...` -> **Install from VSIX...** and select the generated file.

## Requirements
- Python installed and available in your PATH or in a `venv` inside your project.
- The `code_reviewer` folder must be in the root of your workspace.
