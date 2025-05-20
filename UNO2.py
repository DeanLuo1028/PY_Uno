# 這是 uno.py
# -*- coding: UTF-8 -*-

import random

class Card:
    def __init__(self, color, rank):
        self.color = color
        self.rank = rank
    
    def show(self):
        return self.color + self.rank + ", "

class Deck:
    # 建構函式，初始化牌組
    def __init__(self):
        #        紅 ，黃    ，綠   ，藍
        #        red,yellow,green,blue
        colors =["R ", "Y ", "G ","B "] # 顏色的簡稱
        ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"] # 點數
        self.cards = [] # 牌堆
        self.discard = [] # 棄牌堆
        #每個顏色的0只有1張
        for i in range(4):
            self.cards.append( Card(colors[i], "0"))
        #每個顏色的數字1~9和Skip", "Reverse", "+2"都各有兩張
        for color in colors:
            for rank in ranks:
                self.cards.append(Card(color, rank))
                self.cards.append(Card(color, rank))
        # special wild 和 special +4 各有4張
        for _ in (None,) * 4:
            self.cards.append(Card("special", "wild"))
            self.cards.append(Card("special","+4"))
        
    
    # 洗牌的方法
    def shuffle(self):
        random.shuffle(self.cards)
        print("洗牌完成!")
    
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def deal(self, numCards, deck):
        for _ in range(numCards):
            if len(deck.cards): # 牌組中有牌
                self.hand.append(deck.cards.pop(0))
                
                if not self.isRobot:
                    print(self.name + "抽到了" + self.hand[-1].show())
            else:
                print("牌已經沒了！")
                break # 當牌已經發完時終止循環

    def win(self):# 如果手牌數量為 0，則傳回 True，否則傳回 False
        if len(self.hand) == 0:
            print(self.name+"獲勝了！")
            return True
        else: False
    

    # 顯示手牌的方法
    def displayHand(self):
        print(self.name + "的手牌:")
        i = 1
        for card in self.hand:
            print("第"+str(i)+"張:"+card.show(), end=" ") #不要換行
            i += 1
        print(" ") # 只是為了換行
    

    
    

    def play(self, deck):
        dPC = deck.discard[len(deck.discard)-1]
        print("以下是你的牌:")
        self.displayHand()
        
        # 循環直到用戶輸入合法的整數在指定範圍內
        while (True):
            print(self.name+"請問你要出第幾張牌?(如果不想出牌，請輸入0)")
            s = input()
            # 檢查用戶輸入是否為整數
            if s.isdigit():
                userInput = int(s)
                # 檢查用戶輸入是否在0~牌數之間
                if userInput >= 0 and userInput <= len(self.hand):
                    if userInput == 0:
                        break# 用戶輸入合法，退出循環
                    
                    card = self.hand[userInput-1]
                    # 檢查用戶輸入的牌是否符合規則
                    if card.getColor()==dPC.getColor() or card.getRank()==dPC.getRank() or card.getColor()=="special":
                        break# 用戶輸入合法，退出循環
                    else:
                        print("請輸入顏色為"+dPC.getColor()+"或special的牌或者點數為"+dPC.getRank()+"的牌!")
                else:
                    print("請輸入0~"+len(self.hand)+"之間的整數!")   
            else:
                print("請輸入一個有效的整數！")
            
        if (userInput == 0):
            self.deal(1, deck)# 玩家不出牌，就抽一張牌
            return False # 回傳False，表示沒有出牌
        else:# 玩家出牌
            card = self.hand[userInput-1]
            self.hand.remove(card)
            deck.discard.append(card) # 將牌放入棄牌堆
            print(self.name+"出了"+card.show())
            return True # 回傳True，表示有出牌
        
    
    def action(self, deck):
        card = deck.discard[len(deck.discard)-1]
        print("現在牌堆最上方的牌:"+card.show())
        if self.isRobot:
            if not self.robotplay(deck.discard):#若沒牌可出，就抽一張
                print(self.name+" 沒牌可出，抽一張")
                self.deal(1,deck)
                return "normal" #沒出牌是普通情況，回傳normal
        else:
            if not self.humanPlay(deck): return "normal" #沒出牌是普通情況，回傳normal
        
        Iplayed = deck.discard[len(deck.discard)-1] # 棄牌堆最後的牌是剛剛出的牌
        #為了將特殊情況回傳給Main函數
        if Iplayed.getColor() == "special":
            Iplayed.setColor(self.convertColor()) #將特殊牌的顏色轉換成玩家所選的顏色
            if(Iplayed.getRank() == "wild"):
                return "normal"
            else: #是+4
                return "+4"
        elif Iplayed.getRank() == "Skip":
            return "Skip"
        elif Iplayed.getRank() == "Reverse":
            return "Reverse"
        elif Iplayed.getRank() == "+2":
            return "+2"
        else: #一般數字牌
            return "normal"

    def cardNum(self): return len(self.hand)
    def sayCardNum(self): print(self.name+"說:UNO!") if self.cardNum()==1 else print(self.name+"剩"+str(self.cardNum())+"張")
    
    def convertColor(self):#決定特殊牌要轉換成的顏色
        if(self.isRobot==True):#是robot時，robot會選擇最多的顏色
            colorNumber = [0,0,0,0]
            for card in self.hand:
                if card.getColor() == "R ":
                    colorNumber[0] += 1
                elif card.getColor() == "Y ":
                    colorNumber[1] += 1
                elif card.getColor() == "G ":
                    colorNumber[2] += 1
                elif card.getColor() == "B ":
                    colorNumber[3] += 1
                else: pass #特殊牌，不計入   
            
            max = colorNumber[0] # 假設第一個元素是最大的
            maxIndex = 0 # 最大元素的索引
            # 遍歷數組，尋找最大值及其索引
            for i in range(4):
                if colorNumber[i] > max:
                    max = colorNumber[i]
                    maxIndex = i
            
            if maxIndex == 0:
                print("轉成紅色")
                return "R "
            elif maxIndex == 1:
                print("轉成黃色")
                return "Y "
            elif maxIndex == 2:
                print("轉成綠色")
                return "G "
            else:
                print("轉成藍色")
                return "B "
            
        else:#是玩家時，玩家選擇顏色
            while (True):
                print(self.name+"請選擇顏色:(請輸入RYGB其中之一)")
                s = input()
                #返回玩家所選的顏色後函式就會結束，所以不需要再break這個while迴圈
                if s == "R":
                    print(self.name+"選擇了紅色")
                    return "R "
                elif s == "Y":
                    print(self.name+"選擇了黃色")
                    return "Y "
                elif s == "G":
                    print(self.name+"選擇了綠色")
                    return "G "
                elif s == "B":
                    print(self.name+"選擇了藍色")
                    return "B "
                else:
                    print("請輸入有效的顏色!")
    
