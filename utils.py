import random


def sum_gen(gen, suppliers):
    sum = 0
    for bit in gen:
        sum = sum + suppliers[bit]

    return sum

def fix(individual, suppliers, capacity):
    count = 0
    idx_gen = -1

    for idx, gen in enumerate(individual):
        sum = 0
        for bit in gen:
            sum = sum + suppliers[bit]
            if (sum > capacity):
                idx_gen = idx
                count = count + 1
                if (count >= 2):
                    return [False, individual]
    idx_min = 0
    gen_fix = individual[idx_gen]
    min_bit_value = suppliers[gen_fix[idx_min]]

    for idx, bit in enumerate(gen_fix):
        if suppliers[bit] < min_bit_value:
            min_bit_value = suppliers[bit]
            idx_min = idx

    gex_fix_clone = gen_fix.copy()
    bit_pop = gex_fix_clone[idx_min]
    gex_fix_clone.pop(idx_min)

    if (sum_gen(gex_fix_clone, suppliers) > capacity):
        return [False, individual]

    # print('debug')
    # individual[idx_gen] = gex_fix_clone

    for idx, gen in enumerate(individual):
        if (idx == idx_gen):
            continue
        gen_clone = gen.copy()
        gen_clone.append(bit_pop)

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

def evaluate(individual, capacity, suppliers):
    for gen in individual:
        sum = 0
        for bit in gen:
            sum = sum + suppliers[bit]
            if (sum > capacity):
                return -1
    return len(individual)

def makeF0(suppliers, capacity):
    F0 = []
    all_suppliers = list(suppliers.keys())

    len_suppliers = len(all_suppliers)

    for idx1, supplier1 in enumerate(all_suppliers):
        for idx2, supplier2 in enumerate(all_suppliers):
            if (suppliers[supplier1] + suppliers[supplier1] < capacity and idx1 != idx2):
                individual = []
                for supplier3 in all_suppliers:
                    if supplier3 != supplier1 and supplier3 != supplier2:
                        individual.append([supplier3])
                    elif supplier3 == supplier1:
                        individual.append([supplier1, supplier2])
                F0.append(individual)

    return F0

def getRandomTwoIndividual(populations):

    len_populations = len(populations)
    random1 = random.randint(0, len_populations-1)

    while (1):
        random2 = random.randint(0, len_populations-1)
        if (random2 != random1):
            return [populations[random1], populations[random2]]
