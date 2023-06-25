import copy

suppliers ={
    'A':10,
    'B':5,
    'C':4,
    'D':2,
    'E':1,
    'F':7,
    'G':5,
    'H':3,
    'I':1,
    'K':2
}

capacity = 15
current_capacity = 10

#swap 2 phần từ, phần tử vị trí pos1 trong mảng arr1 và  pos2 trong mảng arr2
def print_individual(individual):
    for gen in individual:
        print('+'*20)
        print(gen)

def swap1d(arr:list, pos1:int,pos2:int) -> bool:

    temp = arr[pos1]
    arr[pos1] = arr[pos2]
    arr[pos2] = temp

    return arr

def getSuppliers(suppliers:dict):
    newSuppliers = []

    for key in suppliers.keys():
        newSuppliers.append({
            'key':key,
            'value':suppliers[key]
        })
    
    return sorted(newSuppliers,key=lambda x: x['value'], reverse=True)
    
def seeding_help(seeding,suppliers:list,capacity,is_first_gen):

    if(is_first_gen):
        result = []
        result.append(suppliers[seeding])
        suppliers.pop(seeding)
    else:
        result = []
        result.append(suppliers[0])
        suppliers.pop(0)

    
    current_sum = result[0]['value']
    

    for (index,supplier) in enumerate(suppliers):
        if(current_sum + supplier['value'] <= capacity):
            result.append(supplier)
            current_sum += supplier['value']
            suppliers.pop(index)

    return result

def seeding(suppliers,capacity):
    suppliers = getSuppliers(suppliers)
    population = []

    for i in range(0,len(suppliers)):
        results = []
        suppliers2 = copy.deepcopy(suppliers)
        is_first_gen = True
        while(len(suppliers2)!=0):
            results.append(seeding_help(i,suppliers2,capacity,is_first_gen))
            is_first_gen = False

        population.append(results)

    return population

def permutation(individual1, number_of_internal_change):

    sub_population = []

    count = 0
    for i in range(0,len(individual1)):
        for j in range(i+1,len(individual1) ):
            individual = copy.deepcopy(individual1)
            individual =  swap1d(individual,i,j)
            sub_population.append(individual)
            count += 1

            if(count >= number_of_internal_change):
                return sub_population
                
    return sub_population

def makeF0(suppliers,capacity, popsize):
    population = seeding(suppliers,capacity)
    n_suppliers = len(suppliers.keys())
    new_population = []


    number_of_internal_change = popsize/n_suppliers -1 
    # 100/10 - 1 = 9

    for i in range(len(population)):
        new_population.append(population[i])
        new_population = new_population + permutation(population[i],number_of_internal_change)


    return new_population


init_population = seeding(suppliers,capacity)

final_population = makeF0(suppliers,capacity,50)

def standard_F0(F0):
    new_final_solution = []
    for individual in final_population:
        new_individual = []
        for gen in individual:
            new_bit = []
            for bit in gen :
                new_bit.append(bit['key'])
            new_individual.append(new_bit)
        new_final_solution.append(new_individual)

    print(new_final_solution)

    return new_final_solution


print(len(standard_F0(final_population)))