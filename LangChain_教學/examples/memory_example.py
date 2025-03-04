import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.memory import ConversationBufferWindowMemory, ConversationTokenBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableConfig

load_dotenv()

def main():
    # 初始化 Ollama LLM
    model_name = os.getenv("DEFAULT_MODEL", "llama2")
    llm = Ollama(model=model_name, base_url=os.getenv("OLLAMA_BASE_URL"))
    
    print("\n===== 基本對話記憶 =====")
    # 基本對話記憶
    memory = ConversationBufferMemory()
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )
    
    # 進行對話
    print(conversation.predict(input="你好，我叫小明。"))
    print(conversation.predict(input="我的名字是什麼？"))
    
    # 檢查記憶內容
    print("\n記憶內容:")
    print(memory.buffer)
    
    print("\n===== 滑動窗口記憶 =====")
    # 滑動窗口記憶 - 只保留最近的 k 個交互
    window_memory = ConversationBufferWindowMemory(k=2)
    window_conversation = ConversationChain(
        llm=llm,
        memory=window_memory,
        verbose=True
    )
    
    print(window_conversation.predict(input="我最喜歡的顏色是藍色。"))
    print(window_conversation.predict(input="我喜歡吃蘋果。"))
    print(window_conversation.predict(input="我喜歡什麼水果？"))
    print(window_conversation.predict(input="我最喜歡的顏色是什麼？")) # 這個應該記不住了
    
    print("\n===== 摘要記憶 =====")
    # 摘要記憶 - 保存對話的摘要而非完整對話
    summary_memory = ConversationSummaryMemory(llm=llm)
    summary_conversation = ConversationChain(
        llm=llm,
        memory=summary_memory,
        verbose=True
    )
    
    print(summary_conversation.predict(input="你好，我是一名大學生，正在學習計算機科學。"))
    print(summary_conversation.predict(input="我對人工智能特別感興趣。"))
    print(summary_conversation.predict(input="你能推薦一些入門資源嗎？"))
    
    # 查看摘要
    print("\n對話摘要:")
    print(summary_memory.moving_summary_buffer)
    
    print("\n===== 使用 LCEL 構建帶記憶的鏈 =====")
    # 使用 LCEL 構建具有記憶功能的應用
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.messages import HumanMessage, AIMessage
    
    memory_dict = {"history": []}
    
    # 定義提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一個有幫助的助手。"),
        ("placeholder", "{history}"),
        ("human", "{input}")
    ])
    
    # 定義鏈
    chain = prompt | llm | StrOutputParser()
    
    # 構建記憶功能
    def invoke_with_memory(user_input):
        # 格式化歷史記錄
        formatted_history = []
        for message in memory_dict["history"]:
            if message["type"] == "human":
                formatted_history.append(HumanMessage(content=message["content"]))
            else:
                formatted_history.append(AIMessage(content=message["content"]))
        
        # 生成回應
        response = chain.invoke({
            "history": formatted_history,
            "input": user_input
        })
        
        # 更新記憶
        memory_dict["history"].append({"type": "human", "content": user_input})
        memory_dict["history"].append({"type": "ai", "content": response})
        
        return response
    
    print("\nLCEL自定義記憶對話:")
    print("回應:", invoke_with_memory("我的名字是張三，我今年25歲。"))
    print("回應:", invoke_with_memory("我叫什麼名字？我多大了？"))
    
    # 查看記憶內容
    print("\n記憶內容:")
    for message in memory_dict["history"]:
        print(f"{message['type']}: {message['content']}")

if __name__ == "__main__":
    main()
