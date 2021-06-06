import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.spinner import Spinner
import holdem_engine as hldm
import simulation_engine as estimate_equity
import threading

# see my.kv file for the core GUI code

class MyGrid(Widget):
    """Creating objects to represent the user's cards, the cards on the board, and the number of opponents in the hand"""
    user_cards = ObjectProperty(None)
    board_cards = ObjectProperty(None)
    num_opponents = ObjectProperty(None)


class SimplePopup(Popup):
    """Creates a simple popup window"""
    pass


class CalcButton(Button):

    def fire_popup(self, user_card1, user_card2, board_card1, board_card2, board_card3, board_card4, board_card5, num_opponents):
        """Method that controls the simulation process and generates output window"""
        
        # assigning GUI inputs to python variables
        user_card_names = [user_card1.text, user_card2.text]
        board_cards_input = [board_card1, board_card2, board_card3, board_card4, board_card5]
        board_cards_names = [card.text for card in board_cards_input if card.text is not 'None']
        num_opponents = int(num_opponents.text)
        
           
        # creating a Deck object (see holdem_engine.py) 
        deck = hldm.Deck()
        
        # creating Player objects (see holdem_engine.py) for each opponent left in the hand
        opponents = []
        for _ in range(num_opponents):
            opponent = hldm.Player()
            opponents.append(opponent)
        
        #Creating a Player object to represent the user (see holdem_engine.py)
        user = hldm.Player()
        
        # Matching the user's shortened card names (from GUI inputs) to Card objects in Deck (see holdem_engine.py)
        for name in user_card_names:
            [user.hole_cards.append(card) for card in deck.cards if card.name_short == name]
        
        # Matching the board's shortened card names (from GUI inputs) to Card objects in Deck (see holdem_engine.py)
        board_cards = []
        for name in board_cards_names:
            [board_cards.append(card) for card in deck.cards if card.name_short == name]
        
        # creating a Scenerio object (see simulation_engine.py) with input variables
        scenario = estimate_equity.Scenario(user, opponents, board_cards)
        
        # creating Simulation object (see simulation_engine.py) and running 15,000 sims
        sim = estimate_equity.Simulation(scenario)
        win_pct = sim.run()
        
        # creating popup window that displays the user's estimated hand equity
        self.pop = SimplePopup()
        self.pop.open()
        self.pop.ids.eqty_output.text = win_pct


class MyApp(App): # <- Main Class
    def build(self):
        """Builds the main GUI window"""
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
