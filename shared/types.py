from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class UserLoadResult:
    status: str  # "FOUND" or "NOT_FOUND"
    history: str = ""

@dataclass
class ContextLoadResult:
    status: str  # "FOUND" or "NOT_FOUND"
    context: str = ""

@dataclass
class ChatEntry:
    question: str
    answer: str
    timestamp: str = ""