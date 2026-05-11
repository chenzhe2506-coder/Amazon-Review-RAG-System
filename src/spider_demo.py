import requests
from bs4 import BeautifulSoup
# 修复 1：补上缺失的 LangChain 核心组件导入
# 核心文档结构现在统一放在 langchain_core 里
from langchain_core.documents import Document

# 所有的切片器现在统一独立到了 langchain_text_splitters 里
from langchain_text_splitters import RecursiveCharacterTextSplitter

print("🚀 跑腿小哥已出发...")

# 1. 目标网址
url = "http://books.toscrape.com/"

# 2. requests 上场
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("✅ 网页源代码已成功搬回！交给 BeautifulSoup 理货员...")
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    print(f"📦 一共找到了 {len(books)} 本书。开始提取书名和价格...\n")
    
    documents = []
    
    # 3. 遍历提取数据（这里是循环内部）
    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        star = book.find("p", class_="star-rating")["class"][1]
    
        content = f"书名: {title}, 价格: {price}, 评价星级: {star}"
        doc = Document(page_content=content, metadata={"source": "book_store", "title": title})
        documents.append(doc)
    
    # ---------------- 循环结束的分界线 ----------------

    # 修复 2：将切片器移出 for 循环，跟 for 对齐！
    print("✂️ 开始对收集到的数据进行 LangChain 递归切片...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,      
        chunk_overlap=20     
    )
    
    # 一次性切分整个 documents 列表
    final_chunks = text_splitter.split_documents(documents)

    print(f"✅ 成功将抓取的原始数据转化为 {len(final_chunks)} 个高质量知识碎片！")
    
    # 我们可以随便打印第一个碎片看看效果
    print("-" * 30)
    print("🔍 预览第一个碎片内容：")
    print(final_chunks[0].page_content)
    print("🏷️ 预览第一个碎片元数据：", final_chunks[0].metadata)

else:
    print(f"❌ 完蛋，跑腿小哥被拦住了！状态码：{response.status_code}")