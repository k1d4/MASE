import csv
import sys
import datetime

# store values from each row of the csv
class values:
	def __init__(self):
		self.dupnum = 0
		self.dateopened = ""
		self.security_severity = ""
		self.cve = ""
		self.dup = []
		self.status = ""

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
	next(csvfile)
	reader = csv.reader(csvfile)

	# parse each row
	for row in reader:

		# check if report is a duplicate
		if row[2] == "Duplicate":

			# check if an ID has already been created for the original report ID
			if row[10] not in entries:
				entries[row[10]] = values()

			# save dup information
			tempdup = values()
			tempdup.dateopened = row[6].replace(',','')
			tempdup.cve = row[8].replace(',',' ')
			tempdup.status = row[2]
			tempdup.security_severity = row[9]

			# increment number of dups for the original
			entries[row[10]].dupnum += 1

			# append the dup to the dup list
			entries[row[10]].dup.append(tempdup)

		else:

			# this is an original bug report
			if row[0] not in entries:
				entries[row[0]] = values()

			# add original bug info to dictionary
			entries[row[0]].dateopened = row[6].replace(',','')
			entries[row[0]].cve = row[8].replace(',',' ')
			entries[row[0]].status = row[2]
			entries[row[0]].security_severity = row[9]

# write out to cve
data_output.write("ID, Dup Num, CVE, Date Opened, Status, Severity, Dup Dates\n")

# iterate over the dictionary
for key, value in entries.iteritems():
	data_output.write("%s,%s,%s,%s,%s,%s" % (key, value.dupnum, value.cve, value.dateopened, value.status, value.security_severity))
	
	# turn original date into datetime object
	if value.dateopened:
		orig_day_str = value.dateopened[:11]
		orig_day = datetime.datetime.strptime(orig_day_str, '%b %d %Y').date()

	# write out each dup date
	for dup in value.dup:
		data_output.write(",%s" % dup.dateopened)

	# write out difference in time between dup date and original
	if value.dateopened:
		for dup in value.dup:

			# get datetime object for dup date
			dup_day_str = dup.dateopened[:11]
			dup_day = datetime.datetime.strptime(dup_day_str, '%b %d %Y').date()

			data_output.write(",%d" % (dup_day - orig_day).days)

	data_output.write("\n")



# close the output file
data_output.close()