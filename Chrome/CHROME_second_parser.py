import csv
import sys

# take csv input as first arg 
in_file_name = sys.argv[1]

# take output name as second arg
out_file_name = sys.argv[2]

# output file
data_output = open(out_file_name, "w")

# dictionary for each unique ID
entries = {}

# open the input csv file
with open(in_file_name, 'rb') as csvfile:
	reader = csv.reader(csvfile)

	# cur_month
	cur_month = ""

	for row in reader:
		if row[0]:
			if row[3]:
				if (row[3][:3] + row[3][7:11]) not in entries:
					entries[(row[3][:3] + row[3][7:11])] = {}

				if row[1] not in entries[(row[3][:3] + row[3][7:11])]:
					entries[(row[3][:3] + row[3][7:11])][row[1]] = 0

				entries[(row[3][:3] + row[3][7:11])][row[1]] += 1
				cur_month = row[3][:3] + row[3][7:11]

			else: 
				if row[1] not in entries[cur_month]:
					entries[cur_month][row[1]] = 0

				entries[cur_month][row[1]] += 1

for key, value in entries.iteritems():
	data_output.write("Month, %s\n" % key)
	data_output.write("Num of Dups per Vuln, Num of Vulns\n")
	for dupnum, count in value.iteritems():
		data_output.write("%s, %s\n" % (dupnum, count))
	data_output.write('\n')

data_output.close()