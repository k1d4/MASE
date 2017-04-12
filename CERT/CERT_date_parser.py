import json
import os
from datetime import date

# src should be set to the directory containing the json files
src = "CERT_data/cert_jsons"

# data field you want to extract from files
field = "DateCreated"

# csv output file
data_output = open("%s.csv" % field, "w")

# key is CVEID, value is the data field
entries = {}

# iterate over the files in the directory, making sure they are json files
for file in os.listdir(src):
    if file.endswith(".json"):
		with open(os.path.join(src, file)) as current_file:

			# load the json file
			data = json.load(current_file)

			# check for a CVEID
			try:
				if data["CVEIDs"]:

					# create an empty list to append field entries to
					if data["CVEIDs"] not in entries:
						entries[data["CVEIDs"]] = []

					# append the date onto the list for the given CVEID
					if data[field]:
						entries[data["CVEIDs"]].append(date(int(data[field][:4]), int(data[field][5:7]), int(data[field][8:10])))

			# if file does not have a CVEID
			except:
				pass

# write out the dictionary to a csv file
for key, value in entries.iteritems():

	# write the key
	data_output.write("%s," % key)
	for item in sorted(value):

		# write out the data field
		try:
			data_output.write("%s," % item)

		except:
			pass

	# write out newline in csv
	data_output.write('\n')

data_output.close()