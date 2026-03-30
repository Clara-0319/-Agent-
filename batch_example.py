# -*- coding: utf-8 -*-
"""
批量匹配示例
展示如何批量处理多个婚恋匹配案例
"""

import sys
import json
from pathlib import Path
from tabulate import tabulate

sys.path.insert(0, str(Path(__file__).parent))

from core.agent import MarriageAIAgent
from core.config import logger


def batch_match_example():
    """批量匹配示例"""
    
    print("\n" + "=" * 80)
    print("📊 AI婚恋匹配系统 - 批量匹配分析")
    print("=" * 80 + "\n")
    
    # 初始化智能体
    agent = MarriageAIAgent()
    
    # 定义多个测试案例
    test_cases = [
        {
            "name": "案例1：郎才女貌",
            "input": "男28岁本科北京身高175cm工程师 女26岁硕士北京身高164cm医生"
        },
        {
            "name": "案例2：异地恋爱",
            "input": "男30岁本科北京 女28岁本科上海"
        },
        {
            "name": "案例3：学历差异",
            "input": "男32岁大专深圳 女28岁硕士深圳"
        },
        {
            "name": "案例4：年龄差异",
            "input": "男35岁硕士北京 女26岁本科北京"
        },
        {
            "name": "案例5：经济差异",
            "input": "男28岁本科北京中等家境 女26岁硕士北京富裕家境"
        }
    ]
    
    # 存储结果
    results = []
    
    # 逐个处理案例
    for case in test_cases:
        print(f"🔄 处理: {case['name']}")
        
        result = agent.match(case["input"])
        
        if result["success"]:
            score_result = result["score_result"]
            results.append({
                "案例": case["name"],
                "总分": score_result["total_score"],
                "等级": score_result["match_level"],
                "年龄": score_result["dimensions"]["age"]["score"],
                "学历": score_result["dimensions"]["education"]["score"],
                "城市": score_result["dimensions"]["city"]["score"],
                "经济": score_result["dimensions"]["economic"]["score"],
                "性格": score_result["dimensions"]["character"]["score"],
                "状态": "✅"
            })
            print(f"   ✅ 完成 - 评分: {score_result['total_score']}/100\n")
        else:
            print(f"   ❌ 失败 - {result.get('error')}\n")
    
    # 显示汇总表格
    print("\n" + "=" * 80)
    print("📋 匹配结果汇总")
    print("=" * 80 + "\n")
    
    if results:
        print(tabulate(results, headers="keys", tablefmt="grid"))
    else:
        print("❌ 无成功的匹配结果")
    
    # 统计分析
    if results:
        print("\n" + "=" * 80)
        print("📈 统计分析")
        print("=" * 80 + "\n")
        
        total_scores = [r["总分"] for r in results]
        avg_score = sum(total_scores) / len(total_scores)
        max_score = max(total_scores)
        min_score = min(total_scores)
        
        print(f"总案例数: {len(results)}")
        print(f"平均评分: {avg_score:.1f}/100")
        print(f"最高评分: {max_score}/100 ({results[total_scores.index(max_score)]['案例']})")
        print(f"最低评分: {min_score}/100 ({results[total_scores.index(min_score)]['案例']})")
        
        # 等级分布
        levels = {}
        for r in results:
            level = r["等级"]
            levels[level] = levels.get(level, 0) + 1
        
        print(f"\n等级分布:")
        for level, count in sorted(levels.items()):
            print(f"  • {level}: {count}个")
    
    print("\n" + "=" * 80)
    print("✅ 批量分析完成")
    print("=" * 80 + "\n")
    
    # 导出结果（可选）
    return results


def export_to_csv(results, filename="match_results.csv"):
    """导出结果到CSV"""
    import csv
    
    if not results:
        print("❌ 无数据可导出")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        print(f"✅ 已导出到: {filename}")
    except Exception as e:
        print(f"❌ 导出失败: {str(e)}")


def export_to_json(results, filename="match_results.json"):
    """导出结果到JSON"""
    
    if not results:
        print("❌ 无数据可导出")
        return
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已导出到: {filename}")
    except Exception as e:
        print(f"❌ 导出失败: {str(e)}")


def custom_batch_match():
    """自定义批量匹配（用户输入）"""
    
    print("\n" + "=" * 80)
    print("🔧 自定义批量匹配")
    print("=" * 80)
    print("\n💡 输入格式: 男XX岁XX学历XX城市 女XX岁XX学历XX城市")
    print("输入 'done' 完成添加，'cancel' 取消\n")
    
    agent = MarriageAIAgent()
    cases = []
    
    while True:
        try:
            case = input("➕ 输入案例 (或命令): ").strip()
            
            if case.lower() == "done":
                break
            elif case.lower() == "cancel":
                return
            elif case:
                cases.append({"name": f"自定义案例{len(cases)+1}", "input": case})
                print(f"✅ 已添加（共{len(cases)}个）\n")
        
        except KeyboardInterrupt:
            print("\n❌ 已取消")
            return
    
    if cases:
        results = []
        for case in cases:
            result = agent.match(case["input"])
            if result["success"]:
                results.append({
                    "输入": case["input"],
                    "评分": result["score_result"]["total_score"],
                    "等级": result["score_result"]["match_level"]
                })
        
        if results:
            print("\n" + "=" * 80)
            print("📊 结果")
            print("=" * 80 + "\n")
            print(tabulate(results, headers="keys", tablefmt="grid"))


def main():
    """主程序"""
    
    print("\n" + "=" * 80)
    print("🎯 AI婚恋匹配系统 - 批量处理工具")
    print("=" * 80)
    print("\n选择模式:")
    print("1️⃣  运行预设的5个测试案例")
    print("2️⃣  自定义批量匹配")
    print("0️⃣  退出")
    
    choice = input("\n请选择 (0-2): ").strip()
    
    if choice == "1":
        results = batch_match_example()
        
        # 提示导出选项
        export_choice = input("\n是否导出结果? (csv/json/no): ").strip().lower()
        if export_choice == "csv":
            export_to_csv(results)
        elif export_choice == "json":
            export_to_json(results)
    
    elif choice == "2":
        custom_batch_match()
    
    print("\n✅ 谢谢使用！")


if __name__ == "__main__":
    # 检查tabulate是否安装（可选依赖）
    try:
        main()
    except ImportError:
        print("⚠️ 需要安装 tabulate 库来显示表格")
        print("安装命令: pip install tabulate")
        print("\n即使不安装也可以使用，只是显示效果会受影响")
