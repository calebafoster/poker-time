import functools
map = {'A':14,'K':13,'Q':12,'J':11,'T':10,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2}

def cmp_items(card1, card2):
    num1 = map[card1[0]]
    num2 = map[card2[0]]

    if num1 > num2:
        return 1
    elif num1 == num2:
        return 0
    else:
        return -1
    

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.folded = False
        self.points = 0

    def add_to_hand(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def set_hand(self, hand):
        self.hand = hand

    def sort_showdown(self, streets):
        total = self.hand + streets
        
        self.hand = sorted(total, key=functools.cmp_to_key(cmp_items), reverse=True)

    def reset_player(self):
        self.points = 0
        self.clear_hand()
        self.folded = False

    def pair_bool(self, hand):
        working_hand = []
        kicker_hand = []

        for index, card in enumerate(hand):
            for partner in hand[index + 1:]:
                if card[0] == partner[0]:
                    working_hand.append(card)
                    working_hand.append(partner)
                    kicker_hand = [x for x in hand if x not in working_hand]
                    break
            if kicker_hand:
                break

        if len(working_hand) == 2:
            for i in range(5 - len(working_hand)):
                working_hand.append(kicker_hand[i])
            self.hand = working_hand
            return True
        else:
            return False

    def two_pair_bool(self, hand):
        working_hand = []
        kicker_hand = []

        for index, card in enumerate(hand):
            for partner in hand[index + 1:]:
                if card[0] == partner[0]:
                    working_hand.append(card)
                    working_hand.append(partner)
                    kicker_hand = [x for x in hand if x != card and x != partner]
                    break
            if kicker_hand:
                break

        for index, card in enumerate(kicker_hand):
            for partner in kicker_hand[index + 1:]:
                if card[0] == partner[0]:
                    working_hand.append(card)
                    working_hand.append(partner)
                    kicker_hand = [x for x in hand if x not in working_hand]
                    break
            if len(working_hand) == 4:
                break

        if len(working_hand) == 4:
            for i in range(5 - len(working_hand)):
                working_hand.append(kicker_hand[i])
            self.hand = working_hand
            return True
        else:
            return False

    def set_bool(self, hand):
        working_hand = []
        kicker_hand = []
        count = 1

        for index, card in enumerate(hand):
            if count == 3:
                kicker_hand = [x for x in hand if x not in working_hand]
                break

            working_hand = [hand[index]]
            count = 1
            for partner in hand[index + 1:]:
                if card[0] == partner[0]:
                    count = count + 1
                    working_hand.append(partner)

        if len(working_hand) == 3:
            for i in range(5 - len(working_hand)):
                working_hand.append(kicker_hand[i])
            self.hand = working_hand
            return True
        else:
            return False

    def straight_bool(self, hand):
        count = 1
        working_hand = []

        for index,card in enumerate(hand[:-1]):
            if index == 0:
                working_hand.append(card)

            if map[card[0]] == map[hand[index + 1][0]] + 1:
                count = count + 1
                working_hand.append(hand[index + 1])

                if count == 5:
                    self.hand = working_hand
                    return True
                elif count == 4 and map[working_hand[-1][0]] == 2 and any(x[0] == 'A' for x in hand):
                    working_hand.append(hand[0])
                    self.hand = working_hand
                    return True

            elif map[card[0]] == map[hand[index + 1][0]]:
                pass

            else:
                count = 1
                working_hand = []
                working_hand.append(hand[index + 1])

        return False

    def flush_bool(self, hand):
        count = [0,0,0,0]
        suits = ['s','d','c','h']
        working_hand = []

        for index,suit in enumerate(suits):
            working_hand = []

            for card in hand:
                if card[1] == suit:
                    count[index] = count[index] + 1
                    working_hand.append(card)

            if count[index] >= 5:
                self.hand = working_hand
                return True

        return False

    def full_house_bool(self, hand):
        working_hand = []
        kicker_hand = []
        count = 1
        three = False
        pair = False

        for index, card in enumerate(hand):
            if count == 3:
                three = True
                count = 1
                kicker_hand = [x for x in hand if x not in working_hand]
                break

            working_hand = [hand[index]]
            count = 1
            for partner in hand[index + 1:]:
                if card[0] == partner[0]:
                    count = count + 1
                    working_hand.append(partner)

        for index, card in enumerate(kicker_hand):
            if count == 2:
                pair = True
                break
            count = 1
            for partner in kicker_hand[index + 1:]:
                if card[0] == partner[0]:
                    count = count + 1
                    working_hand.append(card)
                    working_hand.append(partner)

        if three and pair:
            self.hand = working_hand
            return True
        else:
            return False

    def quad_bool(self, hand):
        working_hand = []
        count = 1
        kicker_hand = []

        for index, card in enumerate(hand):
            if count == 4:
                kicker_hand = [x for x in hand if x not in working_hand]
                break

            working_hand = [hand[index]]
            count = 1
            for partner in hand[index + 1:]:
                if card[0] == partner[0]:
                    count = count + 1
                    working_hand.append(partner)

        if len(working_hand) == 4:
            for i in range(5 - len(working_hand)):
                working_hand.append(kicker_hand[i])
            self.hand = working_hand
            return True
        else:
            return False

    def straight_flush_bool(self, hand):
        count = [0,0,0,0]
        suits = ['s','d','c','h']
        working_hand = []

        for index,suit in enumerate(suits):
            working_hand = []

            for card in hand:
                if card[1] == suit:
                    count[index] = count[index] + 1
                    working_hand.append(card)

            if count[index] >= 5:
                break
            elif index == 3:
                return False

        if self.straight_bool(working_hand):
            return True
        else:
            return False

    def royal_bool(self, hand):
        key = ['A','K','Q','J','T']
        working_hand = []

        for card in hand:
            for num in key:
                if card[0] == num:
                    working_hand.append(card)

        if self.flush_bool(working_hand):
            return True
        else:
            return False

    def eval_hand(self, hand):
        if self.royal_bool(hand):
            print(f"{self.name} has a royal flush")
            self.points = 9
        elif self.straight_flush_bool(hand):
            print(f"{self.name} has a straight flush")
            self.points = 8
        elif self.quad_bool(hand):
            print(f"{self.name} has four of a kind")
            self.points = 7
        elif self.full_house_bool(hand):
            print(f"{self.name} has a full house")
            self.points = 6
        elif self.flush_bool(hand):
            print(f"{self.name} has a flush")
            self.points = 5
        elif self.straight_bool(hand):
            print(f"{self.name} has a straight")
            self.points = 4
        elif self.set_bool(hand):
            print(f"{self.name} has three of a kind")
            self.points = 3
        elif self.two_pair_bool(hand):
            print(f"{self.name} has two pairs")
            self.points = 2
        elif self.pair_bool(hand):
            print(f"{self.name} has a pair")
            self.points = 1
        else:
            self.hand = self.hand[:5]
            print(f"{self.name} has {hand[0][0]} high")
            self.points = 0


if __name__ == "__main__":
    streets = ['5c','4s','4c','3s', '2h']
    test = Player("test")
    test.set_hand(['7s','6s'])
    test.sort_showdown(streets)
    print(test.straight_bool(test.hand))
    print(test.hand)
