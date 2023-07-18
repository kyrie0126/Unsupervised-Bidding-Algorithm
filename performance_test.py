from auction import User, Auction
import bidder_thompson_sampling
import bidder_ucb
import numpy as np



if __name__ == "__main__":
    #TODO: Remove before submission or place in third file (like main.py)

    # change these to test bidder 
    # should work with any positive int for any of the values below
    num_rounds = 1000
    num_users = 1
    num_bidders = 2

    # Generates lists of bidders, users, then constructs the Auction with them
    bidders = [bidder_thompson_sampling.Bidder(num_users=num_users, num_rounds=num_rounds),
               bidder_ucb.Bidder(num_users=num_users, num_rounds=num_rounds)]
    users = [User() for _ in range(num_users)]
    auction = Auction(users, bidders)

    # # Runs each auction round
    for round_number in range(num_rounds):
        # print(f'{round_number=}')
        auction.execute_round()
    
    # User Data
    for i in range(len(users)):
        print(f'User {i} Secret Probability: {users[i].get_probability()}')
    for i in range(len(users)):
        print(f'User {i} Actual Output: {users[i].trues/(users[i].falses + users[i].trues)}\n')
        
    # Thompson Sampling Performance
    print(f'Thompson: {bidders[0].balance}')
    print(f'Thompson total wins: {bidders[0].total_wins}')
    for i in range(len(users)):
        # self.betas.append([round(np.random.beta(sum(self.a[i]), sum(self.b[i])),3), i])
        print(f"Thompson Sampling Estimate for User {i}: {np.random.beta(bidders[0].a[i], bidders[0].b[i])}")
    print('\n')
    # UCB Performance
    print(f'bidder_wong (ucb) sampling: {bidders[1].balance}')
    print(f'bidder_wong (ucb) total wins: {bidders[1].total_wins}')
    for key, val in bidders[1].history.items():
        if val:
            print(f"UCB Estimate for User {key}: {np.mean(val)}")

 

