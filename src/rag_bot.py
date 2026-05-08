import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ==========================================
# 0. 安全点火与大脑初始化
# ==========================================
load_dotenv()
my_api_key = os.getenv("DEEPSEEK_API_KEY")

# 初始化写作大模型（温度设为0.5，既要严格遵守SOP，又要让语气稍微生动温和一点）
llm = ChatOpenAI(
    api_key=my_api_key,
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    temperature=0.5 
)

# 初始化国产顶级中文翻译官
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-zh-v1.5"
)

# ==========================================
# 1. 搭建临时记忆库 (模拟真实的亚马逊 SOP 库)
# ==========================================
client = chromadb.Client()
collection = client.create_collection(name="ecommerce_sops_final", embedding_function=ef)

collection.add(
    documents=[
        "如果买家反馈屏幕碎裂、有划痕，请安抚情绪，要求对方提供破损照片，核实后全额退款，并推荐购买带保护壳的新款。",
        "如果买家反馈按开机键没反应、死机变砖，请安抚情绪，指导买家：同时长按电源键和音量下键10秒强制重启。如果依然无效，承诺免费换新。",
        "如果买家抱怨物流一直停在清关状态，请解释海关抽查属正常现象，并直接补偿一张5美金无门槛优惠券。"
    ],
    ids=["sop_01", "sop_02", "sop_03"]
)

# ==========================================
# 2. 真实业务场景：抓取到了极端差评
# ==========================================
buyer_message = "你们卖的什么破玩意？新买的机子跟个砖头一样，按哪都没动静，屏幕一片漆黑！太气人了，立刻给我退钱！"
print(f"🚨 收到暴怒买家消息：【{buyer_message}】\n")


# ==========================================
# 3. RAG 核心机制 1：向量检索 (找外脑)
# ==========================================
print("🔍 正在启动 BGE 语义模型检索公司知识库...")
results = collection.query(query_texts=[buyer_message], n_results=1)
best_sop = results['documents'][0][0]
print(f"🎯 提取到匹配 SOP：{best_sop}\n")


# ==========================================
# 4. RAG 核心机制 2：Prompt 融合编排
# ==========================================
prompt = PromptTemplate(
    template="""你是一名极其专业的亚马逊金牌客服。
请根据【公司内部处理标准】，为买家撰写一封高情商、有同理心的回复邮件。

【公司内部处理标准】：{sop}

【买家的原话】：{buyer_message}

【严格回复要求】：
1. 第一段必须真诚、温和地安抚买家情绪，为带来的不便道歉。
2. 必须且只能按照“公司内部处理标准”给出的方案进行回复，绝对不允许自己瞎编任何其他赔偿方案。
3. 语气要专业、不卑不亢，排版要清晰易读。
4. 结尾要有礼貌的落款。
""",
    input_variables=["sop", "buyer_message"]
)

# ==========================================
# 5. 启动流水线并生成最终回复
# ==========================================
# StrOutputParser() 确保大模型吐出来的直接是干净的字符串，不需要复杂的 JSON 解析
chain = prompt | llm | StrOutputParser()

print("✍️ 正在将 SOP 与买家情绪交由大模型进行深度融合与撰写...")
final_reply = chain.invoke({
    "sop": best_sop, 
    "buyer_message": buyer_message
})

print("=" * 50)
print("✨ 最终生成的完美客服邮件：\n")
print(final_reply)
print("=" * 50)