# 🎯 AI婚恋匹配智能评价系统

**基于大模型Agent与婚恋规则引擎的智能匹配评价系统**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 项目概述

这是一个**生产级别**的AI婚恋匹配系统，融合了：
- **大模型AI（通义千问）**：自然语言理解与专业报告生成
- **规则引擎**：基于婚恋学数据的五维度评分模型
- **智能Agent工作流**：信息提取 → 规则评分 → AI分析

### 核心功能

| 功能 | 描述 |
|------|------|
| 📝 信息提取 | 从自由文本中智能提取男女双方的年龄、学历、城市、家境、性格、职业、婚恋观等 |
| 📊 规则评分 | 五维度加权评分（年龄25%、学历25%、地域20%、经济15%、性格15%） |
| 🤖 AI分析 | 调用通义千问生成专业的匹配分析报告与个性化建议 |
| ⚠️ 风险预警 | 识别潜在的婚恋风险因素（异地、学历差、经济差异等） |
| 💾 备用方案 | 大模型失败时自动降级到规则引擎本地报告 |

---

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
cd marrige_match
pip install -r core/requirements.txt
```

**依赖库：**
- `requests>=2.28.0` - HTTP请求（调用通义千问API）
- `python-dotenv>=0.19.0` - 环境变量管理

### 2️⃣ 配置API密钥

编辑 `core/.env` 文件：

```env
# 从阿里云获取：https://dashscope.console.aliyun.com/
DASHSCOPE_API_KEY=sk-your-api-key-here
DASHSCOPE_MODEL=qwen-turbo

# 模型参数
TEMPERATURE=0.1       # 降低随机性，提高稳定性
TOP_P=0.9
REQUEST_TIMEOUT=30

# 日志配置
LOG_LEVEL=INFO

# 功能开关
ENABLE_FALLBACK=true  # 大模型失败时是否使用规则引擎备用方案
ENABLE_CACHE=true
```

**获取API密钥步骤：**
1. 前往 [阿里云DashScope](https://dashscope.console.aliyun.com/)
2. 创建或选择已有的API密钥
3. 复制密钥到 `.env` 文件中

### 3️⃣ 运行程序

```bash
# 方式1：从项目根目录运行
python main.py

# 方式2：从core目录运行
cd core
python main.py

# 方式3：以模块方式调用
python -c "from core.agent import MarriageAIAgent; agent = MarriageAIAgent(); print(agent.match('男28岁本科北京 女26岁硕士北京'))"
```

选择运行模式：
- **1️⃣ 基础示例** - 单个案例演示
- **2️⃣ 多案例对比** - 三个典型案例对比分析
- **3️⃣ API格式** - 查看API接口返回格式
- **4️⃣ 调试模式** - 显示详细日志
- **5️⃣ 交互模式** - 持续输入进行匹配（推荐！）

---

## 📖 使用示例

### 基础调用（Python脚本）

```python
from core.agent import MarriageAIAgent

# 初始化智能体
agent = MarriageAIAgent()

# 用户输入
user_input = """
男方：28岁，本科，身高175cm，北京，家境中等，性格稳重，软件工程师
女方：26岁，硕士，身高164cm，北京，家境良好，性格独立，医生
"""

# 执行完整的匹配工作流
result = agent.match(user_input)

# 输出结果
if result["success"]:
    print(agent.format_output(result))
    
    # 获取各个详细结果
    extract = result["extract_result"]  # 提取结果
    score = result["score_result"]      # 评分结果
    report = result["report"]            # AI报告
    
    print(f"综合评分: {score['total_score']}/100")
    print(f"匹配等级: {score['match_level']}")
else:
    print(f"错误: {result['error']}")
```

### 交互模式

```
👤 请输入男女信息: 男28岁本科北京175 女26岁硕士北京164

🔄 处理中...

========================================================================
🎯 AI婚恋匹配分析结果
========================================================================

✅ 【信息提取结果】
   男方: {"age": 28, "education": "本科", "height": 175, "city": "北京", ...}
   女方: {"age": 26, "education": "硕士", "height": 164, "city": "北京", ...}

