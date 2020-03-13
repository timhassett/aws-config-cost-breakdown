import os
import json

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    
    return allFiles

def count_items(filename):
    config_items = {}
    if filename.endswith(".json"):
        with open(filename, 'r') as f:
            log_data = json.load(f)
            if 'configurationItems' in log_data:
                for config_item in log_data['configurationItems']:
                    resourceType = config_item['resourceType']
                    if resourceType in config_items:
                        config_items[resourceType] += 1
                    else:
                        config_items[resourceType] = 1

    return config_items

def merge(object1, object2):
    for key in object2.keys():
        if key in object1:
            object1[key] += object2[key]
        else:
            object1[key] = object2[key]

def sum_config_items(items):
    total = 0
    for key in items.keys():
        total += items[key]
    return total

def display_sorted(items):
    out = []
    out.append("{0:45} {1:10} \t{2}".format("ResourceType", "ConfigItems", "Cost"))
    out.append("----------------------------------------------------------------------------------------")
    sorted_items = sorted(items.items(), key=lambda x: x[1], reverse=True)
    for item in sorted_items:
        out.append("{0:45} {1:10} \t$ {2}".format(item[0], item[1], item[1]*0.003))
    total = sum_config_items(items)
    out.append("----------------------------------------------------------------------------------------")
    out.append("{0:45} {1:10} \t$ {2}".format("Total", total, total*0.003))
    return out

months = []
months.append("2019/1")
months.append("2019/2")
months.append("2019/3")
months.append("2019/4")
months.append("2019/5")
months.append("2019/6")
months.append("2019/7")
months.append("2019/8")
months.append("2019/9")
months.append("2019/10")
months.append("2019/11")
months.append("2019/12")
months.append("2020/1")
months.append("2020/2")


for month in months:
    path = "./logs/" + month
    files = sorted(getListOfFiles(path))
    config_item_types = {}

    for filename in files:
        config_items = count_items(filename)
    #    print(filename)
        merge(config_item_types, config_items)
    print(month)
    out = "\n".join(display_sorted(config_item_types))
    print(out)
    with open("reports/" + month.replace("/", "-"), "w") as outfile:
        outfile.write("Month: " + month + "\n")
        outfile.write(out)
        

