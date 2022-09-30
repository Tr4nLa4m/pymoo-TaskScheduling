import sys
import io

import load
from helperModules import getTimeStamp

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

startTime, endTime, endTimeResource, avgSkill, baseSalary, endTimeOrders = dict(), dict(), dict(), dict(), dict(), dict()

ORDERS = load.data["bills"]  #Array of orders
TASKS = load.data["fromStockJobTasks"]
EMPLOYEES = load.data["fromStockHumanResources"]
MACHINES = load.data["fromStockMachineResources"]


# Init Start time and End time each task 
for order in ORDERS :
    orderId = order['id']
    startTime[orderId] = dict()
    endTime[orderId] = dict()
    for item in order["goods"]:
        processId = item['goodId']
        endTime[orderId][processId] = dict()
        startTime[orderId][processId] = dict()
        for task in TASKS:
            taskId = task['id']
            startTime[orderId][processId][taskId] = getTimeStamp(order["startTime"])
            endTime[orderId][processId][taskId] = getTimeStamp(order["startTime"])

# Init avgSkill of each Task each employee
for employee in EMPLOYEES:
    avgSkill[employee['id']] = dict()
    for task in TASKS:
        avg = 0
        sumSkillValue = 0
        sumSkill = 0
        for skill in task["skills"]:
            sumSkillValue += employee["skillLevel"][skill]
            sumSkill += 1
        if(sumSkill != 0):   avg = sumSkillValue / sumSkill
        avgSkill[employee['id']][task['id']] = avg
    

# Init base Salary of employees:
for employee in EMPLOYEES:
    employeeId = employee['id']
    baseSalary[employeeId] = employee['cost']

# Init endTime of orders:
for order in ORDERS:
    endTimeOrders[order['id']] = getTimeStamp(order['deadline'])

# Init list employee Id
listEmployeeIds = list()
for emp in EMPLOYEES:
    listEmployeeIds.append(emp['id'])
        