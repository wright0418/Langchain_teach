from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
 

# 建立 prompt 模板
prompt = PromptTemplate(
    input_variables=["product"],
    template="請幫我寫一個關於{product}的產品說明。"
)

# 初始化 LLM
llm = OllamaLLM(model="qwen2.5:0.5b" ,temperature=0)

# 使用模板生成內容
product_prompt = prompt.format(product="智慧型手機")
result = llm.invoke(product_prompt)
print(result)

# ======================================================
# 建立 prompt 2 var 模板
prompt = PromptTemplate(
    input_variables=["product","user"],
    template="請幫我寫一個關於{user}使用{product}產品遇到的問題"
)

# 使用模板生成內容
product_prompt = prompt.format(product="智慧型手機",user="老師")
result = llm.invoke(product_prompt)
print(result)
