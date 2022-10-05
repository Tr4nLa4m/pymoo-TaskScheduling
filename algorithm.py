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


res = minimize(problem,
               algorithm,
               ('n_gen', N_GEN),
               seed=1,
               verbose=False)

print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
bestSolution = getBestSolution(res.F, res.X)
out = dict()
problem._evaluate(bestSolution[0], out)

# Write data
writeOutput(problem.calcSchedule())