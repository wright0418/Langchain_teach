import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# 載入環境變數
load_dotenv()

def main():
    # 初始化 Ollama LLM
    model_name = os.getenv("DEFAULT_MODEL", "llama2")
    llm = Ollama(model=model_name, base_url=os.getenv("OLLAMA_BASE_URL"))
    
    # 基本對話測試
    print("\n=== 基本對話測試 ===")
    response = llm.invoke("你好，請簡短介紹一下自己")
    print(f"回應：\n{response}")
    
    # 使用 PromptTemplate
    print("\n=== 使用模板提示 ===")
    prompt_template = PromptTemplate.from_template(
        "你是一位專業的{profession}專家。請針對'{topic}'提供三點專業建議。"
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    response = chain.invoke({"profession": "數據科學", "topic": "資料可視化"})
    print(f"回應：\n{response['text']}")

if __name__ == "__main__":
    main()
