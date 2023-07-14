#------------------------------------------------IMPORT THƯ VIỆN-------------------------------------------
import random
import copy
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt


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
    'K':2,
    'L':3,
    'M':6
}

capacity = 15
current_capacity = 10

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
        return [False,individual]
    else:
        return [True, individual]
    
def enhance(individual, capacity, suppliers, current_capacity):
    
    len_individual = len(individual)

    for i in range(0,len_individual-1):
        for j in range(i+1,len_individual):
            result = enhance_helper(individual,capacity,suppliers,current_capacity,i,j)
            if(result[0]):
                return result

    return [False, individual]

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
            print('Enhance thanh cong')
            if(enhanced_individual not in new_F0):
                print('Them vao quan the F0 thanh cong')
                new_F0.append(enhanced_individual)
                if(len(enhanced_individual) in statistic):
                    statistic[len(enhanced_individual)]+=1
                else:
                     statistic[len(enhanced_individual)] = 1
            else:
                print('Them vao quan the that bai do da ton tai ca the nay')
    
    for _ in new_F0:
        f.write(str(_)+ ' ===> Days required: '+ str(len(_))+'\n') 
    
    names = list(statistic.keys())
    values = list(statistic.values())
    plt.bar(range(len(statistic)), values, tick_label=names)
    plt.xlabel('So ngay')
    plt.ylabel('So luong con')
    plt.show()

    return new_F0

    

make_f0_random(suppliers,capacity,current_capacity,10,50)