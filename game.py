import numpy as np

import time

class Player:
    def __init__(self,coins):
        self.coins = coins
        self.properties = []
        self.currency_cards = []
    def copy(self):
        player_copy = Player(self.coins)
        player_copy.properties = self.properties.copy()
        player_copy.currency_cards = self.currency_cards.copy()
        return player_copy
    def __str__(self): return f'Coins: {self.coins}\tProperties: {self.properties}\tCurrency Cards: {self.currency_cards}'
    def __repr__(self): return str(self)
class Game:
    def __init__(self):
        self.num_players = 0
        
        self.players = []
        self.player_bids = []
        
        self.current_active_player = None # the current player's turn; essentially self.players[ self.current_active_player_index ]
        self.current_active_player_index = 0 # index for self.players; essentially self.active_players[ self.active_player_turn ]
        
        self.active_players = [] # list[ indices of active players in self.players ]
        self.active_player_turn = 0 # index for self.active_players
        
        self.board = [] # always sort this
        
        self.property_deck = []
        self.currency_deck = []
        
        self.phase = 0 # 1 = bidding for properties, 2 = bidding for currency cards
        
        self.game_config = { 3 : {'coins':18000,'num_cards_to_acquire':8} ,
                             4 : {'coins':18000,'num_cards_to_acquire':7} ,
                             5 : {'coins':14000,'num_cards_to_acquire':6} ,
                             6 : {'coins':14000,'num_cards_to_acquire':5} }

        self.PROPERTY_CARDS = [i for i in range(1,31)]
        self.CURRENCY_CARDS = [i*1000 for i in range(16) if i != 1]*2
    def copy(self):
        game_copy = Game()
        
        game_copy.num_players = self.num_players
        
        game_copy.players = [player.copy() for player in self.players]
        game_copy.player_bids = self.player_bids.copy()
        
        game_copy.current_active_player = game_copy.players[ self.current_active_player_index ]
        game_copy.current_active_player_index = self.current_active_player_index
        
        game_copy.active_players = self.active_players.copy()
        game_copy.active_player_turn = self.active_player_turn
        
        game_copy.board = self.board.copy()
        
        game_copy.property_deck = self.property_deck.copy()
        game_copy.currency_deck = self.currency_deck.copy()
        np.random.shuffle(game_copy.property_deck)
        np.random.shuffle(game_copy.currency_deck)

        game_copy.phase = self.phase

        return game_copy
    def new_game(self,num_players,starting_index=0):
        self.num_players = num_players
        
        self.players = [ Player(self.game_config[num_players]['coins']) for _ in range(num_players) ]
        self.player_bids = [0 for _ in range(num_players)]
        
        self.current_active_player = self.players[starting_index]
        self.current_active_player_index = starting_index
        
        self.active_players = [i for i in range(num_players)]
        self.active_player_turn = starting_index

        self.board = []
        
        self.property_deck = self.PROPERTY_CARDS.copy()
        self.currency_deck = self.CURRENCY_CARDS.copy()
##        for _ in range(self.game_config[num_players]['num_cards_to_remove']):
##            self.property_deck.remove( np.random.choice(self.property_deck) )
##            self.currency_deck.remove( np.random.choice(self.currency_deck) )
        np.random.shuffle(self.property_deck)
        np.random.shuffle(self.currency_deck)

        self.phase = 1
    def get_available_actions(self,coin_limit): # get all available actions for active player (for property bidding phase (1))
        # bidding coins to buy properties
        # coin_limit: integer (in multiples of 1k) that denotes maximum coin_limit you can bid (coin_limit=2 means you can only bid 2000 higher than highest bid)
        assert self.phase == 1
        highest_bid = max(self.player_bids)
        return [ coin_bid for coin_bid in range( highest_bid+1000 , min( highest_bid + coin_limit*1000 + 1 , self.current_active_player.coins+1 ) , 1000 ) ]

