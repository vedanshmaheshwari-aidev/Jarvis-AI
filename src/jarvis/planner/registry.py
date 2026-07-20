"""
registry.py
===========

Central Agent Registry for Jarvis AI OS.

Every Agent registers itself here.

The Planner NEVER hardcodes agents.
It simply reads this registry.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet


# ==========================================================
# Agent Rule
# ==========================================================

@dataclass(frozen=True)
class AgentRule:
    """
    Configuration for a registered Agent.
    """

    # ------------------------------------------------------
    # Basic Information
    # ------------------------------------------------------

    name: str
    description: str

    # ------------------------------------------------------
    # Intent Detection
    # ------------------------------------------------------

    keyword_weights: Dict[str, int]

    # ------------------------------------------------------
    # Agent Skills
    # ------------------------------------------------------

    capabilities: FrozenSet[str]

    # What actions this Agent can perform
    supported_actions: FrozenSet[str] = frozenset()

    # ------------------------------------------------------
    # Scheduling
    # ------------------------------------------------------

    priority: int = 1
    requires_llm: bool = False
    enabled: bool = True
    max_tasks: int = 3

    # ------------------------------------------------------
    # Runtime (Future)
    # ------------------------------------------------------

    # Actual Agent instance
    # Example:
    # ChatAgent()
    # DataAgent()
    handler: Any | None = None

    # ------------------------------------------------------
    # Versioning
    # ------------------------------------------------------

    version: str = "1.0"

    # ------------------------------------------------------
    # Agent Dependencies
    # ------------------------------------------------------

    dependencies: FrozenSet[str] = frozenset()

    # ------------------------------------------------------
    # Future Expansion
    # ------------------------------------------------------

    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Agent Names
# ==========================================================

CHAT = "chat"
DATA = "data"
PRESENTATION = "presentation"
DEVELOPER = "developer"
SYSTEM = "system"


# ==========================================================
# Chat Agent
# ==========================================================

CHAT_AGENT = AgentRule(
    name=CHAT,
    description="General conversation and question answering.",

    keyword_weights={},

    capabilities=frozenset({
        "conversation",
        "question_answering",
        "summarization",
        "translation",
        "explanation",
    }),

    supported_actions=frozenset({
        "chat",
        "answer",
        "explain",
        "summarize",
        "translate",
    }),

    priority=1,
    requires_llm=True,
    max_tasks=10,
)


# ==========================================================
# Data Agent
# ==========================================================

DATA_AGENT = AgentRule(
    name=DATA,
    description="Professional Data Analyst.",

    keyword_weights={
        "csv": 12,
        "excel": 12,
        "spreadsheet": 10,
        "sql": 12,
        "database": 10,
        "data": 8,
        "dataset": 8,
        "analytics": 8,
        "analysis": 8,
        "statistics": 8,
        "pandas": 10,
        "numpy": 10,
        "clean": 7,
        "cleaning": 7,
        "transform": 7,
        "merge": 6,
        "filter": 5,
        "sort": 5,
        "groupby": 6,
        "report": 4,
    },

    capabilities=frozenset({
        "clean_csv",
        "clean_excel",
        "analyze_data",
        "generate_sql",
        "execute_sql",
        "statistics",
        "feature_engineering",
        "data_validation",
    }),

    supported_actions=frozenset({
        "clean",
        "analyze",
        "visualize",
        "dashboard",
        "query",
        "report",
    }),

    priority=5,
    requires_llm=False,
    max_tasks=5,
)


# ==========================================================
# Presentation Agent
# ==========================================================

PRESENTATION_AGENT = AgentRule(
    name=PRESENTATION,
    description="Dashboards, charts and storytelling.",

    keyword_weights={
        "dashboard": 12,
        "power bi": 15,
        "powerbi": 15,
        "tableau": 15,
        "chart": 8,
        "graph": 8,
        "plot": 8,
        "visualization": 10,
        "visualisation": 10,
        "story": 7,
        "storytelling": 10,
        "presentation": 8,
        "insights": 7,
        "kpi": 8,
        "design": 5,
        "ui": 4,
        "ux": 4,
    },

    capabilities=frozenset({
        "powerbi_dashboard",
        "tableau_dashboard",
        "excel_dashboard",
        "html_dashboard",
        "charts",
        "storytelling",
        "executive_summary",
        "presentation",
    }),

    supported_actions=frozenset({
        "dashboard",
        "visualize",
        "design",
        "present",
    }),

    priority=4,
    requires_llm=True,
    max_tasks=3,

    dependencies=frozenset({
        DATA,
    }),
)


# ==========================================================
# Developer Agent
# ==========================================================

DEVELOPER_AGENT = AgentRule(
    name=DEVELOPER,
    description="Software Development Specialist.",

    keyword_weights={
        "python": 12,
        "java": 12,
        "javascript": 12,
        "typescript": 12,
        "html": 10,
        "css": 10,
        "react": 10,
        "node": 10,
        "api": 10,
        "docker": 10,
        "git": 10,
        "github": 10,
        "json": 6,
        "yaml": 6,
        "xml": 6,
        "code": 8,
        "coding": 8,
        "programming": 10,
        "debug": 12,
        "bug": 10,
        "function": 5,
        "class": 5,
        "algorithm": 8,
        "vscode": 5,
    },

    capabilities=frozenset({
        "generate_code",
        "review_code",
        "debug_code",
        "refactor",
        "api_design",
        "web_development",
        "database_design",
    }),

    supported_actions=frozenset({
        "generate",
        "debug",
        "review",
        "refactor",
        "build",
    }),

    priority=4,
    requires_llm=True,
    max_tasks=4,
)


# ==========================================================
# System Agent
# ==========================================================

SYSTEM_AGENT = AgentRule(
    name=SYSTEM,
    description="Windows Automation Specialist.",

    keyword_weights={
        "open": 8,
        "close": 8,
        "launch": 8,
        "install": 10,
        "uninstall": 10,
        "download": 8,
        "upload": 8,
        "shutdown": 12,
        "restart": 12,
        "sleep": 8,
        "copy": 6,
        "move": 6,
        "rename": 6,
        "delete": 8,
        "folder": 8,
        "file": 8,
        "clipboard": 6,
        "wifi": 8,
        "network": 8,
        "bluetooth": 8,
        "windows": 8,
        "brightness": 6,
        "volume": 6,
        "task manager": 10,
        "process": 8,
        "service": 8,
    },

    capabilities=frozenset({
        "launch_app",
        "manage_files",
        "manage_processes",
        "windows_settings",
        "clipboard",
        "screenshots",
        "downloads",
    }),

    supported_actions=frozenset({
        "open",
        "close",
        "install",
        "delete",
        "rename",
        "move",
    }),

    priority=3,
    requires_llm=False,
    max_tasks=5,
)


# ==========================================================
# Registry
# ==========================================================

REGISTERED_AGENTS = (
    DATA_AGENT,
    PRESENTATION_AGENT,
    DEVELOPER_AGENT,
    SYSTEM_AGENT,
)

DEFAULT_AGENT = CHAT_AGENT