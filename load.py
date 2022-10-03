# Python program to read
# json file


import json

# Opening JSON file
f = open('data.json', "r",encoding='utf-8')

# Load data
data = json.load(f)


# Closing file
f.close()
