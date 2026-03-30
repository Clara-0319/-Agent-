# -*- coding: utf-8 -*-
"""
大模型API配置管理（通义千问）
支持生产环境与测试环境配置切换
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# 加载.env文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class ModelConfig:
    """大模型与系统全局配置"""
    
    # =============== 通义千问配置 ===============
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "sk-default-key")
    DASHSCOPE_MODEL = os.getenv("DASHSCOPE_MODEL", "qwen-turbo")
    
    # =============== 请求参数 ===============
    TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
    TOP_P = float(os.getenv("TOP_P", "0.9"))
    
    # =============== 日志配置 ===============
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # =============== 启用功能开关 ===============
    ENABLE_FALLBACK = os.getenv("ENABLE_FALLBACK", "true").lower() == "true"  # 模型调用失败是否使用备用方案
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"  # 是否启用缓存
    
    @classmethod
    def setup_logging(cls):
        """配置日志"""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format=cls.LOG_FORMAT
        )
        return logging.getLogger(__name__)
    
    @classmethod
    def validate(cls):
        """验证关键配置"""
        if not cls.DASHSCOPE_API_KEY or cls.DASHSCOPE_API_KEY.startswith("sk-default"):
            raise ValueError("❌ DASHSCOPE_API_KEY 未配置，请在 .env 文件中设置")
        return True


# 全局日志对象
logger = ModelConfig.setup_logging()