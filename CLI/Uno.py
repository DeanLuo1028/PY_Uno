# 這是 uno.py
# -*- coding: UTF-8 -*-
from typing import List
from enum import Enum, unique

@unique
class Color(Enum):
    RED = "R"
    YELLOW = "Y"
    GREEN = "G"
    BLUE = "B"
    SPECIAL = "special"

RANKS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"]


class Card:
    def __init__(self, color: Color, rank: str):
        self.color: Color = color
        self.rank: str = rank
    
    def __str__(self):
        return self.color.value + " " + self.rank + ", "
    
    # 遊戲最核心的規則！
    def has_compliance_rules(self, discard_last_card: "Card") -> bool:
        """檢查要出牌是否符合規則
    
        Args:
            discard_last_card (Card): 棄牌堆頂端的牌
        Returns:
            bool: 如果符合規則，傳回 True，否則傳回 False
        """
        return self.color == Color.SPECIAL\
            or self.color == discard_last_card.color\
            or self.rank == discard_last_card.rank


class Deck:
    """有牌組和棄牌堆"""
    # 建構函式，初始化牌組
    def __init__(self):
        self.cards: List[Card] = [] # 用於發牌、抽牌
        self.discard: List[Card] = [] # 棄牌堆
        # 4種顏色
        for c in [Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE]:
            self.cards.append(Card(c, "0")) # 添加4張0
            # 數字1~9和Skip", "Reverse", "+2"都各有兩張
            for r in RANKS:
                self.cards.append(Card(c, r))
                self.cards.append(Card(c, r))
        
        # 特殊牌: wild 和 +4 各有4張
        for _ in range(4):
            self.cards.append(Card(Color.SPECIAL, "wild"))
            self.cards.append(Card(Color.SPECIAL, "+4"))
    
    # 洗牌的方法
    def shuffle(self) -> None:
        from random import shuffle
        shuffle(self.cards)
        print("洗牌完成!")


