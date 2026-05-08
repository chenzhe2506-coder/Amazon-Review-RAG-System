# ==========================================
# 0. 战前准备：导入所有需要的零件
# ==========================================
import os
from dotenv import load_dotenv # 引入搬运工
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# 🚀 启动搬运工：让系统悄悄读取 .env 里的密码
load_dotenv() 

# ==========================================
# 1. 打造“数据模具”
# ==========================================
class ReviewAnalysis(BaseModel):
    core_issue: str = Field(description="差评的核心缺陷分类，请用2-4个字的简短词语概括，例如：屏幕死机、物流延迟等")
    sentiment_score: int = Field(description="买家愤怒指数，必须是 1 到 5 之间的整数，5分代表极其愤怒")
    requires_urgent_action: bool = Field(description="是否需要人工客服紧急介入？(如果是退款或威胁投诉填 True)")
    action_suggestion: str = Field(description="给产品研发或运营团队的一句话改进建议")

# ==========================================
# 2. 准备打工的机器
# ==========================================
# 🛡️ 安全升级：从系统内存里提取密码，代码里再也看不到明文！
my_api_key = os.getenv("DEEPSEEK_API_KEY")

llm = ChatOpenAI(
    api_key=my_api_key, # <--- 完美隐藏
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    temperature=0.1 
)

parser = PydanticOutputParser(pydantic_object=ReviewAnalysis)

# ==========================================
# 3. 绘制带有自动警告说明的“图纸”
# ==========================================
prompt = PromptTemplate(
    template="你是一个资深的跨境电商数据分析师。\n请分析以下差评：\n{review}\n\n{format_instructions}",
    input_variables=["review"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# ==========================================
# 4. 组装终极流水线！
# ==========================================
chain = prompt | llm | parser

print("🏭 高级数据清洗流水线启动中...\n")

# ==========================================
# 5. 倒入原料，一键触发
# ==========================================
review_text = "屏幕15天就坏了，客服4天不回消息，退钱！"
result = chain.invoke({"review": review_text})

# ==========================================
# 6. 见证奇迹：提取结构化对象
# ==========================================
print("【大模型吐出的原始对象】:")
print(result)
print("-" * 40)

print("👉 直接读取单点数据：")
print(f"核心问题是：{result.core_issue}")
print(f"愤怒指数是：{result.sentiment_score} 分")
print(f"是否紧急：{result.requires_urgent_action}")

print("-" * 40)
if result.requires_urgent_action:
    print("🚨 [警报触发] 准备调用钉钉机器人发送紧急通知！")
else:
    print("✅ [状态正常] 准备将该条分析结果静默存入 PostgreSQL 数据库。")