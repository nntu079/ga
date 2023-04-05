import functions
import utils
import random

suppliers = {
    'A': 2,
    'B': 3,
    'C': 4,
    'D': 1,
    'E': 4,
    'F': 2,
    'G': 5
}
capacity = 10

F0 = utils.makeF0(suppliers, capacity)

def crossover_population(population, capacity, suppliers, n_cross):

    [individual1, individual2] = utils.getRandomTwoIndividual(population)

    [child1, child2] = functions.crossover(individual1, individual2)

    for _ in range(0, n_cross):
        if (utils.evaluate(child1, capacity, suppliers) == -1):
            [can_fix, new_child] = utils.fix(child1, suppliers, capacity)
            if (can_fix == True):
                population.append(new_child)
        else:
            population.append(child1)

        if (utils.evaluate(child2, capacity, suppliers) == -1):
            [can_fix, new_child] = utils.fix(child2, suppliers, capacity)
            if (can_fix == True):
                population.append(new_child)
        else:
            population.append(child2)

    return population


F1 = crossover_population(F0,capacity,suppliers,10)

chil1 = F1[0]
chil2 = F1[1]

print(chil1)
print(functions.mutation(chil1))
