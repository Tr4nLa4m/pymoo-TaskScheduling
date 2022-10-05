# Python program to read
import json
import os
from datetime import datetime
from helperModules import getDateTimeFromTimestamp

# Get dir to data ouput folder
def getAbsoluteDirectory(pathFile):
    script_dir = os.path.dirname(__file__)
    rel_path = pathFile
    project_dir = script_dir.split("utils")[0]
    return os.path.join(project_dir, rel_path)

# Write data output
def writeOutput(schedule) :
    # Format date time
    for task in schedule['schedule']:
        task['startTime'] = getDateTimeFromTimestamp(task['startTime']).strftime("%d/%m/%Y, %H:%M")
        task['endTime'] = getDateTimeFromTimestamp(task['endTime']).strftime("%d/%m/%Y, %H:%M")
    schedule['endDateTime'] = getDateTimeFromTimestamp(schedule['endDateTime']).strftime("%d/%m/%Y, %H:%M")
    schedule['startDateTime'] = getDateTimeFromTimestamp(schedule['startDateTime']).strftime("%d/%m/%Y, %H:%M")

    # Write file
    with open("result.json", "w") as outfile:
        json.dump(schedule, outfile)
    
    # Save as history file
    now = datetime.now() # current date and time
    date_time = now.strftime("%d_%m_%Y_%H-%M-%S")
    rel_path = f"data\output\Result_{date_time}.json"
    with open(getAbsoluteDirectory(rel_path), "w") as outfile:
        json.dump(schedule, outfile)
    








