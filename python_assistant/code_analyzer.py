"""
Advanced code analysis and debugging capabilities for Python Assistant
"""

import ast
import re
import sys
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import json
import subprocess

class CodeAnalyzer:
    """
    Advanced code analysis and debugging tools
    """
    
    def __init__(self):
        self.analysis_patterns = {
            'performance': [
                r'for\s+\w+\s+in\s+range\(len\([^)]+\)\)',  # Avoid range(len())
                r'\.append\([^)]*\)\s*$',  # List append in loops
                r'\+=\s*\[[^\]]+\]',  # List concatenation
            ],
            'security': [
                r'eval\s*\(',  # eval() usage
                r'exec\s*\(',  # exec() usage
                r'__import__\s*\(',  # __import__ usage
                r'input\s*\(',  # input() usage
            ],
            'style': [
                r'print\s*\([^)]*\)',  # print statements
                r'==\s+None',  # == None instead of is None
                r'!=\s+None',  # != None instead of is not None
            ]
        }
    
    def deep_analysis(self, file_path: str) -> Dict[str, Any]:
        """
        Perform deep analysis of Python code
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Comprehensive analysis results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis = {
                "file_path": file_path,
                "basic_metrics": self._get_basic_metrics(content),
                "complexity_analysis": self._analyze_complexity(content),
                "pattern_analysis": self._analyze_patterns(content),
                "dependency_analysis": self._analyze_dependencies(content),
                "performance_issues": self._find_performance_issues(content),
                "security_issues": self._find_security_issues(content),
                "style_issues": self._find_style_issues(content),
                "suggestions": []
            }
            
            # Generate suggestions based on analysis
            analysis["suggestions"] = self._generate_suggestions(analysis)
            
            return analysis
            
        except Exception as e:
            return {"error": f"Error in deep analysis: {str(e)}"}
    
    def _get_basic_metrics(self, content: str) -> Dict[str, Any]:
        """Calculate basic code metrics"""
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "total_lines": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "blank_lines": len(lines) - len(non_empty_lines),
            "characters": len(content),
            "average_line_length": sum(len(line) for line in lines) / len(lines) if lines else 0
        }
    
    def _analyze_complexity(self, content: str) -> Dict[str, Any]:
        """Analyze code complexity"""
        try:
            tree = ast.parse(content)
            
            complexity_metrics = {
                "cyclomatic_complexity": 0,
                "function_count": 0,
                "class_count": 0,
                "nested_depth": 0,
                "max_nested_depth": 0
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity_metrics["function_count"] += 1
                    complexity_metrics["cyclomatic_complexity"] += 1
                    
                    # Count decision points
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                            complexity_metrics["cyclomatic_complexity"] += 1
                
                elif isinstance(node, ast.ClassDef):
                    complexity_metrics["class_count"] += 1
                
                # Calculate nesting depth
                if hasattr(node, 'lineno'):
                    depth = self._calculate_nesting_depth(node, tree)
                    complexity_metrics["max_nested_depth"] = max(complexity_metrics["max_nested_depth"], depth)
            
            return complexity_metrics
            
        except SyntaxError:
            return {"error": "Syntax error in code"}
    
    def _calculate_nesting_depth(self, node: ast.AST, tree: ast.AST) -> int:
        """Calculate nesting depth of a node"""
        depth = 0
        for parent in ast.walk(tree):
            if hasattr(parent, 'body') and node in parent.body:
                depth += 1
        return depth
    
    def _analyze_patterns(self, content: str) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze code patterns"""
        patterns = {
            "performance": [],
            "security": [],
            "style": []
        }
        
        lines = content.splitlines()
        
        for category, pattern_list in self.analysis_patterns.items():
            for pattern in pattern_list:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line):
                        patterns[category].append({
                            "line": i,
                            "content": line.strip(),
                            "pattern": pattern,
                            "suggestion": self._get_pattern_suggestion(category, pattern)
                        })
        
        return patterns
    
    def _get_pattern_suggestion(self, category: str, pattern: str) -> str:
        """Get suggestion for a specific pattern"""
        suggestions = {
            "performance": {
                r'for\s+\w+\s+in\s+range\(len\([^)]+\)\)': "Use enumerate() instead of range(len())",
                r'\.append\([^)]*\)\s*$': "Consider using list comprehension for better performance",
                r'\+=\s*\[[^\]]+\]': "Use extend() instead of += for list concatenation"
            },
            "security": {
                r'eval\s*\(': "Avoid using eval() - it's a security risk",
                r'exec\s*\(': "Avoid using exec() - it's a security risk",
                r'__import__\s*\(': "Use importlib instead of __import__",
                r'input\s*\(': "Be careful with input() - validate user input"
            },
            "style": {
                r'print\s*\([^)]*\)': "Consider using logging instead of print for production code",
                r'==\s+None': "Use 'is None' instead of '== None'",
                r'!=\s+None': "Use 'is not None' instead of '!= None'"
            }
        }
        
        return suggestions.get(category, {}).get(pattern, "Consider reviewing this code")
    
    def _analyze_dependencies(self, content: str) -> Dict[str, Any]:
        """Analyze code dependencies"""
        try:
            tree = ast.parse(content)
            imports = []
            local_imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            "module": alias.name,
                            "alias": alias.asname,
                            "line": node.lineno,
                            "type": "import"
                        })
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if node.module:
                            imports.append({
                                "module": node.module,
                                "name": alias.name,
                                "alias": alias.asname,
                                "line": node.lineno,
                                "type": "from_import"
                            })
                        else:
                            local_imports.append({
                                "name": alias.name,
                                "alias": alias.asname,
                                "line": node.lineno,
                                "type": "relative_import"
                            })
            
            return {
                "imports": imports,
                "local_imports": local_imports,
                "total_imports": len(imports) + len(local_imports)
            }
            
        except SyntaxError:
            return {"error": "Syntax error in code"}
    
    def _find_performance_issues(self, content: str) -> List[Dict[str, Any]]:
        """Find potential performance issues"""
        issues = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            # Check for inefficient patterns
            if re.search(r'for\s+\w+\s+in\s+range\(len\([^)]+\)\)', line):
                issues.append({
                    "line": i,
                    "type": "performance",
                    "issue": "Using range(len()) instead of enumerate()",
                    "suggestion": "Use enumerate() for better readability and performance"
                })
            
            if re.search(r'\+=\s*\[[^\]]+\]', line):
                issues.append({
                    "line": i,
                    "type": "performance",
                    "issue": "List concatenation with +=",
                    "suggestion": "Use extend() method for better performance"
                })
        
        return issues
    
    def _find_security_issues(self, content: str) -> List[Dict[str, Any]]:
        """Find potential security issues"""
        issues = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            if re.search(r'eval\s*\(', line):
                issues.append({
                    "line": i,
                    "type": "security",
                    "issue": "Use of eval() function",
                    "suggestion": "Avoid eval() - it's a security risk. Use safer alternatives."
                })
            
            if re.search(r'exec\s*\(', line):
                issues.append({
                    "line": i,
                    "type": "security",
                    "issue": "Use of exec() function",
                    "suggestion": "Avoid exec() - it's a security risk. Use safer alternatives."
                })
        
        return issues
    
    def _find_style_issues(self, content: str) -> List[Dict[str, Any]]:
        """Find style issues"""
        issues = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            if re.search(r'==\s+None', line):
                issues.append({
                    "line": i,
                    "type": "style",
                    "issue": "Using == None instead of is None",
                    "suggestion": "Use 'is None' for identity comparison"
                })
            
            if re.search(r'!=\s+None', line):
                issues.append({
                    "line": i,
                    "type": "style",
                    "issue": "Using != None instead of is not None",
                    "suggestion": "Use 'is not None' for identity comparison"
                })
        
        return issues
    
    def _generate_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions based on analysis"""
        suggestions = []
        
        # Complexity suggestions
        if analysis["complexity_analysis"].get("cyclomatic_complexity", 0) > 10:
            suggestions.append("High cyclomatic complexity detected. Consider refactoring complex functions.")
        
        if analysis["complexity_analysis"].get("max_nested_depth", 0) > 4:
            suggestions.append("High nesting depth detected. Consider reducing nesting levels.")
        
        # Performance suggestions
        if analysis["performance_issues"]:
            suggestions.append(f"Found {len(analysis['performance_issues'])} potential performance issues.")
        
        # Security suggestions
        if analysis["security_issues"]:
            suggestions.append(f"Found {len(analysis['security_issues'])} potential security issues.")
        
        # Style suggestions
        if analysis["style_issues"]:
            suggestions.append(f"Found {len(analysis['style_issues'])} style issues.")
        
        return suggestions
    
    def check_imports(self, file_path: str) -> Dict[str, Any]:
        """
        Check if all imports in a file are available
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Import availability check results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            imports = []
            unavailable_imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        try:
                            importlib.import_module(alias.name)
                            imports.append({
                                "module": alias.name,
                                "status": "available",
                                "line": node.lineno
                            })
                        except ImportError:
                            unavailable_imports.append({
                                "module": alias.name,
                                "status": "unavailable",
                                "line": node.lineno
                            })
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        try:
                            module = importlib.import_module(node.module)
                            for alias in node.names:
                                if hasattr(module, alias.name):
                                    imports.append({
                                        "module": f"{node.module}.{alias.name}",
                                        "status": "available",
                                        "line": node.lineno
                                    })
                                else:
                                    unavailable_imports.append({
                                        "module": f"{node.module}.{alias.name}",
                                        "status": "unavailable",
                                        "line": node.lineno
                                    })
                        except ImportError:
                            for alias in node.names:
                                unavailable_imports.append({
                                    "module": f"{node.module}.{alias.name}",
                                    "status": "unavailable",
                                    "line": node.lineno
                                })
            
            return {
                "available_imports": imports,
                "unavailable_imports": unavailable_imports,
                "total_imports": len(imports) + len(unavailable_imports),
                "success_rate": len(imports) / (len(imports) + len(unavailable_imports)) if (len(imports) + len(unavailable_imports)) > 0 else 1.0
            }
            
        except Exception as e:
            return {"error": f"Error checking imports: {str(e)}"}