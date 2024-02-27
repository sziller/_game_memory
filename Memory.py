import sys
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.clock import Clock
import random


class ButtonMemory(Button):
    pass
    
    
class MemoryGame(GridLayout):
    cards = ListProperty([])
    removing_cards = False  # Flag to indicate if cards are being removed

    def __init__(self, **kwargs):
        super(MemoryGame, self).__init__(**kwargs)
        self.cols = 8
        self.rows = 5
        self.max_icons = self.rows * self.cols // 2  # Maximum number of different icons
        self.icons = list(range(1, self.max_icons + 1))  # Icons range from 0 to max_icons - 1
        self.player1_turn = True
        self.selected_cards = []
        self.load_cards()
        # Clock.schedule_once(self.setup_board)
        self.setup_board()
        self.scores = {True: 0, False: 0}
    
    def reveal_all_cards(self):
        for child in self.children:
            index = (self.children.index(child))
            card = self.children[index]
            card.opacity = 100
            
 
    def load_cards(self):
        # Load the icons
        self.cards = [0] * (self.rows * self.cols)
        for i in range(0, len(self.cards), 2):
            icon = random.choice(self.icons)
            self.icons.remove(icon)
            self.cards[i] = icon
            self.cards[i + 1] = icon
        random.shuffle(self.cards)  # Shuffle the cards


    def setup_board(self, dt=None):
        for card in self.cards:
            btn = ButtonMemory(text='', background_normal='./data/cards/0.png', on_release=self.on_card_click)
            # btn.color = (0, 0, 0, 1)  # Set text color to black
            self.add_widget(btn)


    def on_card_click(self, instance):
        if not self.removing_cards and instance.background_normal == './data/cards/0.png':
            index = self.children.index(instance)
            self.flip_card(index)
            self.check_match()
        
    def flip_card(self, index):
        if index not in self.selected_cards:
            card = self.children[index]
            card.opacity = 100
            # card.text = str(self.cards[index])  # Set the text to the card number
            card.background_normal = './data/cards/' + str(self.cards[index]) + '.png'
            self.selected_cards.append(index)

    def check_match(self):
        if len(self.selected_cards) == 2:
            index1, index2 = self.selected_cards
            if self.cards[index1] == self.cards[index2]:
                print("pair FOUND")
                self.scores[self.player1_turn] += 1
                self.removing_cards = True
                Clock.schedule_once(self.remove_matched_cards, 1)
            else:
                print("pair NOT FOUND")
                Clock.schedule_once(self.reset_unmatched_cards, 1)
                self.player1_turn = not self.player1_turn
            Clock.schedule_once(self.display_score, 1)
            
    def remove_matched_cards(self, dt):
        for index in self.selected_cards:
            self.children[index].opacity = 0.2
        self.selected_cards.clear()
        self.removing_cards = False
        
    def display_score(self, dt):
        if sum(list(self.scores.values())) == self.max_icons:
            p1_score = self.scores[True]
            p2_score = self.scores[False]
            if p1_score == p2_score:
                txt = "Game tied"
            elif p1_score > p2_score:
                txt = "Player 1 Won: {} : {}".format(p1_score, p2_score)
            else:
                txt = "Player 2 Won: {} : {}".format(p2_score, p1_score)
            App.get_running_app().root.ids["board"].text = str(txt)
            self.reveal_all_cards()
        else:
            App.get_running_app().root.ids["board"].text = ("It is player-{}'s turn\n"
                                                            "p1: {}\n"
                                                            "p2: {}").format({True: '1', False: "2"}[self.player1_turn],
                                                                         self.scores[True], self.scores[False])

    def reset_unmatched_cards(self, dt):
        for index in self.selected_cards:
            card = self.children[index]
            card.text = ''  # Reset the text
            card.background_normal = './data/cards/0.png'
        self.selected_cards.clear()


class MemoryGameApp(App):
    def __init__(self, window_content = ""):
        super(MemoryGameApp, self).__init__()
        self.title: str = "Memory"
        self.window_content = window_content
        
    def build(self):
        return self.window_content


if __name__ == '__main__':
    from kivy.lang import Builder  # to freely pick kivy files
    try:
        content = Builder.load_file(str(sys.argv[1]))
    except IndexError:
        content = Builder.load_file("memorygame.kv")
        
    application = MemoryGameApp(window_content=content)
    application.run()
