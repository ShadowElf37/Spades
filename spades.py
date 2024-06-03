import csv, time
import os

ZERO_SCORE_ADD = 70        

class Team:
    def __init__(self, i, players=2):
        self.players = players
        self.i = i+1
        self.names = [input(f'Team {self.i} player {j+1}: ').title().strip() for j in range(players)]
        
        self.score = 0
        self.bids = [0]*players
        self.tricks = [0]*players

        self.stats = [] # bid, made, name

    def playerlist(self):
        return '/'.join(self.names)

    def get_bids(self):
        for i,name in enumerate(self.names):
            self.bids[i] = int(input(f'{name}\'s bid: '))
    def get_tricks(self):
        for i,name in enumerate(self.names):
            self.tricks[i] = int(input(f'{name}\'s tricks: '))

    def add_score(self):
        bust = 1
        if sum(self.tricks) >= sum(self.bids):
            self.score += sum(self.bids)*10 + (sum(self.tricks) - sum(self.bids))
            bust = 0

        for trick, bid, name in zip(self.tricks, self.bids, self.names):
            self.stats.append((bid, trick, bust, name))
            
            if bid == 0:
                if trick == 0:
                    self.score += ZERO_SCORE_ADD
                else:
                    self.score -= ZERO_SCORE_ADD

class Game:
    def __init__(self, teams=2, players_per_team=2):
        self.teams = [Team(i, players=players_per_team) for i in range(teams)]
        self.end = int(input('Score we are playing to: '))

    def start(self):
        i = 0
        while True:
            i += 1
            self.round(i)

            if (winner := max(self.teams, key=(lambda t: t.score))).score > self.end:
                print(f'\n{winner.playerlist()} wins!  {self.score()}')

                os.makedirs('Games', exist_ok=True)
                with open('Games/spades_'+str(int(time.time()))+'.txt', 'w') as f:
                    writer = csv.writer(f, delimiter=' ')
                    for team in self.teams:
                        for stat in team.stats:
                            writer.writerow(stat)
                return i
    
    def score(self):
        scores = '-'.join(str(team.score) for team in self.teams)
        return f'({scores})'
        
    def round(self, i):
        print(f"\nRound {i}  {self.score()}")
        print("="*30)
        for team in self.teams:
            team.get_bids()
        print("="*30)
        for team in self.teams:
            team.get_tricks()
            team.add_score()

        

if __name__ == "__main__":
    g = Game(teams=2)
    g.start()
