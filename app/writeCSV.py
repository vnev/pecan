import csv

csvfile = "data.csv"

#Assuming res is a flat list
"""
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in res:
        writer.writerow([val])    
"""
#Assuming res is a list of lists
def writeCSVFile(res):
	csvfile = "dataSurvey.csv"
	with open(csvfile, "w") as output:
	    writer = csv.writer(output, lineterminator='\n')
	    writer.writerows(res)

