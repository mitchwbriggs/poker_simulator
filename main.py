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
import equity_calculator as eqty_calc
import threading


class MyGrid(Widget):
    user_cards = ObjectProperty(None)
    board_cards = ObjectProperty(None)
    num_opponents = ObjectProperty(None)


class SimplePopup(Popup):
    """Creates a simple popup window"""
    pass


class CalcButton(Button):

    def fire_popup(self, user_card1, user_card2, board_card1, board_card2, board_card3, board_card4, board_card5, num_opponents):
        """Method that creates the main window"""
        user_card_names = [user_card1.text, user_card2.text]
        board_cards_input = [board_card1, board_card2, board_card3, board_card4, board_card5]
        board_cards_names = [card.text for card in board_cards_input if card.text is not 'None']
        num_opponents = int(num_opponents.text)

        opponents = []
        for _ in range(num_opponents):
            opponent = hldm.Player()
            opponents.append(opponent)

        deck = hldm.Deck()
        user = hldm.Player()

        for name in user_card_names:
            [user.hole_cards.append(card) for card in deck.cards if card.name_short == name]

        board_cards = []
        for name in board_cards_names:
            [board_cards.append(card) for card in deck.cards if card.name_short == name]

        scenario = eqty_calc.Scenario(user, opponents, board_cards)
        sim = eqty_calc.Simulation(scenario)
        win_pct = sim.run()

        self.pop = SimplePopup()
        self.pop.open()
        self.pop.ids.eqty_output.text = win_pct


class MyApp(App): # <- Main Class
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()