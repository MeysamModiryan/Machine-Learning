let currentSuggestion = '';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    refreshVariables();
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            executeCode();
        }
        if (e.ctrlKey && e.key === 'k') {
            clearCode();
        }
    });
    
    // Auto-resize textarea
    const textarea = document.getElementById('codeEditor');
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.max(400, this.scrollHeight) + 'px';
    });
});

// Execute Python code
async function executeCode() {
    const code = document.getElementById('codeEditor').value;
    const outputDiv = document.getElementById('output');
    
    if (!code.trim()) {
        showOutput('Please enter some code to execute.', 'error');
        return;
    }
    
    // Show loading state
    showOutput('Executing code...', 'info');
    
    try {
        const response = await fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        });
        
        const result = await response.json();
        
        if (result.success) {
            if (result.output) {
                showOutput(result.output, 'success');
            } else {
                showOutput('Code executed successfully (no output)', 'success');
            }
        } else {
            showOutput(`Error: ${result.error}`, 'error');
            if (result.traceback) {
                showOutput(result.traceback, 'traceback');
            }
        }
        
        // Refresh variables after execution
        refreshVariables();
        
    } catch (error) {
        showOutput(`Network error: ${error.message}`, 'error');
    }
}

// Show output in the output div
function showOutput(message, type = 'info') {
    const outputDiv = document.getElementById('output');
    
    if (type === 'info') {
        outputDiv.innerHTML = `<div class="text-info"><i class="fas fa-spinner fa-spin"></i> ${message}</div>`;
    } else if (type === 'success') {
        outputDiv.innerHTML = `<div class="output-success">${message}</div>`;
    } else if (type === 'error') {
        outputDiv.innerHTML = `<div class="output-error">${message}</div>`;
    } else if (type === 'traceback') {
        outputDiv.innerHTML += `<div class="output-traceback">${message}</div>`;
    }
    
    // Scroll to bottom
    outputDiv.scrollTop = outputDiv.scrollHeight;
}

// Clear the code editor
function clearCode() {
    document.getElementById('codeEditor').value = '';
    document.getElementById('codeEditor').style.height = '400px';
}

// Clear the output
function clearOutput() {
    document.getElementById('output').innerHTML = '<div class="text-muted">Output will appear here...</div>';
}

// Format code (basic indentation)
function formatCode() {
    const textarea = document.getElementById('codeEditor');
    let code = textarea.value;
    
    // Basic Python formatting
    const lines = code.split('\n');
    let formattedLines = [];
    let indentLevel = 0;
    
    for (let line of lines) {
        const trimmedLine = line.trim();
        
        // Decrease indent for certain keywords
        if (trimmedLine.startsWith('elif ') || 
            trimmedLine.startsWith('else:') || 
            trimmedLine.startsWith('except ') ||
            trimmedLine.startsWith('finally:') ||
            trimmedLine.startsWith('except:')) {
            indentLevel = Math.max(0, indentLevel - 1);
        }
        
        // Add indentation
        formattedLines.push('    '.repeat(indentLevel) + trimmedLine);
        
        // Increase indent for certain keywords
        if (trimmedLine.endsWith(':') && 
            !trimmedLine.startsWith('#') &&
            !trimmedLine.startsWith('"""') &&
            !trimmedLine.startsWith("'''")) {
            indentLevel++;
        }
    }
    
    textarea.value = formattedLines.join('\n');
}

// Load a code suggestion
async function loadSuggestion(suggestionType) {
    try {
        const response = await fetch('/suggest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task: suggestionType })
        });
        
        const result = await response.json();
        currentSuggestion = result.suggestion;
        
        // Show suggestion in modal
        document.getElementById('suggestionCode').textContent = currentSuggestion;
        const modal = new bootstrap.Modal(document.getElementById('suggestionModal'));
        modal.show();
        
    } catch (error) {
        showOutput(`Error loading suggestion: ${error.message}`, 'error');
    }
}

// Use the current suggestion
function useSuggestion() {
    document.getElementById('codeEditor').value = currentSuggestion;
    document.getElementById('codeEditor').style.height = 'auto';
    document.getElementById('codeEditor').style.height = Math.max(400, document.getElementById('codeEditor').scrollHeight) + 'px';
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('suggestionModal'));
    modal.hide();
}

// Refresh variables list
async function refreshVariables() {
    try {
        const response = await fetch('/variables');
        const result = await response.json();
        
        const variablesList = document.getElementById('variables-list');
        
        if (Object.keys(result.variables).length === 0) {
            variablesList.innerHTML = '<small class="text-muted">No variables yet</small>';
        } else {
            let html = '';
            for (const [name, info] of Object.entries(result.variables)) {
                html += `
                    <div class="variable-item">
                        <strong>${name}</strong><br>
                        <small>${info.type}: ${info.repr}</small>
                    </div>
                `;
            }
            variablesList.innerHTML = html;
        }
        
    } catch (error) {
        console.error('Error refreshing variables:', error);
    }
}

// Clear session
async function clearSession() {
    if (confirm('Are you sure you want to clear the session? This will remove all variables and data.')) {
        try {
            const response = await fetch('/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const result = await response.json();
            
            if (result.success) {
                showOutput('Session cleared successfully', 'success');
                refreshVariables();
            } else {
                showOutput('Error clearing session', 'error');
            }
            
        } catch (error) {
            showOutput(`Error clearing session: ${error.message}`, 'error');
        }
    }
}

// Get data info
async function getDataInfo(dataName) {
    try {
        const response = await fetch('/data_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data_name: dataName })
        });
        
        const result = await response.json();
        
        if (result.info) {
            let infoText = `Data Info for '${dataName}':\n`;
            infoText += `Type: ${result.info.type}\n`;
            
            if (result.info.shape) {
                infoText += `Shape: ${result.info.shape}\n`;
            }
            
            if (result.info.columns) {
                infoText += `Columns: ${result.info.columns.join(', ')}\n`;
            }
            
            if (result.info.head) {
                infoText += `\nFirst few rows:\n${JSON.stringify(result.info.head, null, 2)}`;
            }
            
            showOutput(infoText, 'success');
        } else {
            showOutput(`Variable '${dataName}' not found`, 'error');
        }
        
    } catch (error) {
        showOutput(`Error getting data info: ${error.message}`, 'error');
    }
}