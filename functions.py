import utils
import copy


def mutation(individual,capacity,suppliers,current_capacity):
    #return new individual (deep copy)
    individual = copy.deepcopy(individual) 

    #print(individual)

    random1 = utils.getRamdomIndex(individual)
    random2 = utils.getRamdomIndex(individual)

    while random1 == random2:
        random2 = utils.getRamdomIndex(individual)
        
    temp = individual[random1[0]][random1[1]]
    individual[random1[0]][random1[1]] = individual[random2[0]][random2[1]]
    individual[random2[0]][random2[1]] = temp

    fix_individual = [True, individual]
    if( utils.evaluate(individual,capacity,suppliers,current_capacity) == -1):
        fix_individual = utils.fix(individual,suppliers,capacity,current_capacity)
    
    if(fix_individual[0]):
        return fix_individual
    else:
        temp = individual[random1[0]][random1[1]]
        individual[random1[0]][random1[1]] = individual[random2[0]][random2[1]]
        individual[random2[0]][random2[1]] = temp

    return [False, individual]

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def flatten(arr):

    return [j for sub in arr for j in sub]

def crossover1(individual1,individual2):
    new_individual1 = copy.deepcopy(individual1)
    new_individual2 = copy.deepcopy(individual2)

    new_part_individual1 = chunkIt(new_individual2,2)[1]
    old_part_individual1_flat = flatten(chunkIt(new_individual1,2)[1])
    new_part_individual2 = chunkIt(new_individual1,2)[1]
    old_part_individual2_flat = flatten(chunkIt(new_individual2,2)[1])

    count = 0
    for index1,value1 in enumerate(new_part_individual1):
        for index2,value2 in enumerate(value1):
            if(count < len(old_part_individual1_flat)):
                new_part_individual1[index1][index2] = old_part_individual1_flat[count]
            else:
                del new_part_individual1[index1][index2]
            count = count + 1

    while(count < len(old_part_individual1_flat)):
        new_part_individual1.append([old_part_individual1_flat[count]])
        count= count + 1
    
    for index1,value1 in enumerate(new_part_individual1):
        if(len(value1)==0):
            del new_part_individual1[index1] 
    
    return chunkIt(new_individual1,2)[0] + new_part_individual1
    
def crossover(indv1,indv2):
    return [crossover1(indv1,indv2),crossover1(indv2,indv1)]


#def crossover(individual1, individual2):
#    index1 = utils.getRamdomIndex(individual1)
#    index2 = utils.getRamdomIndex(individual2)

#    bit1 = individual1[index1[0]][index1[1]]
#    bit2 = individual2[index2[0]][index2[1]]

    newIndividual1 = copy.deepcopy(individual1)
#    newIndividual2 = copy.deepcopy(individual2)
    
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

    #if(newIndividual1 == individual1):
    #    newIndividual1 = []
    #if(newIndividual2 == individual2):
    #    newIndividual2 = []

    return [newIndividual1,newIndividual2]