##        # selling properties to get currency cards
##        else: return self.current_active_player.properties
    def bid_property(self,coin_bid): # bid for a property
        # the active player bids a number of coins equal to coin_amount, which overwrites his current bid
        # if index == 0, then the active player passes
        # self.board should contain properties sorted from lowest value to highest value
        if coin_bid == 0:
            self.current_active_player.properties.append( self.board.pop(0) )
            self.current_active_player.coins -= np.math.ceil( self.player_bids[ self.current_active_player_index ] / 1000 / 2 ) * 1000
            self.player_bids[ self.current_active_player_index ] = 0

            # next turn
            self.active_players.pop( self.active_player_turn )
            self.active_player_turn = self.active_player_turn % len(self.active_players)
        else:
            self.player_bids[ self.current_active_player_index ] = coin_bid

            # next turn
            self.active_player_turn = (self.active_player_turn+1) % len(self.active_players)

        self.update_current_active_player()
##    def bid_currency(self,property_bid): # bid for currency card
##        self.player_bids[ self.current_active_player_index ] = property_bid
##
##        # next turn
##        self.active_player_turn = (self.active_player_turn+1) % len(self.active_players)
    def update_current_active_player(self):
        self.current_active_player_index = self.active_players[ self.active_player_turn ]
        self.current_active_player = self.players[ self.current_active_player_index ]
