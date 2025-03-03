# 課程 02：控制結構 & 遊戲決策

# 使用上一課的概念
player_name = input("請輸入你的角色名稱：")
player_health = 100
player_gold = 50

print(f"\n歡迎，{player_name}！")
print(f"生命值：{player_health} | 金幣：{player_gold}")

# 遊戲選擇的條件陳述式
print("\n=== 你遇到了岔路 ===")
print("1：走暗黑森林的路")
print("2：走山間小徑")

choice = input("請輸入你的選擇 (1-2)：")

# If-else 結構
if choice == "1":
    print("\n你進入了暗黑森林...")
    print("你找到了一瓶治療藥水 (+20 生命值)")
    player_health += 20
    print(f"你的生命值現在是 {player_health}")
elif choice == "2":
    print("\n你攀爬山間小徑...")
    print("你找到了一袋金幣 (+15 金幣)")
    player_gold += 15
    print(f"你的金幣現在是 {player_gold}")
else:
    print("\n無效的選擇！你踉蹌了一下，失去了 10 點生命值")
    player_health -= 10
    print(f"你的生命值現在是 {player_health}")

# 迴圈處理多次遭遇
encounters = 3
for i in range(encounters):
    print(f"\n=== 遭遇 {i+1} ===")
    print("一隻野獸出現了！")
    
    print("1：戰鬥")
    print("2：逃跑")
    action = input("請輸入你的選擇 (1-2)：")
    
    if action == "1":
        damage = 10 * (i + 1)
        player_health -= damage
        print(f"你戰鬥了，損失了 {damage} 點生命值！")
    else:
        print("你安全地逃走了！")
    
    # 檢查玩家狀態
    if player_health <= 0:
        print("\n遊戲結束！你已經被擊敗...")
        break
else:
    print("\n你成功地度過了所有的遭遇！")
    print(f"最終狀態：生命值 = {player_health}，金幣 = {player_gold}")
