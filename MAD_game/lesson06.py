# 第六課：進階戰鬥機制

from random import choice, randint

# 使用前一課的玩家數據結構
player = {
    "name": input("輸入你的角色名稱: "),
    "health": 100,
    "attack": 15,
    "defense": 10,
    "gold": 50,
    "exp": 0
}

# 可能的敵人列表
enemies = [
    {"name": "哥布林", "health": 30, "attack": 8, "defense": 3, "exp": 10, "gold": 5},
    {"name": "獸人", "health": 50, "attack": 12, "defense": 5, "exp": 20, "gold": 12},
    {"name": "巨魔", "health": 80, "attack": 15, "defense": 8, "exp": 35, "gold": 25}
]

# 顯示玩家統計數據的函數
def show_player_stats():
    print(f"角色名稱: {player['name']}")
    print(f"生命值: {player['health']}")
    print(f"攻擊力: {player['attack']}")
    print(f"防禦力: {player['defense']}")
    print(f"金幣: {player['gold']}")
    print(f"經驗值: {player['exp']}")

# 顯示敵人統計數據的函數
def show_enemy_stats(enemy):
    print(f"敵人名稱: {enemy['name']}")
    print(f"生命值: {enemy['health']}")
    print(f"攻擊力: {enemy['attack']}")
    print(f"防禦力: {enemy['defense']}")

# 戰鬥函數
def battle(enemy):
    print(f"你遇到了 {enemy['name']}!")
    show_player_stats()
    show_enemy_stats(enemy)
    while enemy["health"] > 0 and player["health"] > 0:
        action = input("選擇行動: 1) 攻擊 2) 逃跑: ")
        if action == "1":
            damage = player["attack"] - enemy["defense"]
            enemy["health"] -= damage
            print(f"你對 {enemy['name']} 造成了 {damage} 點傷害。")
        elif action == "2":
            print("你逃跑了!")
            break
        if enemy["health"] > 0:
            enemy_damage = enemy["attack"] - player["defense"]
            player["health"] -= enemy_damage
            print(f"{enemy['name']} 對你造成了 {enemy_damage} 點傷害。")
        show_player_stats()
        show_enemy_stats(enemy)
    if player["health"] > 0 and enemy["health"] <= 0:
        print(f"你擊敗了 {enemy['name']}!")
        player["exp"] += enemy["exp"]
        player["gold"] += enemy["gold"]
    elif player["health"] <= 0:
        print("你被擊敗了...")

# 主遊戲循環
def main_game():
    while True:
        show_player_stats()
        action = input("選擇行動: 1) 探索 2) 休息 3) 離開遊戲: ")
        if action == "1":
            enemy = choice(enemies)
            battle(enemy)
        elif action == "2":
            player["health"] = 100
            print("你休息了一會兒，生命值已恢復。")
        elif action == "3":
            print("遊戲結束，謝謝遊玩!")
            break

if __name__ == "__main__":
    main_game()
