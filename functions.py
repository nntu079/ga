import utils
import copy


individual = [['A', 'B'], ['C'], ['D']]
suppliers = {
    'A': 2,
    'B': 2,
    'C': 4,
    'D': 1,
}
capacity = 5



def mutation(individual,capacity,suppliers):
    #return new individual (deep copy)
    individual = copy.deepcopy(individual) 

    random1 = utils.getRamdomIndex(individual)
    random2 = utils.getRamdomIndex(individual)

    while random1 == random2:
        random2 = utils.getRamdomIndex(individual)
        
    temp = individual[random1[0]][random1[1]]
    individual[random1[0]][random1[1]] = individual[random2[0]][random2[1]]
    individual[random2[0]][random2[1]] = temp

    fix_individual = [True, individual]
    if( utils.evaluate(individual,capacity,suppliers) == -1):
        fix_individual = utils.fix(individual,suppliers,capacity)
    
    if(fix_individual[0]):
        return fix_individual
    else:
        temp = individual[random1[0]][random1[1]]
        individual[random1[0]][random1[1]] = individual[random2[0]][random2[1]]
        individual[random2[0]][random2[1]] = temp

    return [False, individual]

def crossover(individual1, individual2):
    index1 = utils.getRamdomIndex(individual1)
    index2 = utils.getRamdomIndex(individual2)

    bit1 = individual1[index1[0]][index1[1]]
    bit2 = individual2[index2[0]][index2[1]]

    newIndividual1 = copy.deepcopy(individual1)
    newIndividual2 = copy.deepcopy(individual2)
    
    for i1 in range(0, len(individual1)):
        for i2 in range(0, len(individual1[i1])):
            if (individual1[i1][i2] == bit1):
                newIndividual1[i1][i2] = bit2
            elif (individual1[i1][i2] == bit2):
                newIndividual1[i1][i2] = bit1

    for i1 in range(0, len(individual2)):
        for i2 in range(0, len(individual2[i1])):
            if (individual2[i1][i2] == bit1):
                newIndividual2[i1][i2] = bit2
            elif (individual2[i1][i2] == bit2):
                newIndividual2[i1][i2] = bit1

    if(newIndividual1 == individual1):
        newIndividual1 = []
    if(newIndividual2 == individual2):
        newIndividual2 = []

    return [newIndividual1,newIndividual2]

