const vscode = require('vscode');
const cp = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    let disposable = vscode.commands.registerCommand('reviewer.reviewSelection', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found.');
            return;
        }

        const document = editor.document;
        const selection = editor.selection;
        const text = document.getText(selection);

        if (!text.trim()) {
            vscode.window.showWarningMessage('Please select some code to review.');
            return;
        }

        // Paths
        let workspaceFolder = vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri.fsPath : path.dirname(document.uri.fsPath);
        let scriptPath = path.join(workspaceFolder, 'code_reviewer', 'reviewer.py');
        
        // Fallback: search relative to extension directory if not found in workspace root
        if (!fs.existsSync(scriptPath)) {
            const extensionPath = context.extensionPath;
            scriptPath = path.join(extensionPath, '..', 'reviewer.py');
        }

        // Detect Python
        let pythonPath = 'python'; // Default fallback
        const venvPython = path.join(workspaceFolder, 'venv', 'Scripts', 'python.exe');
        if (fs.existsSync(venvPython)) {
            pythonPath = venvPython;
        } else {
            // Try to find venv in the root if we are in a subfolder
            const rootVenv = path.join(workspaceFolder, '..', 'venv', 'Scripts', 'python.exe');
            if (fs.existsSync(rootVenv)) {
                pythonPath = rootVenv;
            }
        }

        if (!fs.existsSync(scriptPath)) {
            vscode.window.showErrorMessage(`Code Reviewer: Script not found at ${scriptPath}. Please ensure the extension is correctly placed in the project.`);
            return;
        }

        // Output Channel
        const outputChannel = vscode.window.createOutputChannel("Local Code Reviewer");
        outputChannel.show();
        outputChannel.appendLine("Starting Local Code Reviewer...");

        // Args
        const startLine = selection.start.line + 1;
        const endLine = selection.end.line + 1;
        const filePath = document.uri.fsPath;

        const args = [
            scriptPath,
            '--file', filePath,
            '--start', startLine.toString(),
            '--end', endLine.toString()
        ];

        outputChannel.appendLine(`Executing: ${pythonPath} ${args.join(' ')}`);

        // Spawn
        const process = cp.spawn(pythonPath, args, { cwd: workspaceFolder });

        process.stdout.on('data', (data) => {
            outputChannel.append(data.toString());
        });

        process.stderr.on('data', (data) => {
            outputChannel.append(data.toString());
        });

        process.on('close', (code) => {
            outputChannel.appendLine(`\nReview finished with exit code ${code}.`);
        });
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}
