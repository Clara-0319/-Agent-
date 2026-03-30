# 🔌 API 文档

## 概述

AI婚恋匹配系统提供完整的REST API接口，支持：
- 🔗 完整的婚恋匹配流程
- 📝 单独的信息提取
- 📊 单独的规则评分
- 📦 批量匹配处理

---

## 快速启动

### 安装Flask依赖

```bash
pip install flask flask-cors
```

### 启动API服务

```bash
python api_service.py
```

默认地址：`http://localhost:8000`

---

## API 端点

### 1. 📋 完整匹配 (推荐)

**端点** `POST /api/match`

**描述**: 执行完整的婚恋匹配工作流（信息提取 → 规则评分 → AI分析）

**请求示例**:

```bash
curl -X POST http://localhost:8000/api/match \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "男28岁本科北京身高175 女26岁硕士北京身高164"
  }'
```

**请求参数**:

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| user_input | string | ✅ | 用户输入的男女信息文本 |

**响应示例**:

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "extract": {
      "success": true,
      "male": {
        "age": 28,
        "education": "本科",
        "city": "北京",
        "height": 175,
        ...
      },
      "female": {
        "age": 26,
        "education": "硕士",
        "city": "北京",
        "height": 164,
        ...
      }
    },
    "score": {
      "total_score": 87,
      "match_level": "✅ 很好匹配",
      "dimensions": {
        "age": {
          "score": 88,
          "reason": "优秀年龄差..."
        },
        ...
      },
      "risk_warnings": ["无明显风险"]
    },
    "report": "【综合匹配评价】本组合整体匹配度很好...",
    "duration": 1.23,
    "timestamp": "2024-03-27T16:48:46.123456"
  }
}
```

**响应参数**:

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 结果代码 (0=成功, -1=失败) |
| message | string | 提示信息 |
| data.extract | object | 信息提取结果 |
| data.score | object | 规则评分结果 |
| data.report | string | AI生成的详细分析报告 |
| data.duration | float | 处理耗时（秒） |
| data.timestamp | string | 处理时间戳 |

---

### 2. 📝 信息提取

**端点** `POST /api/extract`

**描述**: 从文本中提取男女双方信息

**请求示例**:

```bash
curl -X POST http://localhost:8000/api/extract \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "男28岁本科北京 女26岁硕士深圳"
  }'
```

**响应示例**:

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "male": {
      "age": 28,
      "education": "本科",
      "city": "北京",
      "height": null,
      ...
    },
    "female": {
      "age": 26,
      "education": "硕士",
      "city": "深圳",
      ...
    }
  }
}
```

---

### 3. 📊 规则评分

**端点** `POST /api/evaluate`

**描述**: 对已提取的信息进行规则引擎评分

**请求示例**:

```bash
curl -X POST http://localhost:8000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "male": {
      "age": 28,
      "education": "本科",
      "city": "北京",
      "family_background": "中等",
      "character": "稳重",
      "career": "工程师"
    },
    "female": {
      "age": 26,
      "education": "硕士",
      "city": "北京",
      "family_background": "富裕",
      "character": "独立",
      "career": "医生"
    }
  }'
```

**响应示例**:

```json
{
  "code": 0,
  "message": "成功",
  "data": {
    "total_score": 87,
    "match_level": "✅ 很好匹配",
    "dimensions": {
      "age": {
        "score": 88,
        "reason": "优秀年龄差（3-4岁）..."
      },
      "education": {
        "score": 80,
        "reason": "学历接近..."
      },
      "city": {
        "score": 95,
        "reason": "同城无异地风险..."
      },
      "economic": {
        "score": 85,
        "reason": "基础硬件条件匹配良好"
      },
      "character": {
        "score": 85,
        "reason": "性格互补性较好..."
      }
    },
    "risk_warnings": ["无明显风险"],
    "weights": {
      "age": 0.25,
      "education": 0.25,
      "city": 0.2,
      "economic": 0.15,
      "character": 0.15
    }
  }
}
```

---

### 4. 📦 批量匹配

**端点** `POST /api/batch-match`

**描述**: 批量处理多个婚恋匹配案例

**请求示例**:

```bash
curl -X POST http://localhost:8000/api/batch-match \
  -H "Content-Type: application/json" \
  -d '{
    "cases": [
      {"user_input": "男28岁本科北京 女26岁硕士北京"},
      {"user_input": "男30岁大专深圳 女28岁大专深圳"},
      {"user_input": "男32岁硕士北京 女29岁本科上海"}
    ]
  }'
```

**响应示例**:

```json
{
  "code": 0,
  "message": "成功处理 3 个案例",
  "data": {
    "total": 3,
    "results": [
      {
        "input": "男28岁本科北京 女26岁硕士北京",
        "result": {
          "success": true,
          "score_result": {
            "total_score": 87,
            "match_level": "✅ 很好匹配",
            ...
          },
          ...
        }
      },
      ...
    ]
  }
}
```

---

### 5. ❤️ 服务健康检查

**端点** `GET /api/health`

**描述**: 检查API服务是否正常运行

