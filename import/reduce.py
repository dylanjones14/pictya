import csv

#with open("title.ratings.tsv", "r") as inp, open("ratings.csv", "w") as out:
	
#	reader = csv.DictReader(inp, delimiter="\t")
#	writer = csv.DictWriter(out, delimiter="\t", fieldnames=reader.fieldnames)

#	headers = {} 
#	for n in writer.fieldnames:
#		headers[n] = n
#	writer.writerow(headers)

#	count = 0
#	for row in reader:
#		if count == 0:
#			pass
#		else:
#			count = count + 1
			
#			writer.writerow('tconst')
#			if count == 200: 
#				exit(0)

with open("title.ratings.tsv",'r') as inp, open("ratings.csv",'w') as out:
    dr = csv.DictReader(inp, delimiter='\t')

    dw = csv.DictWriter(out, delimiter='\t', fieldnames=dr.fieldnames)
    dw.writerow(dict((fn,fn) for fn in dr.fieldnames))
    count = 0
    for row in dr:
        count = count + 1
        dw.writerow(row)
        if count == 100000:
            exit(0)