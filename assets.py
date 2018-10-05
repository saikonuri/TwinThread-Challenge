import urllib2
import json

# Asks the user if they want to search by name or description
# This is just the experience API (to grab user input), the actual service is below
def search(data):
    fields = {1: 'name', 2: 'description'}
    criteria = input("Search by? \n 1: Name \n 2: Description \n Enter: ")
    if criteria not in [1,2]:
        print("Sorry, please try again.")
    user_input = raw_input("Please enter " + fields[criteria] + " to search. \n Enter: ")
    searchService(data, fields[criteria], user_input)

# Prints out JSON formatted assets which meet search criteria
# The logic for filtering/searching on some field (name, description, status) with some initial input
def searchService(data, field, user_input):
    assets = data['assets']
    response = []
    for asset in assets:
        if user_input.lower() in str(asset[field]).lower():
            response.append(asset)
    print(json.dumps(response))

# Using the logic already made in the searchService above! Don't have to repeat.
def list_critical(data):
    searchService(data, 'status', '3')

# Prints out number of unique classes and JSON response of the assets under each class
# Builds a dictionary of unique classes. Keys are class id's while values are asset names that fall under that class
# Simple linear search through all the assets
def class_details(data):
    assets = data['assets']
    class_lists = {}
    for asset in assets:
        class_list = asset['classList']
        for c in class_list:
            if c['id'] in class_lists:
                class_lists[c['id']].append(asset['name'])
            else:
                class_lists[c['id']] = [asset['name']]
    print("Number of Unique Classes: " + str(len(class_lists)))
    print("Unique Classes and Names of Assets under that Class: \n")
    print(json.dumps(class_lists))

# The user layer of building a tree. 
# Builds a dictionary of assetId -> children 
# Calls the logic layer at the end of the function
def tree(data):
    assets = data['assets']
    parents = {}
    for asset in assets:
        if asset['assetId'] not in parents:
            parents[asset['assetId']] = []
        if asset['parentId'] not in parents:
            parents[asset['parentId']] = []
        parents[asset['parentId']].append(asset['assetId'])

    id = input("Which asset would you like to build the tree from? \n Enter: ")
    if id not in parents:
        print("Sorry, could not find that asset!")
        return
    treeHelper(parents,id,"", set())

# Recursive method that prints out the heirarchical view of the assets.
# Using a set to make sure we don't visit an asset that was already processed. 
# Adding indents at each depth to show hierarchy
def treeHelper(parents, id, level, set):
    set.add(id)
    print(level + str(id))
    children = parents[id]
    for child in children:
        if child not in set:
            treeHelper(parents, child, level + "  ", set)



# Read in the text file and convert it into JSON (dict) format
txt = urllib2.urlopen("https://www.twinthread.com/code-challenge/assets.txt").read()
data = json.loads(txt)

# Get user input for what they would like to know about the assets
f = input("What would you like to do? \n 1: Search for Assets \n 2: List all assets of critical status \n 3: Get Class Name Details \n 4: Get Tree View by ID \n Number: ")
# Depending on their input, perform the appropriate function
if f == 1:
    search(data)
elif f == 2:
    list_critical(data)
elif f == 3:
    class_details(data)
elif f == 4:
    tree(data)
else:
    print("Sorry, please try again.")

