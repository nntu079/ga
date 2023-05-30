import random
import copy
import pandas as pd
import numpy as np
import itertools

############### UTILS #############

def sum_gen(gen, suppliers):     #tính tổng supplier trong 1 ngày bất kì
    sum = 0
    for bit in gen:
        sum = sum + suppliers[bit]

    return sum

def cloneIndividual(individual):       #nhân bản 1 con bất kì
    return copy.deepcopy(individual)

def fix(individual, suppliers, capacity,current_capacity):       
    count = 0
    idx_gen = -1           #chưa biết gen thứ mấy nên tạm để -1
                           #idx: thứ tự của bit trong 1 gen
    #đếm số gen cần fix, >=2 => từ chối fix
    for idx, gen in enumerate(individual):      #enumrate là vòng lặp vừa lấy chỉ số vừa lấy giá trị, lấy đoạn gen có thứ tự là idx
        if(idx == 0):
            sum = 0
            for bit in gen:
                sum = sum + suppliers[bit]
                if (sum > current_capacity):     #tìm đoạn gen có tổng stock > cap -> thứ tự của gen/ngày đó
                    idx_gen = idx
                    count = count + 1
                    if (count >= 2):
                        return [False, individual]
        else:
            sum = 0
            for bit in gen:
                sum = sum + suppliers[bit]
                if (sum > capacity):
                    idx_gen = idx
                    count = count + 1
                    if (count >= 2):
                        return [False, individual]

    #idx_gen vị trí gen cần fix
    idx_min = 0
    gen_fix = individual[idx_gen]        #bóc đoạn gen có thứ tự idx_gen trong individual
    min_bit_value = suppliers[gen_fix[idx_min]]       #bit nhỏ nhất trong gen

    #tìm idx_min vị trí bit, min_bit_value giá trị bit của bit nhỏ nhất tron gen cần fix
    for idx, bit in enumerate(gen_fix): 
        if suppliers[bit] < min_bit_value:
            min_bit_value = suppliers[bit]
            idx_min = idx
    
    gen_fix_clone = gen_fix.copy()     #clone gen cần fix ra để thử fix
    bit_pop = gen_fix_clone[idx_min]  #giá trị bit lấy ra của gen gần fix
    gen_fix_clone.pop(idx_min)        #xóa bit nhỏ nhất trong gen cần fix đã clone    #.pop = lấy ra

    #kiểm tra gen sau khi lấy bit nhỏ nhất ra thỏa capacity hay không trong 2 trường hợp
    if(idx_gen == 0):
        if (sum_gen(gen_fix_clone, suppliers) > current_capacity):  
            return [False, individual]
    else:
        if (sum_gen(gen_fix_clone, suppliers) > capacity):  
            return [False, individual]

    #thêm bit pop từ gen fix vào các gen khác
    for idx, gen in enumerate(individual):
        if (idx == idx_gen):
            continue
        gen_clone = gen.copy()
        gen_clone.append(bit_pop)     #.append: thêm ==> thêm supplier bị cắt vào gen đang xét
        if idx == 0:
            if (sum_gen(gen_clone, suppliers) < current_capacity):
                individual[idx] = gen_clone
                individual[idx_gen] = gen_fix_clone
                return [True, individual]
        else:
            if (sum_gen(gen_clone, suppliers) < capacity):
                individual[idx] = gen_clone
                individual[idx_gen] = gen_fix_clone
                return [True, individual]

    return [False, individual]

def getRamdomIndex(individual):
    len1 = len(individual)
    random1 = random.randint(0, len1-1)   #chọn ngẫu nhiên số thứ tự từ 0 tới len-1

    len2 = len(individual[random1])
    random2 = random.randint(0, len2-1)

    return [random1, random2]

def evaluate(individual, capacity, suppliers, current_capacity = 0):
    
    if(current_capacity == 0):
        current_capacity = capacity

    idx = 0
    for gen in individual:             #gen là số ngày
                                       #idx là số thứ tự của supplier trong ngày/gen đó
                                       #ứng với mỗi idx là tên của supplier/bit
                                       #supplier[bit] là stock của supplier
        if(idx == 0):
            sum = 0
            for bit in gen:
                sum = sum + suppliers[bit]
                if (sum > current_capacity):
                    return -1
        else:
            sum = 0
            for bit in gen:
                sum = sum + suppliers[bit]
                if (sum > capacity):
                    return -1
        idx = idx + 1
    return len(individual)

