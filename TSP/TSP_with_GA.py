import numpy as np
import random
from utils import Generation, GA
from visualize import plot_solution, plot_overall_distance_through_generations

overall_distance_list = []


def find_best_solution():
    g1 = Generation()
    print(g1.get_generation_overall_score())
    ga = GA(g1)
    for i in range(1):
        ga.selection()
        ga.do_crossover_and_mutation()
        overall_distance = ga.current_generation.get_generation_overall_score()
        overall_distance_list.append(overall_distance)
        print(str(i) + ' overall distance : ' + str(overall_distance))
    best_chrom, min_distance = ga.current_generation.best_generation_solution()
    return best_chrom, min_distance


best_chrom, min_distance = find_best_solution()


