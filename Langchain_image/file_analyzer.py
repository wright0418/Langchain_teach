import os
import magic
import PyPDF2
import docx
import PIL.Image
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def detect_file_type(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    return file_type

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_pdf_file(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def read_docx_file(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def analyze_image(file_path):
    image = PIL.Image.open(file_path)
    return f"Image format: {image.format}\nSize: {image.size}\nMode: {image.mode}"

def analyze_content(content, file_type):
    # 使用 Ollama 的 mistral 模型
    llm = Ollama(model="mistral")
    
    template = """請分析以下內容，並提供詳細的分析報告：
    文件類型: {file_type}
    內容:
    {content}
    
    請提供：
    1. 文件主要內容概述
    2. 關鍵主題或要點
    3. 如果是圖片，描述圖片的基本特徵
    4. 任何特別發現或建議
    """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["content", "file_type"]
    )
    
    # 使用 LangChain 2.0 的新方式創建處理鏈
    chain = (
        {"content": RunnablePassthrough(), "file_type": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke({"content": content, "file_type": file_type})

def main():
    file_path = input("請輸入要分析的檔案路徑: ")
    
    if not os.path.exists(file_path):
        print("檔案不存在！")
        return
    
    file_type = detect_file_type(file_path)
    print(f"檔案類型: {file_type}")
    
    try:
        content = ""
        if file_type.startswith('text/'):
            content = read_text_file(file_path)
        elif file_type == 'application/pdf':
            content = read_pdf_file(file_path)
        elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            content = read_docx_file(file_path)
        elif file_type.startswith('image/'):
            content = analyze_image(file_path)
        else:
            print("不支援的檔案格式！")
            return
        
        analysis = analyze_content(content, file_type)
        print("\n分析結果:")
        print(analysis)
        
    except Exception as e:
        print(f"處理檔案時發生錯誤: {str(e)}")

if __name__ == "__main__":
    main()
