"""
Python Assistant - A comprehensive Python development and analysis tool
"""

__version__ = "1.0.0"
__author__ = "Python Assistant"

from .assistant import PythonAssistant
from .code_analyzer import CodeAnalyzer
from .ml_helper import MLHelper
from .cli import main

__all__ = ["PythonAssistant", "CodeAnalyzer", "MLHelper", "main"]