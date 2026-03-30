# -*- coding: utf-8 -*-
"""
AI婚恋匹配系统 - Core模块
包含：配置、大模型API、规则引擎、提示词、AI智能体
"""

from core.config import ModelConfig, logger
from core.llm_client import LLMClient, get_llm_client
from core.rules import MarriageRuleEngine
from core.agent import MarriageAIAgent

__all__ = [
    "ModelConfig",
    "logger",
    "LLMClient",
    "get_llm_client",
    "MarriageRuleEngine",
    "MarriageAIAgent",
]

__version__ = "1.0.0"
