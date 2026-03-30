# -*- coding: utf-8 -*-
"""
大模型LLM客户端（通义千问DashScope API）
封装API调用、错误处理、日志记录
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from core.config import ModelConfig

# 配置日志
logger = logging.getLogger(__name__)


class LLMClient:
    """通义千问大模型API客户端"""
    
    def __init__(self):
        """初始化客户端"""
        ModelConfig.setup_logging()
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.model = os.getenv("DASHSCOPE_MODEL", "qwen-turbo")
        self.timeout = ModelConfig.TIMEOUT
        self.temperature = ModelConfig.TEMPERATURE
        self.top_p = ModelConfig.TOP_P
        
        # 验证API密钥
        if not self.api_key or self.api_key.startswith("sk-x"):
            logger.warning("⚠️ API密钥未配置或为默认值，部分调用可能失败")

    def chat(self, system_prompt: str, user_input: str) -> str:
        """
        调用通义千问进行对话
        
        Args:
            system_prompt: 系统提示词（定义AI角色与任务）
            user_input: 用户输入内容
            
        Returns:
            模型输出的文本内容
        """
        logger.info(f"🤖 调用模型: {self.model}")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "input": {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            },
            "parameters": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "result_format": "message"
            }
        }
        
        try:
            logger.debug(f"📤 发送请求到: {self.url}")
            resp = requests.post(
                self.url, 
                json=payload, 
                headers=headers,
                timeout=self.timeout
            )
            
            # 检查HTTP状态码
            if resp.status_code != 200:
                logger.error(f"❌ HTTP错误 {resp.status_code}: {resp.text}")
                return f"大模型API调用失败: HTTP {resp.status_code}"
            
            # 解析响应
            result = resp.json()
            
            # 检查API返回结果
            if result.get("status_code") != 200:
                error_msg = result.get("message", "未知错误")
                logger.error(f"❌ API返回错误: {error_msg}")
                return f"大模型调用异常: {error_msg}"
            
            # 提取回复内容
            content = result.get("output", {}).get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not content:
                logger.error("❌ 模型返回为空")
                return "模型返回内容为空"
            
            logger.info("✅ 模型调用成功")
            return content
            
        except requests.exceptions.Timeout:
            error_msg = f"请求超时(>{self.timeout}s)"
            logger.error(f"❌ {error_msg}")
            return f"大模型调用失败: {error_msg}"
            
        except requests.exceptions.ConnectionError as e:
            error_msg = "网络连接错误，检查网络或API地址"
            logger.error(f"❌ {error_msg}: {str(e)}")
            return f"大模型调用失败: {error_msg}"
            
        except json.JSONDecodeError:
            error_msg = "API返回非JSON格式"
            logger.error(f"❌ {error_msg}")
            return f"大模型调用失败: {error_msg}"
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ 未知错误: {error_msg}")
            return f"大模型调用失败: {error_msg}"

    def chat_json(self, system_prompt: str, user_input: str) -> Dict[str, Any]:
        """
        调用大模型并期望JSON格式返回
        
        Args:
            system_prompt: 系统提示词
            user_input: 用户输入
            
        Returns:
            解析后的JSON字典，解析失败返回空字典
        """
        response = self.chat(system_prompt, user_input)
        
        # 检查是否为错误信息
        if response.startswith("大模型"):
            logger.error(f"模型调用出错: {response}")
            return {}
        
        try:
            # 尝试直接解析
            return json.loads(response)
        except json.JSONDecodeError:
            # 尝试提取JSON部分
            logger.warning("⚠️ 尝试从响应中提取JSON...")
            try:
                # 查找首个 { 和最后一个 }
                start_idx = response.find("{")
                end_idx = response.rfind("}")
                if start_idx != -1 and end_idx != -1:
                    json_str = response[start_idx:end_idx+1]
                    return json.loads(json_str)
            except:
                pass
            
            logger.error(f"❌ 无法解析JSON: {response[:100]}...")
            return {}


# 便捷函数
def get_llm_client() -> LLMClient:
    """获取LLM客户端单例"""
    return LLMClient()