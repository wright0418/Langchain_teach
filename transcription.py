import sys
import openai

# 設定 OpenAI API 金鑰
openai.api_key = "YOUR_OPENAI_API_KEY"  # 請替換成你的 API 金鑰

def remove_fillers(text):
    # 定義需要移除的口語贅詞清單，可根據需求調整
    fillers = ["嗯", "啊", "喔", "所以說", "然後", "其實", "就是", "那個"]
    for filler in fillers:
        text = text.replace(filler, "")
    return text

def transcribe_audio(file_path):
    import subprocess
    # 使用 local ollama 模型進行轉錄，請確認 ollama 模型與命令正確
    command = ["ollama", "run", "whisper", file_path]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python transcription.py <audio_file_path>")
        sys.exit(1)
    
    audio_file_path = sys.argv[1]
    print("正在轉錄中，請稍候...")
    raw_text = transcribe_audio(audio_file_path)
    processed_text = remove_fillers(raw_text)
    print("轉錄結果：")
    print(processed_text)