##    def play_random_game(self): # play a game with all random actions
##        while len(self.players[0].properties) < self.game_config[self.num_players]['num_cards_to_acquire']: # phase 1 - bidding for properties
##            print(self)
##            self.board.extend( self.property_deck[:self.num_players] )
##            self.board.sort()
##            self.property_deck = self.property_deck[self.num_players:]
##            print(self)
##
##            while len(self.active_players) > 1:
##                available_actions = self.get_available_actions()
##                if len(available_actions) == 0: action = 0
##                else: action = np.random.choice( [ 0 , np.random.choice(available_actions) ] )
##                self.bid_property(action)
##                print(self)
##            self.current_active_player.properties.append( self.board.pop(0) )
##            self.current_active_player.coins -= self.player_bids[ self.current_active_player_index ]
##            self.player_bids[ self.current_active_player_index ] = 0
##            print(self)
##
##            self.active_players = [i for i in range(self.num_players)]
##            self.active_player_turn = self.current_active_player_index
##
##        self.phase = 2        
##        while len(self.players[0].currency_cards) < self.game_config[self.num_players]['num_cards_to_acquire']: # phase 2 - bidding for currency cards
##            print(self)
##            self.board.extend( self.currency_deck[:self.num_players] )
##            self.board.sort()
##            self.currency_deck = self.currency_deck[self.num_players:]
##            print(self)
##
##            for player_index,player in enumerate(self.players): self.player_bids[player_index] = np.random.choice( player.properties )
##            print(self)
##
##            for player_index in np.argsort(self.player_bids): # player indices are sorted from lowest bid to highest bid
##                player = self.players[player_index]
##                player.currency_cards.append( self.board.pop(0) )
##                player.properties.remove( self.player_bids[player_index] )
##                self.player_bids[player_index] = 0
##
##        print(self)
##        return np.argsort( [player.coins + sum(player.currency_cards) for player in self.players] )[::-1]
    def play_human_game(self): # play a game with human input
        
        while len(self.players[0].properties) < self.game_config[self.num_players]['num_cards_to_acquire']: # phase 1 - bidding for properties
            board = input('Property board: ').split()
            self.board = [int(property_card) for property_card in board]
            self.board.sort()
            for property_card in self.board: self.property_deck.remove(property_card)
            print(self)

            while len(self.active_players) > 1:
                property_bid = input(f"Player {self.current_active_player_index}'s property bid (in multiples of $1k): ")

                ### MONTE CARLO SIMULATION ###
                if property_bid == 'mc':
                    self.monte_carlo_sims(2e4)

                    property_bid = input(f"Player {self.current_active_player_index}'s property bid (in multiples of $1k): ")
                ###############################

                property_bid = int(property_bid)
                if property_bid != 0: property_bid *= 1000
                
                self.bid_property(property_bid)

            self.current_active_player.properties.append( self.board.pop(0) )
            self.current_active_player.coins -= self.player_bids[ self.current_active_player_index ]
            self.player_bids[ self.current_active_player_index ] = 0

            self.active_players = [i for i in range(self.num_players)]
            self.active_player_turn = self.current_active_player_index

        self.phase = 2        
        while len(self.players[0].currency_cards) < self.game_config[self.num_players]['num_cards_to_acquire']: # phase 2 - bidding for currency cards
            board = input('Currency board (in multiples of $1k): ').split()
            self.board = [int(property_card)*1000 for property_card in board]
            self.board.sort()
            for currency_card in self.board: self.currency_deck.remove(currency_card)
            print(self)

            currency_bids = input('Currency bids: ')


            ### MONTE CARLO SIMULATION ###
            if 'mc' in currency_bids: # format: 'mc[player_index]', for whatever corresponding player you want to do monte carlo simulations for
                self.current_active_player_index = int(currency_bids[2:]) # should be okay modifying this since phase 2 doesn't use self.current_active_player, self.current_active_player_index, self.active_players, or self.active_player_turn 
                self.current_active_player = self.players[ self.current_active_player_index ] # likewise modifying this should also be okay because it isn't used in phase 2
                self.monte_carlo_sims(6e4)

                currency_bids = input('Currency bids: ')
            ###############################

            currency_bids = currency_bids.split()
            self.player_bids = [int(currency_bid) for currency_bid in currency_bids]

            for player_index in np.argsort(self.player_bids): # player indices are sorted from lowest bid to highest bid
                player = self.players[player_index]
                player.currency_cards.append( self.board.pop(0) )
                player.properties.remove( self.player_bids[player_index] )
                self.player_bids[player_index] = 0

        print(self)
        return np.argsort( [player.coins + sum(player.currency_cards) for player in self.players] )[::-1]
    def monte_carlo_sim(self,chosen_action): # run monte carlo simulation to determine best action for current player represented by self.current_active_player_index
        # chosen action is an action passed by monte_carlo_sims() that denotes what is the first action to take
        # the first action is determined from monte_carlo_sims() to ensure uniform distribution of possible actions at the current game state for current player
        # 
        game_copy = self.copy()
        
        monte_carlo_player_index = self.current_active_player_index # the player index that we are running monte carlo simulation for
        chosen_action_executed = False # once the first chosen_action is executed, we will proceed with monte carlo simulation using pre-defined sampling rules
        
        while len(game_copy.players[0].properties) < game_copy.game_config[game_copy.num_players]['num_cards_to_acquire'] and \
              len(game_copy.players[0].currency_cards) <= 0: # phase 1 - bidding for properties
            if len(game_copy.board) == 0:
##                print(game_copy)
                game_copy.board.extend( game_copy.property_deck[:game_copy.num_players] )
                game_copy.board.sort()
                game_copy.property_deck = game_copy.property_deck[game_copy.num_players:]
##            print(game_copy)

            while len(game_copy.active_players) > 1:
                if not chosen_action_executed: # force execution first chosen_action
                    action = chosen_action
                    chosen_action_executed = True

                else: # after first chosen_action is executed, roll out this game instance with the below sampling rules
                    available_actions = game_copy.get_available_actions(coin_limit=2)
                    # if can't bid any higher, make action automatically pass
                    # otherwise make it a percentage P chance of passing, P being a value such that P**(number of active players excluding current active player) = 0.5
                    if len(available_actions) == 0 or np.random.uniform() < np.e**( np.log(0.5) / ( len(game_copy.active_players)-1 ) ): action = 0
                    else: action = np.random.choice(available_actions) # (1-P) percentage of the time, we will not pass and sample a random action (value) to bid
                
                game_copy.bid_property(action)
