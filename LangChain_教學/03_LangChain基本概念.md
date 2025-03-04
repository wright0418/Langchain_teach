# 第三章：LangChain 2.0 基本概念

本章節將介紹 LangChain 2.0 的基本概念和架構，幫助您理解這個框架的設計思想。

## 3.1 LangChain 簡介

LangChain 是一個用於開發由語言模型驅動的應用程序的框架，2.0 版本對架構進行了重大改進，使其更加模組化和靈活。LangChain 提供了以下優勢：

- 標準化與語言模型的交互
- 組合多個組件形成複雜的工作流
- 提供記憶功能管理對話歷史
- 集成外部工具和資料來源

## 3.2 核心概念

### 3.2.1 語言模型 (LLMs)

LangChain 支持多種語言模型，包括：
- OpenAI 的 GPT 系列
- 本地模型（通過 Ollama 等）
- 其他開源模型

在 LangChain 2.0 中，語言模型被標準化為實現相同接口的類。

```python
from langchain_community.llms import Ollama
from langchain_core.language_models import LLM

# 初始化 Ollama LLM
llm = Ollama(model="llama2")

# 基本調用
result = llm.invoke("寫一首關於程式設計的短詩")
```

### 3.2.2 提示模板 (Prompts)

提示模板允許您使用變量創建動態提示：

```python
from langchain_core.prompts import PromptTemplate

# 創建提示模板
template = "您是一位專業的{role}。請回答以下問題：{question}"
prompt = PromptTemplate.from_template(template)

# 使用模板
formatted_prompt = prompt.format(role="數學老師", question="什麼是微積分？")
```

### 3.2.3 輸出解析器 (Output Parsers)

輸出解析器將語言模型的原始輸出轉換為特定格式：

```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()
format_instructions = parser.get_format_instructions()

prompt = PromptTemplate.from_template(
    "列出五種{subject}。{format_instructions}"
)
```

### 3.2.4 鏈 (Chains)

鏈將多個組件連接在一起，形成工作流：

```python
from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.invoke({"role": "營養師", "question": "推薦五種健康食品"})
```

### 3.2.5 記憶 (Memory)

記憶組件用於存儲和管理對話歷史：

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.chat_memory.add_user_message("你好！")
memory.chat_memory.add_ai_message("你好！有什麼我可以幫助你的嗎？")
```

## 3.3 LangChain 2.0 架構

LangChain 2.0 架構分為幾個核心模組：

1. **langchain-core**: 定義了基礎接口和抽象類
2. **langchain**: 主要的應用構建模組
3. **langchain-community**: 包含社區貢獻的各種集成

### 3.3.1 LCEL (LangChain Expression Language)

LCEL 是 LangChain 2.0 最重要的特性之一，它允許以聲明式的方式組合組件：

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("寫一篇關於{topic}的短文")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "人工智能"})
```

## 3.4 與 Ollama 集成

LangChain 提供了與 Ollama 的無縫集成，讓您可以輕鬆使用本地模型：

```python
from langchain_community.llms import Ollama

# 基本配置
llm = Ollama(
    model="llama2",
    base_url="http://localhost:11434",
)

# 模型參數調整
llm_with_params = Ollama(
    model="llama2",
    temperature=0.7,
    top_p=0.9,
    num_ctx=2048
)
```

## 下一步

在了解了 LangChain 2.0 的基本概念後，讓我們在下一章探索一些基本的使用範例。
