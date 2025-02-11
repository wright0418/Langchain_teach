from langchain_ollama.llms import OllamaLLM

# 初始化 LLM
llm = OllamaLLM(model="qwen2.5:0.5b" ,temperature=0.7)

# 簡單的提問
text = "什麼是人工智慧？"

response = llm.invoke(text)
print (f'LLM 回答: {response}')  
print (f'返回內容型態 : {type (response)}') 
print (f'字串長度 : {len(response)}') 



