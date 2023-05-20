import copy
import random

def crossover(individual1, individual2):

    clone_individual1 = copy.deepcopy(individual1)
    clone_individual2 = copy.deepcopy(individual2)

   
    
    new_individual1 = []
    new_individual2 = []

    for gen in individual1:
        for bit in gen:
            new_individual1.append(bit)

    for gen in individual2:
        for bit in gen:
            new_individual2.append(bit)

    clone_new_individua1 = copy.deepcopy(new_individual1)
    clone_new_individua2 = copy.deepcopy(new_individual2)

    len_individual = len(new_individual1)
    random_index1 = random.randint(0,len_individual-1)
    random_index2 = random.randint(random_index1,len_individual-1)
    

    bit_map1 = {}

    for i in range(random_index1,random_index2 + 1):
        if clone_new_individua1[i] not in bit_map1:
            bit_map1[clone_new_individua1[i]]= clone_new_individua2[i]
            bit_map1[clone_new_individua2[i]]= clone_new_individua1[i]

    for index,value in enumerate(new_individual1):
        if(value) in bit_map1:
            new_individual1[index] = bit_map1[value]


    bit_map2 = {}

    for i in range(random_index1,random_index2 + 1):
        if clone_new_individua1[i] not in bit_map2:
            bit_map2[clone_new_individua1[i]]= clone_new_individua2[i]
            bit_map2[clone_new_individua2[i]]= clone_new_individua1[i]

    for index,value in enumerate(new_individual2):
        if(value) in bit_map2:
            new_individual2[index] = bit_map2[value]

    count = 0
    for index1,gen in enumerate(clone_individual1):
        for index2, bit in enumerate(gen):
            clone_individual1[index1][index2] = new_individual1[count]
            count +=1

    count = 0
    for index1,gen in enumerate(clone_individual2):
        for index2, bit in enumerate(gen):
            clone_individual2[index1][index2] = new_individual2[count]
            count +=1

    print(random_index1)
    print(random_index2)
    return [clone_individual1, clone_individual2]



individual1 = [[1,2,3],[4,5]]
individual2 = [[1],[4],[5],[3,2]]

result = crossover(individual1,individual2)
for individual in result:
    print(individual)