def makeF0(suppliers, capacity,current_capacity, n_max):    #CHƯA GIẢNG
    F0 = []
    all_suppliers = list(suppliers.keys())

    idx_gen = 0
    for idx1, supplier1 in enumerate(all_suppliers):
        for idx2, supplier2 in enumerate(all_suppliers):
            if idx_gen == 0:
                if (suppliers[supplier1] + suppliers[supplier2] < current_capacity and idx1 != idx2):
                    individual = []
                    for supplier3 in all_suppliers:
                        if supplier3 != supplier1 and supplier3 != supplier2:
                            individual.append([supplier3])
                        elif supplier3 == supplier1:
                            individual.append([supplier1, supplier2])
                    idx_gen = idx_gen + 1
                    F0.append(individual)
            else:
                if (suppliers[supplier1] + suppliers[supplier2] < capacity and idx1 != idx2):
                    individual = []
                    for supplier3 in all_suppliers:
                        if supplier3 != supplier1 and supplier3 != supplier2:
                            individual.append([supplier3])
                        elif supplier3 == supplier1:
                            individual.append([supplier1, supplier2])
                    idx_gen = idx_gen + 1
                    F0.append(individual)

    set_current_capacity = []
    for sup in all_suppliers:
        if(suppliers[sup] <= current_capacity):
            set_current_capacity.append(sup)
    
    count = 0
    for sup1 in set_current_capacity:
       
       
        temp = []
        for sup in all_suppliers:
            if(sup != sup1):
                temp.append(sup)
     
        temp2 = itertools.permutations(temp)

      
        for half_individual in temp2:
            individual = [[sup1]]
            for gen in half_individual:
                individual.append([gen])
            F0.append(individual)
            count +=1
            if(count>n_max):
                return F0[:n_max]
            
    return F0[:n_max]

def getRandomIndividual(populations,getIndex= False):   #trong mutation
    len_populations = len(populations)
    random_index = random.randint(0, len_populations-1)

    if(getIndex):
        return [copy.deepcopy(populations[random_index]),random_index]
    
    return copy.deepcopy(populations[random_index])

def getRandomTwoIndividual(populations):
 
    if(len(populations) == 1):
        raise ValueError('There is only one supplier left')

    len_populations = len(populations)
    
    random1 = random.randint(0, len_populations-1)
    random2 = random.randint(0, len_populations-1)

    while (random2 == random1):
        random2 = random.randint(0, len_populations-1)
   
    return [copy.deepcopy(populations[random1]), copy.deepcopy(populations[random2])]

def enhance(individual,capacity, suppliers,current_capacity): 

    individual = copy.deepcopy(individual)

    if(len(individual)==0):
        return [False, individual]

    idx_gen = getRamdomIndex(individual)[0]

    individual[idx_gen-1] = individual[idx_gen] + individual[idx_gen-1]
    individual.pop(idx_gen)

    if (evaluate(individual, capacity, suppliers,current_capacity) == -1):  #vị trí -1 là vị trí cuối
        return fix(individual,suppliers,capacity,current_capacity)
    else:
        return [True, individual]
    
def getScore(individual):         #Đếm số ngày trong plan đó
    return len(individual)

def read_file(file_path):

    df = pd.read_csv(file_path)

    return df.to_dict('records')

def read_input(file_path):
    input = read_file("./input/input1.csv")[0]
    capacity = input["capacity"]
    current_capacity=  input["current_capacity"]
    input.pop("capacity")
    input.pop("current_capacity")
    suppliers = input

    flag = True
    for supplier in suppliers:
        if suppliers[supplier] <= current_capacity:
            flag = False

    if(flag):
        raise "Please move to the next day. Capacity returns to the original"
    return [capacity,current_capacity,suppliers]

def write_output(output,file_path):

    with open(file_path,'w') as f:
        for individual in output:
            f.write(str(len(individual)))
            f.write('\n')
            for gen in individual:
                for bit in gen:
                    f.write(bit + ',')
                f.write('\n')

            f.write('\n')

def increase_population(Fi,suppliers,capacity,current_capacity, n_max):
    F0 = makeF0(suppliers,capacity,current_capacity,n_max)

    for individual in F0:
        if individual not in Fi:
            Fi.append(individual)

    return Fi[:n_max]     #ghi tắt của [0:n_max]