class Player:
    """玩家"""
    def __init__(self, name: str, is_robot: bool):
        self.name: str = name
        self.is_robot: bool = is_robot
        self.hand: List[Card] = [] # 玩家手牌，初始為空列表
    
    def deal(self, cards_num: int, deck: Deck) -> None:
        """抽牌
        Args:
            cards_num (int): 抽牌數量
            deck (Deck): 牌組
        """
        for _ in range(cards_num): # 抽cards_num張牌
            if deck.cards: # 牌組中有牌
                # 從牌組中取出一張牌，將牌加入玩家手牌
                self.hand.append( card:=deck.cards.pop() )
                if not self.is_robot:
                    print(f"{self.name}抽到了{card}")
            else:
                print("牌已經沒了！")
                break # 當牌已經發完時終止循環
    
    def win(self) -> bool:
        """如果手牌數量為 0，則傳回 True，否則傳回 False"""
        if not self.hand:
            print(self.name+"獲勝了！")
            return True
        else: return False
    
    def display_hand(self) -> None:
        """顯示玩家手牌"""
        print(self.name + "的手牌:")
        for index, card in enumerate(self.hand, start=1):
            print(f"第{index}張:{card}", end=" ") #不要換行
        print() # 只是為了換行
    
    def robot_play(self, deck: Deck) -> bool:
        """機器人行動
        Args:
            deck (Deck): 牌組
        Returns:
            bool: 是否成功出牌
        """
        discard_last_card = deck.discard[-1] # 取得棄牌堆最後一張牌
        for card in self.hand:
            # 優先出非特殊牌
            if card.color != Color.SPECIAL and card.has_compliance_rules(discard_last_card):
                self.hand.remove(card) # 出手中符合規則的牌中的一張
                deck.discard.append(card) # 將這張牌放入棄牌堆
                print(f"{self.name}出了{card}")
                return True
        
        for card in self.hand:
            if card.color == Color.SPECIAL:
                self.hand.remove(card)
                deck.discard.append(card)
                print(f"{self.name}出了{card}")
                return True
        
        print(self.name+"沒牌可出，抽一張")
        self.deal(1,deck) # 抽一張牌
        return False # 沒有符合規則的牌，回傳False
    
    def human_play(self, deck: Deck) -> bool:
        """玩家行動
        Args:
            deck (Deck): 牌組
        Returns:
            bool: 是否成功出牌
        """
        discard_last_card = deck.discard[-1] # 取得棄牌堆最後一張牌
        print("以下是你的牌:")
        self.display_hand()
        
        # 循環直到用戶輸入合法的整數在指定範圍內
        while True:
            print(self.name+"請問你要出第幾張牌?(如果不想出牌，請輸入0)")
            s = input().strip()
            if s.lower() == "quit": # 用戶想要退出遊戲
                print("遊戲結束!")
                exit()
            
            if not s.isdigit():
                print("請輸入一個有效的整數！")
                continue
            
            user_input = int(s)
            # 檢查用戶輸入是否在0~牌數之間
            if user_input < 0 or user_input > len(self.hand):
                print(f"請輸入0~{len(self.hand)}之間的整數!")
                continue
            # 玩家抽牌
            if user_input == 0:
                self.deal(1, deck) # 玩家不出牌，就抽一張牌
                return False # 回傳False，表示沒有出牌
            # 玩家出牌
            else:
                card: Card = self.hand[user_input-1] # -1 是因為list是從0開始編號的
                if not card.has_compliance_rules(discard_last_card):
                    print(f"請輸入顏色為{discard_last_card.color.value}或special的牌或者點數為{discard_last_card.rank}的牌!")
                    continue
                
                self.hand.remove(card)
                deck.discard.append(card) # 將牌放入棄牌堆
                print(f"{self.name}出了{card}")
                return True # 回傳True，表示有出牌
    
    def action(self, deck: Deck) -> str:
        card: Card = deck.discard[len(deck.discard)-1]
        print("現在牌堆最上方的牌:"+str(card))
        # 玩家行動
        if self.is_robot:
            if not self.robot_play(deck):
                return "normal" # 沒出牌是普通情況，回傳normal
        else:
            if not self.human_play(deck):
                return "normal" # 沒出牌是普通情況，回傳normal
        
        if self.win():
            return "win" # 玩家獲勝，回傳win
        
        played_card: Card = deck.discard[-1] # 棄牌堆最後的牌是剛剛出的牌
        #為了將特殊情況回傳給主函數
        if played_card.color == Color.SPECIAL: # 出了特殊牌
            played_card.color = self.convert_color() # 將特殊牌的顏色轉換成玩家所選的顏色
            match played_card.rank:
                case "wild":
                    return "normal" # 換完顏色後是普通情況，回傳normal
                case "+4":
                    return "+4"
                case _:
                    raise ValueError("錯誤!程式應該不會執行到這裡")
        elif played_card.rank in ["0","1","2","3","4","5","6","7","8","9"]: # 一般數字牌
            return "normal"
        else:
            return played_card.rank # 回傳特殊牌的點數，如Skip, Reverse, +2
    
    def say_card_num(self) -> None:     
        if len(self.hand)==1:
            print(f"{self.name}說:UNO!") 
        else:
            print(f"{self.name}剩{len(self.hand)}張")
    
    def convert_color(self) -> Color: # 決定特殊牌要轉換成的顏色
        if self.is_robot: # 是robot時，robot會選擇手牌中最多的顏色
            color_num = dict.fromkeys(Color, 0) # 記錄各顏色牌的數量
            for card in self.hand:
                color_num[card.color] += 1
            color_num[Color.SPECIAL] = -1 # 特殊牌不計入顏色選擇
            max_color_num = max(color_num.values())
            max_color = Color.RED
            for color, num in color_num.items():
                if num == max_color_num:
                    max_color = color
                    break
            print(self.name+"選擇了"+max_color.value.strip()+"色")
            return max_color
            
        else: # 是玩家時，玩家選擇顏色
            while True:
                print(self.name+"請選擇顏色:(請輸入RYGB其中之一)")
                s = input().strip().upper()
                if s not in ("R","Y","G","B"):
                    print("請輸入有效的顏色代號!")
                else:
                    print(self.name+"選擇了"+Color(s).name+"色")
                    return Color(s)


