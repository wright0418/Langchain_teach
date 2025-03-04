import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from langchain_core.runnables import RunnablePassthrough

# 載入環境變數
load_dotenv()

def main():
    # 初始化 Ollama LLM
    model_name = os.getenv("DEFAULT_MODEL", "llama2")
    llm = Ollama(model=model_name, base_url=os.getenv("OLLAMA_BASE_URL"))
    
    print("\n===== 簡單鏈 =====")
    # 簡單鏈：提示 -> LLM -> 解析器
    prompt = PromptTemplate.from_template("列出五個{topic}的例子。")
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke({"topic": "常見的程式設計語言"})
    print(result)
    
    print("\n===== 序列鏈 =====")
    # 序列鏈：將多個鏈連接起來
    first_prompt = PromptTemplate.from_template("為以下主題提供三個子主題：{topic}")
    second_prompt = PromptTemplate.from_template(
        "為以下子主題列表中的每一項提供一個簡短描述：\n{subtopics}"
    )
    
    # 第一個鏈：獲取子主題
    first_chain = first_prompt | llm | StrOutputParser()
    
    # 完整鏈
    chain = (
        {"topic": RunnablePassthrough()}
        | {"subtopics": first_chain}
        | second_prompt
        | llm
        | StrOutputParser()
    )
    
    result = chain.invoke("Python 編程")
    print(result)
    
    print("\n===== 使用解析器 =====")
    # 使用解析器獲得結構化輸出
    parser = CommaSeparatedListOutputParser()
    format_instructions = parser.get_format_instructions()
    
    list_prompt = PromptTemplate.from_template(
        "列出{number}個{category}。\n{format_instructions}"
    )
    
    list_chain = (
        list_prompt
        | llm
        | parser
    )
    
    result = list_chain.invoke({
        "number": 5,
        "category": "數據科學中的熱門工具",
        "format_instructions": format_instructions
    })
    
    print("結果類型:", type(result))
    for i, item in enumerate(result, 1):
        print(f"{i}. {item}")
    
    print("\n===== 條件鏈 =====")
    # 條件鏈：根據內容切換不同的處理流程
    from langchain.chains import create_tagging_chain
    from langchain_core.pydantic_v1 import BaseModel, Field
    
    # 定義標籤架構
    class QueryType(BaseModel):
        type: str = Field(description="查詢類型：'technical' 或 'general'")
    
    # 創建標籤鏈
    tagging_chain = create_tagging_chain(
        QueryType, llm
    )
    
    # 根據標籤類型使用不同的提示模板
    technical_prompt = PromptTemplate.from_template(
        "您是一位專業的技術專家。請詳細解答以下技術問題：{query}"
    )
    
    general_prompt = PromptTemplate.from_template(
        "您是一位友善的助手。請用簡單的語言回答以下問題：{query}"
    )
    
    # 定義分支流程
    def route_query(input_data):
        query = input_data["query"]
        tag_result = tagging_chain.run(query)
        query_type = tag_result.get("type", "general").lower()
        
        if query_type == "technical":
            return technical_prompt.format(query=query)
        else:
            return general_prompt.format(query=query)
    
    # 建立條件鏈
    conditional_chain = (
        RunnablePassthrough()
        | route_query
        | llm
        | StrOutputParser()
    )
    
    # 測試不同類型的查詢
    technical_query = "解釋HTTP協議中的狀態碼有哪些分類？"
    general_query = "為什麼天空是藍色的？"
    
    print("技術查詢結果:")
    print(conditional_chain.invoke({"query": technical_query}))
    
    print("\n一般查詢結果:")
    print(conditional_chain.invoke({"query": general_query}))

if __name__ == "__main__":
    main()
