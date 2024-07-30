import csv, time, os

ZERO_SCORE_ADD = 70

TIMESTAMP = str(int(time.time()))

def get_input(prompt: str):
    inp = ''
    while not inp:
        inp = input(prompt).strip()
    for i,interrupt in enumerate(Game.INTERRUPTS):
        if inp == interrupt[0]:
            return i
    return inp

class Team:
    def __init__(self, i, players=2, names=()):
        self.players = players
        self.i = i
        if not names:
            self.names = tuple(input(f'Team {self.i} player {j+1}: ').title().strip() for j in range(players))
        else:
            self.names = names
            for j in range(players):
                print(f'Team {self.i} player {j+1}:', self.names[j])
        
        self.score = 0
        self.bids = [0]*players
        self.tricks = [0]*players

        self.stats = [] # bid, made, team_bust?, name, uuid

    def playerlist(self):
        return '/'.join(self.names)

    def get_bids(self):
        for i,name in enumerate(self.names):
            inp = get_input(f'{name}\'s bid: ')
            if type(inp) is int: return inp
            self.bids[i] = int(inp)

    def get_tricks(self, round_tricks_list):
        for i,name in enumerate(self.names):
            if len(round_tricks_list) < 3:
                inp = get_input(f'{name}\'s tricks: ')
                if type(inp) is int: return inp
                self.tricks[i] = int(inp)
                round_tricks_list.append(int(inp))

            else:
                last = 13-sum(round_tricks_list)
                self.tricks[i] = last
                print(f'{name}\'s tricks:', last)

    def add_score(self, round_i):
        global TIMESTAMP

        bust = 1
        if sum(self.tricks) >= sum(self.bids):
            self.score += sum(self.bids)*10 + (sum(self.tricks) - sum(self.bids))
            bust = 0

        for trick, bid, name in zip(self.tricks, self.bids, self.names):
            self.stats.append((bid, trick, bust, name, f'{TIMESTAMP}-{round_i:03}-{self.i}'))
            
            if bid == 0:
                if trick == 0:
                    self.score += ZERO_SCORE_ADD
                else:
                    self.score -= ZERO_SCORE_ADD

class Game:
    INTERRUPTS = [
        ('CANCEL', 'Round canceled!'),
        ('FORFEIT', 'Victory by forfeit!')
    ]

    AYEL_PLAYERS = (('Aviva', 'Yovel'), ('Ezra', 'Leia'))

    def __init__(self, teams=2, players_per_team=2, ayel=False):
        if ayel:
            self.teams = [Team(i+1, players=players_per_team, names=Game.AYEL_PLAYERS[i]) for i in range(teams)]
        else:
            self.teams = [Team(i+1, players=players_per_team) for i in range(teams)]
        self.end = int(input('Score we are playing to: '))

    def save(self):
        os.makedirs('Games', exist_ok=True)
        with open('Games/spades_'+TIMESTAMP+'.txt', 'w') as f:
            writer = csv.writer(f, delimiter=' ')
            for team in self.teams:
                for stat in team.stats:
                    writer.writerow(stat)

    def start(self):
        global TIMESTAMP
        
        i = 1
        while True:
            interrupt = self.round(i)
            if interrupt == 0:
                continue
            possible_winner = max(self.teams, key=(lambda t: t.score))
            if interrupt == 1 or possible_winner.score > self.end:
                print(f'\n{possible_winner.playerlist()} wins!  {self.score()}')
                self.save()
                return i
            i += 1
    
    def score(self):
        scores = '-'.join(str(team.score) for team in self.teams)
        return f'({scores})'
        
    def round(self, i):
        print(f"\nRound {i}  {self.score()}")
        print("="*30)

        # collect bids
        for team in self.teams:
            inter = team.get_bids()
            if inter is not None:
                print(Game.INTERRUPTS[inter][1])
                return inter

        print("="*30)

        # collect tricks
        round_tricks_list = []
        for team in self.teams:
            inter = team.get_tricks(round_tricks_list)
            if inter is not None:
                print(Game.INTERRUPTS[inter][1])
                return inter
            team.add_score(i)

        

if __name__ == "__main__":
    g = Game(teams=2, ayel=True)
    g.start()
