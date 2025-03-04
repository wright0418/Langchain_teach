import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

# 載入 LangChain 組件
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool

# 載入環境變數
load_dotenv()

class PersonalAssistant:
    """個人知識助手，整合了記憶、工具和個性化功能"""
    
    def __init__(self, model_name: str = None, base_url: str = None):
        # 初始化模型
        self.model_name = model_name or os.getenv("DEFAULT_MODEL", "llama2")
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = Ollama(model=self.model_name, base_url=self.base_url)
        
        # 初始化記憶
        self.memory = {"history": [], "summary": "", "user_profile": {"name": "", "interests": []}}
        self.memory_file = "chatbot_memory.json"
        self.load_memory()
        
        # 初始化工具
        self.setup_tools()
        
        # 系統提示
        self.system_prompt = """你是一位有幫助的個人助手，提供友好、準確的回應。
回答時請考慮用戶的興趣和之前的對話內容。
如果需要，可以使用可用的工具來幫助回答問題。
"""
    
    def setup_tools(self):
        """設置可用工具"""
        @tool
        def calculator(expression: str) -> str:
            """計算數學表達式"""
            try:
                return str(eval(expression))
            except Exception as e:
                return f"計算錯誤: {str(e)}"
        
        @tool
        def current_time() -> str:
            """獲取當前時間"""
            now = datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        
        @tool
        def remember(key: str, value: str = None) -> str:
            """存儲或檢索信息"""
            if value:
                self.memory.setdefault("notes", {})[key] = value
                return f"已記住: {key} = {value}"
            else:
                return self.memory.get("notes", {}).get(key, f"沒有找到關於 '{key}' 的記錄")
        
        self.tools = {
            "calculator": calculator,
            "current_time": current_time,
            "remember": remember
        }
    
    def load_memory(self):
        """從文件加載記憶"""
        try:
            if Path(self.memory_file).exists():
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
                print(f"已加載記憶，包含 {len(self.memory['history'])} 條對話記錄")
        except Exception as e:
            print(f"加載記憶失敗: {e}")
    
    def save_memory(self):
        """將記憶保存到文件"""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存記憶失敗: {e}")
    
    def update_profile(self, message: str):
        """更新用戶資料"""
        # 使用 LLM 更新用戶資料
        profile_update_prompt = f"""
        分析以下消息，提取用戶的姓名和興趣。如果找到，請以 JSON 格式返回，否則返回空 JSON。
        
        消息: {message}
        
        僅返回 JSON 格式，例如:
        {{"name": "姓名", "interests": ["興趣1", "興趣2"]}}
        """
        
        try:
            response = self.llm.invoke(profile_update_prompt)
            # 嘗試解析 JSON
            try:
                data = json.loads(response)
                if data.get("name"):
                    self.memory["user_profile"]["name"] = data["name"]
                
                if data.get("interests"):
                    for interest in data["interests"]:
                        if interest not in self.memory["user_profile"]["interests"]:
                            self.memory["user_profile"]["interests"].append(interest)
            except:
                pass  # 解析失敗則忽略
        except:
            pass  # 模型呼叫失敗則忽略
    
    def should_use_tool(self, message: str) -> Optional[Dict]:
        """決定是否使用工具以及使用哪個工具"""
        tool_select_prompt = f"""
        分析以下用戶消息，判斷是否需要使用工具以及使用哪個工具。
        
        可用工具:
        - calculator: 計算數學表達式
        - current_time: 獲取當前時間
        - remember: 存儲或檢索信息 (參數格式: "key" 或 "key:value")
        
        用戶消息: {message}
        
        只回答以下 JSON 格式:
        {{"use_tool": true/false, "tool_name": "tool_name", "tool_input": "input"}}
        """
        
        try:
            response = self.llm.invoke(tool_select_prompt)
            # 嘗試解析回應
            try:
                data = json.loads(response)
                if data.get("use_tool") is True:
                    return {
                        "tool_name": data.get("tool_name", ""),
                        "tool_input": data.get("tool_input", "")
                    }
            except:
                return None  # 解析失敗則不使用工具
        except:
            return None  # 呼叫失敗則不使用工具
        
        return None
    
    def format_history(self) -> str:
        """格式化對話歷史"""
        history = ""
        # 只使用最近的 10 條對話
        recent_history = self.memory["history"][-10:] if len(self.memory["history"]) > 10 else self.memory["history"]
        for message in recent_history:
            role = "用戶" if message["role"] == "human" else "助手"
            history += f"{role}: {message['content']}\n"
        return history
    
    def generate_response(self, message: str) -> str:
        """根據用戶輸入生成回應"""
        # 更新用戶資料
        self.update_profile(message)
        
        # 檢查是否需要使用工具
        tool_info = self.should_use_tool(message)
        tool_result = ""
        
        if tool_info:
            tool_name = tool_info["tool_name"]
            tool_input = tool_info["tool_input"]
            
            if tool_name in self.tools:
                try:
                    # 處理 remember 工具的特殊情況
                    if tool_name == "remember":
                        parts = tool_input.split(":", 1)
                        if len(parts) == 2:
                            key, value = parts
                            tool_result = self.tools[tool_name](key, value)
                        else:
                            tool_result = self.tools[tool_name](tool_input)
                    else:
                        # 執行其他工具
                        tool_result = self.tools[tool_name](tool_input)
                    
                    print(f"使用工具 '{tool_name}'，結果: {tool_result}")
                except Exception as e:
                    tool_result = f"工具執行錯誤: {str(e)}"
        
        # 構建提示
        user_name = self.memory["user_profile"]["name"] or "用戶"
        interests = ", ".join(self.memory["user_profile"]["interests"]) or "未知"
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("system", f"""
            用戶資料:
            - 名稱: {user_name}
            - 興趣: {interests}
            
            對話歷史:
            {self.format_history()}
            
            {f"工具結果: {tool_result}" if tool_result else ""}
            """),
            ("human", message)
        ])
        
        # 生成回應
        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke({})
        
        # 更新記憶
        self.memory["history"].append({"role": "human", "content": message})
        self.memory["history"].append({"role": "ai", "content": response})
        
        # 如果對話記錄太長，進行摘要並清理
        if len(self.memory["history"]) > 100:
            self._summarize_history()
        
        # 保存記憶
        self.save_memory()
        
        return response
    
    def _summarize_history(self):
        """摘要並清理歷史記錄"""
        try:
            # 創建摘要
            history_text = "\n".join([f"{m['role']}: {m['content']}" for m in self.memory["history"]])
            summary_prompt = f"""
            請總結以下對話的關鍵點和重要信息:
            
            {history_text}
            
            請提供簡潔的摘要，包含關鍵事實和信息。
            """
            
            summary = self.llm.invoke(summary_prompt)
            self.memory["summary"] = summary
            
            # 保留最新的 20 條記錄
            self.memory["history"] = self.memory["history"][-20:]
        except Exception as e:
            print(f"摘要創建失敗: {e}")
    
    def chat(self):
        """互動式聊天界面"""
        print(f"歡迎使用個人知識助手！(使用 '{self.model_name}' 模型)")
        print("輸入 'exit' 或 'quit' 結束對話")
        
        while True:
            try:
                user_input = input("\n你: ")
                if user_input.lower() in ["exit", "quit"]:
                    break
                
                response = self.generate_response(user_input)
                print(f"\n助手: {response}")
            
            except KeyboardInterrupt:
                print("\n再見！")
                break
            except Exception as e:
                print(f"\n出錯了: {e}")

def main():
    parser = argparse.ArgumentParser(description="個人知識助手")
    parser.add_argument("--model", help="使用的 Ollama 模型名稱")
    parser.add_argument("--url", help="Ollama API URL")
    args = parser.parse_args()
    
    assistant = PersonalAssistant(model_name=args.model, base_url=args.url)
    assistant.chat()

if __name__ == "__main__":
    main()