PLAYERS_NAME = ["Anna","Bob","Charlotte","Danny","Emily","Frank","Grace","Henry","Isabella","Jessica","Karen","Lisa","Michael","Nancy","Olivia","Peter","Quincy","Rachel","Steve","Tina","Ursula","Victor","Wendy","Xavier","Yvonne","Zachary"]
CLOCKWISE = 1
COUNTERCLOCKWISE = -1

class UNO:
    def __init__(self, player_num: int, human_name: str):
        self.player_num = player_num
        self.players: List[Player] = [Player(human_name,False)]
        for i in range(player_num-1):
            self.players.append(Player(PLAYERS_NAME[i],True)) # 創造Robot玩家
        self.setup()
        self.main()
    
    def setup(self) -> None:
        self.is_finish: bool = False
        self.deck = Deck()
        self.deck.shuffle()
        for player in self.players:
            player.deal(7,self.deck) # 每位玩家發7張牌
        while True:
            first_card = self.deck.cards.pop() # 從牌組中抽出一張牌作為底牌
            if first_card.color == "special" or first_card.rank in ("+2", "Skip", "Reverse"):
                self.deck.cards.insert(0, first_card) # 特殊牌或+2或Skip或Reverse，放回牌組
            else:
                self.deck.discard.append(first_card)
                print(f"底牌是{first_card}")
                break
    
    def main(self) -> None:
        """遊戲主循環"""
        print("遊戲開始!")
        now_index: int = 0 # 從第一位玩家開始
        direction = CLOCKWISE
        while True:
            # 玩家行動
            state = self.players[now_index].action(self.deck)
            self.players[now_index].say_card_num()
            match state:
                case "normal":
                    now_index += direction
                case "Skip":
                    now_index += direction
                    now_index = (now_index+self.player_num) % self.player_num # 自動迴圈控制玩家索引
                    print(self.players[now_index].name+"被跳過了")
                    now_index += direction
                case "Reverse":
                    direction *= -1
                    print("換成逆時針" if direction==COUNTERCLOCKWISE else "換成順時針")
                    now_index += direction
                case "+2":
                    now_index += direction
                    now_index = (now_index+self.player_num) % self.player_num # 自動迴圈控制玩家索引
                    print(self.players[now_index].name+"抽2張牌")
                    self.players[now_index].deal(2,self.deck)
                case "+4":
                    now_index += direction
                    now_index = (now_index+self.player_num) % self.player_num # 自動迴圈控制玩家索引
                    print(self.players[now_index].name+"抽4張牌")
                    self.players[now_index].deal(4,self.deck)
                case "win":
                    self.is_finish = True
                case _: # 錯誤情況
                    print("state:",state)
                    raise ValueError("錯誤!程式應該不會執行到這裡")
            now_index = (now_index+self.player_num) % self.player_num # 自動迴圈控制玩家索引        
            
            if self.is_finish: break # 結束主循環

            print("下一個人是"+self.players[now_index].name+"\n====================")
            
            # 如果牌組已經被抽完
            if not self.deck.cards:
                print("牌已經沒了！")
                self.deck.cards = self.deck.discard # 牌組已經沒了，將棄牌堆的牌當成新牌組
                self.deck.discard = [] # 將棄牌堆變空
                self.deck.shuffle() # 重新洗牌
        
        if self.ask_restart():
            self.setup()
            self.main()
    
    def ask_restart(self) -> bool:
        print("是否要重新開始遊戲？(y/n)")
        while True:
            s = input().strip().lower()
            if s == "y": # 重新開始遊戲
                return True
            elif s == "n":
                print("遊戲結束!")
                return False
            else:
                print("請輸入y或n!")


if __name__ == '__main__':
    UNO(4,"Dean")