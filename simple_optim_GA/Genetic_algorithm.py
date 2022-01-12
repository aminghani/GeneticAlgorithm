import matplotlib.pyplot as plt
import numpy as np
import random


def fit_function(x):
    return x ** 2


def decimal2binary(n):
    return bin(n).replace("0b", "")


def to_eight_bit(binary: str):
    while len(binary) < 8:
        binary = '0' + binary
    return binary


def binary_to_decimal(num):
    sum = 0
    for idx, n in enumerate(num):
        sum += int(n) * 2 ** (len(num) - idx - 1)
    return sum


def generate_initial_generation(count: int):
    l = []
    te = []
    for i in range(count):
        tmp = random.randint(0, 255)
        te.append(tmp)
        l.append(to_eight_bit(decimal2binary(tmp)))
    return l


init = generate_initial_generation(10)

scores = []
for t in init:
    scores.append(binary_to_decimal(t))


def prob_selection(arr):
    tmp = []
    s = sum(arr)
    for i in arr:
        tmp.append(i / s)
    return tmp


def crossover_with_two(x1, x2):
    line_position = random.randint(1, 7)
    solution1 = x1[:line_position] + x2[line_position:]
    solution2 = x2[:line_position] + x1[line_position:]
    return [solution1, solution2]


def do_mutation(arr):
    rand = random.randint(0, len(arr) - 1)
    if arr[rand] == '0':
        arr = arr[:rand] + '1' + arr[rand + 1:]
    else:
        arr = arr[:rand] + '0' + arr[rand + 1:]
    return arr


def do_cross_over_and_mutation_on_generation(current_generation, crossover_prob, mutation_prob):
    next_generation_ = []
    crossover_samples = np.random.choice(current_generation, size=int(crossover_prob * len(current_generation)),
                                         replace=False)
    i = 0
    while i < len(crossover_samples) - 1:
        tmp = crossover_with_two(current_generation[i], current_generation[i + 1])
        next_generation_.append(tmp[0])
        next_generation_.append(tmp[1])
        i += 2
    mutation_samples = np.random.choice(current_generation, size=int(mutation_prob * len(current_generation)),
                                        replace=False)
    for i in mutation_samples:
        next_generation_.append(do_mutation(i))
    while len(next_generation_) < len(current_generation):
        next_generation_.append(random.choice(current_generation))
    return next_generation_


def compute_mean_fitting(generation):
    sum = 0
    for i in generation:
        sum += fit_function(binary_to_decimal(i))
    return sum / len(generation)


TOTAL_GENERATION = 200
GENERATION_SIZE = 30
CROSSOVER_PROB = 0.9
MUTATION_PROB = 0.05


def evolve():
    current_generation = generate_initial_generation(GENERATION_SIZE)
    fitness_over_generations = []
    for _ in range(TOTAL_GENERATION):
        scores = []
        for t in current_generation:
            scores.append(fit_function(binary_to_decimal(t)))
        probs = prob_selection(scores)
        next_generation = []
        for i in range(len(current_generation)):
            randomElement = np.random.choice(current_generation, p=probs)
            next_generation.append(randomElement)
        tm = do_cross_over_and_mutation_on_generation(next_generation, CROSSOVER_PROB, MUTATION_PROB)
        current_generation = tm.copy()
        fitness_over_generations.append(compute_mean_fitting(current_generation))
    return current_generation, fitness_over_generations


final_generation, fitness_over_generations = evolve()

print(final_generation)

with open('final_generation_binary_representation.txt', 'w') as f:
    for item in final_generation:
        f.write("%s\n" % item)

plt.plot(range(len(fitness_over_generations)), fitness_over_generations)
plt.savefig('fitness_over_generations.jpg')
