# A simple tool for scraping a list of infogram accounts and 
# by Juuso Koponen / Koponen+Hildén – https://www.koponen-hilden.fi
# License: Creative Commons Attribution 4.0 International

# Requires https://github.com/arc298/instagram-scraper to work


import csv
import json
import os
import re
from time import sleep
from datetime import datetime, date, timezone


# Read the list of profiles and convert into Dicts – assuming input file is UTF-8
data = csv.DictReader(open("Helsingin_kaupunginvaltuusto_IG.tsv"), delimiter = "\t")


# Collect the profiles into a list
profiles = []
names = {}

for row in data:
	profile = row["profiili"]
	if "instagram.com/" in profile:
		profile = profile.split("instagram.com/")[1].split("/")[0]
	if len(profile) > 0:
		profiles.append(profile)
		names[profile] = row["valtuutettu"] + ", " + row["puolue"]


# Run the scraper – comment this line out if you have already scraped the data and only want to analyze it
# Limiting the results to 100 most recent posts
os.system("instagram-scraper " + ",".join(profiles) + "  --media-metadata --maximum 100")



# ANALYSIS OF SCRAPED DATA

# Tags and words we are interested in in the media captions
# Wildcard * currently works for tags and words, not for usernames
tags_of_interest = ["kaupallinen*", "*promo*", "maino*", "ad", "advertise*", "freebie", "paid*", "spon*", "*sponsor", "*yhteistyö", "*partner*", "*tarjo*", "support*", "uutuus", "uusi*"] # WITHOUT the # sign
words_of_interest = ["kaupallinen", "*promo*", "maino*", "spon*", "*sponsor", "yhteistyö", "*partner*", "suosit*", "support", "uutuus", "uutta"] 
users_of_interest = [] # WITH the @ sign

# Ignore posts older than the start of current city council’s term
cutoff_date = datetime(2017, 6, 1)
cutoff_timestamp = cutoff_date.replace(tzinfo = timezone.utc).timestamp()


# Write the header to the output file
f = open("Helsingin_kaupunginvaltuusto_IG_potentiaaliset_osumat.tsv", mode = "w")
headers = [
	"name",
	"profile",
	"date",
	"matching keywords",
	"url",
	"caption"
]
f.write("\t".join(headers))


all_hashtags = []
all_tagged_users = []

for profile in profiles:
	posts = list(json.load(open(profile + "/" + profile + ".json"))["GraphImages"])
	for post in posts:
		# Check timestamp
		if post["taken_at_timestamp"] < cutoff_timestamp:
			continue
		# Check if there is a caption
		try:
			caption = post["edge_media_to_caption"]["edges"][0]["node"]["text"]
		except:
			continue
		# Split into words – make lowercase and remove everything else than letters, whitespace, # and @
		words = re.sub(r"\s", " ", re.sub(r"[^\w\s\#@]", "", caption.lower())).split(" ")

		# See if there are any matches to the words, tags or usernames of interest – a bit kludgy, but works
		matches = []
		for word in words:
			if len(word) == 0:
				continue

			if word[0] == "@":
				compare_against = users_of_interest
				if word not in all_tagged_users:
					all_tagged_users.append(word)

			elif word[0] == "#":
				compare_against = tags_of_interest
				if word not in all_hashtags:
					all_hashtags.append(word)
				word = word[1:]

			else:
				compare_against = words_of_interest

			for c in compare_against:
				cb = c.replace("*", "")
				if cb in word:
					if c[0] == "*" or word.startswith(cb):
						if c[-1] == "*" or word.endswith(cb):
							# Match
							if word not in matches:
								matches.append(word)

		# Write out the data row, if the caption includes matched terms
		if len(matches) > 0:
			output = [
				names[profile],
				profile,
				datetime.utcfromtimestamp(post["taken_at_timestamp"]).strftime('%Y-%m-%d %H:%M:%S'),
				", ".join(matches),
				"https://www.instagram.com/p/" + post["shortcode"],
				re.sub(r"\s", " ", caption)
			]
			f.write("\n" + "\t".join(output))

f.close()


# Print all hashtags
#print("\n".join(sorted(all_hashtags)))

# Print all tagged users
print("\n".join(sorted(all_tagged_users)))