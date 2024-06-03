import csv
from os import listdir
from collections import defaultdict
import numpy as np
from datetime import datetime as dt
import warnings

records = defaultdict(list)

MIN_DATE = dt(2024, 6, 3)
MAX_DATE = dt.now()


for fname in listdir('Games'):
    timestamp = fname[7:-4]
    date = dt.fromtimestamp(int(timestamp))
    if not MIN_DATE < date < MAX_DATE: continue
    with open('Games/'+fname, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            records[row[-1]].append(tuple(map(int, row[:-1])))

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
    for rnd in record:
        bids.append(rnd[0])
        makes.append(rnd[1])
        busts.append(rnd[2])
        if rnd[0] != 0:
            if rnd[0] < rnd[1]:
                underbids.append(rnd[1]-rnd[0])
            elif rnd[1] < rnd[0]:
                overbids.append(rnd[1]-rnd[0])
            else:
                perfect += 1
        else:
            zero_bid += 1
            if rnd[1] == 0:
                perfect += 1
                zero_made += 1

    bids = np.array(bids)
    makes = np.array(makes)

    warnings.filterwarnings('ignore')
    print(name.upper())
    print(f'Average bid: {round(np.mean(bids), 2)} ± {round(np.std(bids), 2)}')
    print(f'Average made: {round(np.mean(makes), 2)} ± {round(np.std(makes), 2)}')
    print(f'Average miss: {round(np.mean(makes-bids), 2)} ± {round(np.std(makes-bids), 2)}')
    #print(f'Average miss magnitude: {round(np.mean(np.abs(makes - bids)), 2)} ± {round(np.std(np.abs(makes - bids)), 2)}')
    print(f'Average magnitude of overbids: {round(np.mean(overbids), 2)} ± {round(np.std(overbids), 2)}')
    print(f'Average magnitude of underbids: {round(abs(np.mean(underbids)), 2)} ± {round(np.std(underbids), 2)}')
    print(f'Team bust rate: {round(sum(busts) / len(record) * 100)}%')
    #print(f'Zero bid rate: {round(zero_bid / len(record) * 100)}%')
    print(f'Zero success rate: {round(zero_made / len(record) * 100)}%')
    print(f'Over/perfect/under bid rates: {round(len(overbids)/len(record)*100)}% / {round(perfect/len(record)*100)}% / {round(len(underbids)/len(record)*100)}%')
    print('-'*30)