########### functions ########

def mutation_helper(individual,capacity,suppliers,current_capacity):
    #return new individual (deep copy)
    individual = copy.deepcopy(individual) 

    #print(individual)

    random1 = getRamdomIndex(individual)
    random2 = getRamdomIndex(individual)

    temp = individual[random1[0]][random1[1]]
    individual[random1[0]][random1[1]] = individual[random2[0]][random2[1]]
    individual[random2[0]][random2[1]] = temp

    fix_individual = [True, individual]
    if( evaluate(individual,capacity,suppliers,current_capacity) == -1):
        fix_individual = fix(individual,suppliers,capacity,current_capacity)
    
    if(fix_individual[0]):
        return fix_individual
    else:
        temp = individual[random1[0]][random1[1]]
        individual[random1[0]][random1[1]] = individual[random2[0]][random2[1]]
        individual[random2[0]][random2[1]] = temp

    return [False, individual]

def mutation(individual,capacity,suppliers,current_capacity, n_bit_mutation=5):
    individual = copy.deepcopy(individual) 

    result = False
    for i in range(0,n_bit_mutation):
        new_individual = mutation_helper(individual,capacity,suppliers,current_capacity)
        if(new_individual[0] == True):
            result = True
        individual = copy.deepcopy(new_individual[1])
    return [result,individual]

def crossover_helper(individual1, individual2,random_index1,random_index2):
    
    clone_individual1 = copy.deepcopy(individual1)

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

    
    bit_map1 = {}

    for i in range(random_index1,random_index2  + 1):
        bit_map1[clone_new_individua2[i]]= clone_new_individua1[i]

    for index,value in enumerate(new_individual1):
        if index >= random_index1 and index <= random_index2:
            new_individual1[index] = new_individual2[index]
        elif value in bit_map1:
            x = bit_map1[value]
            while(x in bit_map1):
                x = bit_map1[x]
            new_individual1[index] = x

    count = 0
    for index1,gen in enumerate(clone_individual1):
        for index2, bit in enumerate(gen):
            clone_individual1[index1][index2] = new_individual1[count]
            count +=1
    
    return clone_individual1

def crossover(individual1, individual2):

    len_individual = 0
    
    for gen in individual1:
        for bit in gen:
            len_individual += 1

            
    random_index1 = random.randint(0,len_individual-1)
    random_index2 = random.randint(random_index1,len_individual-1)

    return [crossover_helper(individual1,individual2,random_index1,random_index2), 
            crossover_helper(individual2,individual1,random_index1,random_index2)]
############## SUBMAIN ###################

def crossover_population(population, capacity, suppliers, n_cross, current_capacity = 0,percent_cross=0.6):

    if current_capacity == 0:
        current_capacity = capacity

    count = 0

    for _ in range(0, n_cross):
        [individual1, individual2] = getRandomTwoIndividual(population)
        [child1, child2] = crossover(individual1, individual2)

        if (evaluate(child1, capacity, suppliers, current_capacity) == -1) and len(child1) != 0:
            [can_fix, new_child] = fix(child1, suppliers, capacity, current_capacity)
            if (can_fix == True):
                count = count + 1
                population.append(new_child)
        elif len(child1) != 0:
            count = count + 1
            population.append(child1)

        if (evaluate(child2, capacity, suppliers,current_capacity) == -1) and len(child2) != 0:
            [can_fix, new_child] = fix(child2, suppliers, capacity, current_capacity)
            if (can_fix == True):
                count = count + 1
                population.append(new_child)
        elif len(child2) != 0:
            count = count + 1
            population.append(child2)

    for individual in population:
        for index,gen in  enumerate(individual):
            if (len(gen)==0):
                del individual[index]
    return [count,population]

def mutation_population(population, capacity, suppliers, n_mutation,current_capacity,n_bit_mutation):

    count = 0
    for _ in range(0, n_mutation):
        individual = getRandomIndividual(population)
        result = mutation(individual, capacity, suppliers,current_capacity,n_bit_mutation)
        if (result[0]):
            population.append(individual)
            count = count+1
    return [count, population]

