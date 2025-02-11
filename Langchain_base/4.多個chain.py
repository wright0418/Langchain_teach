from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser

# 初始化 LLM
llm = OllamaLLM(model="qwen2.5:0.5b", temperature=0.7)

# 建立第一個 prompt template
first_prompt = PromptTemplate.from_template(
    "請列出{topic}的三個主要特點，用逗號分隔"
)

# 建立第二個 prompt template
second_prompt = PromptTemplate.from_template(
    """根據這些特點：{text}
    請為每個特點提供詳細說明"""
)

# 建立串接的 chain
chain = first_prompt | llm | second_prompt | llm

# 執行 chain
result = chain.invoke({"topic": "Python程式語言"})
print(result)