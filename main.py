import functions
import utils
import copy

suppliers = {
    'Adidas': 20,
    'Converse': 30,
    'Vans': 10,
    'Ananas': 20,
    'Bitis': 10
}

capacity = 100

individual1 = [['Adidas', 'Converse'], ['Vans'], ['Ananas'],['Bitis']]
individual2 = [['Adidas'], ['Vans'], ['Converse', 'Ananas'],['Bitis']]
individual3 = [['Adidas'], ['Converse'], ['Vans'], ['Ananas'],['Bitis']]
individual4 = [['Adidas','Converse'], ['Vans'], ['Ananas'],['Bitis']]
individual5 = [['Adidas'], ['Converse','Vans'], ['Ananas','Bitis']]
individual6 = [['Adidas','Converse','Vans'], ['Ananas'],['Bitis']]


F0 = [individual1,individual2,individual3,individual4,individual5,individual6]

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
        
        if(can_enhance and len(new_individual) !=0):
            population.pop(index)
        

            population.append(new_individual)
            count = count + 1
    return [count,population]

def selection_population(population,n_selection):
    population.sort(key=utils.getScore)        #Sort là hàm mặc định từ nhỏ -> lớn, ở đây Sort số ngày
   
    population = population[:n_selection]

    return population

def GA(population, capacity,suppliers, n_GA, n_cross, n_muation, n_enhance,n_selection, output =""):

    Fi = population
    count = 1
    
    if(output != ""):
        f = open(output, "w")

    for _ in range(n_GA):
        Fi = copy.deepcopy(Fi)
        Fi = crossover_population(Fi, capacity, suppliers, n_cross)[1]
        Fi = mutation_population(Fi,capacity,suppliers,n_muation)[1]
        Fi = enhance_population(Fi,capacity,suppliers,n_enhance)[1]
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

    return population

GA(F0,capacity,suppliers,n_GA=3,n_cross=5,n_muation=5,n_enhance=5,n_selection=10,output="output.txt")