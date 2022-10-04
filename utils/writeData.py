# Python program to read
import json
from utils.helperModules import getDateTimeFromTimestamp


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
    
