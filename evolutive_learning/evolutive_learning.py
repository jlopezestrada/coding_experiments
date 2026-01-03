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
POPULATION_SIZE = 100
GENES = 10
GENERATIONS = 10
MUTATION_RATE = 0.01


def initialize_population():
    return 0


def selection():
    return 0


def crossover():
    return 0


def mutation():
    return 0


def fitness_function():
    return 0
