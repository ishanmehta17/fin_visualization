import json

f = open('../data/orig/Real Estate.json')

data = json.load(f)

cumulative_change = {}
sum = 0

for i in data:
    sum += data[i]
    cumulative_change[i] = sum

f.close()

with open("../data/cumulative/Real Estate.json", "w") as outfile:
    json.dump(cumulative_change, outfile)

