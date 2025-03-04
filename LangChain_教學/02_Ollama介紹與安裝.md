# 第二章：Ollama 介紹與安裝

本章節將介紹 Ollama 工具以及如何在本地運行 AI 模型。

## 2.1 Ollama 簡介

Ollama 是一個開源工具，允許您在本地運行各種大型語言模型（LLMs）。使用 Ollama，您可以：

- 在本地運行模型，保護數據隱私
- 避免 API 收費
- 根據需求自由選擇不同模型
- 在無網絡環境下使用 AI 功能

## 2.2 安裝 Ollama

### Windows 安裝

1. 訪問 [Ollama 官方網站](https://ollama.ai/download) 下載 Windows 安裝程序
2. 雙擊安裝程序並依照指示安裝
3. 安裝完成後，Ollama 會在系統託盤中運行

### macOS 安裝

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Linux 安裝

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## 2.3 拉取模型

安裝完成後，您需要拉取至少一個模型才能使用。開啟命令行，執行：

```bash
# 拉取 Llama2 模型（約 4GB）
ollama pull llama2

# 如果您的電腦資源有限，可以拉取較小的模型
ollama pull tinyllama
```

## 2.4 測試 Ollama 安裝

測試 Ollama 是否正常工作：

```bash
# 使用 Llama2 模型進行簡單的對話
ollama run llama2 "嗨，你好嗎？"
```

如果返回回應，則表示 Ollama 已成功安裝並可以使用。

## 2.5 Ollama API

Ollama 提供了簡單的 REST API，這將是我們在 LangChain 中調用模型的主要方法：

- API 端點：http://localhost:11434
- 主要接口：/api/generate 和 /api/chat

我們可以用一個簡單的 Python 腳本測試 API 連接：

```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama2",
        "prompt": "介紹一下自己",
        "stream": False
    }
)

print(response.json()["response"])
```

## 2.6 使用 Python 程式測試 Ollama

創建文件 `test_ollama.py`：

```python
import requests

def query_ollama(prompt, model="llama2"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

if __name__ == "__main__":
    result = query_ollama("用Python寫一個Hello World程式")
    print(result)
```

執行測試：

```bash
python test_ollama.py
```

## 下一步

現在您已經成功安裝了 Ollama 並拉取了模型，接下來我們將學習 LangChain 2.0 的基本概念。
