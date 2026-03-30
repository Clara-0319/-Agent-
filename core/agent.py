# -*- coding: utf-8 -*-
"""
AI婚恋匹配智能体（Agent）
核心工作流：信息提取 → 规则评分 → AI分析报告
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from core.config import ModelConfig
from core.prompt import EXTRACT_PROMPT, MATCHING_PROMPT, FALLBACK_REPORT_TEMPLATE
from core.rules import MarriageRuleEngine
from core.llm_client import LLMClient

# 配置日志
logger = logging.getLogger(__name__)


class MarriageAIAgent:
    """婚恋匹配AI智能体"""
    
    def __init__(self, model: str = "qwen", enable_fallback: bool = True):
        """
        初始化智能体
        
        Args:
            model: 模型类型（目前支持 'qwen'）
            enable_fallback: 大模型失败时是否使用规则引擎备用方案
        """
        self.model = model
        self.enable_fallback = enable_fallback
        self.rules = MarriageRuleEngine()
        self.llm = LLMClient()
        self.config = ModelConfig()
        
        logger.info(f"🚀 AI婚恋匹配智能体初始化完成 (model={model})")
    
    # ==================== 信息抽取模块 ====================
    
    def extract_info(self, user_input: str) -> Dict[str, Any]:
        """
        从用户输入中提取男女双方信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            {
                "male": {...},
                "female": {...},
                "success": bool,
                "error": 错误信息或None
            }
        """
        logger.info("📝 开始信息提取...")
        
        try:
            # 调用大模型进行JSON提取
            response = self.llm.chat_json(EXTRACT_PROMPT, user_input)
            
            if not response:
                logger.warning("⚠️ 大模型返回空JSON，尝试本地解析")
                return self._fallback_extract(user_input)
            
            # 验证提取结果
            if "male" not in response or "female" not in response:
                logger.error("❌ 大模型返回JSON格式不符")
                return self._fallback_extract(user_input)
            
            # 数据清洗与补全
            male = self._sanitize_info(response.get("male", {}))
            female = self._sanitize_info(response.get("female", {}))
            
            logger.info(f"✅ 信息提取成功 - 男方: {male}, 女方: {female}")
            
            return {
                "male": male,
                "female": female,
                "success": True,
                "error": None
            }
        
        except Exception as e:
            logger.error(f"❌ 信息提取异常: {str(e)}")
            return {
                "male": {},
                "female": {},
                "success": False,
                "error": f"信息提取失败: {str(e)}"
            }
    
    def _fallback_extract(self, user_input: str) -> Dict[str, Any]:
        """本地关键词抽取（备用方案）"""
        logger.warning("⚠️ 使用本地关键词抽取作为备用方案")
        
        # 这是一个简化版本，可根据需要扩展
        male, female = {}, {}
        
        # 简单的关键词匹配（实际生产环境可使用NLP库如jieba）
        text = user_input.lower()
        
        # 提取年龄
        import re
        ages = re.findall(r'(\d{2})岁', text)
        if len(ages) >= 1:
            male["age"] = int(ages[0])
        if len(ages) >= 2:
            female["age"] = int(ages[1])
        
        return {
            "male": male,
            "female": female,
            "success": bool(male or female),
            "error": "使用本地抽取，精度可能不足" if not (male or female) else None
        }
    
    def _sanitize_info(self, info: dict) -> dict:
        """
        数据清洗与类型转换
        
        Args:
            info: 原始信息字典
            
        Returns:
            清洗后的信息
        """
        cleaned = {}
        
        # 年龄：整数
        if "age" in info:
            try:
                cleaned["age"] = int(info["age"])
            except:
                cleaned["age"] = 30  # 默认值
        
        # 身高：整数
        if "height" in info:
            try:
                cleaned["height"] = int(info["height"])
            except:
                cleaned["height"] = 170
        
        # 学历、城市、家境、性格、职业、婚恋观、生育观：字符串
        for key in ["education", "city", "family_background", "character", "career", 
                    "marriage_view", "child_view"]:
            if key in info:
                cleaned[key] = str(info[key]).strip() if info[key] else ""
        
        return cleaned
    
    # ==================== 规则评分模块 ====================
    
    def evaluate(self, male: dict, female: dict) -> Dict[str, Any]:
        """
        使用规则引擎进行匹配评分
        
        Args:
            male: 男性信息
            female: 女性信息
            
        Returns:
            规则引擎返回的评分结果
        """
        logger.info("📊 开始规则引擎评分...")
        return self.rules.calculate_total(male, female)
    
    # ==================== AI报告生成模块 ====================
    
    def generate_report(self, male: dict, female: dict, score_result: dict) -> str:
        """
        调用大模型生成专业的匹配分析报告
        
        Args:
            male: 男性信息
            female: 女性信息
            score_result: 规则引擎的评分结果
            
        Returns:
            AI生成的分析报告文本
        """
        logger.info("✍️ 正在生成AI分析报告...")
        
        try:
            # 构建提示词输入
            user_content = self._format_score_for_llm(male, female, score_result)
            
            # 调用大模型
            report = self.llm.chat(MATCHING_PROMPT, user_content)
            
            # 检查是否调用失败
            if report.startswith("大模型"):
                logger.warning(f"⚠️ 大模型调用失败: {report}")
                if self.enable_fallback:
                    return self._generate_fallback_report(score_result)
                else:
                    return report
            
            logger.info("✅ AI报告生成成功")
            return report
        
        except Exception as e:
            logger.error(f"❌ 报告生成异常: {str(e)}")
            if self.enable_fallback:
                return self._generate_fallback_report(score_result)
            else:
                return f"报告生成失败: {str(e)}"
    
    def _format_score_for_llm(self, male: dict, female: dict, score_result: dict) -> str:
        """格式化评分结果供大模型分析"""
        
        dimensions = score_result.get("dimensions", {})
        
        formatted = f"""
