from langchain.chains import LLMChain
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


# 建立 prompt 模板
prompt = PromptTemplate(
    input_variables=["topic","number"],
    template="請給我{number}個關於{topic}的重點。"
)

# 建立 chain
llm = OllamaLLM(model = "qwen2.5:0.5b", temperature=0.7)
chain = prompt | llm 

# 執行 chain
# result = chain.run("Python程式設計")
result = chain.invoke({"topic": "Python程式設計", "number": 30})

print(result)