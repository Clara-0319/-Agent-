# -*- coding: utf-8 -*-
"""
Flask API 示例 - 展示如何将系统集成为Web服务
可直接用这个文件启动API服务提供给前端调用
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from core.agent import MarriageAIAgent
from core.config import logger

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS支持跨域请求

# 初始化智能体
agent = MarriageAIAgent()


# ==================== API 端点 ====================

@app.route("/api/health", methods=["GET"])
def health_check():
    """健康检查端点"""
    return jsonify({
        "code": 0,
        "message": "服务正常",
        "status": "healthy"
    })


@app.route("/api/match", methods=["POST"])
def api_match():
    """
    婚恋匹配API端点
    
    请求示例：
    POST /api/match
    Content-Type: application/json
    
    {
        "user_input": "男28岁本科北京 女26岁硕士深圳"
    }
    
    响应示例：
    {
        "code": 0,
        "message": "成功",
        "data": {
            "extract": { ... },
            "score": { ... },
            "report": "...",
            "duration": 1.23
        }
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data or "user_input" not in data:
            return jsonify({
                "code": -1,
                "message": "缺少必要参数: user_input"
            }), 400
        
        user_input = data.get("user_input", "").strip()
        
        if not user_input:
            return jsonify({
                "code": -1,
                "message": "user_input 不能为空"
            }), 400
        
        logger.info(f"📥 收到匹配请求: {user_input[:50]}...")
        
        # 执行匹配
        result = agent.match(user_input)
        
        # 构建响应
        if result["success"]:
            return jsonify({
                "code": 0,
                "message": "成功",
                "data": {
                    "extract": result.get("extract_result"),
                    "score": result.get("score_result"),
                    "report": result.get("report"),
                    "duration": result.get("duration"),
                    "timestamp": result.get("timestamp")
                }
            })
        else:
            return jsonify({
                "code": -1,
                "message": result.get("error", "未知错误")
            }), 400
    
    except Exception as e:
        logger.error(f"❌ API错误: {str(e)}")
        return jsonify({
            "code": -1,
            "message": f"服务器错误: {str(e)}"
        }), 500


@app.route("/api/extract", methods=["POST"])
def api_extract():
    """
    单独的信息提取API端点
    
    请求：
    {
        "user_input": "男28岁本科北京 女26岁硕士深圳"
    }
    """
    try:
        data = request.get_json()
        user_input = data.get("user_input", "")
        
        if not user_input:
            return jsonify({
                "code": -1,
                "message": "user_input 不能为空"
            }), 400
        
        result = agent.extract_info(user_input)
        
        return jsonify({
            "code": 0 if result["success"] else -1,
            "message": "成功" if result["success"] else result.get("error"),
            "data": {
                "male": result.get("male"),
                "female": result.get("female")
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": -1,
            "message": str(e)
        }), 500


@app.route("/api/evaluate", methods=["POST"])
def api_evaluate():
    """
    单独的规则评分API端点
    
    请求：
    {
        "male": {"age": 28, "education": "本科", "city": "北京", ...},
        "female": {"age": 26, "education": "硕士", "city": "深圳", ...}
    }
    """
    try:
        data = request.get_json()
        male = data.get("male", {})
        female = data.get("female", {})
        
        if not male or not female:
            return jsonify({
                "code": -1,
                "message": "缺少必要参数: male 和 female"
            }), 400
        
        result = agent.evaluate(male, female)
        
        return jsonify({
            "code": 0,
            "message": "成功",
            "data": result
        })
    
    except Exception as e:
        return jsonify({
            "code": -1,
            "message": str(e)
        }), 500


@app.route("/api/batch-match", methods=["POST"])
def api_batch_match():
    """
    批量匹配API端点
    
    请求：
    {
        "cases": [
            {"user_input": "男28岁本科北京 女26岁硕士北京"},
            {"user_input": "男30岁大专深圳 女28岁大专深圳"}
        ]
    }
    """
    try:
        data = request.get_json()
        cases = data.get("cases", [])
        
        if not cases:
            return jsonify({
                "code": -1,
                "message": "cases 不能为空"
            }), 400
        
        results = []
        
        for case in cases:
            user_input = case.get("user_input", "")
            if user_input:
                result = agent.match(user_input)
                results.append({
                    "input": user_input,
                    "result": result
                })
        
        return jsonify({
            "code": 0,
            "message": f"成功处理 {len(results)} 个案例",
            "data": {
                "total": len(results),
                "results": results
            }
        })
    
    except Exception as e:
        return jsonify({
            "code": -1,
            "message": str(e)
        }), 500


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(e):
    """404错误处理"""
    return jsonify({
        "code": -1,
        "message": "API端点不存在"
    }), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """405错误处理"""
    return jsonify({
        "code": -1,
        "message": "请求方法不允许"
    }), 405


@app.errorhandler(500)
def internal_error(e):
    """500错误处理"""
    return jsonify({
        "code": -1,
        "message": "服务器内部错误"
    }), 500


# ==================== 文档和信息 ====================

@app.route("/", methods=["GET"])
def index():
    """API首页"""
    return jsonify({
        "name": "AI婚恋匹配系统 API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API首页",
            "GET /api/health": "服务健康检查",
            "POST /api/match": "完整婚恋匹配（推荐）",
            "POST /api/extract": "信息提取",
            "POST /api/evaluate": "规则评分",
            "POST /api/batch-match": "批量匹配"
        },
        "documentation": "详见README.md和QUICK_START.md"
    })


# ==================== 启动应用 ====================

if __name__ == "__main__":
    import os
    
    # 获取端口和主机
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"🚀 启动API服务: {host}:{port}")
    logger.info(f"📖 API文档: http://localhost:{port}/")
    
    test_cmd = f"curl -X POST http://localhost:{port}/api/match -H 'Content-Type: application/json' -d '{{\"user_input\": \"男28岁本科北京 女26岁硕士北京\"}}'"
    logger.info(f"🧪 测试命令: {test_cmd}")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )
