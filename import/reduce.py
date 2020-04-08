import csv

# Opens large tsv file and creates a new one with limited number (100,000) rows

# Run once with title.ratings.tsv and ratings.csv, then run again with title.basics.tsv and shows.csv
with open("title.ratings.tsv",'r') as inp, open("ratings.csv",'w') as out:
    
    # Create reader and writer
    dr = csv.DictReader(inp, delimiter='\t')
    dw = csv.DictWriter(out, delimiter='\t', fieldnames=dr.fieldnames)
    
    # Write header names
    dw.writerow(dict((fn,fn) for fn in dr.fieldnames))
    
    # Write 100,000 rows
    count = 0
    for row in dr:
        count = count + 1
        dw.writerow(row)
        if count == 100000:
            exit(0)