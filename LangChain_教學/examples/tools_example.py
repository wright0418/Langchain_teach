import os
import re
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# 載入環境變數
load_dotenv()

def main():
    # 初始化 Ollama LLM
    model_name = os.getenv("DEFAULT_MODEL", "llama2")
    llm = Ollama(model=model_name, base_url=os.getenv("OLLAMA_BASE_URL"))
    
    print("\n===== 基本工具示例 =====")
    # 基本工具定義
    @tool
    def calculator(expression: str) -> str:
        """計算數學表達式的結果。"""
        try:
            return str(eval(expression))
        except Exception as e:
            return f"計算錯誤: {str(e)}"
    
    @tool
    def search(query: str) -> str:
        """搜索網絡以獲取有關特定主題的信息。"""
        # 模擬搜索功能
        return f"這是關於'{query}'的搜索結果: 模擬搜索數據..."
    
    @tool
    def date_time() -> str:
        """返回當前日期和時間。"""
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    
    # 測試基本工具
    print("計算工具結果:", calculator("23 * 7 + 15"))
    print("日期時間工具:", date_time())
    
    print("\n===== 手動工具選擇 =====")
    # 為 Ollama 模型實現手動工具選擇
    class ToolSelection(BaseModel):
        tool_name: str = Field(description="要使用的工具名稱 (calculator, search, date_time)")
        tool_input: str = Field(description="要傳入工具的參數")
    
    # 創建解析器
    parser = PydanticOutputParser(pydantic_object=ToolSelection)
    
    # 創建工具選擇提示
    tool_prompt = PromptTemplate.from_template("""
    你需要選擇最合適的工具來回答用戶的問題。
    
    可用工具:
    - calculator: 計算數學表達式的結果
    - search: 搜索網絡以獲取信息
    - date_time: 返回當前日期和時間
    
    用戶問題: {question}
    
    {format_instructions}
    """)
    
    # 工具選擇鏈
    def select_and_use_tool(question):
        try:
            # 格式化工具選擇提示
            formatted_prompt = tool_prompt.format(
                question=question,
                format_instructions=parser.get_format_instructions()
            )
            
            # 獲取 LLM 回應
            llm_response = llm.invoke(formatted_prompt)
            
            # 嘗試解析回應
            try:
                tool_selection = parser.parse(llm_response)
                tool_name = tool_selection.tool_name
                tool_input = tool_selection.tool_input
            except Exception:
                # 如果解析失敗，使用正則表達式提取
                print("解析器失敗，嘗試使用正則表達式提取...")
                tool_name_match = re.search(r"tool_name[\"']?\s*[:=]\s*[\"']?(\w+)[\"']?", llm_response)
                tool_input_match = re.search(r"tool_input[\"']?\s*[:=]\s*[\"']?(.+?)[\"']?(?:\n|$)", llm_response)
                
                tool_name = tool_name_match.group(1) if tool_name_match else "search"
                tool_input = tool_input_match.group(1) if tool_input_match else question
            
            print(f"選擇工具: {tool_name}")
            print(f"工具參數: {tool_input}")
            
            # 執行選定的工具
            if tool_name == "calculator":
                result = calculator(tool_input)
            elif tool_name == "date_time":
                result = date_time()
            else:  # 默認使用搜索
                result = search(tool_input)
                
            # 生成最終回應
            final_prompt = f"""
            用戶問題: {question}
            
            工具結果: {result}
            
            請基於上述工具結果提供完整回答。
            """
            
            return llm.invoke(final_prompt)
        
        except Exception as e:
            # 如果處理出錯，直接使用 LLM 回答
            print(f"處理工具時出錯: {e}")
            return llm.invoke(f"請回答以下問題: {question}")
    
    # 測試工具選擇函數
    test_questions = [
        "計算 125 除以 8 的結果是多少？",
        "現在是什麼時間？",
        "Python 是什麼編程語言？",
    ]
    
    for q in test_questions:
        print(f"\n問題: {q}")
        print(f"回答: {select_and_use_tool(q)}")
    
    print("\n===== 自定義複雜工具 =====")
    # 創建一個對話摘要工具
    @tool
    def summarize_conversation(conversation: str) -> str:
        """對對話內容進行摘要。"""
        summary_prompt = f"""
        請對以下對話進行摘要，提取關鍵點:
        
        {conversation}
        
        摘要:
        """
        return llm.invoke(summary_prompt)
    
    # 創建文本分類工具
    @tool
    def classify_text(text: str) -> str:
        """將文本分類為不同的類別 (例如：問題、陳述、請求等)。"""
        classify_prompt = f"""
        請將以下文本分類為以下類別之一：問題、陳述、請求、意見、其他
        
        文本: {text}
        
        分類結果:
        """
        return llm.invoke(classify_prompt)
    
    # 測試自定義工具
    conversation_sample = """
    用戶: 你好，我想了解一下如何使用 Python 處理 CSV 文件？
    助手: 你可以使用 Python 的 csv 模塊，它提供了讀取和寫入 CSV 文件的功能。
    用戶: 有沒有簡單的例子可以參考？
    助手: 當然，這裡有一個讀取 CSV 文件的例子：
    import csv
    with open('file.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
    用戶: 謝謝，這很有幫助！我待會試試看。
    """
    
    print("\n對話摘要工具測試:")
    print(summarize_conversation(conversation_sample))
    
    print("\n文本分類工具測試:")
    print(classify_text("你能告訴我明天的天氣嗎？"))
    print(classify_text("我認為這個解決方案不夠好。"))
    
    print("\n===== 工具組合使用 =====")
    # 串聯多個工具
    def process_user_query(query):
        # 第一步: 分類查詢
        category = classify_text(query).strip()
        print(f"查詢分類: {category}")
        
        # 第二步: 基於分類選擇處理方式
        if "問題" in category and ("計算" in query or re.search(r"[\d\+\-\*\/\(\)]+", query)):
            # 提取數學表達式
            expression_prompt = f"從以下文本中提取數學表達式，僅返回表達式本身: '{query}'"
            expression = llm.invoke(expression_prompt).strip()
            print(f"提取的表達式: {expression}")
            
            # 計算結果
            calc_result = calculator(expression)
            print(f"計算結果: {calc_result}")
            
            # 格式化答案
            answer_prompt = f"""
            用戶問題: {query}
            計算結果: {calc_result}
            
            請使用計算結果提供友好的回答。
            """
            return llm.invoke(answer_prompt)
        
        elif "時間" in query.lower() or "日期" in query.lower():
            current_time = date_time()
            return f"現在的時間是 {current_time}"
        
        else:
            # 默認使用搜索
            search_result = search(query)
            
            # 格式化答案
            answer_prompt = f"""
            用戶查詢: {query}
            搜索結果: {search_result}
            
            基於搜索結果提供詳細回答。
            """
            return llm.invoke(answer_prompt)
    
    # 測試工具組合
    combo_questions = [
        "計算 (345 + 678) / 3 的結果",
        "現在是幾點?",
        "解釋量子計算的基本原理"
    ]
    
    for q in combo_questions:
        print(f"\n組合處理問題: {q}")
        print(f"回答: {process_user_query(q)}")

if __name__ == "__main__":
    main()
