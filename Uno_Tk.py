import tkinter as tk
import tkinter.messagebox as mb
import random

# 因為某些問題，暫時用print()代替root.game_state.config(text=word)顯示文字

class Card(tk.Button):
    bg_colors = {"R ": "red", "Y ": "yellow", "G ": "green", "B ": "blue", "special": "gray"} # 一個字典，顏色的簡稱對應表
    # 建構函式
    def __init__(self, master, color, rank):
        super().__init__(master, text=rank, font=("Arial", 20), bg=Card.bg_colors[color], command=lambda: clickCard(self.color, self.rank))
        self.color = color
        self.rank = rank
    
    def getBgColor(self): return Card.bg_colors[self.color]
    def setColor(self, color): self.color = color
    #def getRank(self): return self.rank
    def show(self):
        return self.color + self.rank + ", "

def clickCard(color, rank):
    if Game.can_human_play: Player.CRCHD = [color, rank]
    else: return

class Deck:
    # 建構函式，初始化牌組
    def __init__(self, root):
        self.root = root
        #                顏色   紅 ，黃    ，綠   ，藍
        #               color (red,yellow,green,blue)
        color =["R ", "Y ", "G ","B "] # 顏色的簡稱
        rank = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "+2"] # 點數
        self.cards = []
        self.discard = []
        for i in range(4):
            self.cards.append(Card(root, color[i], "0"))#添加4張0
        #數字1~9和Skip", "Reverse", "+2"都各有兩張
        for c in color:
            for r in rank:
                for _ in range(2): self.cards.append(Card(root, c, r))
            
        for _ in range(4):
            self.cards.append(Card(root, "special", "wild"))
            self.cards.append(Card(root, "special","+4"))
        
    # 洗牌的方法
    def shuffle(self):
        random.shuffle(self.cards)
        print("洗牌完成!")

    def p(self, word): self.root.game_state.config(text=word) # 顯示文字的方法
    


