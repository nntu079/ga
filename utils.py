import random
import copy
import pandas as pd
import csv
import numpy as np
import itertools


def sum_gen(gen, suppliers):
    sum = 0
    for bit in gen:
        sum = sum + suppliers[bit]

    return sum

def cloneIndividual(individual):
    return copy.deepcopy(individual)

def fix(individual, suppliers, capacity,current_capacity):
    count = 0
    idx_gen = -1

    #đếm số gen cần fix, >=2 => từ chối fix
    for idx, gen in enumerate(individual):      #enumrate là vòng lặp vừa lấy chỉ số vừa lấy giá trị
        if(idx == 0):
            sum = 0
            for bit in gen:
                sum = sum + suppliers[bit]
                if (sum > current_capacity):
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
    gen_fix = individual[idx_gen]
    min_bit_value = suppliers[gen_fix[idx_min]] #bit nhỏ nhất trong gen

    #tìm idx_min vị trí bit, min_bit_value giá trị bit của bit nhỏ nhất tron gen cần fix
    for idx, bit in enumerate(gen_fix): 
        if suppliers[bit] < min_bit_value:
            min_bit_value = suppliers[bit]
            idx_min = idx

    
    gex_fix_clone = gen_fix.copy() #clone gen cần fix ra để thử fix
    bit_pop = gex_fix_clone[idx_min]  #giá trị bit lấy ra của gen gần fix
    gex_fix_clone.pop(idx_min)        #xóa bit nhỏ nhất trong gen cần fix đã clone

    #kiểm tra gen sau khi lấy bit nhỏ nhất ra thỏa capacity hay không trong 2 trường hợp
    if(idx_gen == 0):
        if (sum_gen(gex_fix_clone, suppliers) > current_capacity):  
            return [False, individual]
    else:
        if (sum_gen(gex_fix_clone, suppliers) > capacity):  
            return [False, individual]

    #thêm bit pop từ gen fix vào các gen khác
    for idx, gen in enumerate(individual):
        if (idx == idx_gen):
            continue
        gen_clone = gen.copy()
        gen_clone.append(bit_pop)
        if idx == 0:
            if (sum_gen(gen_clone, suppliers) < current_capacity):
                individual[idx] = gen_clone
                individual[idx_gen] = gex_fix_clone
                return [True, individual]
        else:
            if (sum_gen(gen_clone, suppliers) < capacity):
                individual[idx] = gen_clone
                individual[idx_gen] = gex_fix_clone
                return [True, individual]

    return [False, individual]

def getRamdomIndex(individual):
    len1 = len(individual)
 
 
    random1 = random.randint(0, len1-1)

    len2 = len(individual[random1])
    random2 = random.randint(0, len2-1)

    return [random1, random2]

def evaluate(individual, capacity, suppliers, current_capacity = 0):
    
    if(current_capacity == 0):
        current_capacity = capacity

    idx = 0
    for gen in individual:
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

def makeF0(suppliers, capacity,current_capacity, n_max):
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
            
    return F0[:n_max]

def getRandomIndividual(populations,getIndex= False):
    len_populations = len(populations)
    random_index = random.randint(0, len_populations-1)

    if(getIndex):
        return [copy.deepcopy(populations[random_index]),random_index]
    
    return copy.deepcopy(populations[random_index])

def getRandomTwoIndividual(populations):
 
    if(len(populations) == 1):
        raise ValueError('Chỉ còn đúng 1 cách.')

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

    if (evaluate(individual, capacity, suppliers,current_capacity) == -1):
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
        raise "Quay xe"
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