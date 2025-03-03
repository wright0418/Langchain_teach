# 第五課：遊戲存檔處理

import json
import os
from random import choice, randint

# 設置遊戲存檔目錄
saves_dir = "game_saves"
if not os.path.exists(saves_dir):
    os.makedirs(saves_dir)

# 從前一課的遊戲數據結構
player = {
    "name": "",
    "health": 100,
    "max_health": 100,
    "attack": 15,
    "defense": 10,
    "gold": 50,
    "exp": 0,
    "level": 1,
    "inventory": []
}

# 保存和加載遊戲的函數
def save_game(player_data, filename=None):
    """將遊戲數據保存到文件"""
    if filename is None:
        filename = f"{player_data['name']}_save.json"
    
    filepath = os.path.join(saves_dir, filename)
    
    try:
        with open(filepath, 'w') as file:
            json.dump(player_data, file, indent=4)
        print(f"遊戲成功保存到 {filepath}")
        return True
    except Exception as e:
        print(f"保存遊戲時出錯: {e}")
        return False

def load_game(filename=None):
    """從文件加載遊戲數據"""
    # 如果未提供文件名，列出可用的存檔
    if filename is None:
        saves = [f for f in os.listdir(saves_dir) if f.endswith('_save.json')]
        
        if not saves:
            print("未找到存檔！")
            return None
        
        print("可用的存檔：")
        for i, save in enumerate(saves):
            print(f"{i+1}. {save}")
        
        choice = input("輸入要加載的存檔編號（或輸入0取消）：")
        if not choice.isdigit() or int(choice) == 0:
            return None
        
        try:
            filename = saves[int(choice)-1]
        except (IndexError, ValueError):
            print("選擇無效！")
            return None
    
    filepath = os.path.join(saves_dir, filename)
    
    try:
        with open(filepath, 'r') as file:
            player_data = json.load(file)
        print(f"遊戲成功從 {filepath} 加載")
        return player_data
    except Exception as e:
        print(f"加載遊戲時出錯: {e}")
        return None

# 遊戲初始化函數
def initialize_game():
    """初始化新遊戲或加載已保存的遊戲"""
    print("=== 歡迎來到 MAD 遊戲 ===")
    print("1. 新遊戲")
    print("2. 加載遊戲")
    
    choice = input("輸入你的選擇：")
    
    if choice == "2":
        loaded_player = load_game()
        if loaded_player:
            return loaded_player
    
    # 新遊戲或加載失敗
    name = input("輸入你的角色名稱：")
    player["name"] = name
    return player

# 使用前幾課的函數和數據結構
def display_stats(player):
    """顯示玩家統計數據"""
    print(f"\n=== {player['name']} 的統計數據 ===")
    print(f"等級: {player['level']}")
    print(f"生命值: {player['health']}/{player['max_health']}")
    print(f"攻擊: {player['attack']}")
    print(f"防禦: {player['defense']}")
    print(f"金幣: {player['gold']}")
    print(f"經驗: {player['exp']}")
    print(f"背包: {', '.join([item['name'] for item in player['inventory']]) if player['inventory'] else '空'}")

# 簡單的遊戲循環，展示保存和加載功能
def main_game():
    """具有保存/加載功能的主要遊戲循環"""
    # 初始化遊戲
    player = initialize_game()
    
    # 簡單的遊戲循環
    game_running = True
    turn = 0
    
    while game_running and player["health"] > 0:
        turn += 1
        print(f"\n=== 第 {turn} 回合 ===")
        display_stats(player)
        
        print("\n行動：")
        print("1. 探索（獲得經驗和金幣）")
        print("2. 休息（恢復生命值）")
        print("3. 保存遊戲")
        print("4. 加載遊戲")
        print("5. 退出")
        
        action = input("你想做什麼？")
        
        if action == "1":  # 探索
            print("你探索了這個區域...")
            
            # 模擬獲得獎勵
            exp_gain = randint(5, 10) * player["level"]
            gold_gain = randint(3, 8) * player["level"]
            
            player["exp"] += exp_gain
            player["gold"] += gold_gain
            
            print(f"你獲得了 {exp_gain} 經驗和 {gold_gain} 金幣！")
            
            # 受傷的機會
            if randint(1, 10) > 6:  # 40% 受傷機會
                damage = randint(5, 15)
                player["health"] -= damage
                print(f"你遇到了一個怪物，受到了 {damage} 傷害！")
            
            # 檢查是否升級
            if player["exp"] >= player["level"] * 20:
                player["level"] += 1
                player["max_health"] += 10
                player["attack"] += 3
                player["defense"] += 2
                print(f"\n升級了！你現在是 {player['level']} 級！")
        
        elif action == "2":  # 休息
            heal_amount = player["max_health"] // 4
            player["health"] = min(player["max_health"], player["health"] + heal_amount)
            print(f"你休息了一會兒，恢復了 {heal_amount} 點生命值。")
        
        elif action == "3":  # 保存遊戲
            save_game(player)
        
        elif action == "4":  # 加載遊戲
            loaded_player = load_game()
            if loaded_player:
                player = loaded_player
                print("遊戲加載成功！")
        
        elif action == "5":  # 退出
            save_prompt = input("退出前要保存嗎？（y/n）：")
            if save_prompt.lower() == 'y':
                save_game(player)
            game_running = False
    
    if player["health"] <= 0:
        print("\n你被打敗了！遊戲結束。")
    else:
        print("\n感謝你玩 MAD 遊戲！")

# 運行遊戲
if __name__ == "__main__":
    main_game()
