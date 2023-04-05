def mutation_population(population, capacity, suppliers, percent_mutation):

    len_population = len(population)
    n_mutation = int(percent_mutation * len_population)

    for _ in range(0, n_mutation):
        random_index = random.randint(0, len_population-1)

        new_individual = functions.mutation(population[random_index])

        if (utils.evaluate(new_individual, capacity, suppliers) == -1):
            [can_fix, new_child] = utils.fix(
                new_individual, suppliers, capacity)
            if (can_fix == True):
                population.append(new_child)
            else:
                population.append(new_individual)

    return population


F1 = mutation_population(F0, capacity, suppliers, 10)
