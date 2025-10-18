"""
Main Python Assistant class that provides comprehensive Python development support
"""

import os
import sys
import ast
import subprocess
import importlib
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json
import traceback
from datetime import datetime

class PythonAssistant:
    """
    A comprehensive Python Assistant that provides code analysis, debugging,
    machine learning support, and development assistance.
    """
    
    def __init__(self, workspace_path: str = None):
        """
        Initialize the Python Assistant
        
        Args:
            workspace_path: Path to the workspace directory
        """
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.supported_extensions = {'.py', '.ipynb', '.csv', '.json', '.txt', '.md'}
        self.analysis_cache = {}
        
    def analyze_code(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze Python code and provide insights
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {"error": f"File {file_path} does not exist"}
            
            if file_path.suffix != '.py':
                return {"error": "File is not a Python file"}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                return {
                    "error": f"Syntax error in file: {e}",
                    "line": e.lineno,
                    "column": e.offset
                }
            
            analysis = {
                "file_path": str(file_path),
                "timestamp": datetime.now().isoformat(),
                "lines_of_code": len(content.splitlines()),
                "functions": [],
                "classes": [],
                "imports": [],
                "variables": [],
                "complexity": 0,
                "issues": []
            }
            
            # Analyze AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node)
                    })
                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                        "docstring": ast.get_docstring(node)
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append({
                            "module": alias.name,
                            "alias": alias.asname,
                            "line": node.lineno
                        })
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        analysis["imports"].append({
                            "module": node.module,
                            "name": alias.name,
                            "alias": alias.asname,
                            "line": node.lineno
                        })
            
            # Calculate complexity (simple metric)
            analysis["complexity"] = len(analysis["functions"]) + len(analysis["classes"]) * 2
            
            # Check for common issues
            self._check_code_issues(content, analysis)
            
            return analysis
            
        except Exception as e:
            return {"error": f"Error analyzing code: {str(e)}"}
    
    def _check_code_issues(self, content: str, analysis: Dict[str, Any]) -> None:
        """Check for common code issues and add to analysis"""
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Check for long lines
            if len(line) > 100:
                analysis["issues"].append({
                    "type": "long_line",
                    "line": i,
                    "message": f"Line {i} is too long ({len(line)} characters)"
                })
            
            # Check for TODO comments
            if "TODO" in line.upper() or "FIXME" in line.upper():
                analysis["issues"].append({
                    "type": "todo",
                    "line": i,
                    "message": f"TODO/FIXME found: {line}"
                })
            
            # Check for unused imports (basic check)
            if line.startswith("import ") or line.startswith("from "):
                if not any(line.split()[1] in content.replace(line, "") for _ in [1]):
                    analysis["issues"].append({
                        "type": "unused_import",
                        "line": i,
                        "message": f"Potentially unused import: {line}"
                    })
    
    def run_code(self, code: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute Python code safely and return results
        
        Args:
            code: Python code to execute
            timeout: Timeout in seconds
            
        Returns:
            Dictionary containing execution results
        """
        try:
            # Create a temporary file
            temp_file = self.workspace_path / "temp_execution.py"
            
            with open(temp_file, 'w') as f:
                f.write(code)
            
            # Execute the code
            result = subprocess.run(
                [sys.executable, str(temp_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.workspace_path
            )
            
            # Clean up
            temp_file.unlink()
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Code execution timed out after {timeout} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing code: {str(e)}"
            }
    
    def suggest_improvements(self, file_path: str) -> List[str]:
        """
        Suggest improvements for Python code
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            List of improvement suggestions
        """
        analysis = self.analyze_code(file_path)
        
        if "error" in analysis:
            return [f"Error analyzing file: {analysis['error']}"]
        
        suggestions = []
        
        # Check for missing docstrings
        for func in analysis["functions"]:
            if not func["docstring"]:
                suggestions.append(f"Function '{func['name']}' at line {func['line']} should have a docstring")
        
        for cls in analysis["classes"]:
            if not cls["docstring"]:
                suggestions.append(f"Class '{cls['name']}' at line {cls['line']} should have a docstring")
        
        # Check for long functions
        for func in analysis["functions"]:
            if func["line"] > 50:  # Simple heuristic
                suggestions.append(f"Function '{func['name']}' might be too long, consider breaking it down")
        
        # Check for high complexity
        if analysis["complexity"] > 20:
            suggestions.append("Code complexity is high, consider refactoring")
        
        # Check for issues
        for issue in analysis["issues"]:
            if issue["type"] == "long_line":
                suggestions.append(f"Line {issue['line']}: {issue['message']}")
            elif issue["type"] == "todo":
                suggestions.append(f"Line {issue['line']}: {issue['message']}")
        
        return suggestions
    
    def format_code(self, code: str) -> str:
        """
        Format Python code using black formatter
        
        Args:
            code: Python code to format
            
        Returns:
            Formatted code
        """
        try:
            # Try to use black if available
            result = subprocess.run(
                [sys.executable, "-m", "black", "--code", code],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                # Fallback to basic formatting
                return self._basic_format(code)
                
        except FileNotFoundError:
            # Black not available, use basic formatting
            return self._basic_format(code)
    
    def _basic_format(self, code: str) -> str:
        """Basic code formatting when black is not available"""
        lines = code.splitlines()
        formatted_lines = []
        
        for line in lines:
            # Basic indentation fix
            stripped = line.strip()
            if stripped:
                formatted_lines.append(stripped)
            else:
                formatted_lines.append("")
        
        return "\n".join(formatted_lines)
    
    def get_workspace_info(self) -> Dict[str, Any]:
        """
        Get information about the current workspace
        
        Returns:
            Dictionary containing workspace information
        """
        info = {
            "workspace_path": str(self.workspace_path),
            "python_files": [],
            "notebook_files": [],
            "data_files": [],
            "total_files": 0
        }
        
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.supported_extensions:
                info["total_files"] += 1
                
                if file_path.suffix == '.py':
                    info["python_files"].append(str(file_path.relative_to(self.workspace_path)))
                elif file_path.suffix == '.ipynb':
                    info["notebook_files"].append(str(file_path.relative_to(self.workspace_path)))
                elif file_path.suffix in {'.csv', '.json', '.txt'}:
                    info["data_files"].append(str(file_path.relative_to(self.workspace_path)))
        
        return info
    
    def help(self) -> str:
        """
        Get help information about the Python Assistant
        
        Returns:
            Help text
        """
        return """
Python Assistant - Available Commands:

1. analyze_code(file_path) - Analyze Python code and provide insights
2. run_code(code) - Execute Python code safely
3. suggest_improvements(file_path) - Get improvement suggestions
4. format_code(code) - Format Python code
5. get_workspace_info() - Get workspace information
6. help() - Show this help message

Features:
- Code analysis and debugging
- Code execution and testing
- Code formatting and improvement suggestions
- Workspace exploration
- Machine learning support (via MLHelper)
- Jupyter notebook support

Example usage:
    assistant = PythonAssistant()
    analysis = assistant.analyze_code("my_script.py")
    suggestions = assistant.suggest_improvements("my_script.py")
        """