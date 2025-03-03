# 第七課：任務和獎勵

from random import choice

# 使用前一課的玩家數據結構
player = {
    "name": input("輸入你的角色名稱: "),
    "health": 100,
    "attack": 15,
    "defense": 10,
    "gold": 50,
    "exp": 0
}

# 任務列表
quests = [
    {"name": "消滅哥布林", "description": "消滅10隻哥布林", "reward": {"exp": 50, "gold": 20}},
    {"name": "收集藥草", "description": "收集5個藥草", "reward": {"exp": 30, "gold": 10}},
    {"name": "護送商人", "description": "護送商人到下一個城鎮", "reward": {"exp": 70, "gold": 50}}
]

# 顯示玩家統計數據的函數
def show_player_stats():
    print(f"角色名稱: {player['name']}")
    print(f"生命值: {player['health']}")
    print(f"攻擊力: {player['attack']}")
    print(f"防禦力: {player['defense']}")
    print(f"金幣: {player['gold']}")
    print(f"經驗值: {player['exp']}")

# 任務系統
def show_quests():
    print("可用任務:")
    for i, quest in enumerate(quests):
        print(f"{i + 1}. {quest['name']}: {quest['description']} (獎勵: 經驗值 {quest['reward']['exp']}, 金幣 {quest['reward']['gold']})")

def complete_quest(quest_index):
    if 0 <= quest_index < len(quests):
        quest = quests[quest_index]
        player['exp'] += quest['reward']['exp']
        player['gold'] += quest['reward']['gold']
        print(f"你完成了任務: {quest['name']}!")
        print(f"獲得獎勵: 經驗值 {quest['reward']['exp']}, 金幣 {quest['reward']['gold']}")
    else:
        print("無效的任務索引。")

# 主遊戲循環
def main_game():
    while True:
        show_player_stats()
        action = input("選擇行動: 1) 探索 2) 休息 3) 查看任務 4) 離開遊戲: ")
        if action == "1":
            enemy = choice(enemies)
            battle(enemy)
        elif action == "2":
            player["health"] = 100
            print("你休息了一會兒，生命值已恢復。")
        elif action == "3":
            show_quests()
            quest_index = int(input("選擇要完成的任務編號: ")) - 1
            complete_quest(quest_index)
        elif action == "4":
            print("遊戲結束，謝謝遊玩!")
            break

if __name__ == "__main__":
    main_game()
