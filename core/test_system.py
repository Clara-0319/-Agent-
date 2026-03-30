# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证系统各组件是否正常
不需要API密钥即可运行（将使用规则引擎）
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import ModelConfig, logger
from core.rules import MarriageRuleEngine
from core.llm_client import LLMClient
from core.agent import MarriageAIAgent


def test_config():
    """测试配置加载"""
    print("✓ 测试1：配置加载")
    print(f"  • 模型: {ModelConfig.DASHSCOPE_MODEL}")
    print(f"  • 温度: {ModelConfig.TEMPERATURE}")
    print(f"  • 日志级别: {ModelConfig.LOG_LEVEL}")
    print("  ✅ 配置加载成功\n")


def test_rules_engine():
    """测试规则引擎"""
    print("✓ 测试2：规则引擎")
    
    rules = MarriageRuleEngine()
    
    # 测试案例
    male = {
        "age": 28,
        "education": "本科",
        "city": "北京",
        "family_background": "中等",
        "character": "稳重",
        "career": "工程师"
    }
    
    female = {
        "age": 26,
        "education": "硕士",
        "city": "北京",
        "family_background": "富裕",
        "character": "独立",
        "career": "医生"
    }
    
    result = rules.calculate_total(male, female)
    
    print(f"  • 综合评分: {result['total_score']}/100")
    print(f"  • 匹配等级: {result['match_level']}")
    print("  ✅ 规则引擎测试成功\n")
    
    return result


def test_llm_client():
    """测试LLM客户端初始化"""
    print("✓ 测试3：LLM客户端")
    
    try:
        client = LLMClient()
        print(f"  • API地址: {client.url}")
        print(f"  • 模型: {client.model}")
        print("  ✅ LLM客户端初始化成功\n")
        return True
    except Exception as e:
        print(f"  ❌ 错误: {str(e)}\n")
        return False


def test_agent_extract():
    """测试智能体的信息提取"""
    print("✓ 测试4：信息提取（规则引擎模式）")
    
    agent = MarriageAIAgent()
    
    # 简单的测试输入
    test_input = "男28岁本科北京 女26岁硕士深圳"
    
    result = agent.extract_info(test_input)
    
    print(f"  • 提取成功: {result['success']}")
    if not result['success']:
        print(f"  • 错误: {result.get('error', 'N/A')}")
    else:
        print(f"  • 男方: {result.get('male', {})}")
        print(f"  • 女方: {result.get('female', {})}")
    print("  ✅ 信息提取测试完成\n")


def test_full_workflow():
    """测试完整工作流"""
    print("✓ 测试5：完整匹配工作流")
    
    agent = MarriageAIAgent()
    
    test_input = """
    男方：28岁，本科学历，北京人
    女方：26岁，硕士学历，北京人
    """
    
    result = agent.match(test_input)
    
    print(f"  • 成功: {result['success']}")
    if result['success']:
        print(f"  • 提取成功: {result['extract_result']['success']}")
        print(f"  • 评分: {result['score_result']['total_score']}/100")
        print(f"  • 耗时: {result.get('duration', 'N/A')}s")
    else:
        print(f"  • 错误: {result.get('error', 'N/A')}")
    
    print("  ✅ 完整工作流测试完成\n")


def main():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("🧪 AI婚恋匹配系统 - 快速测试")
    print("=" * 70 + "\n")
    
    try:
        test_config()
        test_rules_engine()
        test_llm_client()
        test_agent_extract()
        test_full_workflow()
        
        print("=" * 70)
        print("✅ 所有测试完成！系统可以正常运行")
        print("=" * 70)
        print("\n💡 下一步:")
        print("   1. 在 .env 文件中配置 DASHSCOPE_API_KEY")
        print("   2. 运行: python main.py")
        print("   3. 选择模式5（交互模式）开始使用")
        print()
    
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
