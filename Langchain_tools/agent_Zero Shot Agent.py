
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import LLMMathChain
from langchain.agents import Tool
from langchain.agents import AgentExecutor, create_react_agent

llm = OllamaLLM(model="ishumilin/deepseek-r1-coder-tools:1.5b", temperature=0.7)

llm_math = LLMMathChain.from_llm(llm)

template = ChatPromptTemplate.from_messages([
    ("user", "你是一个能力非凡的人工智能机器人。"),
    ("assistant", "你好~"),
    ("user", "{user_input}"),
])

llm_chain = template | llm

# initialize the math tool
math_tool = Tool(
    name='Calculator',
    func=llm_math.invoke,
    description='Useful for when you need to answer questions about math.'
)

# initialize the general LLM tool
llm_tool = Tool(
    name='Language Model',
    func=llm_chain.invoke,
    description='Use this tool for general purpose queries.'
)

# when giving tools to LLM, we must pass as list of tools
tools = [math_tool, llm_tool]

# get the prompt template string from: 
# https://smith.langchain.com/hub/hwchase17/react?organizationId=c4887cc4-1275-5361-82f2-b22aee75bad1

prompt_template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
prompt = PromptTemplate.from_template(prompt_template)

tool_names = [tool.name for tool in tools]

zero_shot_agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(agent=zero_shot_agent, tools=tools, verbose=True)

res = agent_executor.invoke({"input": "4.1*7.9 是多少?"})


# res = agent_executor.invoke({"input": "2025年美國總統是誰?"})
print(res)