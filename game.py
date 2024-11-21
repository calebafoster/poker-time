from player import Player, map
from deck import Deck

class Game:
    def __init__(self, players):
        self.players = self.set_players(players)
        self.active_players = self.players
        self.winner = ''

        self.active = Deck()
        self.streets = []

    def deal(self):
        for n in range(2):
            for player in self.active_players:
                card = self.active.remove_top_card()
                self.active_players[player].add_to_hand(card)

    def grant_hand(self, player, hand):
        for card in self.active_players[player].hand:
            self.active.add_card(card)

        for card in hand:
            self.active.remove_specific_card(card)

        self.active_players[player].hand = hand

    def set_players(self, names = ["test"]):
        players = {}

        for name in names:
            players[name] = Player(name = name)
        return players

    def flop(self):
        self.active.remove_top_card()
        for i in range(3):
            self.streets.append(self.active.remove_top_card())
        print(self.streets)

    def turn(self):
        self.active.remove_top_card()
        self.streets.append(self.active.remove_top_card())
        print(self.streets)
    
    def river(self):
        self.active.remove_top_card()
        self.streets.append(self.active.remove_top_card())
        print(self.streets)

    def set_streets(self, streets):
        self.streets = streets

    def reset_game(self):
        self.active_players = self.players
        for player in self.active_players:
            self.active_players[player].reset_player()
        self.active = Deck()
        self.streets = []

    def determine_winner(self):
        chop = []
        ties = []
        current_winner = ''

        for player in self.active_players:
            self.active_players[player].sort_showdown(self.streets)
            self.active_players[player].eval_hand(self.active_players[player].hand)
            print(self.active_players[player].hand)
        
        for index, player in enumerate(self.active_players):
            if index == 0:
                current_winner = player
            else:
                if self.active_players[current_winner].points < self.active_players[player].points:
                    current_winner = player
                    ties = []
                elif self.active_players[current_winner].points == self.active_players[player].points:
                    ties.append(current_winner)
                    ties.append(player)
                    current_winner = player

        if ties:
            for player in ties:
                self.active_players[player].points = 0
                for card in self.active_players[player].hand:
                    self.active_players[player].points = self.active_players[player].points + map[card[0]]

            for index, player in enumerate(ties):
                if index == 0:
                    current_winner = player
                else:
                    if self.active_players[current_winner].points < self.active_players[player].points:
                        current_winner = player
                        chop = []
                    elif self.active_players[current_winner].points == self.active_players[player].points:
                        chop.append(current_winner)
                        chop.append(player)
                        current_winner = player
   
        else:
            self.winner = current_winner

        if chop:
            self.winner = f"{chop}"
        else:
            self.winner = current_winner


if __name__ == '__main__':
    game = Game(["Caleb", "Manda", "Blake"])
    game.deal()
    game.flop()
    game.turn()
    game.river()
    game.determine_winner()
    print(game.winner)
    pass
