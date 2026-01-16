# Evolutionary Algorithm to calculate SQRT of a given number
# Goal: find x such as x^2 = Target
# Individual = One possible solution (a float number in this case) [1.234]
# Population = Set of Individuals [1.0, 4.4, 6.44, 9.289, ...]
# Genotype = Number itself (because the features of the individual is the float number itself) [1.234]
# Search Space = Float between 0 and Input number or 1 [0, ..., max(1, number)]
# Operators
#    Selection = Selects a number that would continue the generations
#    Crossover = Perform an operation with another number
#    Mutation = Perform an operation with a random number

import random

POPULATION_SIZE = 10000
GENES = 1
GENERATIONS = 10000
MUTATION_RATE = 0.2


def initialize_population(population_size: int, input: float) -> list[float]:
    return [random.uniform(0, max(1, input)) for _ in range(population_size)]


def selection(population: list[float], target: float) -> float:
    candidates = random.choices(population, k=2)
    score_1 = fitness_function(candidates[0], target)
    score_2 = fitness_function(candidates[1], target)
    if score_1 < score_2:
        return candidates[0]
    else:
        return candidates[1]


def crossover(parent_1: float, parent_2: float) -> float:
    return (parent_1 + parent_2) / 2


def mutation(child: float, rate: float):
    if random.random() < rate:
        scale_factor = random.uniform(0.8, 1.2)
        return child * scale_factor
    return child


def fitness_function(individual: float, target: float) -> float:
    return abs(pow(individual, 2) - target)


def main():
    input = 323
    population = initialize_population(population_size=POPULATION_SIZE, input=input)
    for generation in range(GENERATIONS):
        next_gen = []
        while len(next_gen) < POPULATION_SIZE:
            parent_1 = selection(population, input)
            parent_2 = selection(population, input)

            child = crossover(parent_1, parent_2)
            child = mutation(child, rate=MUTATION_RATE)

            next_gen.append(child)
        population = next_gen

        best_individual = min(population, key=lambda ind: fitness_function(ind, input))
        print(
            f"Gen {generation}: Best solution = {best_individual}, Error = {fitness_function(best_individual, input)}"
        )
        if fitness_function(best_individual, input) < 0.0001:
            print(f"# Best solution = {best_individual} @ Gen {generation} #")
            return


if __name__ == "__main__":
    main()
