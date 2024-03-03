"""Small Memory game-app using kivy
by Sziller"""

import os
import sys
import random
import inspect
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.clock import Clock
import dotenv
import config as conf

from GameBasePackage.WidgetClasses import *


class ButtonMemory(Button):
    pass


class GameScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(GameScreenManager, self).__init__(**kwargs)
        self.statedict = {
            "screen_intro": {
                "seq": 0,
                'inst': "button_nav_intro",
                'down': ["button_nav_intro"],
                'normal': ["button_nav_game"]},
            "screen_game": {
                "seq": 1,
                'inst': 'button_nav_game',
                'down': ['button_nav_game'],
                'normal': ["button_nav_intro"]}
            }
    
class MemoryGame(GridLayout):
    cards = ListProperty([])
    removing_cards = False  # Flag to indicate if cards are being removed

    def __init__(self, **kwargs):
        super(MemoryGame, self).__init__(**kwargs)
        self.cols: int = 8
        self.rows: int = 8
        
        # self.load_cards()
        # Clock.schedule_once(self.setup_board)
        # self.setup_board()
        self.scores = {True: 0, False: 0}
        # self.run()
        
    def run(self):
        self.max_icons = self.rows * self.cols // 2  # Maximum number of different icons
        self.icons = list(range(1, self.max_icons + 1))  # Icons range from 0 to max_icons - 1
        self.player1_turn = True
        self.selected_cards = []
        self.load_cards()
        # Clock.schedule_once(self.setup_board)
        print(self.cols)
        print(self.rows)
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
            print("+++++")
            print(self.icons)
            icon = random.choice(self.icons)
            self.icons.remove(icon)
            self.cards[i] = icon
            self.cards[i + 1] = icon
        random.shuffle(self.cards)  # Shuffle the cards


    def setup_board(self, dt=None):
        c = 0
        print("!!!")
        print(self.cards)
        print("!!!")
        
        for card in self.cards:
            print("---: {} : {}".format(c, card))
            btn = ButtonMemory(text='', background_normal='./data/cards/0.png', on_release=self.on_card_click)
            # btn.color = (0, 0, 0, 1)  # Set text color to black
            self.add_widget(btn)
            c += 1


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
            App.get_running_app().root.ids.screen_game.ids["board"].text = str(txt)
            self.reveal_all_cards()
        else:
            App.get_running_app().root.ids.screen_game.ids["board"].text = ("It is player-{}'s turn\np1: {}\np2: {}".
                format({True: '1', False: "2"}[self.player1_turn], self.scores[True], self.scores[False]))

    def reset_unmatched_cards(self, dt):
        for index in self.selected_cards:
            card = self.children[index]
            card.text = ''  # Reset the text
            card.background_normal = './data/cards/0.png'
        self.selected_cards.clear()


class OpAreaIntro(OperationAreaBox):
    ccn = inspect.currentframe().f_code.co_name

    def __init__(self, **kwargs):
        super(OpAreaIntro, self).__init__(**kwargs)
    
    def on_init(self):
        """=== Method name: on_init ====================================================================================
        Default method to run right after startup (or whenever defaulting back to initial state is necessary)
        ========================================================================================== by Sziller ==="""
        print("Started: {}".format(self.ccn))
        
    def on_release_to_game(self):
        print("to game")
        App.get_running_app().change_screen(screen_name="screen_game", screen_direction="right")

    def on_release_size(self, inst):
        _id_ = list(self.ids.keys())[list(self.ids.values()).index(inst)]
        x, y = _id_.split(sep="_")[1].split(sep="x")
        print(x)
        print(y)
        App.get_running_app().root.ids.screen_game.ids.oparea_game.ids.game_memory.cols = int(x)
        App.get_running_app().root.ids.screen_game.ids.oparea_game.ids.game_memory.rows = int(y)
        App.get_running_app().root.ids.screen_game.ids.oparea_game.ids.game_memory.run()
        
class MemoryGameApp(App):
    def __init__(self, window_content = ""):
        super(MemoryGameApp, self).__init__()
        self.title: str = "Memory"
        self.window_content = window_content
    
    def change_screen(self, screen_name, screen_direction="left"):
        """=== Method name: change_screen ==============================================================================
        Use this screenchanger instead of the built-in method for more customizability and to enable further
        actions before changing the screen.
        Also, if screenchanging first needs to be validated, use this method!
        ========================================================================================== by Sziller ==="""
        smng = self.root  # 'root' refers to the only one root instance in your App. Here it is the actual ROOT
        smng.current = screen_name
        smng.transition.direction = screen_direction
        
    def build(self):
        return self.window_content


if __name__ == '__main__':
    from kivy.lang import Builder  # to freely pick kivy files
    DOTENV_PATH = "./.env"

    # Define different display settings based on an index.
    # 0: Full-screen on any display,
    # 1: Portrait,
    # 2: Elongated Portrait,
    # 3: Raspberry Pi touchscreen - Landscape,
    # 4: Raspberry Pi touchscreen - Portrait,
    # 5: Large square
    display_settings = {0: {'fullscreen': False, 'run': Window.maximize},  # Full-screen on any display
                        1: {'fullscreen': False, 'size': (600, 1000)},  # Portrait
                        2: {'fullscreen': False, 'size': (500, 1000)},  # Portrait elongated
                        3: {'fullscreen': False, 'size': (640, 480)},  # Raspi touchscreen - landscape
                        4: {'fullscreen': False, 'size': (480, 640)},  # Raspi touchscreen - portrait
                        5: {'fullscreen': False, 'size': (1200, 1200)},  # Large square
                        6: {'fullscreen': False, 'size': (600, 600)}  # Midsize square
                        }

    dotenv.load_dotenv(DOTENV_PATH)
    style_code = int(os.getenv("SCREENMODE"))

    Window.fullscreen = display_settings[style_code]['fullscreen']
    if 'size' in display_settings[style_code].keys(): Window.size = display_settings[style_code]['size']
    if 'run' in display_settings[style_code].keys(): display_settings[style_code]['run']()

    # Load a specified Kivy file from the command-line argument or a default file.
    
    try:
        content = Builder.load_file(str(sys.argv[1]))
    except IndexError:
        content = Builder.load_file("memorygame.kv")
        
    application = MemoryGameApp(window_content=content)
    application.run()




