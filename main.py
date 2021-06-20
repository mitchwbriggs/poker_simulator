from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import holdem_engine
import simulation_engine
import sys

class App(QDialog):

    def __init__(self):
        """Setting up the application"""

        super().__init__()
        self.title = "Texas Hold'em Simulator"
        self.drop_down_menus = []
        self.selected_cards = []
        self.num_opps = 1
        self.createCardNames()
        self.card_dict = {}
        self.createCardDict()
        self.initUI()

    def initUI(self):
        """Setting up the UI"""

        # title
        self.setWindowTitle(self.title)

        # add app icon
        icon = QIcon("app_icon.png")
        self.setWindowIcon(icon)

        # add layout segments containing functionality
        self.createHoleCardsLayout()
        self.createBoardCardsLayout()
        self.createNumberOpponentsLayout()
        self.createButtonLayout()

        # add drop down menus to appropriate layouts
        for drop_down in self.drop_down_menus:
            drop_down.currentTextChanged.connect(lambda: self.disableSelectedItem(self.drop_down_menus))

        # add widgets to layouts
        windowLayout = QGridLayout()
        windowLayout.addWidget(self.GroupBoxHoleCards, 0, 0)
        windowLayout.addWidget(self.GroupBoxBoardCards, 0, 1)
        windowLayout.addWidget(self.GroupBoxNumberOpponents, 1, 0, 1, 1)
        windowLayout.addWidget(self.GroupBoxButton, 1, 1)

        # add auto column stretching
        windowLayout.setColumnStretch(0, 1)
        windowLayout.setColumnStretch(1, 1)

        self.setLayout(windowLayout)
        self.center()
        self.show()

    def center(self):
        """Center app on screen"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

    def createHoleCardsLayout(self):
        """Design layout for user card selection"""

        self.GroupBoxHoleCards = QGroupBox("Hole Cards")

        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)

        hole_card1 = self.createDeckDropDown()
        hole_card2 = self.createDeckDropDown()

        drop_downs = [hole_card1, hole_card2]
        self.drop_down_menus += drop_downs

        layout.addWidget(hole_card1, 0, 0)
        layout.addWidget(hole_card2, 0, 1)

        self.GroupBoxHoleCards.setLayout(layout)

    def createBoardCardsLayout(self):
        """Design layout for board card selection"""

        self.GroupBoxBoardCards = QGroupBox("Board Cards")

        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 1)

        self.board_card1 = self.createDeckDropDown()
        self.board_card2 = self.createDeckDropDown()
        self.board_card3 = self.createDeckDropDown()
        self.board_card4 = self.createDeckDropDown()
        self.board_card5 = self.createDeckDropDown()

        drop_downs = [self.board_card1, self.board_card2, self.board_card3, self.board_card4, self.board_card5]
        self.drop_down_menus += drop_downs

        layout.addWidget(self.board_card1, 0, 0)
        layout.addWidget(self.board_card2, 0, 1)
        layout.addWidget(self.board_card3, 0, 2)
        layout.addWidget(self.board_card4, 0, 3)
        layout.addWidget(self.board_card5, 0, 4)

        self.GroupBoxBoardCards.setLayout(layout)

    def createNumberOpponentsLayout(self):
        """Design layout for Number of Opponent selection"""

        self.GroupBoxNumberOpponents = QGroupBox("Number of Opponents in Hand")

        self.drop_down_num_opps = self.createNumOppsDropDown()

        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.addWidget(self.drop_down_num_opps, 0, 0)

        self.GroupBoxNumberOpponents.setLayout(layout)

    def createCardNames(self):
        """List of playing card names"""

        self.card_names = [
            '-',
            'Ace of Hearts', 'Ace of Clubs', 'Ace of Diamonds', 'Ace of Spades',
            'King of Hearts', 'King of Clubs', 'King of Diamonds', 'King of Spades',
            'Queen of Hearts', 'Queen of Clubs', 'Queen of Diamonds', 'Queen of Spades',
            'Jack of Hearts', 'Jack of Clubs', 'Jack of Diamonds', 'Jack of Spades',
            'Ten of Hearts', 'Ten of Clubs', 'Ten of Diamonds', 'Ten of Spades',
            'Nine of Hearts', 'Nine of Clubs', 'Nine of Diamonds', 'Nine of Spades',
            'Eight of Hearts', 'Eight of Clubs', 'Eight of Diamonds', 'Eight of Spades',
            'Seven of Hearts', 'Seven of Clubs', 'Seven of Diamonds', 'Seven of Spades',
            'Six of Hearts', 'Six of Clubs', 'Six of Diamonds', 'Six of Spades',
            'Five of Hearts', 'Five of Clubs', 'Five of Diamonds', 'Five of Spades',
            'Four of Hearts', 'Four of Clubs', 'Four of Diamonds', 'Four of Spades',
            'Three of Hearts', 'Three of Clubs', 'Three of Diamonds', 'Three of Spades',
            'Two of Hearts', 'Two of Clubs', 'Two of Diamonds', 'Two of Spades'
        ]

    def createCardDict(self):
        """Create dictionary mapping full card names to appropriate Card objects (defined in holdem_engine.py)"""

        deck = holdem_engine.Deck()
        card_dict = {'-': None}
        for deck_card in deck.cards:
            for card_name in self.card_names:
                if card_name == deck_card.name:
                    card_dict[card_name] = deck_card

        self.card_dict = card_dict

    def createDeckDropDown(self):
        """Build generic deck of cards drop down menu"""

        drop_down_menu = QComboBox(self)
        drop_down_menu.addItems(self.card_names)

        return drop_down_menu

    def createNumOppsDropDown(self):
        """Build drop down menu to select Number of Opponents"""

        drop_down_menu = QComboBox(self)

        num_opps = ['1', '2', '3', '4', '5', '6', '7', '8']

        drop_down_menu.addItems(num_opps)
        return drop_down_menu

    def create_push_button(self):
        """Create push button to run simulation"""

        self.button = QPushButton(self)
        self.button.setText('Run Simulation')
        self.button.setFixedWidth(500)
        self.button.setFixedHeight(30)
        self.button.pressed.connect(lambda: self.button_pressed())

    def button_pressed(self):
        """Function that runs simulation once button is pressed; returns resultant win pct estimate in a popup window"""

        board = [self.card_dict[card_name] for card_name in self.selected_cards[2:]]

        user = holdem_engine.Player()
        user.hole_cards = [self.card_dict[card_name] for card_name in self.selected_cards[:2]]

        self.num_opps = self.drop_down_num_opps.currentText()
        opps = [holdem_engine.Player() for i in range(int(self.num_opps))]

        scenario = simulation_engine.Scenario(user, opps, board)

        sim = simulation_engine.Simulation(scenario)
        sim.run()
        result = sim.result

        msg = QMessageBox()
        msg.setWindowTitle("Simulation Results")
        msg.setText("Estimated Win Probability: " + result + "                      ")

        msg.exec_()

    def createButtonLayout(self):
        """Create layout for Run Simulation button"""

        self.GroupBoxButton = QGroupBox()

        self.create_push_button()

        layout = QGridLayout()
        layout.addWidget(self.button, 0, 0)

        self.GroupBoxButton.setLayout(layout)

    def disableSelectedItem(self, drop_down_menus):
        """Function that disables all cards currently selected in any drop down menu"""

        # generating list of all selected cards (ignoring 'None' option)
        self.selected_cards = [m.currentText() for m in drop_down_menus if m.currentText() != "-"]
        selected_indices = set([menu.currentIndex() for menu in drop_down_menus if menu.currentIndex() != 0])
        for menu in drop_down_menus:
            for i in range(52): # 53 items because 52 playing cards + 'None' option
                if i in selected_indices: # check if item needs to be disabled
                    menu.model().item(i).setEnabled(False) # disable selected item
                elif i not in selected_indices and menu.model().item(i).isEnabled() is False: # check if needs to be enabled
                    menu.model().item(i).setEnabled(True) # re-enable newly de-selected item
                else:
                    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setFont(QFont("Helvetica", 9))
    ex = App()
    sys.exit(app.exec_())