【用户信息】
男方：{json.dumps(male, ensure_ascii=False, indent=2)}
女方：{json.dumps(female, ensure_ascii=False, indent=2)}

【规则引擎评分结果】
综合评分：{score_result.get('total_score', 0)}分
匹配等级：{score_result.get('match_level', '未知')}

各维度详细评分：
"""
        
        for dim_name, dim_data in dimensions.items():
            score = dim_data.get("score", 0)
            reason = dim_data.get("reason", "")
            formatted += f"- {dim_name}: {score}分 - {reason}\n"
        
        formatted += f"风险预警：{', '.join(score_result.get('risk_warnings', []))}\n"
        
        return formatted
    
    def _generate_fallback_report(self, score_result: dict) -> str:
        """大模型失败时的本地报告生成"""
        logger.warning("⚠️ 使用规则引擎的本地报告作为备用方案")
        
        total_score = score_result.get("total_score", 0)
        match_level = score_result.get("match_level", "未知")
        dimensions = score_result.get("dimensions", {})
        
        # 生成简化报告
        report = f"""
【婚恋匹配分析报告】
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
数据来源：规则引擎本地评分

【综合评价】
总体匹配评分：{total_score}分
匹配等级：{match_level}

【各维度详细评分】
"""
        
        for dim_name, dim_data in dimensions.items():
            score = dim_data.get("score", 0)
            reason = dim_data.get("reason", "")
            report += f"\n✨ {dim_name.upper()}：{score}分\n   {reason}"
        
        report += f"\n\n【风险提示】\n"
        for warning in score_result.get("risk_warnings", []):
            report += f"• {warning}\n"
        
        report += """
