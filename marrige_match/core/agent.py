# -*- coding: utf-8 -*-
# 婚恋匹配AI智能体（完整版）
# 功能：多模态信息抽取 + 规则引擎打分 + 大模型评价生成
# 支持：通义千问
# 工程化结构，可直接上线

import json
import requests
from core.config import ModelConfig
from core.prompt import EXTRACT_PROMPT, MATCHING_PROMPT
from core.rules import MarriageRuleEngine

class MarriageAIAgent:
    def __init__(self, model="qwen"):
        self.model = model
        self.rules = MarriageRuleEngine()
        self.config = ModelConfig()

    # --------------------------
    # 真实大模型调用（通义千问）
    # --------------------------
    def call_qwen(self, prompt, user_input):
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.config.DASHSCOPE_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.DASHSCOPE_MODEL,
            "input": {"messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]},
            "parameters": {
                "temperature": self.config.TEMPERATURE,
                "top_p": self.config.TOP_P,
                "result_format": "message"
            }
        }
        try:
            resp = requests.post(url, json=data, timeout=self.config.TIMEOUT)
            return resp.json()["output"]["choices"][0]["message"]["content"]
        except Exception as e:
            return f"模型调用异常：{str(e)}"

    # --------------------------
    # 信息抽取（真实大模型）
    # --------------------------
    def extract_info(self, user_input):
        response = self.call_qwen(EXTRACT_PROMPT, user_input)
        try:
            return json.loads(response)
        except:
            return {"male": {}, "female": {}}

    # --------------------------
    # 规则引擎匹配打分
    # --------------------------
    def evaluate(self, male, female):
        return self.rules.calculate_total(male, female)

    # --------------------------
    # 生成最终婚恋报告
    # --------------------------
    def generate_report(self, male, female, score_result):
        user_content = f"男方：{male}\n女方：{female}\n评分：{score_result}"
        report = self.call_qwen(MATCHING_PROMPT, user_content)
        return report

# --------------------------
# 测试（可直接运行）
# --------------------------
if __name__ == "__main__":
    agent = MarriageAIAgent(model="qwen")
    test_male = {"age": 28, "education": "本科", "city": "北京"}
    test_female = {"age": 26, "education": "硕士", "city": "北京"}
    result = agent.evaluate(test_male, test_female)
    print(json.dumps(result, ensure_ascii=False, indent=2))