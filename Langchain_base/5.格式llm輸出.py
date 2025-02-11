from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from operator import itemgetter

# 初始化 LLM 和解析器
llm = OllamaLLM(model="qwen2.5:0.5b", temperature=0.7)
parser = CommaSeparatedListOutputParser()

# 建立第一個 prompt template（加入格式說明）
first_prompt = PromptTemplate.from_template(
    """請列出{topic}的三個主要特點
    請用逗號分隔每個特點，不要加編號
    格式範例：特點1, 特點2, 特點3"""
)

# 建立串接的 chain
chain = first_prompt | llm | parser

result = chain.invoke({"topic": "Python程式語言"})
print(result)

