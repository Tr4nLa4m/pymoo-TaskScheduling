from pymoo.core.problem import ElementwiseProblem
from pymoo.core.variable import Real, Integer, Choice, Binary
from helperModules import calculateDuration, getStartTimeShift, getCost

from initializeData import startTime, baseSalary, endTime, endTimeOrders, endTimeResource,listEmployeeIds,  avgSkill, TASKS, MACHINES, EMPLOYEES, ORDERS
e, m = dict(), dict()

class MultiObjectiveMixedVariableProblem(ElementwiseProblem):

    
    def __init__(self, **kwargs):
        
        vars = dict()
        for order in ORDERS :
            for item in order["goods"]:
                for task in TASKS :
                    vars[f"e {order['id']} {item['goodId']} {task['id']}"] = Choice(options=listEmployeeIds)
                    if task["requiredAssets"] :
                        vars[f"m {order['id']} {item['goodId']} {task['id']}"] = Choice(options=task["requiredAssets"])
        

        super().__init__(vars=vars, n_obj=3, **kwargs)
    

    def _evaluate(self, X, out, *args, **kwargs):
        for order in ORDERS :
            orderId = order['id']
            e[orderId] = dict()
            m[orderId] = dict()
            for item in order["goods"]:
                processId = item['goodId']
                e[orderId][processId] = dict()
                m[orderId][processId] = dict()
                for task in TASKS:
                    taskId = task['id']
                    e[orderId][processId][taskId] = X[f"e {orderId} {processId} {taskId}"]
                    if task["requiredAssets"] :
                        m[orderId][processId][taskId] = X[f"m {orderId} {processId} {taskId}"]
                    
            

        schedule = self.calcSchedule()
        f1 = schedule['totalCost']
        f2 = schedule['endTimeAll']
        f3 = schedule['numTaskNotOnTime']
        

        out["F"] = f1, f2, f3

    def calcSchedule(self) :
        scheduleWorkforce = dict()
        scheduleWorkforce['schedule'] = list()
        totalCost = 0
        endTimeAll = 0
        numTaskNotOnTime = 0
        for task in TASKS:
            for order in ORDERS :
                for item in order["goods"]:
                    orderId = order['id']
                    processId = item['goodId']
                    taskId = task['id']
                    empAssignId = e[orderId][processId][taskId]
                    if taskId in m[orderId][processId]: 
                        machineAssignId = m[orderId][processId][taskId]
                    else : machineAssignId = "null"
                    # Calculate duration by employee Skill
                    newDuration = calculateDuration(task, avgSkill, empAssignId)

                    # Calculate Start time 
                    # If task has preceedingTask
                    if(task["preceedingTasks"]):
                        for preceeding in task["preceedingTasks"]:
                            endTimePreceeding = endTime[orderId][processId][preceeding]

                            if( endTimePreceeding > startTime[orderId][processId][taskId]):
                                startTime[orderId][processId][taskId] = endTimePreceeding
                    
                    # If human resource is not available
                    if(hasattr(endTimeResource, empAssignId)):
                        if(startTime[orderId][processId][taskId] < endTimeResource[empAssignId]):
                            # Start time is endTime of emp resource
                            startTime[orderId][processId][taskId] = endTimeResource[empAssignId]
                    
                    # If machine resource is not available
                    if(machineAssignId != "null" and hasattr(endTimeResource, machineAssignId)):
                        if(startTime[orderId][processId][taskId] < endTimeResource[machineAssignId]):
                            # Start time is endTime of emp resource
                            startTime[orderId][processId][taskId] = endTimeResource[machineAssignId]

                    # Calculate start time by shift time
                    startTime[orderId][processId][taskId] = getStartTimeShift(startTime[orderId][processId][taskId], newDuration)

                    # Calculate endtime 
                    endTime[orderId][processId][taskId] = startTime[orderId][processId][taskId] + newDuration
                    # Calculate endtime human resource and machine Resource
                    endTimeResource[empAssignId] = endTime[orderId][processId][taskId]
                    endTimeResource[machineAssignId] = endTime[orderId][processId][taskId]

                    # Calculate total cost
                    totalCost += getCost(empAssignId, newDuration, baseSalary)
                    # Calculate endTimeAll
                    if(endTimeAll < endTime[orderId][processId][taskId]) :   
                        endTimeAll = endTime[orderId][processId][taskId]
                    # Calculate task not on time
                    if(endTime[orderId][processId][taskId] > endTimeOrders[orderId]):
                        numTaskNotOnTime += 1
                    # add Task to Workforce
                    scheduleWorkforce['schedule'].append({
                        "orderId": orderId,
                        "processId": processId,
                        "taskId": taskId,
                        'employeeId': empAssignId,
                        'startTime' : startTime[orderId][processId][taskId],
                        'endTime': endTime[orderId][processId][taskId],
                        'machineId': machineAssignId 
                    })
        scheduleWorkforce['totalCost'] = totalCost
        scheduleWorkforce['endTimeAll'] = endTimeAll
        scheduleWorkforce['numTaskNotOnTime'] = numTaskNotOnTime
        return scheduleWorkforce
                     
                    
# from pymoo.core.mixed import MixedVariableGA
# from pymoo.core.variable import Real, Integer
# from pymoo.optimize import minimize

# problem = MixedVariableProblem()

# algorithm = MixedVariableGA(pop=10)

# res = minimize(problem,
#                algorithm,
#                termination=('n_evals', 1000),
#                seed=1,
#                verbose=False)

# print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
# ORDERS = load.data["bills"]  #Array of orders
# TASKS = load.data["fromStockJobTasks"]
# LIST_TASK = helper.getListTask(ORDERS, TASKS)
# print(LIST_TASK)