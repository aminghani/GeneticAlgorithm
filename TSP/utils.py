import numpy as np
import random

with open('TSP51.txt') as l:
    content = l.readlines()

data = {}
for d in content:
    city_id, x_coord, y_coord = d.split()
    city_id, x_coord, y_coord = int(city_id), int(x_coord), int(y_coord)
    data[city_id] = (x_coord, y_coord)


class Chromosome:

    def __init__(self, solution):
        self.solution = solution

    def distance(self):
        sum = 0
        for i in range(len(self.solution) - 1):
            pos1 = self.solution[i]
            pos2 = self.solution[i + 1]
            sum += ((data[pos1][0] - data[pos2][0]) ** 2 + (data[pos1][1] - data[pos2][1]) ** 2) ** (1 / 2)
        return sum

    def __str__(self):
        st = ''
        for i in self.solution:
            st += str(i) + '-'
        return st


class Generation:

    def __init__(self, size=40):
        self.size = size
        self._init_generation()

    @staticmethod
    def normilize(x):
        tmp = []
        mx = max(x)
        for i in x:
            tmp.append(i / mx)
        return tmp

    def fitness_for_each(self):
        scores = []
        for solution in self.current_solutions:
            scores.append(solution.distance())
        return scores

    def best_generation_solution(self):
        scores = self.fitness_for_each()
        best_index = scores.index(min(scores))
        return self.current_solutions[best_index], min(scores)

    def _init_generation(self):
        self.current_solutions = []
        for i in range(self.size):
            x = list(range(1, 52))
            random.shuffle(x)
            self.current_solutions.append(Chromosome(x))

    def get_generation_overall_score(self):
        return sum(self.fitness_for_each()) / self.size

    def get_solutions(self):
        return self.current_solutions

    def set_solutions(self, solutions):
        self.current_solutions = solutions


class GA:

    def __init__(self, generation):
        self.current_generation = generation

    @staticmethod
    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def selection(self):
        scores = self.current_generation.fitness_for_each()
        next_gen = None
        for i in range(self.current_generation.size):
            next_gen = np.random.choice(self.current_generation.get_solutions(),
                                        self.current_generation.size,
                                        p=self.softmax(max(scores) - np.array(scores)))
        self.current_generation.set_solutions(next_gen)

    def do_crossover_and_mutation(self, crossover_portion=0.9, mutation_portion=0.1):

        def crossover(x1, x2):
            x1 = x1.solution
            x2 = x2.solution
            if len(x1) != len(x2):
                return 'cant do crossover'
            pivot_point = random.randint(1, len(x1) - 1)
            new_solution1 = np.zeros_like(x1)
            new_solution2 = np.zeros_like(x2)
            new_solution1[:pivot_point] = x1[:pivot_point]
            new_solution2[pivot_point:] = x2[pivot_point:]
            counter1 = pivot_point
            counter2 = pivot_point - 1
            for i in x2:
                if i not in new_solution1:
                    new_solution1[counter1] = i
                    counter1 += 1
            for j in x1:
                if j not in new_solution2:
                    new_solution2[counter2] = j
                    counter2 -= 1
            return Chromosome(new_solution1), Chromosome(new_solution2)

        def mutation(x):
            x = x.solution
            ans = x.copy()
            while True:
                pos1 = random.randint(0, len(x) - 1)
                pos2 = random.randint(0, len(x) - 1)
                if pos1 == pos2:
                    continue
                temp = ans[pos1]
                ans[pos1] = ans[pos2]
                ans[pos2] = temp
                break
            return Chromosome(ans)

        crossover_p = int(self.current_generation.size * crossover_portion)
        mutation_p = int(self.current_generation.size * mutation_portion)
        crossover_els = self.current_generation.get_solutions()[:crossover_p]
        mutation_els = self.current_generation.get_solutions()[:mutation_p]
        new_ = []
        counter = 0
        while counter < len(crossover_els) - 1:
            n1, n2 = crossover(crossover_els[counter], crossover_els[counter + 1])
            new_.append(n1)
            new_.append(n2)
            counter += 2
        for el in mutation_els:
            new_.append(mutation(el))
        self.current_generation.set_solutions(new_)
