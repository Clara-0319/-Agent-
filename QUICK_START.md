# 🚀 快速入门指南（3分钟上手）

## ⚡ 60秒快速开始

### 1. 安装依赖（10秒）

```bash
pip install python-dotenv requests
```

### 2. 配置API密钥（可选，10秒）

编辑 `core/.env`：

```env
DASHSCOPE_API_KEY=sk-your-api-key-here
```

获取密钥：[阿里云DashScope](https://dashscope.console.aliyun.com/)

### 3. 运行程序（10秒）

```bash
python main.py
```

### 4. 选择交互模式（5频5秒）

```
选择运行模式:
请选择 (0-5): 5    # 选择 5 进入交互模式

👤 请输入男女信息: 男28岁本科北京 女26岁硕士北京

🔄 处理中...

========================================================================
🎯 AI婚恋匹配分析结果
========================================================================
综合评分: 87/100
匹配等级: ✅ 很好匹配
...
```

---

## 💻 三种使用方式

### 方式1️⃣ ：交互模式（最简单）

```bash
python main.py
# 选择 5 (交互模式)
# 输入男女信息即可获得分析
```

**优点**：即时反馈，无需编程  
**适用**：快速测试、个人使用

### 方式2️⃣ ：Python脚本（灵活）

```python
from core.agent import MarriageAIAgent

agent = MarriageAIAgent()
result = agent.match("男28岁本科北京 女26岁硕士深圳")

if result["success"]:
    print(f"评分: {result['score_result']['total_score']}/100")
    print(result["report"])
```

**优点**：灵活度高，可自定义处理  
**适用**：批量处理、自动化

### 方式3️⃣ ：API服务（生产级）

```python
from flask import Flask, request, jsonify
from core.agent import MarriageAIAgent

app = Flask(__name__)
agent = MarriageAIAgent()

@app.route("/api/match", methods=["POST"])
def api_match():
    user_input = request.json.get("user_input", "")
    result = agent.match(user_input)
    
    return jsonify({
        "code": 0 if result["success"] else -1,
        "message": "成功" if result["success"] else result["error"],
        "data": {
            "score": result.get("score_result"),
            "report": result.get("report")
        }
    })

if __name__ == "__main__":
    app.run(port=8000)
```

**优点**：生产级部署，支持并发  
**适用**：Web应用集成、前后端分离

---

## 📊 输出示例

### 规则引擎评分结果

```json
{
  "total_score": 87,
  "match_level": "✅ 很好匹配",
  "dimensions": {
    "age": {
      "score": 88,
      "reason": "优秀年龄差（3-4岁），社会接受度高"
    },
    "education": {
      "score": 80,
      "reason": "学历接近，理解与尊重是关键"
    },
    "city": {
      "score": 95,
      "reason": "同城无异地风险，生活融合度高"
    },
    "economic": {
      "score": 85,
      "reason": "家境相同，生活预期一致"
    },
    "character": {
      "score": 85,
      "reason": "性格互补，能够互相弥补"
    }
  },
  "risk_warnings": ["无明显风险"]
}
```

### AI详细分析报告

```
【综合匹配评价】
本组合整体匹配度很好，各方面条件相当平衡，具有较高的婚恋参考价值。

【各维度匹配分析】
✨ 年龄：88分 - 优秀年龄差...
✨ 学历：80分 - 学历接近...
...

【潜在风险提示】
• 学习差异造成的认知分歧（可能性较低）
...

【先天优势总结】
这对伴侣组合的核心竞争力在于...

【个性化建议】
男方建议：...
女方建议：...

【专业结论】
强烈推荐这段婚恋关系发展。
```

---

## 🔧 常见配置

### 不配置API密钥也能用吗？

✅ **可以！** 系统会自动降级：
- 🟢 规则引擎评分：**正常工作**
- 🟡 LLM分析报告：无法调用（使用本地报告）

```bash
# 无需.env文件，直接运行
python main.py
```

### 怎样修改评分权重？

编辑 `core/rules.py`：

```python
class MarriageRuleEngine:
    def __init__(self):
        self.weights = {
            "age": 0.30,        # 增加权重
            "education": 0.20,  # 减少权重
            "city": 0.20,
            "economic": 0.15,
            "character": 0.15
        }
```

### 怎样添加新的评分维度？

1. 编辑 `core/rules.py`，添加权重和评分方法
2. 编辑 `core/agent.py`，在工作流中调用

---

## 🐛 故障排查

| 问题 | 解决方案 |
|------|--------|
| `ModuleNotFoundError: dotenv` | 运行 `pip install python-dotenv` |
| `Invalid API-key` | 检查 `.env` 中的密钥是否正确 |
| 提取结果为空 | 确保输入包含年龄和城市信息 |
| 评分为0 | 检查年龄字段是否正确识别 |

---

## 📈 性能基准

- **信息提取**：< 1秒（本地）,  < 2秒（API）
- **规则评分**：< 10ms（极快）
- **AI报告生成**：< 3秒（API调用）
- **完整流程**：< 5秒

---

## 🎓 学习路径

1. **初级**：运行交互模式，理解评分规则
2. **中级**：修改权重，自定义评分模型
3. **高级**：集成API，构建Web应用

---

## 💡 实用建议

### ✅ 最佳实践

```python
# 好的输入格式
"男28岁，本科，北京，工程师" 
"女26岁，硕士，北京，医生"

# 包含更多信息
"男28岁本科北京175cm中等家境稳重性格"
"女26岁硕士北京164cm富裕家境独立性格"
```

### ❌ 容易出错的输入

```python
# 不完整
"男，本科"  # 缺少年龄
"女26北京"  # 缺少年龄

# 格式混乱
"他28了是本科的来自北京"  # 虽然系统能处理，但准确性降低
```

---

## 🚀 下一步

- [ ] 配置API密钥以启用AI分析
- [ ] 尝试交互模式体验完整功能
- [ ] 调整权重以符合你的需求
- [ ] 集成到你的应用中

---

**更多详情请查看 [完整文档](README.md)**
