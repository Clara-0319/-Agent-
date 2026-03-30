# -*- coding: utf-8 -*-
"""
AI婚恋匹配系统 - 主程序入口
支持三种使用方式：
1. 命令行工具模式
2. API服务接口
3. 直接脚本调用
"""

import sys
import json
import logging
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import MarriageAIAgent
from core.config import ModelConfig, logger


def print_banner():
    """打印项目欢迎信息"""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║    🎯 AI 婚恋匹配智能评价系统                              ║
    ║    Version 1.0.0 · 基于大模型Agent + 规则引擎             ║
    ║    支持通义千问DashScope API实时调用                       ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)


def demo_basic():
    """基础示例：最简单的使用方式"""
    print("\n" + "=" * 70)
    print("📋 示例1：基础婚恋匹配")
    print("=" * 70)
    
    # 初始化智能体
    agent = MarriageAIAgent()
    
    # 用户输入（支持自由文本）
    user_input = """
    男方：28岁，本科学历，身高175cm，北京人，家境中等，性格稳重，从事软件工程师 
    女方：26岁，硕士学历，身高164cm，北京人，家境良好，性格独立，从事医生职业
    """
    
    # 执行完整的匹配流程
    result = agent.match(user_input)
    
    # 显示结果
    if result["success"]:
        print(agent.format_output(result))
        
        # 也可以获取原始JSON数据
        print("\n📊 评分详情（JSON格式）:")
        print(json.dumps(result["score_result"], ensure_ascii=False, indent=2))
    else:
        print(f"❌ 匹配失败: {result['error']}")


def demo_multi_case():
    """多案例对比示例"""
    print("\n" + "=" * 70)
    print("📊 示例2：多案例对比分析")
    print("=" * 70)
    
    agent = MarriageAIAgent()
    
    test_cases = [
        {
            "name": "案例A：天造地设",
            "input": "男30岁本科北京工程师 女28岁本科北京医生"
        },
        {
            "name": "案例B：异地恋爱",
            "input": "男28岁本科北京 女26岁本科上海"
        },
        {
            "name": "案例C：学历差异",
            "input": "男30岁大专 女26岁硕士"
        }
    ]
    
    for case in test_cases:
        print(f"\n🔍 {case['name']}")
        print("-" * 70)
        
        result = agent.match(case["input"])
        
        if result["success"]:
            score = result["score_result"]["total_score"]
            level = result["score_result"]["match_level"]
            print(f"  评分: {score}/100 | 等级: {level}")
            
            # 显示各维度
            for dim, data in result["score_result"]["dimensions"].items():
                print(f"    • {dim}: {data['score']}分")
        else:
            print(f"  ❌ 评估失败: {result['error']}")


def demo_api_format():
    """API返回格式示例（用于前端集成）"""
    print("\n" + "=" * 70)
    print("🔌 示例3：API接口返回格式")
    print("=" * 70)
    
    agent = MarriageAIAgent()
    
    user_input = "男28岁本科北京175cm 女26岁硕士北京164cm"
    result = agent.match(user_input)
    
    # 构建API响应格式
    api_response = {
        "code": 0 if result["success"] else -1,
        "message": "成功" if result["success"] else result.get("error", "未知错误"),
        "data": {
            "extract": result.get("extract_result", {}) if result["success"] else None,
            "score": result.get("score_result", {}) if result["success"] else None,
            "report": result.get("report", "") if result["success"] else None,
            "timestamp": result.get("timestamp"),
            "duration": result.get("duration", 0)
        }
    }
    
    print("\n📤 API返回格式示例:")
    print(json.dumps(api_response, ensure_ascii=False, indent=2))


def demo_debug_mode():
    """调试模式：显示详细日志"""
    print("\n" + "=" * 70)
    print("🔧 示例4：调试模式（启用详细日志）")
    print("=" * 70)
    
    # 设置日志级别为DEBUG
    logging.getLogger().setLevel(logging.DEBUG)
    
    agent = MarriageAIAgent()
    
    user_input = "男25岁大专深圳 女23岁大专深圳"
    print(f"\n📝 用户输入: {user_input}")
    
    result = agent.match(user_input)
    
    if result["success"]:
        print(f"\n✅ 处理耗时: {result.get('duration', 'N/A')}秒")
        print(f"📍 时间戳: {result['timestamp']}")


def validate_config():
    """验证配置是否正确"""
    print("\n" + "=" * 70)
    print("⚙️ 配置验证")
    print("=" * 70)
    
    try:
        ModelConfig.validate()
        print("✅ 配置验证通过！API密钥已设置。")
        print(f"   • 模型: {ModelConfig.DASHSCOPE_MODEL}")
        print(f"   • 温度: {ModelConfig.TEMPERATURE}")
        print(f"   • 超时: {ModelConfig.TIMEOUT}s")
        return True
    except ValueError as e:
        print(f"❌ 配置验证失败: {str(e)}")
        print("\n💡 解决方案:")
        print("   1. 在 .env 文件中设置 DASHSCOPE_API_KEY")
        print("   2. 从阿里云官网获取API密钥: https://dashscope.console.aliyun.com/")
        print("   3. 重新运行程序")
        return False


def interactive_mode():
    """交互模式：持续接收用户输入"""
    print("\n" + "=" * 70)
    print("💬 交互模式 - 输入男女信息进行匹配")
    print("=" * 70)
    print("\n✏️ 输入格式示例:")
    print("   男28岁本科北京175 女26岁硕士北京164")
    print("\n输入 'exit' 退出，'example' 查看示例")
    
    agent = MarriageAIAgent()
    
    while True:
        try:
            user_input = input("\n👤 请输入男女信息: ").strip()
            
            if user_input.lower() == "exit":
                print("👋 再见!")
                break
            
            if user_input.lower() == "example":
                print("\n📌 示例：")
                print("  • 男28岁本科北京身高175 女26岁硕士北京身高164")
                print("  • 男30岁大专深圳 女28岁大专深圳")
                print("  • 男32岁硕士北京工程师 女29岁本科上海老师")
                continue
            
            if not user_input:
                print("⚠️ 输入不能为空")
                continue
            
            # 开始匹配
            print("\n🔄 处理中...")
            result = agent.match(user_input)
            
            if result["success"]:
                print(agent.format_output(result))
            else:
                print(f"❌ 错误: {result['error']}")
        
        except KeyboardInterrupt:
            print("\n\n👋 程序中断，再见!")
            break
        except Exception as e:
            print(f"❌ 发生异常: {str(e)}")


def main():
    """主程序入口"""
    print_banner()
    
    # 验证配置
    if not validate_config():
        print("\n⚠️ 警告：由于API密钥未配置，规则引擎仍可正常工作，但无法调用大模型进行深度分析。")
    
    # 选择运行模式
    print("\n" + "=" * 70)
    print("选择运行模式:")
    print("=" * 70)
    print("1️⃣  基础示例 (demo_basic)")
    print("2️⃣  多案例对比 (demo_multi_case)")
    print("3️⃣  API格式 (demo_api_format)")
    print("4️⃣  调试模式 (demo_debug_mode)")
    print("5️⃣  交互模式 (interactive_mode) - 推荐!")
    print("0️⃣  运行所有示例 (run_all)")
    
    choice = input("\n请选择 (0-5): ").strip()
    
    if choice == "1":
        demo_basic()
    elif choice == "2":
        demo_multi_case()
    elif choice == "3":
        demo_api_format()
    elif choice == "4":
        demo_debug_mode()
    elif choice == "5":
        interactive_mode()
    elif choice == "0":
        demo_basic()
        demo_multi_case()
        demo_api_format()
        demo_debug_mode()
    else:
        print("❌ 无效选择，默认运行交互模式...")
        interactive_mode()
    
    print("\n" + "=" * 70)
    print("✅ 程序执行完成")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()