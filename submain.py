import functions
import utils
import copy

def crossover_population(population, capacity, suppliers, n_cross, current_capacity = 0):

    if current_capacity == 0:
        current_capacity = capacity

    count = 0
    for _ in range(0, n_cross):
        [individual1, individual2] = utils.getRandomTwoIndividual(population)
        [child1, child2] = functions.crossover(individual1, individual2)

        if (utils.evaluate(child1, capacity, suppliers, current_capacity) == -1) and len(child1) != 0:
            [can_fix, new_child] = utils.fix(child1, suppliers, capacity, current_capacity)
            if (can_fix == True):
                count = count + 1
                population.append(new_child)
        elif len(child1) != 0:
            count = count + 1
            population.append(child1)

        if (utils.evaluate(child2, capacity, suppliers,current_capacity) == -1) and len(child2) != 0:
            [can_fix, new_child] = utils.fix(child2, suppliers, capacity, current_capacity)
            if (can_fix == True):
                count = count + 1
                population.append(new_child)
        elif len(child2) != 0:
            count = count + 1
            population.append(child2)

    return [count,population]

def mutation_population(population, capacity, suppliers, n_muation,current_capacity):

    count = 0
    for _ in range(0, n_muation):
        individual = utils.getRandomIndividual(population)
        result = functions.mutation(individual, capacity, suppliers,current_capacity)
        if (result[0]):
            population.append(individual)
            count = count+1
    return [count, population]

def enhance_population(population,capacity,suppliers, n_enhance,current_capacity):
    count = 0
    for _ in range(0,n_enhance):
        [new_individual,index] = utils.getRandomIndividual(population,True)
        [can_enhance,new_individual] = utils.enhance(new_individual,capacity,suppliers,current_capacity)
        
        if(can_enhance and len(new_individual) !=0):
            population.pop(index)
        

            population.append(new_individual)
            count = count + 1
    return [count,population]

def selection_population(population,n_selection):
    population.sort(key=utils.getScore)        #Sort là hàm mặc định từ nhỏ -> lớn, ở đây Sort số ngày
   
    population = population[:n_selection]

    return population

def GA(population,n_fix, capacity,suppliers, n_GA, n_cross, n_muation, n_enhance,n_selection, output ="", current_capacity = 0):

    n_muation = int(n_muation * len(population))
    Fi = population
    count = 1
    
    if(output != ""):
        f = open(output, "w")

    for _ in range(n_GA):
        Fi = copy.deepcopy(Fi)
        Fi = crossover_population(Fi, capacity, suppliers, n_cross,current_capacity)[1]

        if(len(Fi) >=n_fix):
            Fi= Fi[:n_fix]

        Fi = mutation_population(Fi,capacity,suppliers,n_muation,current_capacity)[1]

        if(len(Fi) >=n_fix):
            Fi= Fi[:n_fix]
        
        Fi = enhance_population(Fi,capacity,suppliers,n_enhance,current_capacity)[1]
        Fi = selection_population(Fi,n_selection)
    
        if(output != ""):
            f.write('GENERATION '+str(count)+'\n')
            for _ in Fi:
                f.write(str(_)+ ' ===> Days required: '+ str(len(_))+'\n') 
        else:
            print('Đời F'+ str(count))
            for _ in Fi:
                print(str(_))

        count = count +1
        
    return Fi
