import csv
from os import listdir
from collections import defaultdict
import numpy as np
from datetime import datetime as dt

records = defaultdict(list)

MIN_DATE = dt(2024, 6, 3)
MAX_DATE = dt.now()
PRINT_EXTRA = True


for fname in listdir('Games'):
    timestamp = fname[7:-4]
    date = dt.fromtimestamp(int(timestamp))
    if not MIN_DATE < date < MAX_DATE: continue
    with open('Games/'+fname, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            records[row[3]].append(tuple(map(int, row[:3])))

print('All records from', MIN_DATE.strftime('%Y-%m-%d %H:%M:%S'), 'to', MAX_DATE.strftime('%Y-%m-%d %H:%M:%S'))
print('='*60)
for name, record in records.items():

    bids = []
    makes = []
    busts = []
    overbids = []
    underbids = []
    zero_bid = 0
    zero_made = 0
    perfect = 0
    non_zero_bid = 0
    for rnd in record:
        bids.append(rnd[0])
        makes.append(rnd[1])
        busts.append(rnd[2])
        if rnd[0] != 0:
            non_zero_bid += 1
            if rnd[0] < rnd[1]:
                underbids.append(rnd[1]-rnd[0])
            elif rnd[1] < rnd[0]:
                overbids.append(rnd[1]-rnd[0])
            else:
                perfect += 1
        else:
            zero_bid += 1
            if rnd[1] == 0:
                zero_made += 1

    bids = np.array(bids)
    makes = np.array(makes)

    print(name.upper())
    if PRINT_EXTRA: print('Core Stats:')
    print(f'\tAverage bid: {round(np.mean(bids), 2)} ± {round(np.std(bids), 2)}')
    print(f'\tAverage made: {round(np.mean(makes), 2)} ± {round(np.std(makes), 2)}')
    print(f'\tAverage underbid: {round(np.mean(makes-bids), 2)} ± {round(np.std(makes-bids), 2)}')
    print(f'\tAverage misbid magnitude: {round(np.mean(np.abs(makes - bids)), 2)} ± {round(np.std(np.abs(makes - bids)), 2)}')

    if non_zero_bid != 0:
        print(f'\tNonzero over/perfect/under rates: {round(len(overbids)/non_zero_bid*100)}% / {round(perfect/non_zero_bid*100)}% / {round(len(underbids)/non_zero_bid*100)}%')
    else:
        print(f'\tNonzero over/perfect/under rates: 0% / 0% / 0%')

    if zero_bid != 0:
        print(f'\tZero success rate: {round(zero_made / zero_bid * 100)}% ({zero_made}/{zero_bid})')
    else:
        print(f'\tZero success rate: n/a')

    print(f'\tTeam bust rate: {round(sum(busts) / len(record) * 100, 2)}%')

    if PRINT_EXTRA:
        print('Extra Stats:')
        if len(overbids) != 0:
            print(f'\tAverage magnitude of overbids: {round(np.mean(np.abs(overbids)), 2)} ± {round(np.std(overbids), 2)}')
        else:
            print(f'\tAverage magnitude of overbids: n/a')
        if len(underbids) != 0:
            print(f'\tAverage magnitude of underbids: {round(abs(np.mean(underbids)), 2)} ± {round(np.std(underbids), 2)}')
        else:
            print(f'\tAverage magnitude of underbids: n/a')


        print(f'\tZero bid rate: {round(zero_bid / len(record) * 100, 2)}%')


    print('-'*30)
