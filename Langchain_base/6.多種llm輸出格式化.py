from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser,\
    JsonOutputParser

from typing import List



# 初始化 LLM
llm = OllamaLLM(model="qwen2.5:0.5b", temperature=0.7)

# 1. 逗號分隔列表解析器
list_parser = CommaSeparatedListOutputParser()
list_prompt = PromptTemplate.from_template(
    """請列出{topic}的三個主要特點
    請用逗號分隔每個特點，不要加編號
    格式範例：特點1, 特點2, 特點3"""
)

# 2. JSON 格式解析器
json_parser = JsonOutputParser()
json_prompt = PromptTemplate.from_template(
    """請提供{topic}的資訊，包含以下欄位：
    - name: 名稱
    - features: 特點列表
    - description: 簡短描述
    
    請用 JSON 格式回答，範例：
    {{
        "name": "主題名稱",
        "features": ["特點1", "特點2", "特點3"],
        "description": "描述文字"
    }}"""
)


def test_parsers(topic: str):
    # 測試列表解析器
    list_chain = list_prompt | llm | list_parser
    list_result = list_chain.invoke({"topic": topic})
    print("列表格式輸出：")
    print(list_result)
    print("\n")

    # 測試 JSON 解析器
    json_chain = json_prompt | llm | json_parser
    json_result = json_chain.invoke({"topic": topic})
    print("JSON 格式輸出：")
    print(json_result)
    print("\n")



# 執行測試
test_parsers("Python程式語言")