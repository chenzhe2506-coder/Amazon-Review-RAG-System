import chromadb
from chromadb.utils import embedding_functions # 引入翻译官调度中心

# 1. 换上真正的国产中文王者翻译官：BGE 模型
# (首次运行会重新下载，大约 90M，非常快)
multilingual_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-zh-v1.5"  # <--- 名字换成这个！
)

client = chromadb.Client()

# 2. 知识库名字改成 v3，强制系统建一个全新的空库！
collection = client.create_collection(
    name="ecommerce_sops_v3",  # <--- 名字换成 v3！
    embedding_function=multilingual_ef 
)
# ==========================================
# 2. 录入历史经验 (触发自动 Embedding 向量化)
# ==========================================
print("📚 搭载了【多语言高级翻译官】的知识库已建好！")

collection.add(
    documents=[
        "如果买家反馈屏幕碎裂、有物理划痕，请要求对方提供破损照片，核实后全额退款。",
        "如果买家反馈按开机键没反应、死机，请指导买家同时长按电源键和音量下键10秒强制重启。",
        "如果买家抱怨一直停在清关状态、快递太慢，请安抚情绪并直接补偿一张5美金无门槛优惠券。"
    ],
    # 元数据：除了文本，你还可以给这条记录贴上属性标签，方便以后精准过滤
    metadatas=[
        {"type": "硬件破损_退款"},
        {"type": "系统故障_SOP"},
        {"type": "物流客诉_安抚"}
    ],
    # 每一条记录必须有一个唯一的身份证号
    ids=["case_001", "case_002", "case_003"]
)
print("✅ 三条核心 SOP 档案已成功入库！\n")


# ==========================================
# 3. 见证奇迹的时刻：极其模糊的口语化提问
# ==========================================
# 注意看，这句话里【没有】包含“开机键”、“死机”这种精准词汇
buyer_message = "新买的机子跟个砖头一样，按哪都没动静，屏幕一片漆黑！"

print("-" * 40)
print(f"🚨 收到买家新问题：【{buyer_message}】")
print("🔍 正在开启多维向量空间检索...\n")


# ==========================================
# 4. 执行空间物理距离匹配
# ==========================================
results = collection.query(
    query_texts=[buyer_message], # 把买家的话扔进去
    n_results=1                  # 告诉数据库：只要距离最近的那个 1 个最优解
)

print("🎯 【匹配到的最佳处理方案】:")
print(results['documents'][0][0])
print(f"👉 附带的业务标签: {results['metadatas'][0][0]['type']}")