class Player:
    CRCHD = [] #CRCHD 是 Color and Rank of the Card the Human Dealt 的縮寫，用來表示人類玩家出的牌
    WHD = False # WHD 是 Will the Human Draw 的縮寫，用來表示人類玩家是否要抽牌
    def __init__(self, name, isRobot):
        self.name = name
        self.isRobot = isRobot
        self.hand = []
    
    def deal(self, numCards, deck, root):
        for i in range(numCards):
            if len(deck.cards): # 牌組中有牌
                card = deck.cards[0] # 從牌組中取出第一張牌
                del deck.cards[0] # 在cards中刪除，代表抽出這張牌
                self.hand.append(card) # 將牌加入玩家手牌
                if not self.isRobot:
                    print(self.name+"抽到了"+card.show())
            else:
                print("牌已經沒了！")
                break # 當牌已經發完時終止循環

    def win(self, root):# 如果手牌數量為 0，則傳回 True，否則傳回 False
        if len(self.hand) == 0:
            print(self.name+"獲勝了！")
            return True
        else: False
    
    def ACN(self): # ACN 是 Arrange cards neatly 的縮寫，用來排列手牌
        rank = {"Skip": 10, "Reverse": 11, "+2": 12, "wild": 13, "+4": 14}
        reverse_rank = {10: "Skip", 11: "Reverse", 12: "+2", 13: "wild", 14: "+4"}
        for card in self.hand:
            if card.rank in rank: card.rank = rank[card.rank]
            else: card.rank = int(card.rank) # 字串0~9轉成數字

        # 排序手牌
        self.hand.sort(key=lambda x: x.rank)
        """被上面那行取代了
        # 插入排序法
        for i in range(len(self.hand)):
            key = self.hand[i].rank # 取得牌的點數
            j = i - 1
            while j >= 0 and self.hand[j].getRank > key:
                self.hand[j+1] = self.hand[j]
                j -= 1
            self.hand[j+1] = 
        """
            
        for card in self.hand:
            if card.rank in reverse_rank: card.rank = reverse_rank[card.rank]
            else: card.rank = str(card.rank) # 數字0~9轉成字串

    
    """# 顯示手牌的方法
    def displayHand(self):
        self.ACN() # 先進行排序
        print(self.name + "的手牌:")
        i = 1
        for card in self.hand:
            print("第"+str(i)+"張:"+card.show(), end=" ") #不要換行
            i += 1
        p(" ") # 只是為了換行"""
    

    def robotplay(self, d, root): # d 是棄牌堆
        card = d[len(d)-1] # 取得棄牌堆最後一張牌
        print(card.show())
        print([c.show() for c in d])
        for card2 in self.hand:
            if card2.color == card.color or card2.rank == card.rank:
                self.hand.remove(card2) # 出手中符合規則的牌中的一張
                d.append(card2) # 將這張牌放入棄牌堆
                print(self.name+"出了"+card2.show())
                return True
        
        for card2 in self.hand:
            if card2.color == "special":
                self.hand.remove(card2)
                d.append(card2)
                print(self.name+"出了"+card2.show())
                return True
            
        return False#沒有符合規則的牌，回傳False
    

    def humanPlay(self, deck, root):
        dPC = deck.discard[-1]  # 取得棄牌堆最後一張牌(即最上面的牌)
        print(dPC.show())
        print([c.show() for c in deck.discard])
        mb.showinfo("提示", "輪到你了，請選擇要出的牌")
        Game.can_human_play = True  # 玩家可以出牌

        while True:
            while True:
                if len(Player.CRCHD) == 0:
                    # 等待玩家選擇
                    root.update()
                else:
                    break

            card = None  # 預設 card 為 None，避免未初始化的情況
            for c in self.hand:
                if c.color == Player.CRCHD[0] or c.rank == Player.CRCHD[1]:  # 找到符合的牌
                    card = c  # card 就是玩家想出的牌！
                    break

            # 檢查用戶輸入的牌是否符合規則
            if card and (card.color == dPC.color or card.rank == dPC.rank or card.color == "special"):
                break  # 用戶輸入合法，退出循環
            else:
                mb.showerror("錯誤！", "請輸入顏色為" + dPC.color + "或special的牌或者點數為" + dPC.rank + "的牌!")
                Player.CRCHD = []  # 重置Player.CRCHD，等待玩家重新輸入
                root.update()

        if Player.WHD:  # 玩家要抽牌
            self.deal(1, deck, root)  # 玩家不出牌，就抽一張牌
            Player.WHD = False  # 重置Player.WHD，表示玩家不再抽牌
            return False  # 回傳False，表示沒有出牌
        else:  # 玩家出牌
            self.hand.remove(card)
            deck.discard.append(card)  # 將牌放入棄牌堆
            print([c.show() for c in deck.discard])
            print(self.name + "出了" + card.show())
            return True  # 回傳True，表示有出牌
  
    
    def action(self, deck, root):
        card = deck.discard[-1]
        print("現在牌堆最上方的牌:"+card.show())
        print([c.show() for c in deck.discard])
        if self.isRobot:
            if not self.robotplay(deck.discard, root):#若沒牌可出，就抽一張
                print(self.name+" 沒牌可出，抽一張")
                self.deal(1,deck, root)
                return "normal" #沒出牌是普通情況，回傳normal
        else:
            if not self.humanPlay(deck, root): return "normal" #沒出牌是普通情況，回傳normal
        
        Iplayed = deck.discard[-1] # 棄牌堆最後的牌是剛剛出的牌
        #為了將特殊情況回傳給Main函數
        if Iplayed.color == "special":
            Iplayed.setColor(self.convertColor(root)) #將特殊牌的顏色轉換成玩家所選的顏色
            if(Iplayed.rank == "wild"):
                return "normal"
            else: #是+4
                return "+4"
        elif Iplayed.rank == "Skip":
            return "Skip"
        elif Iplayed.rank == "Reverse":
            return "Reverse"
        elif Iplayed.rank == "+2":
            return "+2"
        else: #一般數字牌
            return "normal"

    def cardNum(self): return len(self.hand)
    def sayCardNum(self, root): # 要改
        print(self.name+"說:UNO!") if self.cardNum()==1 else print(self.name+"剩"+str(self.cardNum())+"張")
    
    def convertColor(self, root):#決定特殊牌要轉換成的顏色
        if(self.isRobot==True):#是robot時，robot會選擇最多的顏色
            colorNumber = [0,0,0,0]
            for card in self.hand:
                if card.color == "R ":
                    colorNumber[0] += 1
                elif card.color == "Y ":
                    colorNumber[1] += 1
                elif card.color == "G ":
                    colorNumber[2] += 1
                elif card.color == "B ":
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
            
        else:  # 玩家選擇顏色
            CHC = tk.StringVar()  # 使用StringVar來保存顏色選擇
            def chooseColor(color):
                CHC.set(color)  # 更新StringVar的值

            CC = tk.Tk()
            CC.title("選擇顏色")
            CC.geometry("200x100")
            
            RB = tk.Button(CC, text="紅色", command=lambda: chooseColor("R"), bg="red")
            RB.pack(side="left")
            YB = tk.Button(CC, text="黃色", command=lambda: chooseColor("Y"), bg="yellow")
            YB.pack(side="left")
            GB = tk.Button(CC, text="綠色", command=lambda: chooseColor("G"), bg="green")
            GB.pack(side="left")
            BB = tk.Button(CC, text="藍色", command=lambda: chooseColor("B"), bg="blue")
            BB.pack(side="left")
            CC.mainloop()
            return CHC.get()  # 使用get()來獲取選擇的顏色

            
    def p(self, word): self.root.game_state.config(text=word) # 顯示文字的方法
    