class Robot(Player):
    def play(self, d): # d 是棄牌堆
        card = d[-1] # 獲知棄牌堆最後一張牌
        for card2 in self.hand:
            if card2.getColor() == card.getColor() or card2.getRank() == card.getRank():
                self.hand.remove(card2) # 出手中符合規則的牌中的一張
                d.append(card2) # 將這張牌放入棄牌堆
                print(self.name+"出了"+card2.show())
                return True
        
        for card2 in self.hand:
            if card2.getColor() == "special":
                self.hand.remove(card2)
                d.append(card2)
                print(self.name+"出了"+card2.show())
                return True
            
        return False#沒有符合規則的牌，回傳False
    

def UNO(playerNumber, human_name):
    players_name = ["Anna","Bob","Charlotte","Danny","Emily","Frank","Grace","Henry","Isabella","Jessica","Karen","Lisa","Michael","Nancy","Olivia","Peter","Quincy","Rachel","Steve","Tina","Ursula","Victor","Wendy","Xavier","Yvonne","Zachary"]
    players = [Player(human_name,False)]
    for i in range(playerNumber-1): players.append(Player(players_name[i],True)) # 創造Robot玩家
    deck = Deck()
    deck.shuffle()
    for player in players: player.deal(7,deck)
    while True:
        # 抽一張底牌並放入棄牌堆
        firstCard = deck.cards[0] # 從牌組中取出第一張牌
        deck.cards.remove(firstCard)
        if firstCard.getColor()=="special" or firstCard.getRank() == "+2" or firstCard.getRank() == "Skip"  or firstCard.getRank() == "Reverse":
            deck.cards.append(firstCard) # 特殊牌或+2或Skip或Reverse，放回牌組最後面
        else:
            deck.discard.append(firstCard)
            print("底牌是"+firstCard.show())
            break
        
    print("遊戲開始!")
    isfinish = False
    nowPlayer = 0 # 從第一位玩家開始
    direction = 1 # 順時針
    # 遊戲主程式
    while True:
        # 如果牌組已經被抽完的邏輯
        if len(deck.cards) == 0:
            print("牌已經沒了！")
            deck.cards = deck.discard[:] # 牌組已經沒了，將棄牌堆的牌重新加入牌組
            deck.discard = [] # 將棄牌堆清空
            deck.shuffle() # 重新洗牌
        condition = players[nowPlayer].action(deck)
        players[nowPlayer].sayCardNum()
        if condition == "normal":
            nowPlayer += direction
        elif condition == "Skip":
            nowPlayer += direction
            nowPlayer = (nowPlayer + playerNumber) % playerNumber # 自動迴圈控制玩家索引
            print(players[nowPlayer].name+"被跳過了")
            nowPlayer += direction
        elif condition == "Reverse":
            direction *= -1
            print("換成逆時針")
            nowPlayer += direction
        elif condition == "+2":
            nowPlayer += direction
            nowPlayer = (nowPlayer + playerNumber) % playerNumber # 自動迴圈控制玩家索引
            print(players[nowPlayer].name+"抽2張牌")
            players[nowPlayer].deal(2,deck)
        elif condition == "+4":
            nowPlayer += direction
            nowPlayer = (nowPlayer + playerNumber) % playerNumber # 自動迴圈控制玩家索引
            print(players[nowPlayer].name+"抽4張牌")
            players[nowPlayer].deal(4,deck)
        else: # 錯誤情況
            raise Exception("錯誤!程式應該不會執行到這裡")
        nowPlayer = (nowPlayer + playerNumber) % playerNumber # 自動迴圈控制玩家索引        
        
        for player in players:
            if player.win():
                isfinish = True
                break
        if isfinish: break # 結束主程式

        print("下一個人是"+players[nowPlayer].name+"\n====================")
        
    # 遊戲結束
    print("遊戲結束!")
    
if __name__ == '__main__':
    UNO(4,"Dean")