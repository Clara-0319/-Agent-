# -*- coding: utf-8 -*-
# 大模型API配置（通义千问）
# 真实生产环境使用

class ModelConfig:
    # 通义千问
    DASHSCOPE_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"  # 你的通义千问API密钥
    DASHSCOPE_MODEL = "qwen-turbo"

    # 请求超时 / 温度设置
    TIMEOUT = 30
    TEMPERATURE = 0.1
    TOP_P = 0.9