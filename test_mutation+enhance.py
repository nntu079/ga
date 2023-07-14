#------------------------------------------------IMPORT THƯ VIỆN-------------------------------------------
import random
import copy
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt




#------------------------------------KHAI BÁO CÁC HÀM ĐỌC INPUT VÀ XUẤT OUTPUT-------------------------------
def read_file(file_path):

    df = pd.read_csv(file_path)

    return df.to_dict('records')

def read_input(file_path):
    input = read_file("./input/input1.csv")[0]
    capacity = input["capacity"]
    current_capacity = input["current_capacity"]
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



#--------------------------------------------KHAI BÁO 1 SỐ HÀM DÙNG CHUNG---------------------------------

#Nhân bản 1 con bất kì
def cloneIndividual(individual):        
    return copy.deepcopy(individual)

#HÀM EVALUATE: Check xem có ngày nào bị lố capacity không
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

#Tính tổng stock của các supplier trong 1 ngày bất kì (Trong fix)
def sum_gen(gen, suppliers):      
    sum = 0
    for bit in gen:
        sum = sum + suppliers[bit]

    return sum

#HÀM FIX
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

#Xếp chromosome sao cho stock của các ngày giảm dần (nhiều -> ít) (trong sort_population)
def sort_individual(individual):
    individual = sorted(individual, key=len, reverse=True)
    return individual

def enhance_helper(individual,capacity, suppliers,current_capacity,idx_gen1, idx_gen2): 

    individual = copy.deepcopy(individual)

    if(len(individual)==0):
        return [False, individual]
   
    len_gen1 = len(individual[idx_gen1])
    len_gen2 = len(individual[idx_gen2])

    if(len_gen1>=len_gen2):
        individual[idx_gen1] = individual[idx_gen1] + individual[idx_gen2]
        individual.pop(idx_gen2)
    else:
        individual[idx_gen2] = individual[idx_gen2] + individual[idx_gen1]
        individual.pop(idx_gen1)

    if (evaluate(individual, capacity, suppliers,current_capacity) == -1):  #vị trí -1 là vị trí cuối
        return fix(individual,suppliers,capacity,current_capacity)
    else:
        return [True, individual]
    
def enhance(individual, capacity, suppliers, current_capacity):
    
    len_individual = len(individual)

    for i in range(0,len_individual-1):
        for j in range(i+1,len_individual):
            result = enhance_helper(individual,capacity,suppliers,current_capacity,i,j)
            if(result[0]):
                print('vi tri doan gen 1', i)
                print('vi tri doan gen 2', j)
                return result

    return [False, individual]

#Tạo population mới sao cho số lượng ngày giảm dần (nhiều -> ít) (trong GA)
def sort_population(population):
    new_population = []

    for individual in population:
        new_population.append(sort_individual(individual))
    return new_population



#-------------------------------------------TẠO ĐỜI FeO------------------------------------------------------

def makeF0(suppliers, capacity,current_capacity, n_max):    #CHƯA GIẢNG
    F0 = []
    all_suppliers = list(suppliers.keys())

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


def make_f0_random(suppliers, capacity,current_capacity, n_seeding, pop_size):
    
    f = open('test_makeF02.txt', "w")

    F0 = makeF0(suppliers,capacity,current_capacity,n_seeding)
    new_F0 = []

    random_individual = random.choice(F0)

    statistic = {
        len(random_individual):len(F0)
    }

   

    for individual in F0:
        random.shuffle(individual) 
        if(individual not in new_F0):
            new_F0.append(individual)
        else:
            while(individual in new_F0):
                random.shuffle(individual)    
            new_F0.append(individual)
    
    while(len(new_F0) != pop_size):
        individual = random.choice(new_F0)
        [enhance_result, enhanced_individual] = enhance(individual,capacity,suppliers,current_capacity)
        if(enhance_result):
            #print('Enhance thanh cong')
            if(enhanced_individual not in new_F0):
                #print('Them vao quan the F0 thanh cong')
                new_F0.append(enhanced_individual)
                if(len(enhanced_individual) in statistic):
                    statistic[len(enhanced_individual)]+=1
                else:
                     statistic[len(enhanced_individual)] = 1
            else:
                #print('Them vao quan the that bai do da ton tai ca the nay')
                pass
    
    for _ in new_F0:
        f.write(str(_)+ ' ===> Days required: '+ str(len(_))+'\n') 
    
    names = list(statistic.keys())
    values = list(statistic.values())
    plt.bar(range(len(statistic)), values, tick_label=names)
    plt.xlabel('So ngay')
    plt.ylabel('So luong con')
    plt.show()

    return new_F0

#-------------------------------------------SELECTION--------------------------------------------------------

