# 課程 03：函式 & 遊戲動作

# 使用前面課程的概念
player_name = input("請輸入你的角色名稱：")
player_health = 100
player_gold = 50
player_exp = 0

# 定義遊戲動作的函式
def display_stats():
    """顯示當前玩家統計資料"""
    print(f"\n=== {player_name} 的狀態 ===")
    print(f"生命值：{player_health}")
    print(f"金幣：{player_gold}")
    print(f"經驗值：{player_exp}")

def encounter_enemy(enemy_name, enemy_power):
    """處理敵人遭遇"""
    global player_health, player_exp
    
    print(f"\n一隻 {enemy_name} 出現了！")
    print("1：戰鬥")
    print("2：逃跑")
    action = input("請輸入你的選擇 (1-2)：")
    
    if action == "1":
        damage_taken = enemy_power // 2
        exp_gained = enemy_power
        
        print(f"你與 {enemy_name} 戰鬥了！")
        print(f"你受到了 {damage_taken} 點傷害")
        print(f"你獲得了 {exp_gained} 點經驗值")
        
        player_health -= damage_taken
        player_exp += exp_gained
        
        return True
    else:
        print(f"你從 {enemy_name} 面前逃走了！")
        return False

def find_treasure(gold_amount):
    """處理寶藏發現"""
    global player_gold
    
    print(f"\n你找到了一個寶箱！")
    print(f"你獲得了 {gold_amount} 金幣")
    
    player_gold += gold_amount

def is_game_over():
    """檢查遊戲是否結束"""
    return player_health <= 0

# 主遊戲迴圈
print("=== 歡迎來到 MAD 遊戲 ===")
print(f"歡迎，{player_name}！你的冒險開始了...\n")

# 使用前一課的迴圈
for level in range(1, 4):
    print(f"\n=== 第 {level} 關 ===")
    
    # 使用我們的函式
    display_stats()
    
    # 敵人遭遇，難度逐漸增加
    enemy_power = level * 10
    victory = encounter_enemy(f"第 {level} 關怪物", enemy_power)
    
    if victory:
        # 勝利後尋找寶藏
        find_treasure(level * 15)
    
    # 檢查遊戲結束條件
    if is_game_over():
        print("\n你已被擊敗！遊戲結束。")
        break

# 最終狀態
if not is_game_over():
    print("\n恭喜！你完成了所有關卡！")
    display_stats()
