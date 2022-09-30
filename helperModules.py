from datetime import datetime, timedelta
from machineEntity import Machine
from taskEntity import Task
from employeeEntity import Employee

def getListTask(orders, tasks) :
    listTask = []

    for order in orders :
        for item in order["goods"]:
            for task in tasks:
                t = Task(f"{order['id']} {item['goodId']} {task['id']}", task['estimatedDuration'] )
                if task["requiredAssets"] : 
                    t.setRequiredMachine(task["requiredAssets"])
                task.setStartTime(getTimeStamp(order["startTime"]))
                task.setEndTime(getTimeStamp(order["startTime"]))
                task.setPrecedingTask(task["preceedingTasks"])
                listTask.append(t)

    return listTask

def getListHuman(employees) :
    listEmployees = []

    for employee in employees :
        listEmployees.append(Employee(f"{employee['id']}", employee['cost'], employee['skillLevel']))
    
    return listEmployees

def getListMachine(machines) :
    listMachines = []

    for machine in machines :
        listMachines.append(Machine(f"{machine['id']}"))

def getTimeStamp(stringTime):
    res = datetime.strptime(stringTime, '%d-%m-%Y %H:%M')
    return res.timestamp()

def calculateDuration(task, avgSkill, employeeId):
    oldDuration = task["estimatedDuration"] * 3600
    taskId = task["id"]
    listEmpId = avgSkill.keys()
    totalSkillLevel = 0
    for empId in listEmpId :
        totalSkillLevel += avgSkill[f"{empId}"][taskId]
    avgSkillLevel = totalSkillLevel / len(listEmpId)

    newDuration = oldDuration * (1 - (avgSkill[employeeId][taskId] - avgSkillLevel) / avgSkillLevel)
    return newDuration

def getStartTimeShift(startTime, duration):
    startDateTime = datetime.fromtimestamp(startTime)
    endDateTime = datetime.fromtimestamp(startTime + duration)
    nextDay = startDateTime + timedelta(days=1)
    startHour, endHour = startDateTime.hour, endDateTime.hour
    startMinute, endMinute = startDateTime.minute, endDateTime.minute

    if(startHour > 17 or (startHour == 17 and startMinute > 30) or endHour > 17 or (endHour == 17 and endMinute > 30)):    
        startDateTime = datetime(nextDay.year, nextDay.month, nextDay.day, 8, 0, 0)
    return startDateTime.timestamp()

def getCost(employeeId, duration, baseSalary):
    return baseSalary[employeeId] * duration / 3600
#test
# task = {
#       "id": "j1",
#       "code": "DXT_b06305c0-f150-11ec-9cb9-e72d112caadc",
#       "requiredAssets": [
#       ],
#       "skills": [
#         "62b1a3ac29da55a4b049ae80",
#         "62b1a3ac29da55a4b049ae81",
#         "62b1a3ac29da55a4b049ae83"
#       ],
#       "group": "1",
#       "estimatedDuration": 0.1,
#       "estimateOptimisticTime": 1,
#       "estimateNormalCost": 100,
#       "estimateMaxCost": 200,
#       "estimateAssetCost": 100,
#       "followingTasks": [],
#       "priority": 1,
#       "preceedingTasks": [],
#       "name": "In tài liệu đơn hàng",
#       "taskWeight": {
#         "timeWeight": 0.3333333333333333,
#         "qualityWeight": 0.3333333333333333,
#         "costWeight": 0.3333333333333333
#       }
#     }
# avgSkill = {
#     "62b1a3a691dbfba478012934": {
#         "j1": 0.3,
#         "j2": 0.4
#     },
#     "62b1a3a691dbfba478012931": {
#         "j1": 0.1,
#         "j2": 0.2
#     }
# }
# emp = Employee("62b1a3a691dbfba478012934", 300, [])
# calculateDuration(task, avgSkill, emp)