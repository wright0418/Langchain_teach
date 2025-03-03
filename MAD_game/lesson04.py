# 第四課：遊戲數據的列表和字典

from random import choice, randint

# 使用字典初始化玩家
player = {
    "name": input("輸入你的角色名稱: "),
    "health": 100,
    "max_health": 100,
    "attack": 15,
    "defense": 10,
    "gold": 50,
    "exp": 0,
    "level": 1,
    "inventory": []  # 空的物品列表
}

# 可能的敵人列表
enemies = [
    {"name": "哥布林", "health": 30, "attack": 8, "defense": 3, "exp": 10, "gold": 5},
    {"name": "獸人", "health": 50, "attack": 12, "defense": 5, "exp": 20, "gold": 12},
    {"name": "巨魔", "health": 80, "attack": 15, "defense": 8, "exp": 35, "gold": 25}
]

# 可能的物品列表
items = [
    {"name": "治療藥水", "type": "potion", "value": 30, "cost": 15},
    {"name": "劍", "type": "weapon", "value": 10, "cost": 50},
    {"name": "盾牌", "type": "armor", "value": 10, "cost": 40},
    {"name": "魔法卷軸", "type": "magic", "value": 20, "cost": 30}
]

# 遊戲地點字典
locations = {
    "town": {
        "name": "和平小鎮",
        "description": "一個有商店和友好市民的小鎮",
        "options": ["shop", "inn", "explore"]
    },
    "forest": {
        "name": "神秘森林",
        "description": "一個充滿危險和寶藏的黑暗森林",
        "options": ["explore", "return"]
    },
    "dungeon": {
        "name": "古老地牢",
        "description": "一個有強大敵人和寶貴戰利品的危險地牢",
        "options": ["explore", "return"]
    }
}

# 使用前一課的函數
def display_stats():
    """顯示玩家統計數據"""
    print(f"\n=== {player['name']} 的統計數據 ===")
    print(f"等級: {player['level']}")
    print(f"健康: {player['health']}/{player['max_health']}")
    print(f"攻擊: {player['attack']}")
    print(f"防禦: {player['defense']}")
    print(f"金幣: {player['gold']}")
    print(f"經驗: {player['exp']}")
    print(f"物品: {', '.join([item['name'] for item in player['inventory']]) if player['inventory'] else '空'}")

def encounter_enemy():
    """隨機遇到敵人"""
    # 選擇一個隨機敵人，但要符合玩家等級
    potential_enemies = [e for e in enemies if e["health"] <= player["level"] * 40]
    if not potential_enemies:
        potential_enemies = [enemies[0]]  # 默認為最弱的敵人
    
    enemy = choice(potential_enemies).copy()  # 複製以避免修改原始數據
    
    print(f"\n一個 {enemy['name']} 出現了!")
    
    while enemy["health"] > 0 and player["health"] > 0:
        print(f"\n{enemy['name']} 的健康: {enemy['health']}")
        print(f"你的健康: {player['health']}")
        
        print("1. 攻擊")
        print("2. 使用藥水")
        print("3. 逃跑")
        action = input("選擇你的行動: ")
        
        if action == "1":
            damage = max(1, player["attack"] - enemy["defense"] // 2)
            enemy["health"] -= damage
            print(f"你攻擊了 {enemy['name']}，造成了 {damage} 點傷害!")
            
            # 如果敵人還活著，敵人會反擊
            if enemy["health"] > 0:
                enemy_damage = max(1, enemy["attack"] - player["defense"] // 2)
                player["health"] -= enemy_damage
                print(f"{enemy['name']} 攻擊了你，造成了 {enemy_damage} 點傷害!")
        
        elif action == "2":
            potions = [item for item in player["inventory"] if item["type"] == "potion"]
            if potions:
                potion = potions[0]  # 使用第一個藥水
                player["health"] = min(player["max_health"], player["health"] + potion["value"])
                player["inventory"].remove(potion)
                print(f"你使用了一個 {potion['name']}，恢復了 {potion['value']} 點健康!")
            else:
                print("你沒有任何藥水!")
        
        elif action == "3":
            if randint(1, 10) > 3:  # 70% 的機會逃跑
                print("你成功逃跑了!")
                return
            else:
                print("你無法逃跑!")
                enemy_damage = enemy["attack"] - player["defense"] // 2
                player["health"] -= enemy_damage
                print(f"{enemy['name']} 攻擊了你，造成了 {enemy_damage} 點傷害!")
        else:
            print("無效的選擇!")
    
    if player["health"] > 0:
        print(f"你擊敗了 {enemy['name']}!")
        player["exp"] += enemy["exp"]
        player["gold"] += enemy["gold"]
        print(f"你獲得了 {enemy['exp']} 點經驗和 {enemy['gold']} 金幣!")
        
        # 檢查玩家是否升級
        if player["exp"] >= player["level"] * 20:
            player["level"] += 1
            player["max_health"] += 10
            player["health"] = player["max_health"]
            player["attack"] += 3
            player["defense"] += 2
            print(f"\n升級了! 你現在是 {player['level']} 級!")

# 使用 current_location 的簡單遊戲循環
current_location = "town"

print("=== 歡迎來到 MAD 遊戲 ===")
print(f"歡迎, {player['name']}! 你的冒險開始了...\n")

game_running = True
while game_running and player["health"] > 0:
    location = locations[current_location]
    
    print(f"\n=== {location['name']} ===")
    print(location["description"])
    print(f"選項: {', '.join(location['options'])}")
    
    display_stats()
    
    print("\n1. 探索")
    if "shop" in location["options"]:
        print("2. 商店")
    if "inn" in location["options"]:
        print("3. 旅館")
    if current_location != "town":
        print("4. 返回")
    print("5. 退出")
    
    action = input("選擇你的行動: ")
    
    if action == "1":
        print("你探索了這個地區...")
        if current_location != "town":
            if randint(1, 10) > 5:  # 50% 的機會遇到敵人
                encounter_enemy()
            else:
                # 找到一個隨機物品
                found_item = choice(items).copy()
                print(f"你找到了一個 {found_item['name']}!")
                player["inventory"].append(found_item)
    elif action == "2" and "shop" in location["options"]:
        print("\n=== 商店 ===")
        print("歡迎來到商店! 你想買什麼?")
        for i, item in enumerate(items):
            print(f"{i+1}. {item['name']} - {item['cost']} 金幣")
        
        choice = input("輸入物品編號 (或 'exit'): ")
        if choice.isdigit() and 0 < int(choice) <= len(items):
            item_index = int(choice) - 1
            item = items[item_index].copy()
            
            if player["gold"] >= item["cost"]:
                player["gold"] -= item["cost"]
                player["inventory"].append(item)
                print(f"你買了 {item['name']}，花費了 {item['cost']} 金幣!")
            else:
                print("金幣不足!")
    elif action == "3" and "inn" in location["options"]:
        print("你在旅館休息了一晚，恢復了所有健康。")
        player["health"] = player["max_health"]
    elif action == "4" and current_location != "town":
        current_location = "town"
    elif action == "5":
        game_running = False
    else:
        print("無效的選擇!")

if player["health"] <= 0:
    print("\n你被擊敗了! 遊戲結束.")
else:
    print("\n感謝你玩 MAD 遊戲!")
