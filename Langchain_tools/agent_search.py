from langchain_ollama.llms import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun

# 初始化 LLM
llm = OllamaLLM(model="qwen2.5:0.5b", temperature=0.7)

# 初始化搜尋工具
search = DuckDuckGoSearchRun()

# 建立 Agent
agent = initialize_agent(
    tools=[search],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 執行 Agent
print(agent.run("今天新竹的天氣如何？"))