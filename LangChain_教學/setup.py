import os
import subprocess
import sys
from pathlib import Path

def create_venv():
    """創建並啟動虛擬環境"""
    venv_name = "langchain_course"
    
    print(f"建立虛擬環境 '{venv_name}'...")
    subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
    
    # 根據作業系統決定激活指令
    if sys.platform == "win32":
        activate_script = os.path.join(venv_name, "Scripts", "activate")
        pip_path = os.path.join(venv_name, "Scripts", "pip")
    else:
        activate_script = os.path.join(venv_name, "bin", "activate")
        pip_path = os.path.join(venv_name, "bin", "pip")
    
    print(f"請執行以下指令來啟動虛擬環境：")
    if sys.platform == "win32":
        print(f"{activate_script}")
    else:
        print(f"source {activate_script}")
    
    return pip_path

def install_packages(pip_path):
    """安裝必要的套件"""
    packages = [
        "langchain>=0.2.0",
        "langchain-community",
        "langchain-core",
        "langsmith",
        "python-dotenv",
        "requests",
    ]
    
    print("\n安裝必要的套件...")
    for package in packages:
        print(f"安裝 {package}...")
        subprocess.run([pip_path, "install", package], check=True)

def create_project_structure():
    """創建專案結構"""
    dirs = ["examples", "applications"]
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    
    # 創建 .env 文件
    with open(".env", "w") as f:
        f.write("# Ollama 設定\n")
        f.write("OLLAMA_BASE_URL=http://localhost:11434\n")
        f.write("DEFAULT_MODEL=llama2\n")
    
    print("\n專案結構已創建！")

def main():
    print("===== LangChain 2.0 與 Ollama 課程環境設置 =====")
    try:
        pip_path = create_venv()
        # 提示用戶先啟動虛擬環境
        print("\n請先啟動虛擬環境，然後再運行此腳本繼續安裝套件。")
        input("啟動後，按 Enter 繼續...")
        
        install_packages(pip_path)
        create_project_structure()
        
        print("\n===== 設置完成！=====")
        print("您現在可以開始課程了。")
    except Exception as e:
        print(f"設置過程中發生錯誤: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
