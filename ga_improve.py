from asyncore import write
from json.encoder import INFINITY
import random
from random import uniform
import math

class Chromosome:
    def __init__(self, sequence) -> None:
        self.sequence = sequence.copy()
        self.length = len(self.sequence)
        self.fitness = self.calculate_fitness()
    
    def calculate_fitness(self):
        f = 0
        for i in range(self.length-1):
            f += math.sqrt(sum([(a - b) ** 2 for a, b in zip(self.sequence[i], self.sequence[i+1])]))
        f += math.sqrt(sum([(a - b) ** 2 for a, b in zip(self.sequence[i+1], self.sequence[0])]))
        return 1/f


class Population:
    def __init__(self, cities) -> None:
        self.population = []
        self.sum_of_fitnesses = 0
        self.population_size = 60
        self.best_chromosome = None
        self.MakeInitialPopulation(self.population_size, cities)
        self.CalculateSumOfFitnesses()

    def dispop(self, popu):
        for c in popu:
            print(c.sequence, 1/c.fitness, c.fitness)

    def avgmaxmin(self):
        maxm = sum = 0
        minm = float("inf")
        for ch in self.population:
            maxm = max(maxm, ch.fitness)
            minm = min(minm, ch.fitness)
            sum += ch.fitness
        print(f"\nmax = {maxm*10000} min = {minm*10000} avg = {sum/len(self.population)*10000}\n")

    def GeneticAlgo(self):
        iterations = 3000
        termination_counter = 0
        termination_limit = 2000
        last_fitness = self.best_chromosome.fitness
        #self.CalculateSumOfFitnesses() #FIRST TIME

        #distribution of crossover, mutation and random initiation
        cross_upto = self.population_size * 0.64
        mutate_upto = self.population_size * 0.92
        for t in range(iterations):
            new_population = []
            new_sum_of_fitnesses = 0
            self.CalculateSumOfFitnesses()
            #print(f"sum of fitness = {self.sum_of_fitnesses}")
            #p_crossover = random.random()
            
            for i in range(self.population_size - 1):
                #CROSSOVER FOR SOME
                if i < cross_upto:
                    p_mutation = random.random()
                    p1_index=p2_index=0
                    while(p1_index == p2_index):
                        p1_index = self.RouletteSelection()
                        p2_index = self.RouletteSelection()
                    child = self.CrossOver(p1_index, p2_index)
                    # child = self.Mutation(child)
                    if p_mutation > 0.8:
                        child = self.Mutation(child)
                
                elif i>cross_upto and i<mutate_upto:
                    p_index = self.RouletteSelection()
                    child = self.Mutation(self.population[p_index])
                
                else:
                    child = self.population[self.RouletteSelection()]                    
                    # parent = self.population[0].sequence.copy()
                    # random.shuffle(parent)
                    # child = Chromosome(parent)

                new_population.append(child)
                new_sum_of_fitnesses += child.fitness
                if child.fitness > self.best_chromosome.fitness: #CHANGED
                        self.best_chromosome = child

            # print(f"old:")
            # self.dispop(self.population)
            new_population.append(self.best_chromosome)
            self.population = new_population
            self.sum_of_fitnesses = new_sum_of_fitnesses + self.best_chromosome.fitness
            # print(f"new:")
            # self.dispop(self.population)
            print(f"Generation: {t}")
            print(f"best yet distance: {1/self.best_chromosome.fitness}")
            self.avgmaxmin()
            print(f"termination count: {termination_counter}")
            
            if self.best_chromosome.fitness > last_fitness:
                last_fitness = self.best_chromosome.fitness
                termination_counter = 0
            else:
                termination_counter += 1
            if termination_counter == termination_limit:
                break
        return self.best_chromosome


    def MakeInitialPopulation(self, size, cities):
        for i in range(size):
            random.shuffle(cities)
            chromosome =  Chromosome(cities)
            if (self.best_chromosome == None or chromosome.fitness < self.best_chromosome.fitness):
                self.best_chromosome = chromosome
            self.population.append(chromosome)
        #return self.population

    def CalculateSumOfFitnesses(self):
        self.sum_of_fitnesses = 0
        for chromosome in self.population:
            self.sum_of_fitnesses += chromosome.fitness

    def RouletteSelection(self):
        random_val = uniform(0,self.sum_of_fitnesses)
        partial_sum = 0
        for i in range(len(self.population)):
            partial_sum += self.population[i].fitness
            if (partial_sum >= random_val):
                # #check roulette
                # print(f"best fit: {self.best_chromosome.fitness}")
                # print(f"roul fit: {self.population[i].fitness}")
                # #
                return i
        

    def CrossOver(self, p1_index, p2_index):
        point_a = random.randint(0, self.population[p1_index].length - 1)
        point_b = random.randint(0, self.population[p2_index].length - 1)
        if (point_a > point_b):
            point_a, point_b = point_b, point_a
        
        lookup = {}
        child = [None] * self.population[p1_index].length
        for i in range(point_a, point_b+1):
            child[i] = self.population[p1_index].sequence[i]
            lookup[child[i]] = True

        start = 0
        for i in range(point_a):
            for j in range(start, self.population[p2_index].length):
                if ( lookup.get(self.population[p2_index].sequence[j]) == None):
                    child[i] = self.population[p2_index].sequence[j]
                    lookup[child[i]] = True
                    start += 1
                    break
        
        for i in range(point_b+1, self.population[p1_index].length):
            for j in range(start, self.population[p2_index].length):
                if ( lookup.get(self.population[p2_index].sequence[j]) == None):
                    child[i] = self.population[p2_index].sequence[j]
                    lookup[child[i]] = True
                    start = j+1
                    break

        return Chromosome(child)
    
    def Mutation(self, parent):
        child = parent.sequence.copy()
        point_a = random.randint(0, len(child)-1)
        point_b = random.randint(0, len(child)-1)
        if (point_a > point_b):
            point_a, point_b = point_b, point_a
        child[point_a:point_b] = child[point_a:point_b][::-1]
        return Chromosome(child)
        # child[point_a] , child[point_b] = child[point_b], child[point_a]
        # return Chromosome(child) 

def main():
    f = open('input.txt', 'r')
    count = int(f.readline())
    cities = []
    for i in range(count):
        t = tuple(int(x) for x in f.readline().split())
        cities.append(t)
    pop = Population(cities)
    best_chromosome = pop.GeneticAlgo()
    best_path = best_chromosome.sequence
    best_path.append(best_path[0])
    f = open('output.txt', 'w')
    for points in best_path:
        f.write(f"{points[0]} {points[1]} {points[2]}")
        f.write("\n")

    # #TEST CROSSOVER
    # p = Population(cities)
    # p.dispop(p.population)
    # for i in range(5):
    #     print(p.RouletteSelection())

    f.close()


if __name__ == "__main__":
    main()