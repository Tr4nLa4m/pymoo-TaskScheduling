from problem.problem import MultiObjectiveMixedVariableProblem

from pymoo.algorithms.moo.nsga2 import NSGA2, RankAndCrowdingSurvival
from pymoo.core.mixed import MixedVariableGA
from pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.core.mixed import MixedVariableMating, MixedVariableGA, MixedVariableSampling, MixedVariableDuplicateElimination
from pymoo.optimize import minimize
from utils.writeData import writeOutput
from utils.helperModules import getBestSolution
from config.configParams import POP_SIZE, PROB_MUTATION, N_GEN


# Get problem
problem = MultiObjectiveMixedVariableProblem()

# Get algorithm
# algorithm = MixedVariableGA(pop_size=20, survival=RankAndCrowdingSurvival())
algorithm = NSGA2(pop_size=POP_SIZE,
                  sampling=MixedVariableSampling(),
                  mating=MixedVariableMating(eliminate_duplicates=MixedVariableDuplicateElimination()),
                  mutation=PolynomialMutation(prob=PROB_MUTATION),
                  eliminate_duplicates=MixedVariableDuplicateElimination(),
                  )

# Minimize algorithm - details in doc of pymoo
res = minimize(problem,
               algorithm,
               ('n_gen', N_GEN),
               seed=1,
               verbose=False)

# Print solutions
print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))

# get List solutions to write
# bestSolution = getBestSolution(res.F, res.X)
schedules = list()
# Out param is required
out = dict()

for solution in res.X :
    problem._evaluate(solution, out)
    schedules.append(problem.calcSchedule())

# Write data
writeOutput(schedules)