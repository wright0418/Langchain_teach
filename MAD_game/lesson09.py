# 第九課：進階物件導向程式設計 - 繼承與多型

# 引入所需模組
from random import choice, randint
from abc import ABC, abstractmethod

# 定義遊戲實體的抽象基類
class GameEntity(ABC):
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
    
    @abstractmethod
    def show_stats(self):
        """顯示統計數據（抽象方法）"""
        pass
    
    def take_damage(self, amount):
        """受到傷害"""
        actual_damage = max(1, amount - self.defense // 2)
        self.health -= actual_damage
        print(f"{self.name} 受到 {actual_damage} 點傷害！")
        return self.health > 0
    
    def is_alive(self):
        """檢查實體是否存活"""
        return self.health > 0

# 定義玩家類別（繼承自GameEntity）
class Player(GameEntity):
    def __init__(self, name):
        super().__init__(name, 100, 15, 10)
        self.gold = 50
        self.exp = 0
        self.level = 1
        self.inventory = []
        self.quests = []

    def show_stats(self):
        """顯示玩家統計數據（多型）"""
        print(f"\n=== {self.name} 的統計數據 ===")
        print(f"等級: {self.level}")
        print(f"生命值: {self.health}/{self.max_health}")
        print(f"攻擊力: {self.attack}")
        print(f"防禦力: {self.defense}")
        print(f"金幣: {self.gold}")
        print(f"經驗值: {self.exp}")
        if self.inventory:
            print("背包:")
            for item in self.inventory:
                print(f"  - {item.name}")
        
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
        
    def rest(self):
        """休息恢復生命值"""
        heal_amount = self.max_health // 4
        old_health = self.health
        self.health = min(self.max_health, self.health + heal_amount)
        print(f"你休息了一會兒，恢復了 {self.health - old_health} 點生命值。")
    
    def add_item(self, item):
        """加入物品到背包"""
        self.inventory.append(item)
        print(f"你獲得了 {item.name}！")
    
    def add_quest(self, quest):
        """接受任務"""
        self.quests.append(quest)
        print(f"你接受了任務: {quest.name}")
    
    def use_item(self, item_index):
        """使用背包中的物品"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            item.use(self)
            if item.consumable:
                self.inventory.remove(item)
        else:
            print("無效的物品索引！")

# 定義敵人類別（繼承自GameEntity）
class Enemy(GameEntity):
    def __init__(self, name, health, attack, defense, exp_reward, gold_reward):
        super().__init__(name, health, attack, defense)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
    
    def show_stats(self):
        """顯示敵人統計數據（多型）"""
        print(f"\n=== {self.name} 統計數據 ===")
        print(f"生命值: {self.health}")
        print(f"攻擊力: {self.attack}")
        print(f"防禦力: {self.defense}")

# 定義不同類型的敵人（繼承自Enemy）
class Goblin(Enemy):
    def __init__(self):
        super().__init__("哥布林", 30, 8, 3, 10, 5)

class Orc(Enemy):
    def __init__(self):
        super().__init__("獸人", 50, 12, 5, 20, 12)
    
    # 獸人特有的技能
    def rage(self):
        self.attack += 5
        print(f"{self.name} 發怒了！攻擊力增加了！")

class Troll(Enemy):
    def __init__(self):
        super().__init__("巨魔", 80, 15, 8, 35, 25)
    
    # 巨魔特有的技能
    def regenerate(self):
        heal_amount = 10
        self.health = min(self.max_health, self.health + heal_amount)
        print(f"{self.name} 恢復了 {heal_amount} 點生命值！")

# 定義物品抽象基類
class Item(ABC):
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value
        self.consumable = False
    
    @abstractmethod
    def use(self, entity):
        """使用物品的效果（抽象方法）"""
        pass

# 定義消耗品
class Consumable(Item):
    def __init__(self, name, description, value):
        super().__init__(name, description, value)
        self.consumable = True

# 定義治療藥水
class HealthPotion(Consumable):
    def __init__(self):
        super().__init__("治療藥水", "恢復生命值的藥水", 15)
    
    def use(self, entity):
        """使用藥水恢復生命值"""
        heal_amount = 30
        old_health = entity.health
        entity.health = min(entity.max_health, entity.health + heal_amount)
        print(f"{entity.name} 使用了治療藥水，恢復了 {entity.health - old_health} 點生命值！")

# 定義武器
class Weapon(Item):
    def __init__(self, name, description, value, attack_bonus):
        super().__init__(name, description, value)
        self.attack_bonus = attack_bonus
    
    def use(self, entity):
        """裝備武器"""
        entity.attack += self.attack_bonus
        print(f"{entity.name} 裝備了 {self.name}，攻擊力增加了 {self.attack_bonus} 點！")

# 定義盾牌
class Shield(Item):
    def __init__(self, name, description, value, defense_bonus):
        super().__init__(name, description, value)
        self.defense_bonus = defense_bonus
    
    def use(self, entity):
        """裝備盾牌"""
        entity.defense += self.defense_bonus
        print(f"{entity.name} 裝備了 {self.name}，防禦力增加了 {self.defense_bonus} 點！")

# 定義任務類別
class Quest:
    def __init__(self, name, description, enemy_target, count, exp_reward, gold_reward):
        self.name = name
        self.description = description
        self.enemy_target = enemy_target
        self.count = count
        self.progress = 0
        self.completed = False
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
    
    def update_progress(self, enemy_name):
        """更新任務進度"""
        if enemy_name == self.enemy_target and not self.completed:
            self.progress += 1
            print(f"任務進度更新: {self.progress}/{self.count}")
            
            if self.progress >= self.count:
                self.completed = True
                print(f"任務完成: {self.name}！")
                return True
        return False

# 戰鬥系統
def battle(player, enemy):
    """玩家和敵人之間的戰鬥"""
    print(f"\n你遇到了 {enemy.name}!")
    
    # 特殊敵人功能（多型示例）
    if isinstance(enemy, Orc) and randint(1, 10) > 7:
        enemy.rage()
    
    while enemy.is_alive() and player.is_alive():
        player.show_stats()
        enemy.show_stats()
        
        print("\n選擇行動:")
        print("1. 攻擊")
        print("2. 使用物品")
        print("3. 逃跑")
        
        user_choice = input("你的選擇: ")
        
        if user_choice == "1":  # 攻擊
            # 玩家攻擊敵人
            enemy.take_damage(player.attack)
            
            # 特殊敵人功能（多型示例）
            if isinstance(enemy, Troll) and enemy.is_alive() and randint(1, 10) > 7:
                enemy.regenerate()
            
            # 敵人反擊（如果還活著）
            if enemy.is_alive():
                player.take_damage(enemy.attack)
        
        elif user_choice == "2":  # 使用物品
            if player.inventory:
                print("\n選擇物品:")
                for i, item in enumerate(player.inventory):
                    print(f"{i+1}. {item.name} - {item.description}")
                
                try:
                    item_choice = int(input("選擇物品編號 (0 取消): "))
                    if item_choice > 0:
                        player.use_item(item_choice - 1)
                    
                    # 敵人反擊
                    if enemy.is_alive():
                        player.take_damage(enemy.attack)
                except ValueError:
                    print("請輸入有效的數字！")
            else:
                print("你的背包是空的！")
        
        elif user_choice == "3":  # 逃跑
            if randint(1, 10) > 4:  # 60% 的逃跑成功率
                print("你成功逃脫了！")
                return False
            else:
                print("你逃跑失敗！")
                player.take_damage(enemy.attack)
        
        else:
            print("無效的選擇！")
    
    # 戰鬥結束
    if not enemy.is_alive():
        print(f"你擊敗了 {enemy.name}！")
        player.gain_exp(enemy.exp_reward)
        player.gain_gold(enemy.gold_reward)
        
        # 檢查任務進度
        for quest in player.quests:
            quest.update_progress(enemy.name)
        
        # 掉落物品機率
        if randint(1, 10) > 6:  # 40% 的掉落機率
            items = [HealthPotion(), Weapon("鋒利短劍", "一把鋒利的短劍", 25, 5), Shield("木盾", "一個基本的木盾", 20, 3)]
            dropped_item = choice(items)
            player.add_item(dropped_item)
        
        return True
    
    return False

# 主要遊戲迴圈
def main():
    print("=== 歡迎來到 MAD 遊戲 - 進階 OOP 版本 ===")
    
    # 創建玩家
    player_name = input("輸入你的角色名稱: ")
    player = Player(player_name)
    
    # 預設物品
    player.inventory.append(HealthPotion())
    
    # 預設任務
    goblin_quest = Quest("哥布林狩獵", "擊敗 3 個哥布林", "哥布林", 3, 50, 30)
    orc_quest = Quest("獸人威脅", "擊敗 2 個獸人", "獸人", 2, 70, 50)
    
    # 遊戲主循環
    game_running = True
    current_location = "town"  # 起始位置
    
    while game_running and player.is_alive():
        # 顯示玩家狀態
        player.show_stats()
        
        if current_location == "town":
            print("\n=== 小鎮 ===")
            print("1. 探索森林 (遇到敵人)")
            print("2. 休息 (恢復生命值)")
            print("3. 任務板")
            print("4. 商店")
            print("5. 離開遊戲")
            
            user_choice = input("你的選擇: ")
            
            if user_choice == "1":
                current_location = "forest"
            elif user_choice == "2":
                player.rest()
            elif user_choice == "3":
                print("\n=== 任務板 ===")
                print("可用任務：")
                print(f"1. {goblin_quest.name}: {goblin_quest.description}")
                print(f"2. {orc_quest.name}: {orc_quest.description}")
                
                quest_choice = input("選擇要接受的任務 (0 取消): ")
                if quest_choice == "1" and goblin_quest not in player.quests:
                    player.add_quest(goblin_quest)
                elif quest_choice == "2" and orc_quest not in player.quests:
                    player.add_quest(orc_quest)
            elif user_choice == "4":
                print("\n=== 商店 ===")
                shop_items = [
                    HealthPotion(),
                    Weapon("鋒利短劍", "一把鋒利的短劍", 25, 5),
                    Shield("木盾", "一個基本的木盾", 20, 3)
                ]
                
                print("可購買的物品:")
                for i, item in enumerate(shop_items):
                    print(f"{i+1}. {item.name} - {item.description} (價格: {item.value} 金幣)")
                
                shop_choice = input("選擇要購買的物品 (0 取消): ")
                if shop_choice.isdigit() and int(shop_choice) > 0 and int(shop_choice) <= len(shop_items):
                    item_index = int(shop_choice) - 1
                    item = shop_items[item_index]
                    
                    if player.gold >= item.value:
                        player.gold -= item.value
                        # 創建一個新的物品實例以避免共享引用
                        if isinstance(item, HealthPotion):
                            player.add_item(HealthPotion())
                        elif isinstance(item, Weapon):
                            player.add_item(Weapon(item.name, item.description, item.value, item.attack_bonus))
                        elif isinstance(item, Shield):
                            player.add_item(Shield(item.name, item.description, item.value, item.defense_bonus))
                        
                        print(f"你購買了 {item.name}！")
                    else:
                        print("金幣不足！")
            elif user_choice == "5":
                game_running = False
                print("遊戲結束，謝謝遊玩！")
        
        elif current_location == "forest":
            print("\n=== 森林 ===")
            print("1. 深入探索 (遇到敵人)")
            print("2. 返回小鎮")
            
            user_choice = input("你的選擇: ")
            
            if user_choice == "1":
                # 隨機生成敵人
                enemy_type = randint(1, 3)
                if enemy_type == 1:
                    enemy = Goblin()
                elif enemy_type == 2:
                    enemy = Orc()
                else:
                    enemy = Troll()
                
                battle(player, enemy)
                
                # 檢查已完成的任務
                completed_quests = [q for q in player.quests if q.completed]
                for quest in completed_quests:
                    player.gain_exp(quest.exp_reward)
                    player.gain_gold(quest.gold_reward)
                    player.quests.remove(quest)
                    print(f"你完成了任務 '{quest.name}' 並獲得了 {quest.exp_reward} 經驗和 {quest.gold_reward} 金幣！")
            
            elif user_choice == "2":
                current_location = "town"
    
    # 玩家死亡或離開遊戲
    if not player.is_alive():
        print("你被打敗了！遊戲結束。")
    else:
        print("感謝遊玩！")

# 執行遊戲
if __name__ == "__main__":
    main()
