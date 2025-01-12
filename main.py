"""
Single-file War card game with Kivy for cross-platform (Android/iOS) builds.
To package for mobile:
1) Install Kivy (pip install kivy).
2) Install Buildozer (pip install buildozer) on Linux/WSL (or use kivy-ios on macOS for iOS).
3) Run 'buildozer init' in the same folder. Edit buildozer.spec as needed.
4) buildozer android debug (or release) -- or buildozer ios debug, etc.
"""

import random
import os
from datetime import datetime

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color

# ---------- Card, Deck, and Player Classes (same logic as before) ---------- #
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.get_value()

    def get_value(self):
        rank_values = {'2': 2, '3': 3, '4': 5, '5': 5, '6': 6, '7': 7, '8': 8,
                       '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return rank_values[self.rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal(self):
        mid = len(self.cards) // 2
        return self.cards[:mid], self.cards[mid:]

class Player:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.cards_won = 0  # track how many cards the player has won

    def play_card(self):
        return self.cards.pop(0) if self.cards else None

    def add_cards(self, cards):
        self.cards.extend(cards)
        self.cards_won += len(cards)

    def card_count(self):
        return len(self.cards)

# ---------- The Main Kivy App Class ---------- #
class WarApp(App):
    def build(self):
        """
        This is called once when the app starts.
        We'll build the layout with BoxLayouts and Buttons, 
        then initialize the game logic.
        """
        # Root layout
        self.root_layout = FloatLayout()

        # Initialize game data
        self.human_player = 1
        self.start_time = None
        self.end_time = None
        self.rounds_played = 0
        self.winner = None
        self.center_pile = []
        self.deck = Deck()
        p1_cards, p2_cards = self.deck.deal()
        self.player1 = Player("Player 1", p1_cards)
        self.player2 = Player("Player 2", p2_cards)

        # Start time
        self.start_time = datetime.now()

        # -- Create UI components --
        # Player 1 info
        self.label_p1_title = Label(text="Player 1 👤", size_hint=(0.4, 0.1), pos_hint={"x": 0.05, "y": 0.85})
        self.label_p1_card = Label(text="(card here)", size_hint=(0.4, 0.1), pos_hint={"x": 0.05, "y": 0.75})
        self.label_p1_count = Label(text="Cards: 26", size_hint=(0.4, 0.1), pos_hint={"x": 0.05, "y": 0.65})

        # Player 2 info
        self.label_p2_title = Label(text="Player 2 🤖", size_hint=(0.4, 0.1), pos_hint={"x": 0.55, "y": 0.85})
        self.label_p2_card = Label(text="(card here)", size_hint=(0.4, 0.1), pos_hint={"x": 0.55, "y": 0.75})
        self.label_p2_count = Label(text="Cards: 26", size_hint=(0.4, 0.1), pos_hint={"x": 0.55, "y": 0.65})

        # Play Next Round button
        self.btn_play = Button(
            text="Play Next Round",
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0.35, "y": 0.45},
            on_release=self.play_round
        )

        # Settings button
        self.btn_settings = Button(
            text="⚙️ Settings",
            size_hint=(0.2, 0.07),
            pos_hint={"x": 0.05, "y": 0.05},
            on_release=self.open_settings_menu
        )

        # Add UI components to root_layout
        self.root_layout.add_widget(self.label_p1_title)
        self.root_layout.add_widget(self.label_p1_card)
        self.root_layout.add_widget(self.label_p1_count)

        self.root_layout.add_widget(self.label_p2_title)
        self.root_layout.add_widget(self.label_p2_card)
        self.root_layout.add_widget(self.label_p2_count)

        self.root_layout.add_widget(self.btn_play)
        self.root_layout.add_widget(self.btn_settings)

        # Return the root layout to display
        return self.root_layout

    # ---------- Game Logic Methods (Adapted for Kivy) ---------- #
    def play_round(self, *args):
        # Check if either player is out of cards
        if not self.player1.cards or not self.player2.cards:
            self.check_winner()
            return

        # Each player flips a card
        p1_card = self.player1.play_card()
        p2_card = self.player2.play_card()

        # Update UI
        self.label_p1_card.text = str(p1_card)
        self.label_p2_card.text = str(p2_card)

        # Add to center pile
        self.center_pile.extend([p1_card, p2_card])

        # Compare values
        if p1_card.value > p2_card.value:
            self.player1.add_cards(self.center_pile)
            self.center_pile = []
        elif p2_card.value > p1_card.value:
            self.player2.add_cards(self.center_pile)
            self.center_pile = []
        else:
            # War scenario
            self.handle_war()

        self.rounds_played += 1
        self.update_gui()

    def handle_war(self):
        # Each player places 3 additional cards if they have them
        for _ in range(3):
            if self.player1.cards:
                self.center_pile.append(self.player1.play_card())
            if self.player2.cards:
                self.center_pile.append(self.player2.play_card())

        # Flip next card to decide the war, or end game if a player runs out
        if self.player1.cards and self.player2.cards:
            self.play_round()  # Recursively compare again
        else:
            self.check_winner()

    def check_winner(self):
        self.end_time = datetime.now()
        if self.player1.card_count() > self.player2.card_count():
            self.winner = "Player 1"
            winner_text = "🎉 Player 1 wins the game! 🎉"
        elif self.player2.card_count() > self.player1.card_count():
            self.winner = "Player 2"
            winner_text = "🎉 Player 2 wins the game! 🎉"
        else:
            self.winner = "Tie"
            winner_text = "It's a tie!"

        self.show_winner_popup(winner_text)

    def update_gui(self):
        """Refresh the card counts on the screen."""
        self.label_p1_count.text = f"Cards: {self.player1.card_count()}"
        self.label_p2_count.text = f"Cards: {self.player2.card_count()}"

    # ---------- Popups / Overlays ---------- #
    def show_winner_popup(self, winner_text):
        # A Kivy Popup to show final results
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text=winner_text, font_size=20))

        btn_export = Button(text="Export Stats", size_hint=(1, 0.2))
        btn_export.bind(on_release=self.export_stats_to_file)
        box.add_widget(btn_export)

        btn_close = Button(text="Close", size_hint=(1, 0.2))
        btn_close.bind(on_release=lambda *_: self.stop())  # .stop() ends the app
        box.add_widget(btn_close)

        popup = Popup(
            title="Game Over",
            content=box,
            size_hint=(0.8, 0.5)
        )
        popup.open()

    def open_settings_menu(self, *args):
        # Simple popup with settings
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        btn_view_stats = Button(text="View Stats")
        btn_view_stats.bind(on_release=lambda *_: self.show_stats())
        box.add_widget(btn_view_stats)

        btn_export = Button(text="Export Stats")
        btn_export.bind(on_release=lambda *_: self.export_stats_to_file())
        box.add_widget(btn_export)

        btn_close = Button(text="Close")
        box.add_widget(btn_close)

        popup = Popup(
            title="Settings",
            content=box,
            size_hint=(0.8, 0.5)
        )
        btn_close.bind(on_release=popup.dismiss)

        popup.open()

    # ---------- Stats & Export ---------- #
    def show_stats(self):
        duration = (datetime.now() - self.start_time) if self.end_time is None else (self.end_time - self.start_time)
        text = (
            f"Game Start: {self.start_time}\n"
            f"Game End:   {self.end_time if self.end_time else 'In Progress'}\n"
            f"Duration:   {duration}\n"
            f"Rounds Played: {self.rounds_played}\n\n"
            f"Current Winner: {self.winner if self.winner else 'Undecided'}\n\n"
            f"Player 1 Cards Won: {self.player1.cards_won}\n"
            f"Player 2 Cards Won: {self.player2.cards_won}\n"
        )
        self._show_popup("Game Stats", text)

    def export_stats_to_file(self, *args):
        duration = (datetime.now() - self.start_time) if self.end_time is None else (self.end_time - self.start_time)
        stats_str = (
            f"Date/Time:     {datetime.now()}\n"
            f"Winner:        {self.winner}\n"
            f"Rounds Played: {self.rounds_played}\n"
            f"Duration:      {duration}\n"
            f"Player 1 Won:  {self.player1.cards_won} cards\n"
            f"Player 2 Won:  {self.player2.cards_won} cards\n"
            "----------------------------------------\n"
        )
        filename = "war_stats.txt"
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(stats_str)
            self._show_popup("Export Stats", f"Stats exported to:\n{os.path.abspath(filename)}")
        except Exception as e:
            self._show_popup("Export Stats Error", f"Failed to export stats:\n{e}")

    def _show_popup(self, title, msg):
        """Utility function to show a quick info popup."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=msg))
        btn_close = Button(text="Close", size_hint=(1, 0.2))
        content.add_widget(btn_close)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.5))
        btn_close.bind(on_release=popup.dismiss)
        popup.open()


# ---------- Launch the App ---------- #
if __name__ == "__main__":
    WarApp().run()
