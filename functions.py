import utils


individual = [['A', 'B'], ['C'], ['D']]


def mutation(individual):
    idx_gen = utils.getRamdomIndex(individual)[0]

    individual[idx_gen-1] = individual[idx_gen] + individual[idx_gen-1]
    individual.pop(idx_gen)
    
    return individual

def crossover(individual1, individual2):
    index1 = utils.getRamdomIndex(individual1)
    index2 = utils.getRamdomIndex(individual2)

    bit1 = individual1[index1[0]][index1[1]]
    bit2 = individual2[index2[0]][index2[1]]

    newIndividual1 = [row[:] for row in individual1]
    newIndividual2 = [row[:] for row in individual2]

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

    return [newIndividual1,newIndividual2]

