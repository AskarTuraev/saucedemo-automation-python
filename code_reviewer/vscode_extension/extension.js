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
        const workspaceFolder = vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri.fsPath : path.dirname(document.uri.fsPath);
        const scriptPath = path.join(workspaceFolder, 'code_reviewer', 'reviewer.py');
        
        // Detect Python
        let pythonPath = 'python'; // Default fallback
        const venvPython = path.join(workspaceFolder, 'venv', 'Scripts', 'python.exe');
        if (fs.existsSync(venvPython)) {
            pythonPath = venvPython;
        }

        if (!fs.existsSync(scriptPath)) {
            vscode.window.showErrorMessage(`Reviewer script not found at: ${scriptPath}`);
            return;
        }

        // Output Channel
        const outputChannel = vscode.window.createOutputChannel("AI Code Reviewer");
        outputChannel.show();
        outputChannel.appendLine("Starting AI Code Review...");

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
