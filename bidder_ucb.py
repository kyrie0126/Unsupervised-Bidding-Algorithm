import numpy as np

class Bidder:
    """
    Creates a bidder class that utilizes an Upper Confidence Bound (UCB) approach for unsupervised bid optimization.
    
    Args:
        num_users (int): number of users in the auction
        num_rounds (int): number of rounds in the auction
    """

    def __init__(self, num_users, num_rounds):
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.current_round = 1
        self.user_id = 0
        self.balance = 0
        self.total_wins = 0
        self.max_bid = 1.01
        
        # UCB init
        self.history = {user_id: [0.5] for user_id in range(num_users)}
        
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Bidder's score: {sum(self.balance)}"

    def bid(self, user_id):
        """
        Return non-negative amount of money, in dollars rounded to three decimal places.
        Will use upper confidence bound algorithm to determine bid: mu + ucb.
        
        Args:
            user_id (int): the id of the user to bid for
        """
        self.user_id = user_id
        self.current_round += 1
        
        if len(self.history[self.user_id]) < 5:
            return self.max_bid
        else:
            return round(np.mean(self.history[self.user_id]) + np.sqrt(np.log(self.current_round)/len(self.history[self.user_id])),3)

    def notify(self, auction_winner, price, clicked = None):
        """
        Used to send information about what happened in a round back to the bidder.
        
        Args:
            auction_winner (bool): whether or not the bidder won the auction
            price (float): the price of the second highest bid
            clicked (bool): whether or not the user clicked on the ad
        """
        
        # If won, update info
        if auction_winner:
            self.total_wins += 1
            if clicked:
                self.balance += 1 - price
                self.history[self.user_id].append(1)
            else:
                self.balance -= price
                self.history[self.user_id].append(0)
                
        #  Update max_bid logic with info about other's bidding behaviors - but cap at 5
        if price > self.max_bid:
            if price < 5:
                self.max_bid = price + 0.01
        
