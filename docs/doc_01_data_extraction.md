# 📝 01. 结构化数据清洗引擎 (Data Extraction)

## 🎯 模块简介
本模块利用 LangChain 与大语言模型，结合 Pydantic 严格的数据校验机制，将非结构化的自然语言（如杂乱的买家差评）精准清洗并提取为严谨的 JSON 结构化数据。
这是衔接大模型与传统业务系统（如 PostgreSQL 数据库、RPA 机器人）的核心关卡。

## 🛠️ 核心技术栈
* **框架**: LangChain
* **LLM**: DeepSeek-Chat (或其他兼容 OpenAI 格式的模型)
* **数据校验**: Pydantic `BaseModel`

## 🚀 运行前提
1. 确保已安装项目依赖：`pip install -r requirements.txt`
2. 项目根目录下存在 `.env` 文件，并包含有效的 API 密钥：
   `DEEPSEEK_API_KEY=your_api_key_here`

## 💡 核心功能
* **信息定性**: 自动概括 2-4 个字的核心问题（如：屏幕死机、物流延迟）。
* **情绪打分**: 量化买家愤怒指数（1-5分）。
* **自动预警**: 判断是否需要人工客服紧急介入（输出 True/False 布尔值）。

## 🖥️ 使用示例
运行对应的 Python 文件后，系统将自动打印出可以直接用 `result.字段名` 调用的 Python 对象，方便后续无缝接入业务逻辑。