📊 【规则引擎评分】
   综合评分: 87/100
   匹配等级: ✅ 很好匹配
   ...

✍️ 【AI专业分析报告】
【综合匹配评价】
本组合整体匹配度很好，各方面条件相当平衡...
   ...
```

### API集成示例

```python
# 用于前端调用
def api_match(user_input: str) -> dict:
    agent = MarriageAIAgent()
    result = agent.match(user_input)
    
    return {
        "code": 0 if result["success"] else -1,
        "message": "成功" if result["success"] else result.get("error"),
        "data": {
            "extract": result.get("extract_result"),
            "score": result.get("score_result"),
            "report": result.get("report"),
            "timestamp": result.get("timestamp"),
            "duration": result.get("duration")
        }
    }
```

---

## 🏗️ 项目结构

```
marrige_match/
├── main.py                 # 🚀 项目主入口（快速启动）
├── requirements.txt        # 依赖库
├── README.md              # 本文档
├── .env                   # 环境配置（API密钥）
├── .gitignore             # git忽略文件
│
└── core/                  # 核心模块包
    ├── __init__.py        # 包初始化
    ├── main.py            # 完整的主程序（含多种运行模式）
    ├── config.py          # ⚙️ 配置管理（从.env加载）
    ├── llm_client.py      # 🤖 大模型API客户端（通义千问）
    ├── agent.py           # 🧠 AI智能体（核心工作流）
    ├── rules.py           # 📊 婚恋规则引擎（五维度评分）
    ├── prompt.py          # 💬 提示词模板库
    └── requirements.txt   # 依赖库（core目录）

└── demo/                  # 前端演示（Vue3 + Tailwind）
    ├── src/
    │   ├── components/    # React组件
    │   │   ├── InputTabs.jsx      # 信息输入组件
    │   │   ├── MatchResult.jsx    # 结果显示
    │   │   ├── ImageUpload.jsx    # 图片上传
    │   │   └── ui/               # UI组件库
    │   └── hooks/
    │       └── useMatchAnalysis.js # 数据获取hooks
    └── package.json       # 前端依赖
```

---

## 📊 评分规则详解

### 五维度评分模型

#### 1️⃣ 年龄匹配（权重25%）

| 年龄差 | 评分 | 等级 | 说明 |
|--------|------|------|------|
| 0-2岁 | 98 | ✅ 黄金 | 生活阶段完全同步，离婚率最低 |
| 3-4岁 | 88 | ✅ 优秀 | 社会接受度高，观点基本相同 |
| 5-6岁 | 75 | 👍 良好 | 可接受，需关注沟通 |
| 7-8岁 | 55 | ⚠️ 警告 | 观念分歧风险，离婚风险+30% |
| 9-12岁 | 35 | ❌ 危险 | 代际差异明显 |
| >12岁 | 15 | ❌❌ 极危 | 普遍不被看好 |

#### 2️⃣ 学历匹配（权重25%）

| 学历差异 | 评分 | 说明 |
|---------|------|------|
| 完全相同 | 96 | ✅ 认知同频，沟通成本低 |
| 相差1级 | 80 | 👍 可接受，需互相理解 |
| 相差2级 | 55 | ⚠️ 可能产生认知分歧 |
| >2级 | 30 | ❌ 认知差异大，离婚风险+40% |

#### 3️⃣ 地域匹配（权重20%）

| 情况 | 评分 | 说明 |
|------|------|------|
| 同城 | 95 | ✅ 离婚率低 (~30%) |
| 相邻城市 | 70 | 👍 距离近，勉强可控 |
| 异地 | 50 | ⚠️ 离婚率高 (~47%) |

#### 4️⃣ 经济条件（权重15%）

考虑：家境匹配、职业稳定性、生活成本预期

#### 5️⃣ 性格互补（权重15%）

- **相同性格**：稳定但缺乏激情 (~75-85分)
- **互补性格**：丰富充实，需理解 (~85分)
- **冲突性格**：长期压力 (~60分)

### 综合评分等级

| 总分 | 等级 | 前景评估 |
|------|------|--------|
| 85-100 | 🌟 优秀匹配 | 强烈推荐，成仙率高 |
| 70-84 | ✅ 很好匹配 | 推荐，需要沟通与理解 |
| 50-69 | 👍 中等匹配 | 可以尝试，需要重点关注风险 |
| 30-49 | ⚠️ 较差匹配 | 谨慎，有明显风险 |
| <30 | ❌ 不推荐 | 不建议深入发展 |

---

## 🔧 开发指南

### 添加新的评分维度

编辑 `core/rules.py`：

```python
class MarriageRuleEngine:
    def __init__(self):
        self.weights = {
            "age": 0.25,
            "education": 0.25,
            "city": 0.20,
            "economic": 0.15,
            "character": 0.15,
            "your_new_dimension": 0.05  # 新维度
        }
    
    def score_your_dimension(self, male: dict, female: dict) -> tuple:
        """新维度的评分逻辑"""
        # 实现评分算法
        return score, reason