#Đếm tổng số ngày của từng chromosome (Trong selection_population)
def getScore(individual):         
    return len(individual)

#Sort chrosome theo chiều số ngày giảm dần (tốt -> xấu) + lấy % con tốt nhất (n_selection)
def selection_population(population,n_selection):
    population.sort(key=getScore)        #Sort là hàm mặc định từ nhỏ -> lớn, ở đây Sort số ngày
    population = population[:n_selection]
    return population



#------------------------------------------------CROSSOVER-------------------------------------------------

#Chọn ngẫu nhiên 2 chromosomes
def getRandomTwoIndividual(populations):
 
    if(len(populations) == 1):
        raise ValueError('There is only one supplier left')

    len_populations = len(populations)
    
    random1 = random.randint(0, len_populations-1)
    random2 = random.randint(0, len_populations-1)

    while (random2 == random1):
        random2 = random.randint(0, len_populations-1)
   
    return [copy.deepcopy(populations[random1]), copy.deepcopy(populations[random2])]

#HÀM CROSS HELPER
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

#HÀM CROSSOVER: crossover 2 cá thể
def crossover(individual1, individual2):      #chọn vị trí 2 point bị cắt

    len_individual = 0
    
    for gen in individual1:
        for bit in gen:
            len_individual += 1

            
    random_index1 = random.randint(0,len_individual-1)
    random_index2 = random.randint(random_index1,len_individual-1)

    return [crossover_helper(individual1,individual2,random_index1,random_index2), 
            crossover_helper(individual2,individual1,random_index1,random_index2)]



#------------------------------------------------MUTATION--------------------------------------------------

#Chọn ngẫu nhiên 1 chromosome trong population
def getRandomIndividual(populations):     
    len_populations = len(populations)
    random_index = random.randint(0, len_populations-1)
    
    return copy.deepcopy(populations[random_index])

#Chọn ngẫu nhiên thứ tự của 1 bit trong chromosome. random1:thứ tự ngày, randome2: thứ tự supplier trong ngày (trong mutation_helper)
def getRamdomIndex(individual):
    len1 = len(individual)
    random1 = random.randint(0, len1-1)   #chọn ngẫu nhiên số thứ tự từ 0 tới len-1

    len2 = len(individual[random1])
    random2 = random.randint(0, len2-1)

    return [random1, random2]

#HÀM MUTATION HELPER
def mutation_helper(individual,capacity,suppliers,current_capacity):
    #return new individual (deep copy)
    individual = copy.deepcopy(individual) 

    #print(individual)


    
    random1 = getRamdomIndex(individual)
    random2 = getRamdomIndex(individual)

    print('vi tri cua bit1:', random1)
    print('vi tri cua bit2:', random2)

    temp = individual[random1[0]][random1[1]]
    individual[random1[0]][random1[1]] = individual[random2[0]][random2[1]]
    individual[random2[0]][random2[1]] = temp


    return [True, individual]

#HÀM MUTATION: mutation 1 cá thể
def mutation(individual,capacity,suppliers,current_capacity,n_bit_mutation):
    individual = copy.deepcopy(individual) 

    result = False
    mutated_individual =  individual
    for i in range(0,n_bit_mutation):
        mutation_result= mutation_helper(mutated_individual,capacity,suppliers,current_capacity)
        mutated_individual = mutation_result[1]
        print(mutated_individual)
    
    
    if( evaluate(mutated_individual,capacity,suppliers,current_capacity) == -1):
        [result_fix,fixed_individual] = fix(mutated_individual,suppliers,capacity,current_capacity)
        print('Can fix')
        if(result_fix):
            print('Fix thanh cong')
            print('Ket qua fix',fixed_individual)
            [result_enhance,enhanced_individual] = enhance(mutated_individual,capacity,suppliers,current_capacity)
            
            if(result_enhance):
                print('Enhance thanh cong')
                print('Ket qua enhance', enhanced_individual)
                return [True,enhanced_individual]
            else:
                print('Enhance that bai')
                return [True,fixed_individual]
        else:
            print('Fix that bai')
            return [False,mutated_individual]
    else:
        print('K can fix')
        [result_enhance,enhanced_individual] = enhance(mutated_individual,capacity,suppliers,current_capacity)
        if(result_enhance):
            return [True,enhanced_individual]
        else:
            return [True,mutated_individual]

        

suppliers = {
    'A':10,
    'B':5,
    'C':4,
    'D':2,
    'E':1,
    'F':7,
    'G':5,
    'H':3,
    'I':1,
    'K':2,
    'L':3,
    'M':6
}

capacity = 15
current_capacity = 10

individual1 = [['A','B'],['C','D','E'],['F','G'],['H','I','K'],['L','M']]

mutation(individual1,capacity,suppliers,current_capacity,1)