# LangChain 解析器選擇指南

根據不同的使用場景，建議以下選擇準則：

## 1. CommaSeparatedListOutputParser

適用場景：

- 需要簡單的列表輸出
- 資料項目間用逗號分隔
- 不需要複雜的資料結構

```python
# 簡單列表示例
parser = CommaSeparatedListOutputParser()
prompt = """列出三種顏色：
輸出格式：紅色, 藍色, 綠色"""
```

## 2. JsonOutputParser

適用場景：

- 需要結構化的資料輸出
- 資料包含多個欄位
- 需要巢狀結構

```python
# JSON 格式示例
parser = JsonOutputParser()
prompt = """輸出使用者資料：
{
    "name": "使用者名稱",
    "skills": ["技能1", "技能2"],
    "profile": {
        "age": 25,
        "city": "台北"
    }
}"""
```

## 3. PydanticOutputParser

適用場景：

- 需要強型別檢查
- 有複雜的資料驗證需求
- 需要與其他系統整合

```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    name: str = Field(description="使用者名稱")
    age: int = Field(description="年齡", ge=0, le=150)
    skills: List[str] = Field(description="技能列表")

parser = PydanticOutputParser(pydantic_object=UserProfile)
```

## 4. BooleanOutputParser

適用場景：

- 需要是/否的答案
- 做簡單的判斷
- 需要布林值結果

```python
parser = BooleanOutputParser()
prompt = "這個答案是正確的嗎？請回答 true 或 false"
```

## 選擇建議

1. 如果只需要**簡單列表**：使用 `CommaSeparatedListOutputParser`
2. 如果需要**結構化資料**但不需驗證：使用 `JsonOutputParser`
3. 如果需要**嚴格的資料驗證**：使用 `PydanticOutputParser`
4. 如果需要**是/否答案**：使用 `BooleanOutputParser`
5. 如果需要**自定義格式**：考慮自行擴展 `BaseOutputParser`

記住：

- 選擇最簡單且符合需求的解析器
- 考慮後續維護和擴展性
- 注意錯誤處理機制
- 確保 prompt 模板清楚說明輸出格式