```

### 自定义提示词

编辑 `core/prompt.py`，修改 `EXTRACT_PROMPT` 或 `MATCHING_PROMPT`

### 集成到前端

前端发送POST请求到后端API：

```javascript
const response = await fetch('/api/match', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        male: { ... },
        female: { ... }
    })
});

const result = await response.json();
console.log(result.data.score);
console.log(result.data.report);
```

---

## ⚠️ 常见问题

### Q: API密钥怎么获取？
**A:** 
1. 访问 [阿里云DashScope](https://dashscope.console.aliyun.com/)
2. 完成实名认证
3. 创建或复制已有的API密钥
4. 添加到 `.env` 文件

### Q: 可以不配置API密钥就使用吗？
**A:** 可以。系统会自动降级到规则引擎模式，只进行规则评分，但**无法调用大模型生成深度分析报告**。

### Q: 怎么部署到生产环境？
**A:** 
1. 配置完整的 `.env` 文件
2. 使用 `python main.py` 启动交互模式，或
3. 将 `agent.match()` 接口作为API服务集成到Django/FastAPI中

### Q: 支持批量处理吗？
**A:** 支持。可以编写循环调用 `agent.match()` 处理多个案例，或修改API支持批量请求。

### Q: 评分结果不准确怎么办？
**A:** 
1. 检查输入数据完整性（年龄、学历、城市是必要字段）
2. 调整 `core/rules.py` 中的权重配置
3. 优化提示词模板（`core/prompt.py`）

### Q: 如何修改评分权重？
**A:** 编辑 `core/rules.py` 中的 `weights` 字典，确保各权重之和为1.0

---

## 🔐 隐私与安全

- ✅ **敏感信息**：API密钥存储在 `.env` 中，**永不上传**
- ✅ **数据处理**：所有数据在本地处理或通过HTTPS发送到阿里云
- ✅ **.gitignore**：已配置忽略 `.env` 和其他敏感文件

---

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📞 联系方式

- 📧 如有技术问题，请在项目中提Issue
- 💡 功能建议欢迎讨论

---

## 🎓 学习资源

- [通义千问API文档](https://help.aliyun.com/zh/dashscope/)
- [婚恋心理学研究](https://psychologytoday.com/us/basics/relationships)
- [Prompt Engineering最佳实践](https://platform.openai.com/docs/guides/prompt-engineering)

---

## ✨ 功能亮点

✅ **生产级代码质量**
- 完整的异常处理与日志系统
- 类型注解与文档字符串
- 代码注释清晰

✅ **灵活的工作流**
- 支持多种输入格式与用户交互方式
- 自动降级机制（大模型失败→规则引擎）
- 可扩展的评分模型

✅ **真实的婚恋数据**
- 基于心理学与社会统计数据
- 具有参考价值的风险预警
- 科学的评分模型

✅ **开箱即用**
- 配置简单，运行快速
- 支持多种运行模式
- 完整的使用示例

---

**祝你找到心仪的那个人！💕**

版本：1.0.0 | 更新：2024年 | 基于Python 3.8+
