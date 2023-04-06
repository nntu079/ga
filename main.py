import functions
import utils
import copy

suppliers = {
    'A': 2,
    'B': 3,
    'C': 4,
    'D': 1
}

capacity = 7

individual1 = [['A', 'B'], ['C'], ['D']]
individual2 = [['A'], ['C'], ['B', 'D']]
individual3 = [['A'], ['B'], ['C'], ['D']]

F0 = [individual1, individual2, individual3]

def crossover_population(population, capacity, suppliers, n_cross):

    count = 0
    for _ in range(0, n_cross):
        [individual1, individual2] = utils.getRandomTwoIndividual(population)
        [child1, child2] = functions.crossover(individual1, individual2)

        if (utils.evaluate(child1, capacity, suppliers) == -1) and len(child1) != 0:
            [can_fix, new_child] = utils.fix(child1, suppliers, capacity)
            if (can_fix == True):
                count = count + 1
                population.append(new_child)
        elif len(child1) != 0:
            count = count + 1
            population.append(child1)

        if (utils.evaluate(child2, capacity, suppliers) == -1) and len(child2) != 0:
            [can_fix, new_child] = utils.fix(child2, suppliers, capacity)
            if (can_fix == True):
                count = count + 1
                population.append(new_child)
        elif len(child2) != 0:
            count = count + 1
            population.append(child2)

    return [count,population]

def mutation_population(population, capacity, suppliers, n_muation):

    count = 0
    for _ in range(0, n_muation):
        individual = utils.getRandomIndividual(population)
        result = functions.mutation(individual, capacity, suppliers)
        if (result[0]):
            population.append(individual)
            count = count+1
    return [count, population]

def enhance_population(population,capacity,suppliers, n_enhance):
    count = 0
    for _ in range(0,n_enhance):
        [new_individual,index] = utils.getRandomIndividual(population,True)
        [can_enhance,new_individual] = utils.enhance(new_individual,capacity,suppliers)
        
        if(can_enhance):
            population.pop(index)
        

            population.append(new_individual)
            count = count + 1
    return [count,population]

def selection_populatio(population,n_selection):
    population.sort(key=utils.getScore)
    population = population[:n_selection]

    return population

def GA(population, capacity,suppliers, n_GA, n_cross, n_muation, n_enhance,n_selection):

    Fi = population
    count = 1
    for _ in range(n_GA):
        Fi = copy.deepcopy(F0)
        Fi = crossover_population(Fi, capacity, suppliers, n_cross)[1]
        Fi = mutation_population(Fi,capacity,suppliers,n_muation)[1]
        Fi = enhance_population(Fi,capacity,suppliers,n_enhance)[1]
        Fi = selection_populatio(Fi,n_selection)

        print('Đời F'+ str(count))
        for _ in Fi:
            print(_)

        count = count +1

    return population


GA(F0,capacity,suppliers,2,10,10,3,15)