##                print(game_copy)
            game_copy.current_active_player.properties.append( game_copy.board.pop(0) )
            game_copy.current_active_player.coins -= game_copy.player_bids[ game_copy.current_active_player_index ]
            game_copy.player_bids[ game_copy.current_active_player_index ] = 0
##            print(game_copy)

            game_copy.active_players = [i for i in range(game_copy.num_players)]
            game_copy.active_player_turn = game_copy.current_active_player_index

        game_copy.phase = 2
        while len(game_copy.players[0].currency_cards) < game_copy.game_config[game_copy.num_players]['num_cards_to_acquire']: # phase 2 - bidding for currency cards
            if len(game_copy.board) == 0:
##                print(game_copy)
                game_copy.board.extend( game_copy.currency_deck[:game_copy.num_players] )
                game_copy.board.sort()
                game_copy.currency_deck = game_copy.currency_deck[game_copy.num_players:]
##            print(game_copy)

            for player_index,player in enumerate(game_copy.players):
                game_copy.player_bids[player_index] = np.random.choice( player.properties )

                if not chosen_action_executed: # force execution first chosen_action
                    game_copy.player_bids[monte_carlo_player_index] = chosen_action
                    chosen_action_executed = True
                
##            print(game_copy)

            for player_index in np.argsort(game_copy.player_bids): # player indices are sorted from lowest bid to highest bid
                player = game_copy.players[player_index]
                player.currency_cards.append( game_copy.board.pop(0) )
                player.properties.remove( game_copy.player_bids[player_index] )
                game_copy.player_bids[player_index] = 0

##        print(game_copy)
        rankings = np.argsort( [player.coins + sum(player.currency_cards) for player in game_copy.players] )[::-1].tolist() # list[ player_indices ], where 0-index has most total money and last-index has least total money
        return rankings.index(monte_carlo_player_index)
    def monte_carlo_sims(self,num_sims): # run self.monte_carlo_sim() multiple times and average the results
        
        results = {} # dict{ action:total_ranking }
        count = {} # dict{ action:count }

        start = time.time()
        
        for _ in range( int(num_sims) ): # TODO: REPLACE THIS NUMBER
            if self.phase == 1: action = np.random.choice( [0] + self.get_available_actions(coin_limit=14) ) # 14 placeholder for infinite, since we want all possible actions for the starting point of monte carlo sim for our player
            else: action = np.random.choice( self.current_active_player.properties ) # if we're in phase 2, self.current_active_player and self.current_active_player_index should be modified already to be the player index that we queried in the input
            
            ranking = self.monte_carlo_sim(action)
            if action not in results:
                results[action] = 0
                count[action] = 0
            results[action] += ranking
            count[action] += 1
            
        print(f'\n{int(num_sims)} simulations run in {time.time()-start} seconds')
        
        average_ranking = []
        actions = []
        for action in results:
            actions.append(action)
            average_ranking.append( results[action]/count[action] )
        for action_index in np.argsort(average_ranking): print(f'Action: {actions[action_index]}\tAverage Ranking: {average_ranking[action_index]}\tTotal Count: {count[actions[action_index]]}')
        print()
    def __str__(self):
        # f'Property Deck: {self.property_deck}\nCurrency Deck: {self.currency_deck}\n' + \
        return '\n\n' + f'Board: {self.board}\nPlayer Bids: {self.player_bids}\n\n' + \
               '\n'.join([f'Player {i}: '+str(player) for i,player in enumerate(self.players)])
    def __repr__(self): return str(self)


if __name__ == '__main__':
    num_players = int(input('Number of players: '))
    starting_index = int(input('Starting index: '))
    
    game = Game()
    game.new_game(num_players,starting_index)
    game.play_human_game()
    
##8 9 14 24 29
##activate ml-cpu
##D:
##cd D:\Desktop\for sale
##python game.py
##mc