def enhance_population(population,capacity,suppliers, n_enhance,current_capacity):
    count = 0

    for _ in range(0,n_enhance):
        [new_individual,index] = getRandomIndividual(population,True)

        #print(index)
        
        for index,gen in  enumerate(new_individual):
            if (len(gen)==0):
    
                del new_individual[index]
                

        [can_enhance,new_individual] = enhance(new_individual,capacity,suppliers,current_capacity)
        
        if(can_enhance and len(new_individual) !=0):
            #print(index)
            #print(len(population))
            #population.pop(index)
        

            population.append(new_individual)
            count = count + 1
    
    return [count,population]

def selection_population(population,n_selection):
    population.sort(key=getScore)        #Sort là hàm mặc định từ nhỏ -> lớn, ở đây Sort số ngày
   
    population = population[:n_selection]

    return population

def GA(population,n_fix, capacity,suppliers, n_GA, n_cross, n_mutation, n_enhance,n_selection, output ="", current_capacity = 0, percent_cross = 1,n_bit_mutation = 6):

    n_mutation = int(n_mutation * len(population))
    n_enhance = int(n_enhance * len(population))
    n_selection = int(n_selection * len(population))

    Fi = population
    count = 1
    
    if(output != ""):       #nếu output khác rỗng (rỗng: ko có data) thì mở file output
        f = open(output, "w")

    for _ in range(n_GA):
       
        Fi_1 = copy.deepcopy(Fi)
        N0 = len(Fi_1)
        Fi = selection_population(Fi,n_selection)     #lấy 25% của đời trước
          
        Fi = copy.deepcopy(Fi)
        #tăng dân số
        #if(len(Fi) <= n_fix):
        #    Fi= increase_population(Fi,suppliers,capacity,current_capacity,n_fix)
        #0.25 (n_selection)  -> (0.85) n_selct

        #0.2
        #n_cross =1 =>0.25+2 
        #        =2  => 0.25 +2x2 
        #       = x => 0.25n0 + 2x  = 0.85no 
        #       => x => n_selection*n0 + 2x = (n_cross + n_selection)n0
        #        => x = n_cross*n0/2

        num_cross = int(n_cross*N0/2)  
        Fi = crossover_population(Fi, capacity, suppliers, num_cross,current_capacity,percent_cross)[1]

        #kiểm tra đủ 85% chưa để thêm từ đời fi-1
        if(len(Fi)<(n_cross + n_selection)*N0):
            for individual in Fi_1:
                if individual not in Fi:
                    Fi.append(individual)
                if(len(Fi) >= (n_cross + n_selection) *N0):
                    break

        # n_selection*n0 + n_cross*n0 + num_mutation = n0
        # 0.25N0 + 0.6N0 + num_mutation = N0
        # num_mutation = N0 - (n_selection*n0 + n_cross*n0 ) = N0(1 - n_selection -n_cross )

        num_mutation = int(N0*(1 - n_selection -n_cross ))
        Fi = mutation_population(Fi,capacity,suppliers,num_mutation,current_capacity,n_bit_mutation)[1]

        #kiểm tra sau khi mutation đủ 100% chưa để thêm từ đời fi-1
        if(len(Fi)<N0):
            for individual in Fi_1:
                if individual not in Fi:
                    Fi.append(individual)
                if(len(Fi) >= N0):
                    break
       
        Fi = enhance_population(Fi,capacity,suppliers,n_enhance,current_capacity)[1]
        Fi = Fi[:N0]

    
        if(output != ""):
            f.write('GENERATION '+str(count)+'\n')
            for _ in Fi:
                f.write(str(_)+ ' ===> Days required: '+ str(len(_))+'\n') 
        else:
            print('Đời F'+ str(count))
            for _ in Fi:
                print(str(_))

        print(f"Progress {(count)/n_GA *100: .2f}%")
        count = count +1
 
    return Fi

######### MAIN ############

[capacity,current_capacity,suppliers] = read_input("./input/input1.csv")

F0 = makeF0(
    suppliers = suppliers,
    capacity = capacity,
    current_capacity = current_capacity,
    n_max=100
)

ga = GA(
    population = F0,
    capacity = capacity,
    suppliers = suppliers,
    n_fix = 100,
    n_selection = 0.25, #25%
    n_GA = 500,
    n_cross = 0.6, #60% cua population
    n_mutation = 0.15, #15%
    n_enhance = 1,
    output = "output.txt",
    current_capacity = current_capacity,
    percent_cross=0.6,
    n_bit_mutation = 20
)

write_output(ga,"./output/output.csv")