【建议】
此为规则引擎生成的初步评分报告。若需更深入的心理学分析和专业建议，
建议确保网络连接正常以调用AI大模型进行全面分析。
"""
        
        return report
    
    # ==================== 完整流程：match ====================
    
    def match(self, user_input: str) -> Dict[str, Any]:
        """
        完整的婚恋匹配工作流
        
        流程：
        1. 信息提取 → 2. 规则评分 → 3. AI报告生成
        
        Args:
            user_input: 用户输入的男女信息文本
            
        Returns:
            {
                "success": bool,
                "extract_result": 提取结果,
                "score_result": 评分结果,
                "report": 分析报告,
                "error": 错误信息或None,
                "timestamp": 处理时间戳
            }
        """
        logger.info("=" * 60)
        logger.info("🎯 开始婚恋匹配工作流")
        logger.info("=" * 60)
        
        start_time = datetime.now()
        
        try:
            # 第一步：信息提取
            extract_result = self.extract_info(user_input)
            
            if not extract_result["success"]:
                logger.error("❌ 信息提取失败，工作流中断")
                return {
                    "success": False,
                    "extract_result": extract_result,
                    "score_result": None,
                    "report": None,
                    "error": extract_result["error"],
                    "timestamp": datetime.now().isoformat()
                }
            
            male = extract_result["male"]
            female = extract_result["female"]
            
            # 验证必要信息
            if not male.get("age") or not female.get("age"):
                error_msg = "缺少必要信息：年龄（age）"
                logger.error(f"❌ {error_msg}")
                return {
                    "success": False,
                    "extract_result": extract_result,
                    "score_result": None,
                    "report": None,
                    "error": error_msg,
                    "timestamp": datetime.now().isoformat()
                }
            
            # 第二步：规则评分
            score_result = self.evaluate(male, female)
            
            # 第三步：AI报告生成
            report = self.generate_report(male, female, score_result)
            
            # 工作流完成
            duration = (datetime.now() - start_time).total_seconds()
            logger.info("=" * 60)
            logger.info(f"✅ 婚恋匹配工作流完成，耗时 {duration:.2f}秒")
            logger.info("=" * 60)
            
            return {
                "success": True,
                "extract_result": extract_result,
                "score_result": score_result,
                "report": report,
                "error": None,
                "timestamp": datetime.now().isoformat(),
                "duration": round(duration, 2)
            }
        
        except Exception as e:
            logger.error(f"❌ 工作流异常: {str(e)}", exc_info=True)
            return {
                "success": False,
                "extract_result": None,
                "score_result": None,
                "report": None,
                "error": f"工作流异常: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    # ==================== 输出格式化 ====================
    
    def format_output(self, result: dict) -> str:
        """
        将匹配结果格式化为用户友好的输出
        
        Args:
            result: match() 的返回结果
            
        Returns:
            格式化后的输出字符串
        """
        if not result["success"]:
            return f"❌ 匹配失败: {result.get('error', '未知错误')}"
        
        output = []
        output.append("\n" + "=" * 70)
        output.append("🎯 AI婚恋匹配分析结果")
        output.append("=" * 70)
        
        # 提取结果
        extract = result.get("extract_result", {})
        if extract.get("success"):
            output.append("\n✅ 【信息提取结果】")
            output.append(f"   男方: {json.dumps(extract['male'], ensure_ascii=False)}")
            output.append(f"   女方: {json.dumps(extract['female'], ensure_ascii=False)}")
        
        # 评分结果
        score = result.get("score_result", {})
        output.append("\n📊 【规则引擎评分】")
        output.append(f"   综合评分: {score.get('total_score', 0)}/100")
        output.append(f"   匹配等级: {score.get('match_level', '未知')}")
        
        for dim_name, dim_data in score.get("dimensions", {}).items():
            s = dim_data.get("score", 0)
            r = dim_data.get("reason", "")
            output.append(f"   - {dim_name}: {s}分 ({r})")
        
        # AI报告
        report = result.get("report", "")
        if report and not report.startswith("大模型"):
            output.append("\n✍️ 【AI专业分析报告】")
            output.append(report)
        
        output.append("\n" + "=" * 70)
        output.append(f"处理时间: {result.get('timestamp', 'N/A')}")
        output.append("=" * 70 + "\n")
        
        return "\n".join(output)