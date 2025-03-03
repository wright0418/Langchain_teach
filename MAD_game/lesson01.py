# 課程 01：Python 基礎 & 遊戲介紹

# 變數和基本資料型態
player_name = "冒險者"
player_health = 100
player_is_alive = True
game_difficulty = 1.5

# 基本輸出
print("=== 歡迎來到 MAD 遊戲 ===")
print(f"玩家：{player_name}")
print(f"生命值：{player_health}")
print(f"狀態：{'存活' if player_is_alive else '已倒下'}")
print(f"難度：{game_difficulty}")

# 基本輸入
player_name = input("請輸入你的角色名稱：")
print(f"歡迎，{player_name}！你的冒險即將開始...")

# 簡單的遊戲訊息
print("\n你發現自己身處在一個充滿危險與寶藏的神秘世界。")
print("你的任務是生存下來並找到回家的路。")
