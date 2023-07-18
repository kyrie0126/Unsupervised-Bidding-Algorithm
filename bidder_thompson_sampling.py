import numpy as np

class Bidder:
    """Class to implement slow-fitting upper confidence bound (UCB) algorithm
    
    Args:
        num_users (int): number of users
        num_rounds (int): number of rounds
    """

    def __init__(self, num_users, num_rounds):
        self.num_rounds = num_rounds
        self.num_users = num_users
        self.current_round = 1
        self.balance = 0
        self.user_id = 0
        self.total_wins = 0
        
        # Beta probability parameters
        # use increments of 0.5 to prevent initial overcorrections
        self.a = [1 for user in range(self.num_users)]
        self.b = [1 for user in range(self.num_users)]
        self.betas = []
        
        # create a max bid that outbids all others
        # this is a second-price auction so hopefully others don't ahve the same strategy lol
        self.history = [0 for user in range(self.num_users)]
        
        self.max_bid = 1.01

    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return f"Bidder's score: {self.balance}"


    def bid(self, user_id):
        """Selects an arm for each round.
        
        Args:
            random_seed (int): The seed for random number generator.
            
        Returns:
            An integer corresponding to the index of the selected 
            arm.
        """
        # Select each arm at least once
        self.user_id = user_id
        self.betas = []
        
        random_seed = np.random.randint(0, 1000)
        np.random.seed(seed=random_seed)
        for i in range(self.num_users):
            temp_val = [round(np.random.beta(self.a[i], self.b[i]),3), i]
                
            # avoid low prob betas
            self.betas.append(temp_val)
        choices = sorted(self.betas, key=lambda x: x[0], reverse=True)
        if self.history[self.user_id] < 10:
            return self.max_bid
        else:
            for [i,v] in choices:
                if v == self.user_id:
                    return round(i,3)
            return 0


    def notify(self, auction_winner, price, clicked = False):
        """Updates the parameters of the chosen arm.
    
        Args:
            chosen_arm (int): The index of the selected arm. 
            reward (int): The reward obtained. Either 0 or 1.
        """
        # track progression through rounds
        self.current_round += 1
        self.history[self.user_id] += 1
        
        #  avoid high costs if others have similar strategies
        if price > self.max_bid:
            if price < 5:
                self.max_bid = price + 0.01
                
        # update if auction is won
        if auction_winner:
            self.total_wins += 1
            if clicked == True:
                # a is based on total counts of successes of an arm
                self.a[self.user_id] += 1
                self.balance += 1 - price
            else:
            # b is based on total counts of failures of an arm
                self.b[self.user_id] += 1
                self.balance -= price
            return self.balance

        