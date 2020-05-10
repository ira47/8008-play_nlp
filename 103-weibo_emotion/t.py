import csv

a=[
    [1,1,2],
    [],
    [2,3]
]
with open('eggs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    spamwriter = csv.writer(csvfile)
    for aa in a:
        spamwriter.writerow(aa)