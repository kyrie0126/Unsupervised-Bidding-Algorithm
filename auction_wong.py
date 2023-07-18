import numpy as np

class User:
    """
    Creates a user class that has a secret probability of clicking on an ad.
    T/F actual outputs are tracked for testing purposes.

    Args:
        None
    """
    def __init__(self):
        self.__probability = np.random.uniform(0, 1)
        self.trues = 0
        self.falses = 0

    def __repr__(self):
        return f"My observed click rate was: {self.__str__}"

    def __str__(self):
        return str(self.trues/(self.trues + self.falses))

    def get_probability(self):
        """
        Used to retrieve a user's secret probability
        
        Args:
            None
        """
        return self.__probability

    def show_ad(self):
        """
        Returns True if the user clicks on the ad, False otherwise.
        
        Args:
            None
        """
        out = np.random.choice(a = [True, False], p = [self.__probability, 1 - self.__probability])
        if out:
            self.trues += 1
        else:
            self.falses += 1
        return out

class Auction:
    """
    Creates an auction class that takes in a list of users and bidders.
    
    Args:
        users (list): list of User objects
        bidders (list): list of Bidder objects
    """

    def __init__(self, users, bidders):
        self.users = users
        self.user_id = 0
        self.num_users = len(users)
        self.bidders = bidders
        self.balances = {i:0 for i in range(len(bidders))}

    def __repr__(self):
        return f"The auction winner is bidder {max(self.balances, key=self.balances.get)} with a balance of {max(self.balances.values())}"

    def __str__(self):
        return str(self.balances)

    def execute_round(self):
        """
        Executes a single round of the auction.
        
        Args:
            None
        """
        # user is chosen at random
        random_seed = np.random.randint(0, 1000)
        np.random.seed(seed=random_seed)
        self.user_id = np.random.randint(0, self.num_users)
        
        # bidders are told the user_id, then make a bid
        # bids tracked in tuple of (bid, index)
        bid_list = [(self.bidders[i].bid(self.user_id), i) for i in range(len(self.bidders))]
        max_bid = max(bid_list)
        highest_bidders = []
        losing_bidders = []
        for i in bid_list:
            if i[0] == max_bid[0]:
                highest_bidders.append(i)
            else:
                losing_bidders.append(i)
        everyone_else = sorted(losing_bidders, key=lambda x: x[0], reverse=True)
        
        # edge case with equal highest bets
        if len(highest_bidders) > 1:
            random_winner = np.random.randint(len(highest_bidders))
            auction_winner = highest_bidders[random_winner][1]
            price = highest_bidders[random_winner][0]
        # auction winner pays second-highest bid
        else:
            auction_winner = highest_bidders[0][1]
            price = everyone_else[0][0]
            
        # user is shown ad and clicks with probability
        clicked = self.users[self.user_id].show_ad()
        
        # adjust balances
        self.balances[auction_winner] -= price
        if clicked:
            self.balances[auction_winner] += 1
                
        # notify winners of results
        for i in range(len(self.bidders)):
            if i != auction_winner:
                self.bidders[i].notify(auction_winner=False, price=price, clicked=None)
            else:
                self.bidders[auction_winner].notify(auction_winner=True, price=price, clicked=clicked)
