# 第八課：基礎物件導向程式設計 (OOP)

# 引入所需模組
from random import choice, randint

# 定義玩家類別
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.defense = 10
        self.gold = 50
        self.exp = 0
        self.level = 1
        self.inventory = []

    def show_stats(self):
        """顯示玩家統計數據"""
        print(f"\n=== {self.name} 的統計數據 ===")
        print(f"等級: {self.level}")
        print(f"生命值: {self.health}/{self.max_health}")
        print(f"攻擊力: {self.attack}")
        print(f"防禦力: {self.defense}")
        print(f"金幣: {self.gold}")
        print(f"經驗值: {self.exp}")
        
    def gain_exp(self, amount):
        """獲得經驗並檢查升級"""
        self.exp += amount
        print(f"獲得 {amount} 經驗值！")
        
        # 檢查是否升級
        if self.exp >= self.level * 20:
            self.level_up()
    
    def level_up(self):
        """升級玩家"""
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.attack += 3
        self.defense += 2
        print(f"\n升級了！你現在是 {self.level} 級！")
        
    def gain_gold(self, amount):
        """獲得金幣"""
        self.gold += amount
        print(f"獲得 {amount} 金幣！")
        
    def take_damage(self, amount):
        """受到傷害"""
        actual_damage = max(1, amount - self.defense // 2)
        self.health -= actual_damage
        print(f"{self.name} 受到 {actual_damage} 點傷害！")
        return self.health > 0
        
    def rest(self):
        """休息恢復生命值"""
        heal_amount = self.max_health // 4
        old_health = self.health
        self.health = min(self.max_health, self.health + heal_amount)
        print(f"你休息了一會兒，恢復了 {self.health - old_health} 點生命值。")

# 定義敵人類別
class Enemy:
    def __init__(self, name, health, attack, defense, exp_reward, gold_reward):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
    
    def show_stats(self):
        """顯示敵人統計數據"""
        print(f"\n=== {self.name} 統計數據 ===")
        print(f"生命值: {self.health}")
        print(f"攻擊力: {self.attack}")
        print(f"防禦力: {self.defense}")
        
    def take_damage(self, amount):
        """敵人受到傷害"""
        actual_damage = max(1, amount - self.defense // 2)
        self.health -= actual_damage
        print(f"{self.name} 受到 {actual_damage} 點傷害！")
        return self.health > 0

# 戰鬥系統
def battle(player, enemy):
    """玩家和敵人之間的戰鬥"""
    print(f"\n你遇到了 {enemy.name}!")
    
    while enemy.health > 0 and player.health > 0:
        player.show_stats()
        enemy.show_stats()
        
        print("\n選擇行動:")
        print("1. 攻擊")
        print("2. 逃跑")
        
        choice = input("你的選擇: ")
        
        if choice == "1":  # 攻擊
            # 玩家攻擊敵人
            enemy.take_damage(player.attack)
            
            # 敵人反擊（如果還活著）
            if enemy.health > 0:
                player.take_damage(enemy.attack)
        
        elif choice == "2":  # 逃跑
            if randint(1, 10) > 4:  # 60% 的逃跑成功率
                print("你成功逃脫了！")
                return False
            else:
                print("你逃跑失敗！")
                player.take_damage(enemy.attack)
        
        else:
            print("無效的選擇！")
    
    # 戰鬥結束
    if enemy.health <= 0:
        print(f"你擊敗了 {enemy.name}！")
        player.gain_exp(enemy.exp_reward)
        player.gain_gold(enemy.gold_reward)
        return True
    
    return False

# 主要遊戲迴圈
def main():
    print("=== 歡迎來到 MAD 遊戲 - OOP 版本 ===")
    
    # 創建玩家
    player_name = input("輸入你的角色名稱: ")
    player = Player(player_name)
    
    # 預定義敵人
    enemies = [
        Enemy("哥布林", 30, 8, 3, 10, 5),
        Enemy("獸人", 50, 12, 5, 20, 12),
        Enemy("巨魔", 80, 15, 8, 35, 25)
    ]
    
    # 遊戲主循環
    game_running = True
    while game_running and player.health > 0:
        # 顯示玩家狀態
        player.show_stats()
        
        print("\n選擇行動:")
        print("1. 探索 (可能遇到敵人)")
        print("2. 休息 (恢復生命值)")
        print("3. 離開遊戲")
        
        action = input("你的選擇: ")
        
        if action == "1":  # 探索
            enemy = choice(enemies)
            # 創建敵人的副本以避免修改原始敵人
            current_enemy = Enemy(
                enemy.name, 
                enemy.health, 
                enemy.attack, 
                enemy.defense, 
                enemy.exp_reward, 
                enemy.gold_reward
            )
            battle(player, current_enemy)
        
        elif action == "2":  # 休息
            player.rest()
        
        elif action == "3":  # 離開
            game_running = False
            print("遊戲結束，謝謝遊玩！")
        
        else:
            print("無效的選擇！")
    
    # 玩家死亡
    if player.health <= 0:
        print("你被打敗了！遊戲結束。")

# 執行遊戲
if __name__ == "__main__":
    main()