class Game:
    can_human_play = False  # 玩家是否可以出牌的標記
    def __init__(self, root, player_number, human_name, game_state):
        self.root = root
        self.game_state = game_state
        self.player_number = player_number
        self.Players_name = ["Anna", "Bob", "Charlotte", "Danny", "Emily", "Frank", "Grace", "Henry"]
        self.Players = [Player(human_name, False)] + [
            Player(self.Players_name[i], True) for i in range(player_number - 1)
        ]
        self.deck = Deck(root)
        self.deck.shuffle()
        for player in self.Players:
            player.deal(7, self.deck, root)

        self.direction = 1  # 初始為順時針
        self.now_player_index = 0  # 初始玩家為第一個
        self.is_game_over = False  # 遊戲結束標記

        # GUI設定
        self.game_state.grid(row=1, column=0, columnspan=4)
        
        self.deck_label = tk.Label(root, text="", font=("Arial", 20), width=5, height=3)
        self.deck_label.grid(row=2, column=1, columnspan=2)
        
        self.draw_card_button = tk.Button(root, text="抽牌", font=("Arial", 12), command=lambda: self.draw_card(self.Players[0].hand))
        self.draw_card_button.grid(row=2, column=3)
        
        self.update_discard_pile()

        # 顯示機器人玩家牌數
        for i, player in enumerate(self.Players[1:], start=1):
            tk.Label(root, text=f"機器人{player.name}有{player.cardNum()}張牌", font=("Arial", 12)).grid(row=0, column=i - 1)

        # 顯示玩家手牌
        self.display_human_hand()

        self.next_turn()

    def draw_card(self, hand):
        if Game.can_human_play: 
            Player.WHD = True

    def update_discard_pile(self):
        # 初始化底牌
        while True:
            firstCard = self.deck.cards[0]  # 從牌組中取出第一張牌
            self.deck.cards.remove(firstCard)  # 從牌組中移除第一張牌
            if firstCard.color == "special" or firstCard.rank in ["+2", "Skip", "Reverse"]:
                self.deck.cards.append(firstCard)
            else:
                self.deck.discard.append(firstCard)
                break
        # 更新 deck_label，顯示最上方牌的點數和顏色
        last_card = self.deck.discard[-1]
        self.deck_label.config(text=last_card.rank, bg=last_card.getBgColor())

    def display_human_hand(self):
        human = self.Players[0]
        human.ACN()  # 先進行排序
        tk.Label(self.root, text="這是你的牌：", font=("Arial", 12)).grid(row=5, column=0)
        for i, card in enumerate(human.hand):
            card.grid(row=10, column=i)  # 放置手牌按鈕

    def next_turn(self):
        if self.is_game_over:
            self.game_state.config(text="遊戲結束！")
            self.root.uppdate()
            return

        # 如果牌組已經被抽完，重新洗棄牌堆作為新牌組
        if len(self.deck.cards) == 0:
            self.deck.cards = self.deck.discard[:]
            self.deck.discard.clear()  # clear() 清空列表
            self.deck.shuffle()
            self.game_state.config(text="牌已經沒了，重新洗牌！")
            self.root.update()

        # 取得當前玩家
        current_player = self.Players[self.now_player_index]
        self.game_state.config(text=f"現在是{current_player.name}的回合！")
        self.root.update()
        
        # 進行玩家行動並取得結果
        action_result = current_player.action(self.deck, self.root)
        self.update_discard_pile()
        self.root.update()
        
        # 更新遊戲狀態
        if current_player.win(self):
            self.is_game_over = True
            self.game_state.config(text=f"{current_player.name} 獲勝了！")
            self.root.update()
            return
        
        # 根據行動結果調整遊戲流程
        if action_result == "Skip":
            self.now_player_index = (self.now_player_index + 2 * self.direction) % self.player_number
        elif action_result == "Reverse":
            self.direction *= -1
            self.now_player_index = (self.now_player_index + self.direction) % self.player_number
        elif action_result == "+2":
            next_player = self.Players[(self.now_player_index + self.direction) % self.player_number]
            next_player.deal(2, self.deck, self.root)
            self.now_player_index = (self.now_player_index + self.direction) % self.player_number
        elif action_result == "+4":
            next_player = self.Players[(self.now_player_index + self.direction) % self.player_number]
            next_player.deal(4, self.deck, self.root)
            self.now_player_index = (self.now_player_index + self.direction) % self.player_number
        else:
            self.now_player_index = (self.now_player_index + self.direction) % self.player_number
        self.root.update()
        # 下一回合
        print("=====================")
        self.root.after(1000, self.next_turn)

    def p(self, word):
        self.game_state.config(text=word)


def UNO(player_number, human_name):
    root = tk.Tk()
    root.title("UNO")
    root.geometry("800x600")
    
    # 初始化 game_state 在這裡，這樣確保在 Game 類初始化之前 game_state 存在
    game_state = tk.Label(root, text="遊戲開始！", font=("Arial", 12))
    game_state.grid(row=1, column=0, columnspan=4)
    
    # 把 game_state 作為參數傳給 Game
    Game(root, player_number, human_name, game_state)
    
    root.mainloop()


if __name__ == '__main__':
    UNO(4,"Dean")