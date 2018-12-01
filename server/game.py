from models import Card, CardValue, CardSuit, Deck, PlayerStatus, Action, Street, HandType, Hand
import collections

NUM_SEATS = 6
SMALL_BLIND_AMOUNT = 1
BIG_BLIND_AMOUNT = 2


#Room contains a list of PlayerStates and a GameState
#Note: position goes clockwise
class Room:
    def __init__(self, room_id):
        self.room_id = room_id #room id
        self.current_occupants = [] # List of users in the room
        self.player_states = {} # player_id to PlayerState
        # self.game_state = GameState() # maybe we want a game state?
        self.board = []
        self.pot = 0
        self.deck = Deck()
        self.positions = [None] * NUM_SEATS # mapping of playerid to location
        self.button_pos = 0
        self.current_turn = 0 # which position in the array is the current turn
        self.allowed_moves = [Action.FOLD, Action.CHECK, Action.CALL, Action.BET, Action.RAISE]
        self.min_raise = BIG_BLIND_AMOUNT #minimum amount you must raise. Based on what the previous person raised by.
        self.history = [] #list of events of this game
        self.street = Street.DEALING
        self.best_hand = {} # mapping of playerid to their best hand based on this board. noned out at the end of each hand

    def __str__(self):
    	return ("Room ID: %s: \nthe current player states are the following: \n\n%s\n\nThe board looks like: \n%s\n\nThe pot is: \n%s\n\nIt's position %s turn\n\n" % (self.room_id, list(self.player_states.values()), self.board, self.pot, self.current_turn))

    def add_player(self, user_id, buy_in, seat):
        #Add a new player with id user_id to our Room
        if (user_id in self.player_states):
        	raise ValueError("two ids are the same in this room nani")
        self.player_states[user_id] = PlayerState(buy_in, user_id, seat)

    def remove_player(self, user_id):
        # Remove the player with user_id from our current room
        # self.current_occupants.remove(user)
        del self.player_states[user_id]

    def begin_hand(self):
    	if (self.positions.count(None) < NUM_SEATS-1):
    		self.deal()
    		self.ante_up()

    	else:
    		raise ValueError("Can't start hand with fewer than 2 ppl")


    def win_pot(self, user_id):
        # Player with user_id wins the pot
        self.player_states[user_id].stack += self.pot
        self.pot = 0

    def end_street():
        # Take all the money players have in and add it to the pot
        for user_id in self.player_states:
            self.pot += self.player_states[user_id].amount_in
            self.player_states[user_id].amount_in = 0

    def deal(self):
        # Deal new cards to all the players
        for player in self.player_states.items():
            player[1].cards = (self.deck.next(), self.deck.next())


    def ante_up(self):
        # Update players to new round with ante and blinds
        self.current_turn = self.button_pos
        if(self.positions.count(None) > NUM_SEATS - 2):
        	print ("multiway")
        	self.nextTurn()
        self.positions[self.current_turn].gamble(SMALL_BLIND_AMOUNT)
        self.nextTurn()
        self.positions[self.current_turn].gamble(BIG_BLIND_AMOUNT)
        self.nextTurn()
        # self.history.append(Event(Action.RAISE, self.positions[self.current_turn].user_id, BIG_BLIND_AMOUNT))
        self.history.append(SMALL_BLIND_AMOUNT)
        self.history.append(BIG_BLIND_AMOUNT)

    def get_allowable_moves(self):
        return self.allowed_moves

    def make_move(self, move, value=None):
        current_player = self.positions[self.current_turn]
        print (str(current_player.user_id) + " is making move " + str(move))
        if (move == Action.FOLD):
            self.fold(current_player.user_id)
        elif (move == Action.CALL):
            self.call(current_player.user_id)
        elif (move == Action.BET):
            self.bet(current_player.user_id, value)
        else:
            self.bet_raise(current_player.user_id, value)
        self.nextTurn()


    def bet(self, user_id, value):
        # user_id bets value
        if (Action.BET in self.allowed_moves and user_id == self.positions[self.current_turn].user_id):
            self.positions[self.current_turn].gamble(value)
            self.history.append(value)
        else:
            raise ValueError

    def bet_raise(self, user_id, value):
        # user_id raises to value
        if (Action.RAISE in self.allowed_moves and user_id == self.positions[self.current_turn].user_id and (value-self.history[-1]) > (self.history[-1]-self.history[-2])):
            self.positions[self.current_turn].gamble(value - self.positions[self.current_turn].amount_in)
            self.history.append(value)
        else:
            raise ValueError

    def call(self, user_id):
        # user_id calls the previous person
        if (Action.CALL in self.allowed_moves and user_id == self.positions[self.current_turn].user_id):
            self.positions[self.current_turn].gamble(self.history[-1] - self.positions[self.current_turn].amount_in)

    def fold(self, user_id):
        # user_id folds        
        self.positions[self.current_turn].status = PlayerStatus.FOLDED

    def sit_down(self, user_id, seat):
        # have a user sit down at a table
        if (self.street == Street.DEALING):
            self.positions[seat] = self.player_states[user_id]
            self.best_hand[user_id] = None
            self.player_states[user_id].status = PlayerStatus.PLAYING
        else:
            raise RuntimeError

    def next_street(self):
        # deal the next street
        if (self.street == Street.FLOP):
            self.board.extend([self.deck.next(), self.deck.next(), self.deck(next)])
        elif (self.street == Street.TURN or self.street == Street.RIVER):
            self.board.append(self.deck.next())
        else:
            raise RuntimeError

    def recalculate_best_hands(self):
        # recalculate the best hand for every single player still in the game
        def calculate_best_hand(cards):
            # takes a list of cards and returns a Hand Object that represents the best hand
            # maybe optimize?

            #calc if flush
            suit_counts = [len(filter(lambda card: card.suit == s, cards)) for s in range(4)]
            is_flush = max(suit_counts) >= 5
            suit = CardSuit(suit_counts.index(max(suit_counts)))
            flush_val = max([lambda card: card.value for suited_card in filter(lambda card: card.suit == suit, cards)])
            
            #calc if straight
            sorted_cards = sorted(cards)
            stack = []
            is_straight = False
            for c in sorted_cards:
                if stack == [] or c.value - 1 == stack[-1]:
                    stack.append(c.value)
                else:
                    stack = []
                if (len(stack >= 5)):
                    is_straight = True
                    straight_val = stack[-1]


            #calc groupings of cards
            groups = collections.Counter(arr)
            ones = [card_value for card_value in groups if groups[card_value] == 1]
            twos = [card_value for card_value in groups if groups[card_value] == 2]
            threes = [card_value for card_value in groups if groups[card_value] == 3]
            fours = [card_value for card_value in groups if groups[card_value] == 4]

            if (is_straight and is_flush):
                return Hand(HandType.STRAIGHTFLUSH, flush_val)
            elif (len(fours) != 0):
                return Hand(HandType.QUADS, max(fours))
            elif (len(threes) > 0 and len(twos) > 1):
                return Hand(HandType.FULLHOUSE, max(threes)*13 + max(filter(twos, lambda x: x != max(threes))))
            elif (is_flush):
                return Hand(HandType.FLUSH, flush_val)
            elif (is_straight):
                return Hand(HandType.STRAIGHT, straight_val)
            elif (len(threes) > 0):
                return Hand(HandType.TRIPS, max(threes))
            elif (len(twos) > 0):
                return Hand(HandType.PAIR, max(twos))
            else:
                return Hand(HandType.HIGHCARD, max(ones))


        for player_id in player_states:
            player = player_states[player_id]
            if (player.status == PlayerStatus.PLAYING):
                self.best_hand[player_id] = calculate_best_hand(self.board + list(player.cards))



    def showdown(self):
        #takes current board and hands and returns the user_id of winner as well as the hand that won it
        max_user = max(self.best_hand, key=lambda k: self.best_hand[k])
        return (max_user, self.best_hand[max_user])

    def nextTurn(self):
        #go to the next player eligible to play a turn
        self.current_turn = (self.current_turn + 1)%NUM_SEATS
        while(self.positions[self.current_turn] == None or self.positions[self.current_turn].status != PlayerStatus.PLAYING):
            self.current_turn = (self.current_turn + 1)%NUM_SEATS



class PlayerState:
    def __init__(self, buy_in, user_id, seat):
        self.stack = buy_in
        self.amount_in = 0
        self.user_id = user_id
        self.seat = seat
        self.status = PlayerStatus.SITTINGOUT
        self.cards = (None, None)

    def __repr__(self):
    	return self.__str__()

    def __str__(self):
    	return ("\n\nPlayerID:%s\nStatus: %s\nStack size: %s\nCurrent cards: %s" % (self.user_id, self.status, self.stack, self.cards))


    def gamble(self, amount):
        if (amount < self.stack):
            self.stack -= amount
            self.amount_in += amount
        else:
            raise ValueError


class Event:
    def __init__(self, action, user_id, amount):
        self.action = action
        self.user_id = user_id
        self.amount = amount






game_room = Room('123')
game_room.add_player("id", 100, 0)
game_room.add_player("id2", 100, 0)
game_room.sit_down("id", 0)
game_room.sit_down("id2", 1)
game_room.begin_hand()
game_room.make_move(Action.RAISE, 5)
print (game_room)