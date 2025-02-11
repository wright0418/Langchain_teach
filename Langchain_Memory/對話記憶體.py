from langchain_ollama.llms import OllamaLLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# 初始化 LLM
llm = OllamaLLM(model="qwen2.5:0.5b", temperature=0.7)

# 建立記憶體元件
memory = ConversationBufferMemory()

# 建立 ConversationChain，並傳入記憶體
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # 顯示對話過程
)

# 進行對話
print(conversation.predict(input="你好！"))
print(conversation.predict(input="我名字是小明。"))
print(conversation.predict(input="你還記得我的名字嗎？"))

# 顯示目前的記憶體內容（除錯用）
print(memory.load_memory_variables({}))