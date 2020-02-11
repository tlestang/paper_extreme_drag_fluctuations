import csv
# Files extremes.csv contains the index of the events and the corresponding
# peak drag amplitude, in units of sigma
# First row is lowest fluctuation
idx = []
F = []
with open("extremes.csv", mode='r') as extremes_file:
        extremes_reader = csv.reader(extremes_file, delimiter=',')
        line_count=0
        for _idx, _F in extremes_reader:
            idx.append(_idx)
            F.append(_F)

print(idx)
        