**请求示例**:

```bash
curl http://localhost:8000/api/health
```

**响应示例**:

```json
{
  "code": 0,
  "message": "服务正常",
  "status": "healthy"
}
```

---

### 6. 📚 API首页

**端点** `GET /`

**描述**: 获取API文档和端点列表

**响应示例**:

```json
{
  "name": "AI婚恋匹配系统 API",
  "version": "1.0.0",
  "endpoints": {
    "GET /": "API首页",
    "GET /api/health": "服务健康检查",
    ...
  }
}
```

---

## 错误处理

### 常见错误状态码

| 状态码 | 错误代码 | 说明 |
|--------|--------|------|
| 200 | 0 | ✅ 请求成功 |
| 400 | -1 | ❌ 请求参数错误 |
| 404 | -1 | ❌ 端点不存在 |
| 405 | -1 | ❌ 请求方法不允许 |
| 500 | -1 | ❌ 服务器错误 |

### 错误响应示例

```json
{
  "code": -1,
  "message": "缺少必要参数: user_input"
}
```

---

## 输入格式

### user_input 支持的格式

系统支持**灵活的自由文本输入**，以下都是有效格式：

```
基础格式：
"男28北京 女26北京"

详细格式：
"男28岁本科身高175cm北京中等家境稳重性格工程师 女26岁硕士身高164cm北京富裕家境独立性格医生"

结构化文本：
"男方：28岁，本科，北京，175
 女方：26岁，硕士，北京，164"

自然语言：
"他今年28岁，本科学历，北京来的，是工程师
 她26岁，硕士毕业，也在北京工作，做医生"
```

### male/female 对象结构

```json
{
  "age": 28,                      // 年龄（整数）
  "education": "本科",            // 学历
  "height": 175,                  // 身高（cm）
  "city": "北京",                // 城市
  "family_background": "中等",    // 家境
  "character": "稳重",           // 性格
  "career": "工程师",            // 职业
  "marriage_view": "...",        // 婚恋观
  "child_view": "..."           // 生育观
}
```

---

## 集成示例

### JavaScript/React

```javascript
async function matchCouple(userInput) {
  const response = await fetch('/api/match', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_input: userInput })
  });
  
  const data = await response.json();
  
  if (data.code === 0) {
    const score = data.data.score.total_score;
    const report = data.data.report;
    console.log(`匹配评分: ${score}`);
    console.log(`详细报告: ${report}`);
  } else {
    console.error(data.message);
  }
}

// 使用
matchCouple("男28岁本科北京 女26岁硕士北京");
```

### Python

```python
import requests

API_URL = "http://localhost:8000/api/match"

def match_couple(user_input):
    response = requests.post(API_URL, json={"user_input": user_input})
    data = response.json()
    
    if data["code"] == 0:
        score = data["data"]["score"]["total_score"]
        report = data["data"]["report"]
        print(f"匹配评分: {score}")
        print(f"详细报告: {report}")
    else:
        print(f"错误: {data['message']}")

# 使用
match_couple("男28岁本科北京 女26岁硕士北京")
```

### cURL

```bash
# 完整匹配
curl -X POST http://localhost:8000/api/match \
  -H "Content-Type: application/json" \
  -d '{"user_input":"男28岁本科北京 女26岁硕士北京"}'

# 信息提取
curl -X POST http://localhost:8000/api/extract \
  -H "Content-Type: application/json" \
  -d '{"user_input":"男28岁本科北京 女26岁硕士北京"}'

# 规则评分
curl -X POST http://localhost:8000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"male":{"age":28,"education":"本科","city":"北京"},"female":{"age":26,"education":"硕士","city":"北京"}}'
```

---

## 性能和限制

| 指标 | 值 |
|------|-----|
| 请求超时 | 30秒 |
| 最大信息长度 | 5000字符 |
| 最大并发连接 | 无限制 |
| 速率限制 | 无（可根据需要添加） |
| 批量操作最大案例数 | 1000个 |

---

## 部署建议

### 生产环境

```python
# 使用gunicorn或uwsgi运行
# gunicorn -w 4 -b 0.0.0.0:8000 api_service:app
```

### 环境变量配置

```bash
export HOST=0.0.0.0
export PORT=8000
export DEBUG=False
```

### Docker部署 (可选)

```dockerfile
FROM python:3.8

WORKDIR /app
COPY . .
RUN pip install -r core/requirements.txt flask flask-cors

CMD ["python", "api_service.py"]
```

---

## 常见问题

**Q: 如何启用CORS？**  
A: Flask应用已配置`flask_cors`，支持跨域请求。

**Q: 如何添加身份验证？**  
A: 可在`api_service.py`中添加JWT或API Key验证。

**Q: 支持WebSocket吗？**  
A: 目前仅支持HTTP REST API，可根据需要扩展。

**Q: 如何监控调用量？**  
A: 所有请求都有日志记录，可接入ELK或Prometheus进行监控。

---

**📖 更多文档：** [README.md](README.md) | [快速入门](QUICK_START.md)
